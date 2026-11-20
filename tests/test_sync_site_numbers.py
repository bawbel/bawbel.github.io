"""Tests for scripts/sync_site_numbers.py. Run: python -m pytest tests -q"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import sync_site_numbers as sync  # noqa: E402

VALUES = {"C-01": 87, "C-03": 43, "C-06": 12, "C-07": 120, "C-08": 6}

PAGE = """<html><body>
<div class="stats-bar">
  <!-- stat:start -->
  <!-- stat:end -->
</div>
<p>Built-in attack chains.</p>
<pre><code>Pattern     40 rules  .  always active</code></pre>
<span>Findings: 2  Chains: 1</span>
</body></html>
"""


def write_register(path: Path, values: dict, schema: str = sync.REGISTER_SCHEMA) -> Path:
    claims = [{"id": cid, "expect": value} for cid, value in values.items()]
    path.write_text(yaml.safe_dump({"schema": schema, "claims": claims}), encoding="utf-8")
    return path


@pytest.fixture
def site(tmp_path, monkeypatch):
    (tmp_path / "docs").mkdir()
    (tmp_path / "index.html").write_text(PAGE, encoding="utf-8")
    (tmp_path / "docs" / "index.html").write_text("<p>Detection rules</p>\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("Published records.\n", encoding="utf-8")
    monkeypatch.setattr(sync, "ROOT", tmp_path)
    monkeypatch.setattr(sync, "INDEX", tmp_path / "index.html")
    monkeypatch.setattr(sync, "PAGES", tuple(tmp_path / p for p in ("index.html", "docs/index.html", "README.md")))
    return tmp_path


def test_writes_every_value_then_check_passes(site):
    register = write_register(site / "register.yaml", VALUES)
    assert sync.main(["--register", str(register)]) == 0
    html = (site / "index.html").read_text(encoding="utf-8")
    for claim_id, label in sync.STATS:
        assert f'stat-num">{VALUES[claim_id]}</div><div class="stat-label">{label}' in html
    assert sync.main(["--register", str(register), "--check"]) == 0


def test_rewrite_is_idempotent(site):
    register = write_register(site / "register.yaml", VALUES)
    sync.main(["--register", str(register)])
    first = (site / "index.html").read_text(encoding="utf-8")
    sync.main(["--register", str(register)])
    assert (site / "index.html").read_text(encoding="utf-8") == first


def test_check_fails_when_the_register_changes(site):
    sync.main(["--register", str(write_register(site / "register.yaml", VALUES))])
    changed = write_register(site / "changed.yaml", {**VALUES, "C-01": 90})
    assert sync.main(["--register", str(changed), "--check"]) == 1


def test_check_flags_a_count_typed_outside_the_block(site):
    register = write_register(site / "register.yaml", VALUES)
    sync.main(["--register", str(register)])
    (site / "README.md").write_text("Covers 51 AVE records.\n", encoding="utf-8")
    assert sync.main(["--register", str(register), "--check"]) == 1


def test_check_flags_a_count_in_a_badge(site):
    (site / "README.md").write_text("![AVE](https://img.shields.io/badge/AVE_records-51-1DB894)\n", encoding="utf-8")
    assert sync.typed_counts(site / "README.md") == ["README.md:1: 'records-51'"]


def test_samples_are_not_counts(site):
    assert sync.typed_counts(site / "index.html") == []


@pytest.mark.parametrize("values", [
    {k: v for k, v in VALUES.items() if k != "C-03"},  # missing
    {**VALUES, "C-07": None},                          # null
    {**VALUES, "C-08": "6"},                           # not a number
    {**VALUES, "C-06": True},                          # bool is not a count
    {**VALUES, "C-01": -1},                            # negative
])
def test_a_bad_value_exits_2_and_writes_nothing(site, values):
    before = (site / "index.html").read_text(encoding="utf-8")
    assert sync.main(["--register", str(write_register(site / "register.yaml", values))]) == 2
    assert (site / "index.html").read_text(encoding="utf-8") == before


def test_wrong_schema_exits_2(site):
    register = write_register(site / "register.yaml", VALUES, schema="something/else")
    assert sync.main(["--register", str(register)]) == 2


@pytest.mark.parametrize("source", ["http://example.com/register.yaml", "file:///etc/passwd", "register.yaml"])
def test_only_a_file_or_an_https_url_is_read(site, source):
    assert sync.main(["--register", source]) == 2


def test_missing_markers_exit_2(site):
    (site / "index.html").write_text("<html></html>\n", encoding="utf-8")
    register = write_register(site / "register.yaml", VALUES)
    assert sync.main(["--register", str(register)]) == 2

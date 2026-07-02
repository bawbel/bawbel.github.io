<div align="center">

<img src="https://bawbel.io/assets/bawbel-logo.svg" alt="Bawbel logo" width="72" />

## Bawbel

**The security layer for agentic AI.**

Open-source tools for scanning MCP servers, skill files, and agent components
before they reach production. Free forever. Apache 2.0.

[![Scanner](https://img.shields.io/pypi/v/bawbel-scanner?label=bawbel-scanner&color=1DB894&style=flat-square)](https://pypi.org/project/bawbel-scanner/)
[![Downloads](https://img.shields.io/pypi/dm/bawbel-scanner?label=downloads%2Fmonth&color=1DB894&style=flat-square)](https://pepy.tech/project/bawbel-scanner)
[![AVE Records](https://img.shields.io/badge/AVE_records-51-1DB894?style=flat-square)](https://github.com/bawbel/ave)
[![License](https://img.shields.io/badge/license-Apache_2.0-1DB894?style=flat-square)](https://github.com/bawbel/scanner/blob/main/LICENSE)

</div>

---

### What we build

| Repo | What it is |
|---|---|
| [bawbel/scanner](https://github.com/bawbel/scanner) | CLI scanner for agentic AI components -- SKILL.md files, MCP servers, system prompts. Confidence and evidence metadata on every finding. |
| [bawbel/ave](https://github.com/bawbel/ave) | AVE -- the behavioral classification standard for agentic AI components. 51 published records, scored with OWASP AIVSS v0.8, mapped to OWASP MCP Top 10 and MITRE ATLAS. |
| [bawbel/piranha-api](https://github.com/bawbel/piranha-api) | Free, no-auth REST API serving the full AVE record set and threat intelligence. |
| [bawbel/integrations](https://github.com/bawbel/integrations) | GitHub Action, VS Code extension, and pre-commit hooks. |

---

### Quick start

```bash
pip install "bawbel-scanner[all]"
bawbel scan ./skills/
```

---

### The problem

Skill files, MCP server manifests, and system prompts are executable instructions, not documentation. Any process that loads them runs them. There is no compiler, no sandbox, no type checker. The runtime is an LLM that reads natural language and acts on it.

Your CI pipeline scans dependencies for known package vulnerabilities. It does not scan your SKILL.md for prompt injection. Bawbel fixes that, scored against a shared behavioral classification standard rather than a one-off internal taxonomy.

---

### Links

[bawbel.io](https://bawbel.io) &nbsp;·&nbsp;
[docs](https://bawbel.io/docs) &nbsp;·&nbsp;
[AVE registry](https://ave.bawbel.io) &nbsp;·&nbsp;
[PiranhaDB](https://api.piranha.bawbel.io) &nbsp;·&nbsp;
[OWASP AIVSS](https://aivss.owasp.org) &nbsp;·&nbsp;
[@bawbel_io](https://twitter.com/bawbel_io)
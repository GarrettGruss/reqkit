# reqkit (requirements kit)

This project is intended to be a requirements management solution for software, based around traces. This project is inspired by speckit, but is intended to be more lightweight and focus just on architecture and traceability.

## Overview

1. Store requirements as unique, immutable slugs. EX:
```md
type: requirement
name: example requirement
version: 0.1.0
org: garrett.gruss@gmail.com
---
- **FR-RQnWXOLG(Slug Generation)**: The CLI shall generate a unique, immutable slug for each new requirement, prefixed by its requirement type.
- **FR-RQD025V3(Trace Discovery)**: The CLI shall grep the codebase for trace comments and associate each match with its corresponding requirement slug.
- **FR-RQoaZjGz(Report Compilation)**: The CLI shall compile a report linking each requirement to the use cases, code locations, and test cases that reference its slug.
- **NFR-RQpQ7Lks(Slug Collision Resistance)**: Slug generation shall not produce a collision for at least 1,000,000 requirements within a single project.
- **UC-RQVt3xRz(Impact Assessment)**: As a developer, I want to find every place a requirement is implemented so that I can assess the impact of changing it.
- **VC-RQHm9Ydw(Orphan Detection)**: Verify that running the report command against a project with orphaned trace comments flags them as unmatched.
- **TC-RQBr2Nfq(Trace Round Trip)**: Generate a slug, insert it as a trace comment in a sample file, run the report, and confirm the trace appears under the originating requirement.
```
To simplify usage, offer a cli that parses the markdown documents and adds requirements (slug generator). Could construct a lock file that stores all the slugs in usage and the seed for the project.
2. Within each module, include the slug within a comment to inject a trace. EX:
```python
import secrets
import string

ALPHABET = string.ascii_letters + string.digits

def generate_slug(prefix: str, length: int = 6) -> str:
    """Generate a unique, immutable slug, e.g. FR-RQnWXOLG."""
    suffix = "".join(secrets.choice(ALPHABET) for _ in range(length))
    return f"{prefix}-RQ{suffix}"
```
The resulting slug is then injected into the implementing module as a trace comment:
```python
# trace: FR-RQnWXOLG
def generate_slug(prefix: str, length: int = 6) -> str:
    ...
```
3. Grep across the code base to identify the usage of a slug. The slug could be prefixed for different components, such as FR (functional requirement), NFR (nonfunctional requirement), UC(use case), VC(verification criteria), TC(test case). 
- the CLI could compile the various traces of the grep into a report of what your requirements are, where they are implemented, which use cases they correspond to, and how to perform tests. Effectively, the slugs become a graph that traces the code base (use cases trace to child requirements trace to code.) EX Report:
```bash
user: ~/code$ reqkit audit .
--------------------------------------
               Traces
--------------------------------------
FR-RQnWXOLG(Slug Generation)
- /src/slug_generator.py: L 10, 21
- /src/main.py: L 3

FR-RQD025V3(Trace Discovery)
- /src/audit.py: L 14, 47

FR-RQoaZjGz(Report Compilation)
- /src/audit.py: L 52

NFR-RQpQ7Lks(Slug Collision Resistance)
- /src/slug_generator.py: L 28
- /tests/test_slug_generator.py: L 9

UC-RQVt3xRz(Impact Assessment)
- /src/audit.py: L 47

VC-RQHm9Ydw(Orphan Detection)
- /src/audit.py: L 60
- /tests/test_audit.py: L 18

TC-RQBr2Nfq(Trace Round Trip)
- /tests/test_audit.py: L 33

--------------------------------------
               Warnings
--------------------------------------
- UC-RQVt3xRz(Impact Assessment): no VC or TC trace found
- TC-RQBr2Nfq(Trace Round Trip): no UC trace found

6 requirements traced, 0 orphaned trace comments, 2 warnings
```
4. Use git to perform version control of requirements and co locate reqs to implementation logic
5. The CLI will have an audit feature that can be ran in a github pipeline as a job -> Include an agent in this stage that reviews the audit and leaves comments on PRs for stale requirements, missing traces, etc.

## Staleness

Traceability tools typically rot: nothing stops a trace comment from drifting out of sync with the code it annotates, or a requirement from losing all its traces once code is refactored. Because traces here are plain text co-located with the code (not entries in a separate system), an AI coding agent can be tasked with maintaining trace freshness as part of routine maintenance, e.g. updating or removing trace comments when it edits annotated code, and flagging requirements that lose all their traces. This is the main advantage of the text-based, co-located approach over a separate requirements database.

## Risks

- Bloat: The system is adding overhead and can quickly add more cognitive load to the project than it is trying to solve
- Staleness: See above
- False sense of coverage: a trace proves a comment exists, not that the code actually satisfies the requirement; nothing checks correctness, only presence
- Gaming the audit: once the audit gates a PR pipeline, the path of least resistance is pasting in a trace comment to silence a warning rather than fixing the real gap
- Refactor/rename fragility: grep-based matching breaks silently across moves, renames, or copy-pasted code, leaving stale or duplicated traces that go unnoticed
- Slug squatting / ambiguous prefixes: nothing prevents colliding prefixes across unrelated docs, or a trace referencing a slug from a different project in a shared monorepo
- Governance overhead: someone has to own the requirements doc itself (who can add/retire a requirement, how slugs get deprecated) or the doc becomes the stale artifact instead of the code
- Agent reliability and cost: tying CI health to an AI agent reviewing audits and commenting on PRs adds recurring latency/API cost and a new failure mode of the agent misjudging a gap as fine (or vice versa)

## References

- [Markdig](https://github.com/xoofx/markdig)
- [ShortUUID](https://shortunique.id/)
- [MarkSpecs](https://github.com/NagoDede/MarkSpecs)
- [NASA Requirements Management](https://www.nasa.gov/reference/6-2-requirements-management/)
# Requirements Tool

This project is intended to be a requirements management solution for software, based around traces. This project is inspired by speckit, but is intended to be more lightweight and focus just on architecture and traceability.

## Overview

1. Store requirements as unique, immutable slugs. EX:
```md
type: requirement
name: example requirement
version: 0.1.0
org: garrett.gruss@gmail.com
---
- FR-nWXOLG:
- FR-D025V3:
- FR-oaZjGz:
```
To simplify usage, offer a cli that parses the markdown documents and adds requirements (slug generator). Could construct a lock file that stores all the slugs in usage and the seed for the project.
2. Within each module, include the slug within a comment to inject a trace
3. Grep across the code base to identify the usage of a slug. The slug could be prefixed for different components, such as FR (functional requirement), NFR (nonfunctional requirement), UC(use case), VC(verification criteria), TC(test case). 
- the CLI could compile the various traces of the grep into a report of what your requirements are, where they are implemented, which use cases they correspond to, and how to perform tests. Effectively, the slugs become a graph that traces the code base (use cases trace to child requirements trace to code.)
4. Use git to perform version control of requirements and co locate reqs to implementation logic

## References

- [Markdig](https://github.com/xoofx/markdig)
- [ShortUUID](https://shortunique.id/)
- [MarkSpecs](https://github.com/NagoDede/MarkSpecs)
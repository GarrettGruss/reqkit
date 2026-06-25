---
name: reqkit
description: Use this skill when working with reqkit requirements documents (.md files with a `type: requirement` header) in this project — creating a doc, adding FR/NFR/UC/VC/TC requirements, inspecting document metadata, or building a traceability matrix that links requirements to code via trace comments and span tags. Invoke for requests like "add a requirement for X", "trace requirements against the codebase", "show requirement info", or "what's a span trace".
---

# reqkit

`reqkit` (implemented in `reqdoc.py` at the project root) scaffolds and manages requirements
documents and traces requirement slugs to the code that implements them.

A requirements document is plain markdown: a `key: value` header, a `---` separator, then one
requirement per line, e.g. `- FR-RQnWXOLG(Slug Generation): The CLI shall ...`.

## Commands

Run everything through `python3 reqdoc.py <command> ...` from the project root (or `uv run
reqdoc.py ...` if using uv).

### `init` — create a new requirements document

```bash
python3 reqdoc.py init <path> --name <name> --org <org> [--type requirement] [--version 0.1.0]
```

Fails if `<path>` already exists.

### `add` — append requirement(s) with generated slugs

```bash
python3 reqdoc.py add <path> --prefix FR [--name "..."] [--description "..."] [--qty 1]
```

- `--prefix` must be one of `NFR`, `FR`, `UC`, `VC`, `TC` (nonfunctional/functional requirement,
  use case, verification criteria, test case).
- Slugs are generated as `<PREFIX>-RQ<6 random alphanumeric chars>` and are meant to be immutable
  once created.
- Prints each newly generated slug to stdout, one per line.

### `info` — show document metadata

```bash
python3 reqdoc.py info <path>
```

Prints the header fields plus `requirement_count` and `counts_by_prefix`.

### `trace` — build a verification matrix

```bash
python3 reqdoc.py trace <path> [root] [--output <file>]
```

- Greps `root` (recursively) for every slug in `<path>`. If `root` is omitted, it defaults to the
  nearest ancestor directory containing a `.git` folder (the project root), not the cwd.
- If `--output` is omitted, the matrix is printed to stdout — pipe it where you want:
  `python3 reqdoc.py trace doc.md > trace.md`.
- Excludes `.git`, `__pycache__`, `node_modules`, `.venv`, `venv`, and the requirements doc itself.
- Each requirement section in the matrix shows a trace count, e.g.
  `## FR-RQnWXOLG(Slug Generation) — 2 trace(s) (1 simple, 1 span)`, and the footer summarizes
  total requirements traced, total traces found, and orphaned (untraced) requirements.

## Trace tagging in code

Two ways to link code back to a requirement slug:

1. **Simple trace** — just put the slug anywhere on a line, typically in a comment:
   ```python
   # ref FR-RQnWXOLG
   ```
   This only records the file and line number.

2. **Span trace** — wrap a block of code in an HTML-style tag pair to capture the actual
   implementing content in the matrix, not just a pointer to it:
   ```python
   # <ref FR-RQnWXOLG>
   def generate_slug(prefix: str, length: int = 6) -> str:
       ...
   # </ref>
   ```
   Valid tag names: `ref`, `parent`, `acceptance-criteria`, `test`, `deprecated`, `note`, `risk` —
   each represents a different relation to the requirement (see README's "Trace Tagging Methods"
   and "Relating Requirements" sections for the full semantics).
   A single span can reference multiple slugs comma-separated: `<ref FR-RQabc123,NFR-RQdef456>`.
   Spans can be single-line or multi-line; the tracer captures everything between the open and
   close tags and renders it under the matching requirement(s).

## When to reach for this skill

- Adding a new requirement to an existing doc: use `add` with the right prefix rather than
  hand-writing a slug (slugs must come from `generate_slug` to stay collision-resistant).
- Checking whether requirements still have implementing code: run `trace` and look at the
  orphaned list in the footer.
- Annotating code so it shows up in the matrix with context, not just a line number: use a span
  trace instead of a simple trace.

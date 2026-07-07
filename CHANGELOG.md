# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-07-06

### Added
- `src/reqkit/reports/table.py`: `ReqkitTable` class wrapping Rich `Table` for reqkit objects,
  configured via a `TableConfig` dataclass (`columns`, `title`, `style`, `header_style`, `show_lines`)
- `extract_column(obj, column)` helper in `table.py` for extracting named column values from any
  `ReqkitBase` object — delegates to `model_dump()` rather than branching on `isinstance`
- `@computed_field type` property on `ReqkitBase`, `ReqkitRequirement`, and `ReqkitTrace` so
  `model_dump()` includes `"type": "req" | "trace"` automatically
- `rich>=13.0` dependency for terminal table rendering

### Changed
- Rebuilt `cli` to use `click` (replacing `argparse`); `MintInterface` pydantic model replaced
  by click's native option/argument validation
- `parse` command now renders output as a Rich table via `ReqkitTable`
- CLI prints the app version on every invocation via the `click.group` callback

## [0.2.0] - 2026-06-29

Complete rewrite of the project around `reqkit`: a pseudo-XML tag scheme (`<rq-req>`/`<rq-trace>`)
for tracking requirements and tracing them against code, replacing the 0.1.0 implementation.

### Added
- `reqkit` pydantic models (`src/reqkit/types.py`) with validation for `subtype` and `parent_rel`
- `mint` command to generate new `<rq-req>` tags with auto-generated ids
- `parser` module to extract `<rq-req>`/`<rq-trace>` tags from arbitrary text, tolerant of
  unescaped characters and invalid XML in tag bodies
- `tracer` module and `trace` CLI command for recursive compliance reporting (non-compliant /
  partially-compliant / compliant / orphaned traces) across requirement docs and code, with
  `--full`/`--partial`/`--minimal` output verbosity
- Parser fixtures and tests, including coverage for invalid characters in tag bodies

### Changed
- Migrated `mint` constructor and validators into `types.py`
- Switched `__str__` rendering to use `ElementTree`
- Restructured project to use `uv`

## [0.1.0] - 2026-06-25

### Added
Initial commit
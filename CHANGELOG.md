# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
"""Scaffolding for requirements .md documents.

A requirements document looks like:

    type: requirement
    name: example requirement
    version: 0.1.0
    org: garrett.gruss@gmail.com
    ---
    - FR-nWXOLG(Slug Generation): The CLI shall generate a unique, immutable slug...
"""

import argparse
import re
import secrets
import string
from pathlib import Path

ALPHABET = string.ascii_letters + string.digits

# Order matters: NFR must be tried before FR since "NFR" starts with "F" at
# index 1 — listing the longer prefix first keeps alternation unambiguous.
PREFIXES = ("NFR", "FR", "UC", "VC", "TC")

# A requirement line may be wrapped in list/heading/emphasis markup
# (e.g. "- **FR-RQxxxx(Name): desc**" or "## FR-RQxxxx(Name): desc"), so the
# pattern tolerates an optional list marker or heading prefix and optional
# emphasis marks around the slug rather than requiring plain "- " text.
_LEADING = r"^\s*(?:[-*+]\s+|#{1,6}\s+)?[*_~]{0,2}"
_TRAILING = r"[*_~]{0,2}:\s*(.*)$"


def _build_pattern(prefix: str) -> re.Pattern:
    return re.compile(rf"{_LEADING}{prefix}-([A-Za-z0-9]+)\(([^)]*)\){_TRAILING}")


PREFIX_PATTERNS = {prefix: _build_pattern(prefix) for prefix in PREFIXES}
ITEM_PATTERN = re.compile(
    rf"{_LEADING}({'|'.join(PREFIXES)})-([A-Za-z0-9]+)\(([^)]*)\){_TRAILING}"
)


def generate_slug(prefix: str, length: int = 6) -> str:
    suffix = "".join(secrets.choice(ALPHABET) for _ in range(length))
    return f"{prefix}-RQ{suffix}"


def create_document(path: Path, type_: str, name: str, version: str, org: str) -> None:
    if path.exists():
        raise FileExistsError(f"{path} already exists")
    header = (
        f"type: {type_}\n"
        f"name: {name}\n"
        f"version: {version}\n"
        f"org: {org}\n"
        "---\n"
    )
    path.write_text(header)


def add_requirement(
    path: Path,
    prefix: str,
    name: str = "requirement name",
    description: str = "requirement text",
    qty: int = 1,
) -> list[str]:
    slugs = [generate_slug(prefix) for _ in range(qty)]
    lines = "".join(f"- {slug}({name}): {description}\n" for slug in slugs)
    with path.open("a") as f:
        f.write(lines)
    return slugs


def parse_document(path: Path) -> tuple[dict, list[tuple[str, str, str, str]]]:
    lines = path.read_text().splitlines()
    header = {}
    items = []
    in_header = True
    for line in lines:
        if in_header:
            if line.strip() == "---":
                in_header = False
                continue
            if ":" in line:
                key, _, value = line.partition(":")
                header[key.strip()] = value.strip()
            continue
        match = ITEM_PATTERN.match(line.strip())
        if match:
            items.append(match.groups())
    return header, items


def get_info(path: Path) -> dict:
    header, items = parse_document(path)

    by_prefix = {}
    for prefix, _, _, _ in items:
        by_prefix[prefix] = by_prefix.get(prefix, 0) + 1

    return {
        **header,
        "requirement_count": len(items),
        "counts_by_prefix": by_prefix,
    }


def get_requirements(path: Path) -> list[dict]:
    _, items = parse_document(path)
    return [
        {"slug": f"{prefix}-{rid}", "prefix": prefix, "name": name, "description": desc}
        for prefix, rid, name, desc in items
    ]


TRACE_EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}


def find_project_root(start: Path | None = None) -> Path:
    """Walk up from `start` (default cwd) looking for a `.git` directory."""
    start = (start or Path.cwd()).resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return start


# Tag types from README's "Trace Tagging Methods" — each names a different
# edge in the requirements graph (implementation, test, deprecated, etc.).
SPAN_TAGS = ("ref", "parent", "acceptance-criteria", "test", "deprecated", "note", "risk")
_SPAN_OPEN = re.compile(rf"<({'|'.join(SPAN_TAGS)})\s+([^>]+)>")
_SPAN_CLOSE = re.compile(rf"</({'|'.join(SPAN_TAGS)})>")


def find_traces(slugs: list[str], root: Path, exclude: Path | None = None) -> dict[str, list[tuple[str, int]]]:
    traces: dict[str, list[tuple[str, int]]] = {slug: [] for slug in slugs}
    exclude = exclude.resolve() if exclude else None
    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue
        if any(part in TRACE_EXCLUDE_DIRS for part in file_path.parts):
            continue
        if exclude is not None and file_path.resolve() == exclude:
            continue
        try:
            text = file_path.read_text(errors="ignore")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for slug in slugs:
                if slug in line:
                    traces[slug].append((str(file_path.relative_to(root)), lineno))
    return traces


def find_span_traces(root: Path, exclude: Path | None = None) -> list[dict]:
    """Scan files for `<tag slug,...> ... </tag>` span traces and capture their content."""
    spans: list[dict] = []
    exclude = exclude.resolve() if exclude else None
    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue
        if any(part in TRACE_EXCLUDE_DIRS for part in file_path.parts):
            continue
        if exclude is not None and file_path.resolve() == exclude:
            continue
        try:
            text = file_path.read_text(errors="ignore")
        except OSError:
            continue
        rel = str(file_path.relative_to(root))
        open_spans: list[dict] = []  # stack of unclosed spans, LIFO per tag name
        for lineno, line in enumerate(text.splitlines(), start=1):
            offset = 0
            while True:
                open_m = _SPAN_OPEN.search(line, offset)
                close_m = _SPAN_CLOSE.search(line, offset)
                if open_m and (not close_m or open_m.start() <= close_m.start()):
                    if open_spans:
                        open_spans[-1]["content"].append(line[offset:open_m.start()])
                    slugs = [s.strip() for s in open_m.group(2).split(",") if s.strip()]
                    open_spans.append(
                        {"tag": open_m.group(1), "slugs": slugs, "start_line": lineno, "content": []}
                    )
                    offset = open_m.end()
                    continue
                if close_m:
                    if open_spans:
                        open_spans[-1]["content"].append(line[offset:close_m.start()])
                    tag = close_m.group(1)
                    idx = next(
                        (i for i in range(len(open_spans) - 1, -1, -1) if open_spans[i]["tag"] == tag), None
                    )
                    if idx is not None:
                        span = open_spans.pop(idx)
                        spans.append(
                            {
                                "tag": span["tag"],
                                "slugs": span["slugs"],
                                "file": rel,
                                "start_line": span["start_line"],
                                "end_line": lineno,
                                "content": "\n".join(span["content"]).strip("\n"),
                            }
                        )
                    offset = close_m.end()
                    continue
                if open_spans:
                    open_spans[-1]["content"].append(line[offset:])
                break
    return spans


def build_matrix(requirements: list[dict], traces: dict[str, list]) -> str:
    lines = ["# Verification Matrix", ""]
    orphaned = []
    total_traces = 0
    for req in requirements:
        slug = req["slug"]
        locations = traces.get(slug, [])
        span_count = sum(1 for loc in locations if isinstance(loc, dict))
        simple_count = len(locations) - span_count
        total_traces += len(locations)
        if locations:
            lines.append(
                f"## {slug}({req['name']}) — {len(locations)} trace(s) ({simple_count} simple, {span_count} span)"
            )
        else:
            lines.append(f"## {slug}({req['name']})")
        if locations:
            for loc in locations:
                if isinstance(loc, dict):
                    lines.append(f"- {loc['file']}: L{loc['start_line']}-L{loc['end_line']} ({loc['tag']})")
                    if loc["content"]:
                        lines.append("  ```")
                        lines.extend(f"  {content_line}" for content_line in loc["content"].splitlines())
                        lines.append("  ```")
                else:
                    file, lineno = loc
                    lines.append(f"- {file}: L{lineno}")
        else:
            lines.append("- _no trace found_")
            orphaned.append(slug)
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        f"{len(requirements)} requirements traced, {total_traces} trace(s) found, "
        f"{len(orphaned)} orphaned requirement(s)"
    )
    if orphaned:
        lines.append("")
        lines.append("Orphaned requirements (no trace found):")
        for slug in orphaned:
            lines.append(f"- {slug}")

    return "\n".join(lines) + "\n"


def trace_requirements(doc_path: Path, root: Path) -> str:
    requirements = get_requirements(doc_path)
    slugs = [req["slug"] for req in requirements]
    traces: dict[str, list] = {slug: list(locs) for slug, locs in find_traces(slugs, root, exclude=doc_path).items()}
    for span in find_span_traces(root, exclude=doc_path):
        for slug in span["slugs"]:
            if slug in traces:
                traces[slug].append(span)
    return build_matrix(requirements, traces)


def _cmd_init(args: argparse.Namespace) -> None:
    create_document(Path(args.path), args.type, args.name, args.version, args.org)
    print(f"Created {args.path}")


def _cmd_add(args: argparse.Namespace) -> None:
    slugs = add_requirement(Path(args.path), args.prefix, args.name, args.description, args.qty)
    for slug in slugs:
        print(slug)


def _cmd_info(args: argparse.Namespace) -> None:
    info = get_info(Path(args.path))
    for key, value in info.items():
        print(f"{key}: {value}")


def _cmd_trace(args: argparse.Namespace) -> None:
    root = Path(args.root) if args.root else find_project_root()
    matrix = trace_requirements(Path(args.path), root)
    if args.output:
        Path(args.output).write_text(matrix)
    else:
        print(matrix, end="")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold and manage requirements .md documents")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a new requirements document")
    init_parser.add_argument("path")
    init_parser.add_argument("--type", default="requirement")
    init_parser.add_argument("--name", required=True)
    init_parser.add_argument("--version", default="0.1.0")
    init_parser.add_argument("--org", required=True)
    init_parser.set_defaults(func=_cmd_init)

    add_parser = subparsers.add_parser("add", help="Append a new requirement to a document")
    add_parser.add_argument("path")
    add_parser.add_argument("--prefix", required=True, help="e.g. FR, NFR, UC, VC, TC")
    add_parser.add_argument("--name", default="requirement name")
    add_parser.add_argument("--description", default="requirement text")
    add_parser.add_argument("--qty", type=int, default=1, help="number of requirements to add")
    add_parser.set_defaults(func=_cmd_add)

    info_parser = subparsers.add_parser("info", help="Show metadata about a document")
    info_parser.add_argument("path")
    info_parser.set_defaults(func=_cmd_info)

    trace_parser = subparsers.add_parser(
        "trace", help="Grep the codebase for requirement traces and build a verification matrix"
    )
    trace_parser.add_argument("path", help="Path to the requirements document")
    trace_parser.add_argument(
        "root",
        nargs="?",
        default=None,
        help="Directory to recursively search for trace comments (default: nearest ancestor containing .git)",
    )
    trace_parser.add_argument("--output", help="Optional path to write the verification matrix instead of stdout")
    trace_parser.set_defaults(func=_cmd_trace)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

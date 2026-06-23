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
ITEM_PATTERN = re.compile(r"^-\s+([A-Za-z]+)-([A-Za-z0-9]+)\(([^)]*)\):\s*(.*)$")


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


def get_info(path: Path) -> dict:
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

    by_prefix = {}
    for prefix, _, _, _ in items:
        by_prefix[prefix] = by_prefix.get(prefix, 0) + 1

    return {
        **header,
        "requirement_count": len(items),
        "counts_by_prefix": by_prefix,
    }


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

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

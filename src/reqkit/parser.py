"""Parses raw strings into reqkit objects."""

import re
import xml.etree.ElementTree as ET
from typing import List

from pydantic import ValidationError

from reqkit.types import ReqkitBase, ReqkitRequirement, ReqkitTrace

_TAG_CLASSES = {
    "rq-req": ReqkitRequirement,
    "rq-trace": ReqkitTrace,
}

_TAG_PATTERN = re.compile(
    r"<(" + "|".join(_TAG_CLASSES) + r")\b([^>]*?)(?:/>|>(.*?)</\1>)", re.DOTALL
)


def parse_str(text: str) -> List[ReqkitBase]:
    """Parse rq- tags out of a raw string into reqkit objects.

    Tags are extracted from the surrounding non-xml text individually, since
    the source document as a whole is not valid XML. Only the opening tag's
    attributes are run through the XML parser; the body is kept as raw text,
    since it may be arbitrary source code containing unescaped `&`/`<`. Tags
    whose attributes fail to parse as XML, or fail reqkit validation, are
    skipped.
    """

    objs: List[ReqkitBase] = []
    for match in _TAG_PATTERN.finditer(text):
        tag, attrs, body = match.group(1), match.group(2), match.group(3)

        try:
            elem = ET.fromstring(f"<{tag}{attrs}/>")
        except ET.ParseError as e:
            print(f"Skipping tag that failed xml parsing: {match.group(0)!r} ({e})")
            continue

        try:
            objs.append(_TAG_CLASSES[tag](body=body, **elem.attrib))
        except ValidationError as e:
            print(f"Skipping tag that failed validation: {match.group(0)!r} ({e})")
            continue

    return objs

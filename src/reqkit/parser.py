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
    r"<(" + "|".join(_TAG_CLASSES) + r")\b[^>]*?(?:/>|>.*?</\1>)", re.DOTALL
)


def parse_str(text: str) -> List[ReqkitBase]:
    """Parse rq- tags out of a raw string into reqkit objects.

    Tags are extracted from the surrounding non-xml text individually, since
    the source document as a whole is not valid XML. Tags that fail to parse
    as XML, or fail reqkit validation, are skipped.
    """

    objs: List[ReqkitBase] = []
    for match in _TAG_PATTERN.finditer(text):
        raw = match.group(0)

        try:
            elem = ET.fromstring(raw)
        except ET.ParseError as e:
            print(f"Skipping tag that failed xml parsing: {raw!r} ({e})")
            continue

        try:
            objs.append(_TAG_CLASSES[elem.tag](body=elem.text, **elem.attrib))
        except ValidationError as e:
            print(f"Skipping tag that failed validation: {raw!r} ({e})")
            continue

    return objs

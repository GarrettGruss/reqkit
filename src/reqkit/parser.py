"""Parses raw strings into reqkit objects."""

from reqkit.types import ReqkitBase
from typing import List
# note: might require pydantic validators to implement parsing from raw string
# into reqkit objects

def parse_str(str) -> List[ReqkitBase]:
    """Parse a string into a list of reqkit objects."""

    # example input: 
    # <rq-req id="3a5cf8 subtype="fr" category="my_cat"></rq-req>
    # <rq-trace subtype="derive" category="my_cat" parent_id="3a5cf8"></rq-trace>
    # should parse this into
    # [ ReqkitRequirement(id="3a5cf8", subtype="fr", category="my_cat", body=""),
    #   ReqkitTrace(subtype="derive", category="my_cat", parent_id="3a5cf8")
    # ]

    raise NotImplementedError
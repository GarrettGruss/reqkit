"""Constructs a list of reqkit objects into a trace"""

from dataclasses import dataclass
from reqkit.types import ReqkitBase
from typing import List, Dict

@dataclass
class parse_object:
    parent: ReqkitBase
    children: List[ReqkitBase]
# alternative option would be to use treelib, since we are constructing
# a tree here.

def construct_traces(str) -> Dict[str, parse_object]:
    """Parse a string into a dictonary of reqkit traces."""

    # example input: <rq-trace subtype="derive" category="my_cat" parent_idid="3a5cf8></rq-req>
    # should parse this into
    # { "3a5cf8": [ReqkitTrace(subtype="fr", category="my_cat", body="")]
    # }

    # example input: <rq-trace parent_id="3a5cf8"

    raise NotImplementedError

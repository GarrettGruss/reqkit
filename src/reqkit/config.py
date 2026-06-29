"""Config for reqkit."""

import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class Config:
    generate_id_strategy = os.getenv("RQ_ID_STRATEGY", "hex")
    allowed_requirement_types = {"req", "fr", "nfr", "br", "ur", "tr", "sr"}
    allowed_relationship_types = {"satisfy", "derive", "trace", "verify", "refine"}

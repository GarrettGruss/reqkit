## System Requirements

Requirements fixture for testing purposes.

### Generation
- <rq-req id="fd0eb6" subtype="fr" category="minting">The system shall mint a unique six-character id for every new reqkit object.</rq-req>
- <rq-req id="dcb5ec" subtype="fr" category="minting" parent_id="fd0eb6" parent_rel="derive">Minted ids shall use a configurable generation strategy, defaulting to hex.</rq-req>
- <rq-req id="fb950e" subtype="tr" category="serialization">Requirement objects shall serialize to well-formed XML via ElementTree.</rq-req>
- <rq-req id="82b96f" subtype="ur" category="cli">Users shall be able to mint multiple requirements in a single CLI invocation.</rq-req>

### Parsing
- <rq-req id="7f6532" subtype="nfr" category="parsing">The parser shall reject malformed XML tags without raising an exception.</rq-req>
- <rq-req id="83ecc1" subtype="nfr" category="performance">Parsing a 10,000-line document shall complete in under one second.</rq-req>

### Traceability
- <rq-req id="223ea0" subtype="br" category="traceability">The tool shall support tracing every requirement back to its implementing code.</rq-req>
- <rq-req id="e8c152" subtype="req" category="reporting">The tracer shall classify each requirement as compliant, partially-compliant, or non-compliant.</rq-req>
- <rq-req id="eb29f1" subtype="sr" category="reporting" parent_id="e8c152" parent_rel="refine">The compliance report shall print orphaned trace counts for traces with unresolved parents.</rq-req>
- <rq-req id="5b24dd" subtype="sr" category="reporting">Stakeholders shall be able to review a compliance report summarizing trace coverage.</rq-req>

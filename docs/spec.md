# Object Types

Reqkit objects will take the form of various sysml objects. This will enable the system to parse all the Reqkit objects within a code base and construct a trace matrix.

## Design Mantra

- Make each program do one thing well. To do a new job, build afresh rather than complicate old programs by adding new "features".
- Expect the output of every program to become the input to another, as yet unknown, program. Don't clutter output with extraneous information. Avoid stringently columnar or binary input formats. Don't insist on interactive input.
- Design and build software, even operating systems, to be tried early, ideally within weeks. Don't hesitate to throw away the clumsy parts and rebuild them.
- Use tools in preference to unskilled help to lighten a programming task, even if you have to detour to build the tools and expect to throw some of them out after you've finished using them.
**Doug Mcllory, 1978**

## Core design shape

- Each reqkit object will be represented as pseudo-xml, meaning it adheres to XML schema, but will appear in non-xml documents. The parser will need to work across ts, c++, python, markdown, etc.
- Example shape: `<rq-element type="subtype" id="" parent_id="">encapsulated text</rq-element>`
- Each reqkit element will begin with the prefix `rq-` to enable the parser to pick elements out of source code without matching on xml or html elements with similar names. Risk: If someone does use the `rq-` prefix within an xml tag, there will be a collision.
- The parser should be capable of handling additional attributes. Users will want to encode more information into each reqkit element which we do not yet know of.

## Elements

### Requirement

`<rq-req type="" id="" category=""  parent_id="" parent_rel="">requirement text</rq-req>`
- requirements have an optional parent_id field to enable dependency tracing while retaining immutable IDs - this enables a requirement to exist within nesting within a trace element.
- id is an immutable hash assigned to each element on creation. It should be created by running the `rq mint` command.
- A requirement can have an optional type attribute, assume the type is `req` (requirement) for a general requirement. Other options: 
    * `req` (requirement)
    * `fr` (functional requirement)
    * `nfr` (non-functional requirement)
    * `br` (business requirement)
    * `ur` (user requirement)
    * `tr` (technical requirements)
    * `sr` (stakeholder requirement), 
- Category is an optional field that users can specify, such as `User interface`, `Data management`, `Integration` to seperate their design into domains. The parser can optional filter/sort a trace by these categories. The parser should lowercase and remove whitespace when validating this field.
- `parent_rel` is an optional field that defines the relationship of the element relative to it's parent.
    * `trace` - default and assumed value if null
    * `satisfy` - a dependency towards a parent requirement
    * `verify` - 



### Traces

`<rq-trace parent_id="" parent_rel="">encapsulated code</rq-trace>`

- Traces are reqkit objects that exist to establish an edge within the requirement graph. They can serve as references to guidelines, design docs, or source code implementation of a requirement. They do not need an ID
- inherits the parent_rel rules of requirements.

## References


Beyond tracing a requirement to the code that implements it, requirements can relate to *each other* and to other model elements (use cases, tests, diagrams). The following relation types (borrowed from SysML) describe the different kinds of edges in that graph:

| Relation | Description |
| --- | --- |
| **Satisfy** | A dependency between a requirement and a model element (code, design) that fulfills it. The arrow points from the satisfying (client) element to the (supplier) requirement being satisfied — this is the relation today's `# trace: <slug>` comments and `<ref>` tags approximate. |
| **Derive** | A dependency between two requirements, where a derived requirement is generated or inferred from a source requirement (e.g. a phase-2 requirement that exists because of a phase-1 decision). |
| **Copy** | A dependency between a supplier requirement (master) and a client requirement (slave), where the client's text is a read-only copy of the supplier's text — useful when the same requirement needs to appear in more than one document without forking its wording. |
| **Trace** | A dependency between a requirement and an arbitrary model element traced by that requirement, without implying satisfaction or verification — a looser link than `Satisfy`. |
| **Verify** | A dependency between a requirement and a test case (or other element) that can determine whether the system fulfills it. The arrow points from the (client) test case to the (supplier) requirement — this maps to the `<test>` tag and `TC`/`VC` slugs. |
| **Refine** | Describes how a model element (or set of elements) refines a requirement — e.g. a use case or activity diagram refining a text-based functional requirement, or elaborated text refining a coarser-grained model element. |

This is a design note only — these relation types are not implemented yet; today's slug graph only expresses `Satisfy`-like traces via prefix and tag.



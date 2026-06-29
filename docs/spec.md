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

| Relation | Description |
| --- | --- |
| **Satisfy** | A dependency between a requirement and a model element (code, design) that fulfills it. |
| **Derive** | A dependency between two requirements, where a derived requirement is generated or inferred from a source requirement. |
| **Trace** | A dependency between a requirement and an arbitrary model element traced by that requirement, without implying satisfaction or verification — a looser link than `Satisfy`. |
| **Verify** | A dependency between a requirement and a test case (or other element) that can determine whether the system fulfills it. The arrow points from the (client) test case to the (supplier) requirement. |
| **Refine** | Describes how a model element (or set of elements) refines a requirement — e.g. a use case or activity diagram refining a text-based functional requirement, or elaborated text refining a coarser-grained model element. |

### Traces

`<rq-trace parent_id="" parent_rel="">encapsulated code</rq-trace>`

- Traces are reqkit objects that exist to establish an edge within the requirement graph. They can serve as references to guidelines, design docs, or source code implementation of a requirement. They do not need an ID
- inherits the parent_rel rules of requirements.

## CLI

- `rq mint --type <subtypes> --category <rq_categories> --parent_id <rq_id> --parent_rel <rq_rels>`: Creates a new element with a minted tag. All fields are optional. Outputs to Cli
- `rq trace --root <rq_id>|<filename> --type <subtypes> --category <rq_categories> --scope <dir> --qty <int>`: Outputs a trace to stdio. returns a report detailing the number of each type of element traces, and the same metrics for master element. Verifies compliance (compliant, partially-compliant, non-compliant)
    * root is the required origin IDs to performe the trace against. This option is either an rq_id or a filename. Check first if it is a rq_id type, then fallback to filename.
    * type and category are optional filters to restrict the trace to this type of origin element types/categories
    * scope is an optional directory filter to restrict the trace.
    * qty is the number of objects to mint (repeats using the same input params)

### Trace
The trace function is the primary feature of reqkit - the ability to perform a deep recursive trace amongst the code base to asses compliance or drift against a requirement.

- user calls `rq trace --root <rq_id>|<filename> --type <subtypes> --category <rq_categories> --scope<dir>`
- if no scope is specified, tracer walks upwards to the .git dir, assume this is root of the project
- Tracer recursively walks the project, constructing a dictonary of `{<parent_id>:List[<rq_obj>]}`
> note: both `<rq_trace>` and `<rq_req>` should inherit from the base `<rq_obj>` class
> note: set an internal recursion limit in the ENV
- tracer walks the root document and constructs a list of origin elements. If an element does not satisfy the optional category or type filter, do not add it
- sort the origin elements list
- loop through the elements and map them to trace dictonary, constructing a trace object - need to define this as a dataclass
- Call the report function to dump the trace object to text
- print to stdio
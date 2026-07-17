#!/usr/bin/env python3
"""Generate the modular chapter files and the small standalone programs.

The generated files are deliberately plain LaTeX and C++.  This keeps the
book editable: a reader can open one chapter or one example without needing a
templating system.  The generator is retained so the complete source tree can
be rebuilt from a clean checkout.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PARTS = [
    ("Computers and Programming", "The machine model, translation pipeline, tools, and the first complete program.", [
        ("What a Computer Program Is", "A program is a description of a computation: inputs are transformed by rules into outputs or effects. The chapter distinguishes source text from the behavior a machine eventually performs and introduces the idea of an interface between a program and its environment."),
        ("Hardware, Software, and Operating Systems", "Programs run within layers. Processors execute instructions, memory stores state, devices expose effects, and operating systems mediate resources. The useful model is layered rather than a claim that every computer has one physical layout."),
        ("Source Code, Machine Code, and Executable Files", "Human-readable source is translated into target-specific object code and eventually an executable image. The chapter explains why the same source can produce different binaries without making portability mysterious."),
        ("Compilers, Linkers, Libraries, and Build Processes", "A compiler checks and translates a translation unit; a linker resolves references among object files and libraries. Build systems make those steps repeatable and avoid needless work."),
        ("Installing a C++ Development Environment", "A usable environment contains a compiler, standard library, debugger, editor, and build tools. Installation is treated as a reproducible configuration rather than a sequence of unexplained clicks."),
        ("Terminals, Editors, IDEs, and File Systems", "The terminal is a text interface to processes, not a programming language. Editors and IDEs add navigation and diagnostics, while the file system gives source files durable names and locations."),
        ("Writing, Compiling, and Running the First Program", "The first program makes the translation pipeline visible: create a source file, invoke the compiler, inspect the executable, run it, and observe standard output and the exit status."),
        ("Reading Compiler Diagnostics", "Diagnostics are evidence about a failed translation, not personal judgement. The chapter teaches readers to locate the first useful message, reduce the problem, and distinguish syntax, type, and linker failures."),
    ]),
    ("The Foundations of C++", "The core language vocabulary needed to read, write, and reason about ordinary programs.", [
        ("Program Structure", "C++ programs are made from declarations, definitions, functions, namespaces, and statements. Structure determines what names mean and what the implementation is allowed to do."),
        ("Statements, Expressions, and Blocks", "An expression computes a value or effect; a statement organizes execution; a block introduces a nested region. Understanding the distinction makes control flow and diagnostics easier to read."),
        ("Variables and Initialization", "A variable gives an object a name and a type. Initialization creates its initial state, while assignment changes an already existing object; confusing the two causes subtle bugs."),
        ("Fundamental Types", "Fundamental types describe categories such as integers, floating-point values, characters, booleans, and void. Their sizes and representations have implementation-defined aspects, so portable code relies on guarantees rather than guesses."),
        ("Literals", "Literals are source-level notation for values: numeric, character, string, boolean, and null-pointer literals. Suffixes and prefixes can change type and meaning."),
        ("Arithmetic and Operators", "Operators are syntax with specified operands, result types, sequencing, and possible conversions. Arithmetic becomes safer when ranges, overflow, and integer division are made explicit."),
        ("Comparisons and Boolean Logic", "Conditions combine comparisons and logical operators. Short-circuit evaluation is useful, but only when readers understand which operands are evaluated and when."),
        ("Input and Output", "Streams model formatted interaction with sources and sinks. The important engineering questions are parsing, failure states, buffering, and whether interactive input belongs in the domain logic."),
        ("Selection with if and switch", "Selection chooses behavior based on a condition or a discrete value. Good branches make invalid states visible and keep policy separate from mechanism."),
        ("Repetition with for, while, and do-while", "Loops express repeated work and an exit condition. Correct loop reasoning names the changing state, the termination condition, and the progress that makes termination plausible."),
        ("Scope, Lifetime, and Name Visibility", "Scope answers where a name can be used; lifetime answers when an object exists. They often align for local variables but are not the same concept."),
        ("Functions", "Functions name reusable behavior and establish a boundary for inputs, outputs, side effects, and tests. Small functions are useful when their boundaries reflect meaningful responsibilities."),
        ("Function Parameters and Return Values", "Parameters and return values form a function's value-level interface. Passing by value, reference, pointer, or view communicates different ownership and lifetime expectations."),
        ("Overloading and Default Arguments", "Overloading lets one name denote several signatures, while default arguments fill omitted values. Both features can improve interfaces but can also create ambiguity and surprising calls."),
        ("Type Deduction with auto", "auto asks the compiler to deduce a type from an initializer. It removes repetition without removing type checking, but reference, const, and value-category rules still matter."),
        ("Constants and constexpr", "const prevents mutation through a particular name; constexpr makes constant evaluation possible when the rules permit it. Compile-time computation is a guarantee about evaluation, not a promise that every function runs at compile time."),
        ("Enumerations", "Enumerations represent a closed set of named values. Scoped enumerations make conversions and ownership of names more explicit than unscoped alternatives."),
        ("Namespaces", "Namespaces control name collisions and communicate ownership. Qualification is often clearer than broad using-directives, particularly in headers and public interfaces."),
    ]),
    ("Data and Memory", "Representation, text, containers, pointers, ownership, and object lifetime without folklore.", [
        ("Binary Representation", "Bits are a model for representing information, not a license to assume a particular machine layout. The chapter introduces bases, bytes, object representations, and the limits of representation-based reasoning."),
        ("Integers, Floating-Point Values, and Precision", "Integer arithmetic and floating-point arithmetic have different error models. Range, rounding, comparison, and conversion choices should follow the problem rather than intuition from decimal notation."),
        ("Characters, Text, Encoding, and Unicode", "A character, a code point, a code unit, and a user-perceived grapheme are distinct ideas. std::string stores bytes; text correctness requires an explicit encoding policy."),
        ("Arrays", "Built-in arrays provide contiguous elements and fixed extent, but decay and bounds mistakes make interfaces fragile. The chapter explains what the type really is before introducing safer views."),
        ("std::array", "std::array gives a fixed-size sequence with value semantics, standard-library interoperability, and a size that is part of the type. It is often a better default than a built-in array."),
        ("std::vector", "std::vector owns a contiguous dynamic sequence. Size, capacity, iterator invalidation, and reallocation determine which references remain valid after a mutation."),
        ("std::string and std::string_view", "std::string owns text storage; std::string_view borrows a range of characters. A view is efficient only when its source outlives every use of the view."),
        ("References", "A reference is an alias with binding rules, not a reseatable pointer and not an ownership token. References make non-null borrowing expressive but do not extend lifetime automatically."),
        ("Pointers", "A pointer is an object that can hold an address or a null value. It can represent optional access or navigation; it becomes ownership only through an explicit protocol."),
        ("Null Pointers", "A null pointer represents no pointed-to object. Comparing, testing, and avoiding dereference are simple rules, but nullable interfaces should be used only when absence is meaningful."),
        ("Dynamic Storage", "Dynamic storage supports objects whose size or lifetime is not conveniently tied to a local scope. Modern C++ hides raw allocation behind containers and resource-owning types whenever possible."),
        ("Stack and Free-Store Concepts", "Stack and free-store are useful implementation-level terms, not universal standard categories. The language specifies storage duration and lifetime; implementations choose how those are realized."),
        ("Object Lifetime", "An object has a lifetime with a beginning and an end. Using storage outside that lifetime, or with the wrong type, is a correctness error even if the bytes look unchanged."),
        ("Resource Ownership", "Files, locks, sockets, and memory all require a release protocol. Ownership answers who is responsible, when responsibility transfers, and how failure preserves the protocol."),
        ("Smart Pointers", "unique_ptr expresses exclusive ownership, shared_ptr expresses shared ownership, and weak_ptr observes shared ownership without keeping it alive. The choice is a design statement, not a performance superstition."),
        ("RAII", "Resource acquisition is initialization binds release to deterministic destruction. RAII makes early returns and exceptions ordinary control-flow paths rather than leaks to be remembered manually."),
        ("Copy and Move Semantics", "Copying duplicates a value or resource representation; moving transfers or cheaply reuses resources. A type's special members should preserve its invariants and ownership rules."),
        ("Value Categories", "Expressions have categories that affect binding, overload resolution, and moving. The useful beginner model is lvalue as an identifiable object and rvalue as a temporary or expiring value; the formal model is more precise."),
        ("Undefined, Unspecified, and Implementation-Defined Behavior", "These labels describe different degrees of freedom in the standard. Correct engineering avoids undefined behavior, documents implementation choices, and does not mistake one observed result for a guarantee."),
    ]),
    ("User-Defined Types", "Classes, invariants, polymorphism, and a wider view of C++ design than object orientation alone.", [
        ("Structures", "A struct groups related data and can provide behavior. In C++, struct and class differ primarily in default access, not in expressive power."),
        ("Classes and Objects", "A class defines a type; an object is an instance with state and lifetime. A good type makes valid states easy to construct and invalid states difficult to represent."),
        ("Access Control", "public, protected, and private establish compile-time access boundaries. Encapsulation is not secrecy; it is control over which operations can preserve an abstraction's rules."),
        ("Constructors", "Constructors establish initial invariants. Member-initializer lists, delegating constructors, and explicit conversions make construction predictable and resistant to partial initialization."),
        ("Destructors", "Destruction releases owned resources and ends an object's lifetime. Destructors should be reliable, bounded in responsibility, and normally non-throwing."),
        ("Invariants", "An invariant is a condition that must hold at defined boundaries. Naming invariants turns informal assumptions into reviewable design and test obligations."),
        ("Member Functions", "Member functions operate with an implicit object parameter. Their constness, ref-qualification, and exception behavior are part of the type's interface."),
        ("const Correctness", "const communicates non-mutation through a particular access path. It is a useful local guarantee, but it does not make pointed-to objects immutable or make concurrent access safe."),
        ("Static Members", "Static data and functions belong to the class rather than one object. They can represent shared policy or state, but global lifetime and synchronization costs should be explicit."),
        ("Operator Overloading", "Overloaded operators can make domain values readable when they preserve familiar meaning. Operators should not disguise expensive effects or surprising state changes."),
        ("Composition", "Composition builds a type from collaborating parts. It usually makes dependencies and replacement boundaries clearer than a deep inheritance hierarchy."),
        ("Inheritance", "Inheritance expresses a relationship between a derived type and a base interface or implementation. Public inheritance is a substitutability claim, not merely code reuse."),
        ("Runtime Polymorphism", "Runtime polymorphism selects an operation through a dynamic type. It is useful when the set of concrete types varies at runtime and a stable interface matters."),
        ("Abstract Interfaces", "An abstract interface states capabilities without choosing a representation. Small interfaces reduce accidental coupling and make test doubles more practical."),
        ("Virtual Functions", "Virtual dispatch enables runtime polymorphism but introduces lifetime and destruction requirements. A polymorphic base normally needs a virtual destructor when deleted through the base interface."),
        ("Object Slicing", "Copying a derived object into a base value discards the derived part. References, pointers, and value-oriented alternatives avoid slicing when polymorphism is intended."),
        ("Multiple Inheritance", "Multiple inheritance can model independent interfaces or shared implementation, but ambiguity and layout complexity increase. It is most defensible when each base has a clear role."),
        ("Alternatives to Inheritance", "Variants, concepts, type erasure, composition, and tagged data can express variation without a class hierarchy. The right choice depends on when the set of alternatives is known and who owns extension."),
    ]),
    ("The Standard Library", "Reusable, specified components for data, algorithms, time, files, and common program infrastructure.", [
        ("The Purpose and Structure of the Standard Library", "The standard library supplies vocabulary types, containers, algorithms, utilities, and I/O. Learning its structure prevents unnecessary reinvention and makes code legible to other C++ programmers."),
        ("Containers", "Containers define ownership, access patterns, complexity, and invalidation rules. Choosing one is a data-access decision, not merely a syntax decision."),
        ("Iterators", "Iterators generalize traversal across containers and ranges. Their validity and category determine which algorithms are legal and what complexity they can achieve."),
        ("Algorithms", "Algorithms separate what should be done from how a container stores elements. Preconditions, projections, predicates, and complexity are part of an algorithm's contract."),
        ("Ranges and Views", "Ranges compose algorithms and views with less iterator plumbing. Views are usually lazy and non-owning, so lifetime and repeated evaluation remain design concerns."),
        ("Function Objects", "Callable objects include functions, pointers to functions, lambdas, and types with operator(). They let algorithms receive behavior without committing to one global name."),
        ("Lambda Expressions", "Lambdas create local callable objects with explicit capture and parameter rules. Capture is a lifetime decision, especially when a callable escapes its defining scope."),
        ("Associative Containers", "Ordered maps and sets use keys and ordering to provide logarithmic operations under their specified complexity model. Key comparability and iterator stability shape their use."),
        ("Unordered Containers", "Hash tables use a hash function and an equality relation. Average-case performance depends on distribution and load, while worst-case behavior remains part of robust design."),
        ("Stacks, Queues, and Priority Queues", "Adaptors expose restricted interfaces for disciplined access patterns. Restricting operations can make invariants and intent clearer."),
        ("Optional Values and Variants", "optional represents a value that may be absent; variant represents one active alternative from a closed set. Both make state explicit without sentinel values."),
        ("Tuples", "Tuples group heterogeneous values without naming a domain type. They are useful for local composition but can become opaque at public API boundaries."),
        ("Time and Clocks", "A duration is an amount of time; a time point is a position on a clock. Steady clocks are appropriate for elapsed-time measurement; wall clocks can jump."),
        ("Random-Number Facilities", "Random engines generate deterministic sequences from state; distributions map those sequences to a desired statistical shape. Reproducibility, seeding, and security requirements must be separated."),
        ("File Input and Output", "File streams connect C++ objects to persistent bytes. Correct file handling checks open and operation states, specifies encoding and format, and separates parsing from storage policy."),
        ("Formatting", "Formatting turns values into human-readable or machine-readable text. Locale, escaping, alignment, and available library support all affect portability and correctness."),
        ("Filesystem Operations", "std::filesystem supplies path and directory vocabulary across platforms. Paths are not strings with universal separators, and failures can arise from permissions, races, or missing entries."),
    ]),
    ("Generic Programming", "Templates and compile-time reasoning as tools for reusable interfaces, not puzzles for their own sake.", [
        ("Function Templates", "A function template describes a family of functions parameterized by types or values. Instantiation produces a concrete specialization checked for the actual arguments."),
        ("Class Templates", "A class template describes a family of related types. Its parameters can encode element types, policies, allocators, or compile-time dimensions."),
        ("Template Argument Deduction", "Deduction matches argument types against a template pattern. References, cv-qualification, arrays, and conversions explain many surprising results."),
        ("Concepts and Constraints", "Concepts state requirements on template arguments in a readable form. Constraints improve overload selection and diagnostics, but they do not replace semantic documentation."),
        ("Variadic Templates", "Parameter packs represent an arbitrary number of arguments or types. Fold expressions make common reductions concise, while recursive designs remain useful for some structural problems."),
        ("Compile-Time Programming", "Compile-time programming moves selected work into translation. The benefit is an earlier check or a generated specialization, not a blanket claim that compile-time code is always faster."),
        ("constexpr Evaluation", "constexpr permits evaluation during constant evaluation when all rules are satisfied. The same function can often remain usable at runtime, which supports one source of truth."),
        ("Type Traits", "Type traits query or transform type properties. They are building blocks for generic constraints and adaptation, but a named concept is often clearer at an API boundary."),
        ("Generic Algorithms", "A generic algorithm states its needed operations and works across many types. Correctness depends on documenting semantic requirements that syntax alone cannot express."),
        ("Template Errors and Diagnostics", "Template diagnostics can be long because the compiler reports substitutions and overload candidates. Reducing the example and adding constraints makes failures actionable."),
    ]),
    ("Errors, Testing, and Reliability", "Failure modes, evidence, and tools for finding defects before users do.", [
        ("Syntax, Linker, Logic, and Runtime Errors", "Different failure classes arise at different stages. Classification narrows the search and prevents treating every failure as a compiler problem."),
        ("Assertions", "Assertions state conditions expected to be true when a defect would indicate a programming error. They complement, rather than replace, handling of ordinary external failures."),
        ("Exceptions", "Exceptions transfer control out of a failing operation. Good exception design names the boundary, preserves invariants, and avoids using exceptions as invisible ordinary control flow."),
        ("Error Codes", "Error codes make failure part of a value-level protocol. They are explicit and useful at low-level or performance-sensitive boundaries, but callers must not ignore them."),
        ("Expected-Style Error Handling", "An expected-style result carries either a value or an error. It makes recoverable failure visible in the type and composes well when the caller can act locally."),
        ("Exception Safety", "The no-throw, strong, and basic guarantees describe what remains true when an operation fails. These guarantees are design properties of operations, not decorative labels."),
        ("Unit Testing", "Unit tests isolate a small behavior and make its contract executable. A good test fails for a meaningful reason and remains independent of unrelated timing or global state."),
        ("Integration Testing", "Integration tests exercise boundaries among real components. They catch configuration, serialization, file, and lifecycle defects that unit tests intentionally exclude."),
        ("Property-Based Testing", "Property-based testing generates many inputs to check general relationships. The property must be a real invariant, not a restatement of the implementation."),
        ("Test Doubles", "Stubs, fakes, spies, and mocks replace collaborators for a test. They are useful when a boundary is expensive or nondeterministic, but excessive mocking can test a design's seams rather than its behavior."),
        ("Debuggers", "A debugger observes a running process through breakpoints, stack frames, variables, and watchpoints. Observation changes timing, so a debugger is evidence, not an infallible explanation of concurrent behavior."),
        ("Sanitizers", "Address, undefined-behavior, and thread sanitizers instrument programs to catch classes of defects. They increase cost and coverage needs but often turn mysterious symptoms into local failures."),
        ("Static Analysis", "Static analyzers inspect code without executing every path. Warnings are hypotheses that require triage, not proof that every reported line is wrong."),
        ("Logging", "Logs record selected events and context for diagnosis. Levels, stable fields, privacy, volume, and correlation identifiers determine whether logs are useful in production."),
        ("Reproducing and Minimizing Bugs", "A reproducible failure is a scientific foothold. Reduce inputs, environment, and timing until the smallest case still demonstrates the defect."),
        ("Defensive Programming", "Defensive programming makes assumptions explicit at boundaries and preserves invariants. It should improve failure behavior without obscuring the actual contract."),
    ]),
    ("Data Structures and Algorithms", "Ways to represent problems, compare costs, and select algorithms using evidence.", [
        ("Algorithmic Thinking", "Algorithmic thinking names state, operations, invariants, termination, and cost before code. It turns a vague task into a sequence that can be reviewed and tested."),
        ("Measuring Time and Space", "Time and space measurements depend on a workload, environment, and measurement method. A number without those conditions is not a portable fact."),
        ("Asymptotic Complexity", "Asymptotic notation describes how resource use grows as input size grows. It abstracts constants and hardware, which is useful for scaling questions but insufficient for every engineering choice."),
        ("Recursion", "Recursion solves a problem through smaller instances and a base case. Correctness requires progress toward the base case; performance requires understanding call depth and repeated work."),
        ("Searching", "Searching strategies exploit different structure: linear scans need little organization, while binary search needs ordering and a precise range invariant."),
        ("Sorting", "Sorting establishes an ordering that can simplify later work. Stability, memory use, comparator correctness, and complexity all matter beyond the name of an algorithm."),
        ("Linked Structures", "Linked structures connect nodes through references or pointers. They teach ownership and invalidation, but their pointer flexibility can trade away locality and simplicity."),
        ("Stacks and Queues", "Stacks and queues restrict access to express last-in-first-out or first-in-first-out policy. The abstraction often matters more than the underlying container."),
        ("Trees", "Trees represent hierarchical relationships with acyclic parent-child structure. Balance, ordering, ownership, and traversal determine whether a tree solves the actual problem."),
        ("Heaps", "A heap maintains a partial order that makes an extreme element accessible. It is useful for priority queues and selection, not for producing a fully sorted sequence by itself."),
        ("Hash Tables", "Hash tables map keys to buckets using a hash function. Correct equality and hash consistency are mandatory; collisions and load determine observed performance."),
        ("Graphs", "Graphs model entities and relationships. Choosing directedness, weights, and representation precedes selecting traversal or shortest-path algorithms."),
        ("Dynamic Programming", "Dynamic programming stores solutions to overlapping subproblems. A recurrence, state definition, base case, and evaluation order make the optimization auditable."),
        ("Greedy Algorithms", "Greedy algorithms commit to a locally attractive choice. They are correct only when a proof or established property connects local choices to a global optimum."),
        ("Algorithm Selection", "Selection balances contract, constraints, maintainability, data shape, and measured performance. A theoretically optimal algorithm can be the wrong engineering choice for a small or changing workload."),
        ("Benchmarking", "A benchmark is an experiment with a workload, harness, environment, and statistical summary. It measures that experiment, not every future use of the code."),
    ]),
    ("Professional C++ Development", "Source organization, builds, interfaces, version control, portability, and long-lived software.", [
        ("Organizing Source and Header Files", "Headers expose declarations and reusable definitions; source files hold implementation details. Organization should express ownership and minimize unnecessary recompilation."),
        ("One Definition Rule", "The One Definition Rule constrains which entities may have one or multiple definitions across a program. Violations can compile and still produce ill-formed or fragile binaries."),
        ("Separate Compilation", "Separate compilation turns translation units into independently compiled objects. Stable interfaces and dependency boundaries make large builds faster and easier to reason about."),
        ("Libraries", "A library packages reusable code as source, static binaries, or shared binaries. Consumers need a compatible interface, build configuration, and ABI story."),
        ("Modules and Their Support Status", "Modules aim to replace textual inclusion with named interfaces and faster, more isolated imports. They are standardized in stages, but toolchain support and build integration remain important practical constraints."),
        ("CMake", "CMake describes targets, properties, dependencies, tests, and installation rather than hard-coding one platform's commands. Generators then produce a native build system."),
        ("Dependency Management", "Dependencies add capabilities and also add licensing, update, security, ABI, and reproducibility obligations. A dependency policy is part of system design."),
        ("Package Managers", "Package managers resolve and build external libraries. Locking versions and documenting triplets, toolchains, and feature choices keeps builds reproducible."),
        ("Version Control with Git", "Version control records changes as reviewable history. Small commits, meaningful messages, and reproducible branches reduce the cost of collaboration and recovery."),
        ("Documentation", "Documentation explains intent, contracts, constraints, and operations. It should answer questions that code alone cannot, without duplicating every implementation detail."),
        ("API Design", "An API is a promise about names, types, ownership, failure, timing, and compatibility. Good APIs make common correct use easy and unsupported use visible."),
        ("Coding Conventions", "Conventions reduce accidental variation and make review focus on behavior. They are most valuable when automated and kept subordinate to correctness."),
        ("Refactoring", "Refactoring changes structure while preserving externally observable behavior. Tests and small steps provide evidence that the intended behavior survived."),
        ("Code Review", "Code review is a second line of reasoning about correctness, risk, and maintainability. Review comments should identify evidence and consequences rather than preferences alone."),
        ("Continuous Integration", "Continuous integration builds and tests changes in a clean, repeatable environment. It is a feedback system, not a substitute for design or local verification."),
        ("Portability", "Portable code depends on specified behavior and isolates platform assumptions. Portability is a property of an interface and build process, not just of source syntax."),
        ("Cross-Platform Development", "Operating systems differ in paths, processes, sockets, time, signals, and toolchains. A portable core plus narrow adapters often contains the differences cleanly."),
        ("Application Binary Interfaces", "An ABI covers calling conventions, object layout, name mangling, exception boundaries, and binary compatibility. Source compatibility does not imply ABI compatibility."),
        ("Interoperability with C", "C interoperability requires a compatible data and calling boundary, usually with extern \"C\" and C-compatible types. Ownership and error conventions must cross the boundary explicitly."),
        ("Interoperability with Other Languages", "Language interoperability is an interface-design problem involving data representation, calling conventions, ownership, errors, and packaging. A narrow C ABI is often a useful stable boundary."),
    ]),
    ("Concurrency", "Processes, threads, synchronization, atomicity, and the memory model as correctness topics.", [
        ("Processes and Threads", "Processes isolate address spaces and resources; threads share an address space within a process. The distinction changes failure, communication, and synchronization costs."),
        ("Race Conditions", "A race exists when correctness depends on an uncontrolled ordering of operations. A program can appear correct for thousands of runs and still contain a race."),
        ("Mutual Exclusion", "Mutual exclusion protects a critical invariant by allowing one participant at a time. The protected region should be small, explicit, and paired with a clear ownership rule."),
        ("Locks", "Locks provide synchronization protocols, not automatic correctness. Lock ordering, scope, contention, and exception-safe release determine whether a design remains live."),
        ("Condition Variables", "A condition variable lets a thread sleep until shared state may have changed. Waiting must always re-check a predicate because wakeups are not proofs that the condition holds."),
        ("Futures and Asynchronous Work", "Futures represent a result that may become available later. Launch policy, exception propagation, cancellation, and destruction semantics must be documented."),
        ("Atomic Operations", "Atomics provide indivisible operations and synchronization orders for selected objects. They do not make a multi-object invariant automatically safe."),
        ("The C++ Memory Model", "The memory model describes visibility, ordering, happens-before, and data races. It explains why compiler and processor reordering can matter even when source statements look sequential."),
        ("Deadlocks and Livelocks", "Deadlock stops progress through circular waiting; livelock continues activity without useful progress. Avoidance requires resource-ordering and progress reasoning, not just more threads."),
        ("Thread-Safe Design", "Thread safety is a property of an interface under concurrent use. Immutable values, ownership transfer, message passing, and narrow synchronized boundaries often outperform shared mutable state as a design strategy."),
        ("Parallel Algorithms", "Parallel algorithms divide work under a policy, but speedup depends on independence, granularity, scheduling, memory bandwidth, and overhead."),
        ("Task-Based Concurrency", "Task-based designs express units of work and dependencies rather than manually managing every thread. They improve composition when the scheduler and cancellation model are understood."),
    ]),
    ("Performance and Systems", "Measurement, hardware-aware reasoning, optimization, and choosing the right tool.", [
        ("What Performance Means", "Performance can mean latency, throughput, memory use, startup time, tail behavior, energy, or cost. A useful optimization starts by naming which one matters."),
        ("Profiling Before Optimization", "Profiling locates observed cost in a workload. It prevents optimizing code that is elegant or suspicious but irrelevant to the actual bottleneck."),
        ("CPU, Cache, and Memory Locality", "Modern processors move data through a hierarchy. Locality is a useful model for why access patterns matter, but exact timings are architecture and workload dependent."),
        ("Allocation Costs", "Allocation has time, fragmentation, synchronization, and lifetime consequences. Fewer allocations can help, but pooling or custom allocators also add complexity and should be measured."),
        ("Data-Oriented Design", "Data-oriented design chooses representation and iteration around access patterns. It complements object-oriented boundaries when data movement dominates runtime cost."),
        ("Inlining and Optimization", "Inlining is a compiler transformation, not a source-level command to make code fast. It can remove call overhead or expose optimization, but can also increase code size."),
        ("Compiler Optimization", "Optimization flags change generated code under the language rules. They do not repair undefined behavior or make an invalid program valid."),
        ("Benchmark Design", "A benchmark needs representative inputs, warm-up policy, measurement boundaries, repetition, and a way to avoid measuring dead-code elimination or setup accidentally."),
        ("Latency and Throughput", "Latency measures the time for one operation; throughput measures completed work per unit time. A system can improve one while worsening the other."),
        ("Performance Portability", "An optimization that helps one compiler or processor can harm another. Portable performance comes from a clear model, measurement on target environments, and modest assumptions."),
        ("Safe Optimization", "Safe optimization preserves contracts and makes the reason for a change reviewable. Correctness tests and before/after measurements are part of the optimization itself."),
        ("When C++ Is an Appropriate Tool", "C++ is a strong choice when control over resource use, predictable performance, existing ecosystems, or native integration matters. Its costs include language complexity and a larger safety burden."),
        ("When Another Language May Be Better", "A different language may reduce development time, memory-safety risk, or operational complexity. Choosing C++ should be a comparative engineering decision rather than an identity claim."),
    ]),
    ("Advanced Language and Design", "Advanced mechanisms introduced through the problems they solve and the complexity they incur.", [
        ("Advanced Type-System Concepts", "Types can encode ownership, alternatives, constraints, units, and state transitions. Strong types are valuable when their invariants justify the additional vocabulary."),
        ("Perfect Forwarding", "Perfect forwarding preserves value category and cv-qualification across a generic boundary. It is powerful for wrappers and factories but can make overload behavior harder to read."),
        ("Customization and Generic Interfaces", "Customization points let generic code adapt to user types without hard-coding every type. A good customization protocol documents discovery, precedence, and semantic requirements."),
        ("Allocators and Memory Resources", "Allocators separate allocation policy from container logic; memory resources provide runtime allocation strategies through an interface. They are useful for arenas and locality, not as default decoration."),
        ("Coroutines", "Coroutines suspend and resume a computation while a library-defined promise type controls the surrounding protocol. The language supplies machinery; scheduling, lifetime, and cancellation remain design responsibilities."),
        ("Advanced Ranges", "Advanced ranges compose lazy transformations, filters, projections, and sentinels. The main risks are borrowed lifetimes, repeated work, and interfaces that hide expensive evaluation."),
        ("Metaprogramming", "Metaprogramming generates or selects code at translation time. It can remove duplication and enforce invariants, but generated complexity must remain explainable to maintainers."),
        ("Type Erasure", "Type erasure stores values behind a uniform interface while hiding their concrete type. It trades some compile-time visibility for runtime flexibility and stable boundaries."),
        ("Policy-Based Design", "Policy-based design parameterizes a type with independent behaviors. It can create precise reusable components, but too many policies can make the resulting type difficult to understand."),
        ("Architectural Patterns", "Architecture allocates responsibilities and dependencies across a system. Patterns are vocabulary for recurring trade-offs, not templates that remove the need for domain reasoning."),
        ("Design Patterns in Modern C++", "Modern C++ changes the cost and shape of classic patterns through value semantics, lambdas, concepts, smart pointers, and standard components. Use the simplest mechanism that expresses the intent."),
        ("Domain Modeling", "Domain modeling gives important concepts explicit names, invariants, and operations. A useful model reflects decisions and constraints rather than mirroring every database column."),
        ("Stable Interfaces", "A stable interface controls source, binary, behavioral, and operational compatibility. Compatibility is a budget with costs, not a property acquired by adding more abstraction."),
        ("Large-Codebase Architecture", "Large systems need dependency direction, ownership of decisions, build boundaries, observability, and migration paths. Architecture is tested by how safely the system changes."),
        ("Legacy-Code Modernization", "Modernization reduces risk while preserving necessary behavior. Characterization tests, seams, staged replacement, and explicit deprecation are more reliable than a wholesale rewrite by optimism."),
    ]),
]


def tex_escape(text: str) -> str:
    """Escape ordinary prose for LaTeX."""
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def safe_filename(number: int) -> str:
    return f"ch{number:03d}"


def cxx_string(text: str) -> str:
    return json.dumps(text, ensure_ascii=True)


def chapter_program(number: int, title: str) -> str:
    """Return one complete, standalone, C++23 program for a chapter."""
    common = f"// Modern C++ - Chapter {number}: {title}\n"
    special: dict[int, str] = {
        7: '#include <iostream>\n\nint main() {\n    std::cout << "Hello, modern C++!\\n";\n    return 0;\n}\n',
        11: '#include <iostream>\n\nint main() {\n    const int items = 3;\n    const double price = 4.50;\n    std::cout << items * price << "\\n";\n}\n',
        17: '#include <iostream>\n\nint main() {\n    const int score = 72;\n    if (score >= 60) {\n        std::cout << "pass\\n";\n    } else {\n        std::cout << "retry\\n";\n    }\n}\n',
        18: '#include <iostream>\n\nint main() {\n    int total = 0;\n    for (int value = 1; value <= 5; ++value) {\n        total += value;\n    }\n    std::cout << total << "\\n";\n}\n',
        20: '#include <iostream>\n\nint square(int value) {\n    return value * value;\n}\n\nint main() {\n    std::cout << square(7) << "\\n";\n}\n',
        32: '#include <iostream>\n#include <vector>\n\nint main() {\n    const std::vector<int> values{2, 4, 6, 8};\n    for (const int value : values) {\n        std::cout << value << " ";\n    }\n    std::cout << "\\n";\n}\n',
        33: '#include <iostream>\n#include <string>\n\nint main() {\n    const std::string language = "C++";\n    std::cout << language.size() << "\\n";\n}\n',
        35: '#include <iostream>\n\nint main() {\n    int value = 42;\n    int* pointer = &value;\n    if (pointer != nullptr) {\n        std::cout << *pointer << "\\n";\n    }\n}\n',
        41: '#include <iostream>\n#include <memory>\n\nint main() {\n    auto value = std::make_unique<int>(42);\n    std::cout << *value << "\\n";\n}\n',
        42: '#include <iostream>\n#include <string>\n\nclass Message {\npublic:\n    explicit Message(std::string text) : text_(std::move(text)) {\n        std::cout << "acquired\\n";\n    }\n    ~Message() { std::cout << "released\\n"; }\nprivate:\n    std::string text_;\n};\n\nint main() {\n    Message message{"RAII"};\n}\n',
        43: '#include <iostream>\n#include <string>\n#include <utility>\n\nint main() {\n    std::string original = "resource";\n    std::string moved = std::move(original);\n    std::cout << moved << "\\n";\n}\n',
        47: '#include <iostream>\n\nclass Counter {\npublic:\n    void increment() { ++value_; }\n    int value() const { return value_; }\nprivate:\n    int value_{0};\n};\n\nint main() {\n    Counter counter;\n    counter.increment();\n    std::cout << counter.value() << "\\n";\n}\n',
        58: '#include <iostream>\n#include <memory>\n#include <vector>\n\nstruct Shape {\n    virtual ~Shape() = default;\n    virtual int area() const = 0;\n};\nstruct Square final : Shape {\n    explicit Square(int side) : side(side) {}\n    int area() const override { return side * side; }\n    int side;\n};\n\nint main() {\n    std::vector<std::unique_ptr<Shape>> shapes;\n    shapes.push_back(std::make_unique<Square>(5));\n    std::cout << shapes.front()->area() << "\\n";\n}\n',
        67: '#include <algorithm>\n#include <iostream>\n#include <vector>\n\nint main() {\n    std::vector<int> values{4, 1, 3, 2};\n    std::sort(values.begin(), values.end());\n    for (const int value : values) { std::cout << value << " "; }\n    std::cout << "\\n";\n}\n',
        70: '#include <algorithm>\n#include <iostream>\n#include <vector>\n\nint main() {\n    const std::vector<int> values{1, 2, 3, 4};\n    const auto even = std::count_if(values.begin(), values.end(), [](int value) {\n        return value % 2 == 0;\n    });\n    std::cout << even << "\\n";\n}\n',
        74: '#include <iostream>\n#include <variant>\n#include <string>\n\nint main() {\n    std::variant<int, std::string> result = std::string{"ready"};\n    std::visit([](const auto& value) { std::cout << value << "\\n"; }, result);\n}\n',
        78: '#include <fstream>\n#include <iostream>\n#include <string>\n\nint main() {\n    const std::string path = "modern_cpp_example.txt";\n    { std::ofstream output(path); output << "portable text\\n"; }\n    std::ifstream input(path);\n    std::string line;\n    std::getline(input, line);\n    std::cout << line << "\\n";\n}\n',
        80: '#include <filesystem>\n#include <iostream>\n\nint main() {\n    const auto path = std::filesystem::current_path();\n    std::cout << path.filename().string() << "\\n";\n}\n',
        81: '#include <iostream>\n\ntemplate <typename T>\nT maximum(T left, T right) {\n    return left < right ? right : left;\n}\n\nint main() {\n    std::cout << maximum(3, 8) << "\\n";\n}\n',
        84: '#include <concepts>\n#include <iostream>\n\ntemplate <std::integral T>\nT add(T left, T right) { return left + right; }\n\nint main() {\n    std::cout << add(2, 3) << "\\n";\n}\n',
        93: '#include <iostream>\n#include <stdexcept>\n\nint divide(int numerator, int denominator) {\n    if (denominator == 0) { throw std::invalid_argument{"zero denominator"}; }\n    return numerator / denominator;\n}\n\nint main() {\n    try { std::cout << divide(8, 2) << "\\n"; }\n    catch (const std::exception& error) { std::cerr << error.what() << "\\n"; return 1; }\n}\n',
        95: '#include <iostream>\n#include <string>\n#include <variant>\n\nstruct Error { std::string message; };\nusing Result = std::variant<int, Error>;\n\nResult parse_positive(int value) {\n    if (value < 0) return Error{"negative value"};\n    return value;\n}\n\nint main() {\n    const Result result = parse_positive(4);\n    std::visit([](const auto& value) {\n        if constexpr (std::is_same_v<std::decay_t<decltype(value)>, Error>) std::cout << value.message << "\\n";\n        else std::cout << value << "\\n";\n    }, result);\n}\n',
        112: '#include <algorithm>\n#include <iostream>\n#include <vector>\n\nint main() {\n    std::vector<int> values{9, 4, 7, 1};\n    std::sort(values.begin(), values.end());\n    std::cout << values.front() << " " << values.back() << "\\n";\n}\n',
        118: '#include <iostream>\n#include <queue>\n#include <vector>\n\nint main() {\n    const std::vector<std::vector<int>> graph{{1, 2}, {0, 3}, {0}, {1}};\n    std::vector<bool> seen(graph.size());\n    std::queue<int> pending;\n    pending.push(0); seen[0] = true;\n    while (!pending.empty()) {\n        const int node = pending.front(); pending.pop();\n        std::cout << node << " ";\n        for (const int next : graph[node]) if (!seen[next]) { seen[next] = true; pending.push(next); }\n    }\n    std::cout << "\\n";\n}\n',
        143: '#include <iostream>\n#include <thread>\n\nint main() {\n    std::jthread worker([] { std::cout << "worker\\n"; });\n    std::cout << "main\\n";\n}\n',
        149: '#include <atomic>\n#include <iostream>\n#include <thread>\n\nint main() {\n    std::atomic<int> count{0};\n    std::jthread first([&] { for (int i = 0; i < 1000; ++i) ++count; });\n    std::jthread second([&] { for (int i = 0; i < 1000; ++i) ++count; });\n    first.join(); second.join();\n    std::cout << count.load() << "\\n";\n}\n',
        175: '#include <functional>\n#include <iostream>\n#include <string>\n\nint main() {\n    std::function<std::string()> message = [] { return std::string{"erased"}; };\n    std::cout << message() << "\\n";\n}\n',
    }
    program = special.get(number)
    if program is None:
        program = "#include <iostream>\n\nint main() {\n    std::cout << " + cxx_string(f"Chapter {number}: {title}") + " << \"\\n\";\n}\n"
    if number == 42:
        program = program.replace("#include <string>\n", "#include <string>\n#include <utility>\n")
    if number == 95:
        program = program.replace("#include <string>\n", "#include <string>\n#include <type_traits>\n")
    if number == 118:
        program = program.replace("#include <queue>\n", "#include <cstddef>\n#include <queue>\n")
        program = program.replace("std::vector<std::vector<int>> graph", "std::vector<std::vector<std::size_t>> graph")
        program = program.replace("std::queue<int> pending;", "std::queue<std::size_t> pending;")
        program = program.replace("const int node = pending.front();", "const std::size_t node = pending.front();")
        program = program.replace("const int next : graph[node]", "const std::size_t next : graph[node]")
    return common + program


def part_intro(number: int, title: str, description: str) -> str:
    figure = ""
    if number == 1:
        figure = r"""
\begin{figure}[ht]
\centering
\input{figures/translation-pipeline}
\caption{A simplified translation pipeline. The exact tools and intermediate files vary by platform, but the boundaries are useful for debugging.}
\label{fig:translation-pipeline}
\end{figure}
"""
    return f"""\\chapter*{{Part {number}: {tex_escape(title)}}}
\\addcontentsline{{toc}}{{chapter}}{{Part {number}: {tex_escape(title)}}}

{tex_escape(description)}

{figure}
\\partnote{{\\textbf{{Design lens.}} Read the chapters in this part as answers to one question: what decision does this topic make visible, and what assumption must remain true for that decision to be safe? The code examples are intentionally small; the projects later combine the same ideas under realistic constraints.}}

"""


def chapter_tex(number: int, part_number: int, part_title: str, title: str, focus: str) -> str:
    previous = "the preceding chapter" if number > 1 else "the orientation in the front matter"
    program_path = f"examples/chapters/{safe_filename(number)}.cpp"
    topic = tex_escape(title)
    focus_tex = tex_escape(focus)
    code_note = tex_escape(f"The complete standalone program for this chapter is stored at {program_path} and is compiled by the verification script.")
    return f"""\\chapter{{{topic}}}
\\index{{{topic}}}
\\begin{{chaptermeta}}
\\textbf{{Learning objectives}}
\\begin{{itemize}}
  \\item Explain the central problem addressed by {topic} and relate it to the C++ object, type, or program model.
  \\item Use the idea in a small program, identify its main failure modes, and state one trade-off honestly.
\\end{{itemize}}
\\textbf{{Prerequisites}}: {previous}, plus the vocabulary introduced in Part {part_number}.

\\textbf{{Key terminology}}: {topic}; contract; representation; lifetime; invariant; diagnostic; trade-off.
\\end{{chaptermeta}}

\\section{{The problem and the mental model}}
{focus_tex}

The practical question is not merely “what syntax produces this result?” It is “what must be true before the operation, what changes during it, and what remains true afterward?” That question gives the topic a place in a larger program. A provisional beginner model is useful here, but it must be refined whenever the standard leaves a choice to the implementation or a library component adds a precondition.

\\section{{A small working program}}
{code_note}

\\inputminted[fontsize=\\scriptsize,breaklines]{{cpp}}{{{program_path}}}

The program is intentionally complete: it includes its headers, defines `main`, and has no dependency on a hidden project file. The code is a teaching instrument, not a claim that the smallest program is the best production design. Larger interfaces should expose ownership, failure, and lifetime explicitly.

\\section{{Rules, mistakes, and diagnostics}}
The language rule and the engineering guideline are related but different. The compiler can diagnose violations that are visible in the translation unit, while runtime errors can arise from invalid input, environmental failure, lifetime mistakes, data races, or an incorrect model. Begin debugging with the first reproducible symptom and reduce the case before changing several things at once.

Common mistakes include using a name before its declaration, assuming a representation is universal, ignoring a returned error, retaining a reference or view beyond its source lifetime, and relying on an observed implementation detail. When a rule is about undefined behavior, no particular output is evidence of correctness.

\\begin{{warning}}
\\textbf{{Undefined-behavior check.}} If an example in this chapter would be wrong because an object is out of lifetime, an access is out of bounds, a precondition is violated, or two unsynchronized operations race, the program is wrong even if it compiles. Run the relevant sanitizer and add a test that exercises the boundary.
\\end{{warning}}

\\section{{Design, performance, and testing}}
Choose the simplest representation that makes the contract visible. Measure performance only after naming the workload and the metric. A local optimization that changes ownership, ordering, or error behavior is a design change and should be reviewed as such. A useful test checks an observable property, includes a boundary case, and fails with enough context to explain what was expected.

\\begin{{worked}}
\\textbf{{Worked micro-check.}} Suppose a program uses {topic.lower()} and a test fails only for an empty input or a repeated call. First write down the expected contract for that boundary, then make the smallest input that distinguishes valid absence from invalid use. The answer is not to add a guard blindly: decide whether the API should reject, represent absence, or preserve an invariant before the next call.
\\end{{worked}}

\\section{{Exercises}}
\\begin{{enumerate}}
  \\item Explain the topic in three sentences: one about purpose, one about a rule, and one about a limitation.
  \\item Modify the complete program so that it accepts one relevant input and reports one meaningful failure through the interface chosen in this chapter.
  \\item Write a test for the smallest boundary case and a second test for the case that would expose a lifetime, ownership, ordering, or complexity mistake.
\\end{{enumerate}}

\\textbf{{Selected solution.}} A sound solution states the precondition before it changes the code, uses a named value or type for the result, checks the failure path, and tests both the ordinary case and the boundary. If the change cannot be explained without referring to an undocumented implementation detail, redesign the interface or document the assumption.

\\section{{Summary and further study}}
{topic} is best understood as a contract inside a larger system. Keep the distinction between standard requirement, implementation behavior, and engineering recommendation visible. Re-run the example, inspect its diagnostics, and compare the result with the corresponding project when the idea appears in a multi-file program. Further study should include the relevant standard-library reference, the C++ Core Guidelines, and the citations listed in the bibliography.

"""


def main() -> None:
    chapter_number = 0
    generated_inputs: list[str] = []
    generated_inputs.append("% Generated by tools/generate_book.py. Edit chapter files, then regenerate if needed.\n")
    for part_number, (part_title, description, chapters) in enumerate(PARTS, start=1):
        part_path = ROOT / "parts" / f"part{part_number:02d}.tex"
        part_path.write_text(part_intro(part_number, part_title, description), encoding="utf-8")
        generated_inputs.append(f"\\part{{{tex_escape(part_title)}}}\n")
        generated_inputs.append(f"\\input{{parts/part{part_number:02d}}}\n")
        for title, focus in chapters:
            chapter_number += 1
            chapter_path = ROOT / "chapters" / f"{safe_filename(chapter_number)}.tex"
            code_path = ROOT / "examples" / "chapters" / f"{safe_filename(chapter_number)}.cpp"
            chapter_path.write_text(chapter_tex(chapter_number, part_number, part_title, title, focus), encoding="utf-8")
            code_path.write_text(chapter_program(chapter_number, title), encoding="utf-8")
            generated_inputs.append(f"\\input{{chapters/{safe_filename(chapter_number)}}}\n")
    if chapter_number != 182:
        raise RuntimeError(f"Expected 182 chapters, generated {chapter_number}")
    (ROOT / "generated_inputs.tex").write_text("\n".join(generated_inputs), encoding="utf-8")

    manifest = {
        "title": "MODERN C++: From First Program to Professional Software",
        "author": "Scott Brodie Forsyth",
        "standard_baseline": "C++23",
        "chapter_count": chapter_number,
        "generated_programs": chapter_number,
        "parts": [title for title, _, _ in PARTS],
    }
    (ROOT / "docs" / "book_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {chapter_number} modular chapters and standalone programs.")


if __name__ == "__main__":
    main()

Notes on complexities of function parameters/returns recovery
=============================================================

1. A live-in set on function entry includes both parameters and
preserved locations. To find out real parameters, liveness analysis
should be performed after the dead code elimination of preservation
instructions, which requires propagation and stack variable rewriting
passes. The propagation in turn requires first-stage liveness (and
reaching definitions) analysis.

2. Any value computed by a function may be its potential return.
Unless we found *all* callers of a function, we can't write off
some potential return. And any new discovered caller may extend
set of returns. If a caller is not known, we should conservatively
assume an initial proposition that any value which reaches exit
may be live and used by a caller. That's why for such, caller-less
functions, we initialize its live-out set to the set of registers
which reach exit (as computed by reaching definitions, or, as a
simplification, a union of all function defineds).

3. A particular issue with registers defined only along some paths
of execution. Per p.2, such register is a potential return of the
function. But as it's only defined on some paths, the only way to
implement proper semantics for this case (that's, set the register
to a particular value sometimes, and not change it other times) is
to accept it as argument. Note that this happens completely
automatically, the dataflow analysis is "smart" to "know" that this
is needed. However, in each particular case, this fact may be not
immediately obvious to a human. TODO: implement an annotation
algorithm describing why this or that register got into a parameter
set of a function. The summary or of this paragraph can be described
as follows: superfluous returns lead to superfluous parameters.

4. All the above is especially aggravated for RISC architectures
with large register sets. For example, a low-level assembly-coded
routine written by a human may modify a number of registers (in
preference of saving/restoring or using stack variables), while C
routines calling them may be more reserved in register usage. This
will cause original modifieds of assembly routine to leak into a
caller, not being killed there, and leak into another caller,
leading to long chains of functions with unrealistic returns (and
parameters, as described in 3). Thus, it should be expected that
in many realistic cases pure dataflow analysis won't be enough -
it requires many diverse callers for each function, and only
small subset of functions in a real program usually have this
property. Instead, heuristics should be expected to be employed.
This includes parameter and return filters based on ABI conventions,
register order restrictions (registers are usually allocated to
params/returns from an ordered sequence, so if some register is
not in a params/returns set, any registers after it are unlikely
candidates for real params/returns, etc. A useful heuristic also
comes from p.3 - if some register is not defined along all execution
paths, it's not a good candidate for returns, and thus params too. All
these criteria are indeed heuristic - there can be some functions
for which they are not true. Thus, a human should be able to select
which heuristics to use, easily oversee results achieved, and be
able to override them on a case by case basis.

5. Preserveds set is calculated in regards to function parameters.
It may seem strange that a register which isn't defined locally
(i.e. never explicitly saved/restored) is in preserveds set, but
that means that it's a parameter, which serves as an arguments to
another function, and that another function doesn't modify it, so
it's really preserved for the current function. A more involved
example is that some function has 2 paths: one modifying the
parameter register, but ending with an infinite loop, while another
path truly preserves that register, so overall semantics is
preserving the register in the normal program flow, and this is
signified in the preserveds.

6. Assuming RISC-style register calling convention, $sp being in
function parameters after dataflow analysis may mean the function
takes addresses of the objects on the stack. Otherwise, if they
were just derefences of stack pointer, they would have been
rewritten as stack variables. Note that referencing objects via
stack pointer may create aliasing problems for rewritten stack
vars.

Van Emmerik "3.4.5 Stack Pointer as Parameter" p.86/146 talks
about the fact that with stack calling convention, stack pointer
would appear to be a parameter of any function, and thus needs
to be explicitly filtered out for final decompilation results.
This is definitely true, but the previous paragraph talks about
what it means that $sp is deemed as a parameter by the dataflow
analysis even after stack variable rewriting pass (which should
eliminate explicit $sp references).

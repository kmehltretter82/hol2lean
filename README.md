# hol2lean

The goal is to import higher-order logic (HOL) proofs into Lean 4, starting with OpenTheory articles. A Lean user should be able to apply an imported theorem and trace its statement, proof and assumptions back to the source development.

## Export experiment

On 21 November 2026, current HOL Light checked all three list statements, but its default kernel lacked the proof-reading functions used by the pinned exporter. Current HOL4 rebuilt the three proof bodies with its OpenTheory logging kernel and wrote a 32,631-byte version 6 article. A clean build reproduced it byte for byte. [HOL Light probe](experiments/list-export/hol-light/) · [HOL4 reproduction command](experiments/list-export/hol4/) · [Raw article](experiments/list-export/hol4/listPilot.art)

The reference checker executed 651 inferences and exported the three expected sequents in their source orientations. All ten external assumptions are listed in its report. Seven concern logic, one gives list induction, and two give the recursion equations for reverse and append. The three exports are disjoint from these assumptions. Lean replay is pending. The next implementation step is to read this article and match its three exports and ten imports against the reference result. [Reference check and inventory](experiments/list-export/check/)

## First milestone — replay three list theorems from a current prover

Start with HOL Light's `APPEND_NIL`, `APPEND_ASSOC` and `REVERSE_APPEND`. The source proof of `REVERSE_APPEND` uses the other two, so this fixture exercises reuse within a replayed development. [HOL Light list theory](https://github.com/jrh13/hol-light/blob/1a0c0e6b182cd9e271946ba8d78f7942619f4acb/lists.ml#L157-L169)

Use ordinary Lean `List α`, `++` and `List.reverse` in the first release. Interpret the source list type and operations directly with their Lean counterparts and prove that they satisfy the source definitions. Retain `[Nonempty α]` for each polymorphic HOL type variable. The recorded source statements and independent Lean signatures fix the hypotheses, binders and equality orientations before replay, including `xs ++ (ys ++ zs) = (xs ++ ys) ++ zs`. [Source statements](experiments/list-export/statements.txt) · [Lean signatures](experiments/list-export/Signatures.lean)

1. **Establish that export works.** Pin a current upstream HOL Light revision and an exporter revision. Record the three source statements before running the exporter. Rebuild their proofs with proof logging enabled, collect the article and its dependencies, and check them with the reference OpenTheory tool. Save the commands, revisions and artifact hashes. The documented HOL Light exporter uses a proof-logging snapshot, so compatibility with the pinned prover is the first experiment. If it fails, record the failing step and try the same list identities in current HOL4. [OpenTheory export instructions](https://www.gilith.com/opentheory/faq.html)
2. **Build the smallest reader that covers the fixture.** Pin Lean in a Lake project. Start with a hand-checkable article proving reflexivity, then inventory the real articles' versions, commands, imported assumptions and exported sequents. Implement the required stack and dictionary operations with source-line diagnostics. Compare the reader's imports and exports with the reference tool. An unknown command or unresolved reference must fail the run. [Article file format](https://www.gilith.com/opentheory/article.html)
3. **Replay the proofs.** Discharge every external source assumption with a kernel-checked Lean proof of its exact interpretation. Keep all three target sequents out of the pre-established import table, including renamed equivalents. Produce each target declaration by replaying its exported derivation. Later steps may use earlier theorems replayed in the same development. Reject a corrupted inference and a missing dependency.
4. **Enforce the axiom policy.** For each imported theorem, audit the transitive axiom dependencies reported by Lean. Fail the run if any name falls outside the fixed set `{propext, Classical.choice, Quot.sound}`. This rejects custom axioms, placeholders (`sorryAx`) and axioms introduced by native evaluation, including ones inherited from a dependency. Retain each theorem's audit in the results. [Lean axiom dependencies](https://lean-lang.org/doc/reference/latest/Axioms/)
5. **Demonstrate reuse.** In a separate Lean module, prove `((xs ++ ys) ++ (zs ++ [])).reverse = (zs.reverse ++ ys.reverse) ++ xs.reverse` by explicit rewrites with the three imported declarations. For each negative test, build a module that withholds one imported name but still contains the other two. Require that module to build and the consumer to fail at its reference to the withheld name.

From a clean checkout, one documented command must export, replay, audit and compile the downstream example. Report the outcome of each stage for each theorem. The milestone passes when all three replayed declarations check against the independent signatures, pass the axiom policy and satisfy the positive and negative tests.

## Second milestone — prove what successful replay guarantees

* Specify the HOL interpretation independently of the replay implementation. It must account for nonempty type domains, HOL booleans as both data and propositions, polymorphism, binding and capture-avoiding substitution. Interpret a sequent as its conclusion under **all** of its hypotheses.
* Prove that each supported inference preserves validity and that each definition extends the interpretation correctly. Lift these lemmas to a theorem about the article machine. Given valid interpretations of the imports, successful execution must establish the interpreted sequent of every export.
* Connect that theorem to the declarations Lean users apply. Derive each declaration's type from the checked source sequent and its proof from replay soundness. Check a regression where dropping a hypothesis changes the expected Lean signature.
* Track serialized input separately. State the article-machine theorem over decoded commands and identify the trusted decoder. Claim coverage from article bytes only after proving that successful decoding agrees with the pinned format specification.

## Third milestone — measure coverage and choose the next target

Run the same pipeline on a pinned OpenTheory standard-library package and its dependencies. Publish source, export and kernel-checked theorem counts alongside unsupported commands, unresolved assumptions, elapsed time and peak memory. Choose the next package or prover integration from the observed failures. Use the current-prover fixture as a regression test as coverage grows. [OpenTheory project](https://www.gilith.com/opentheory/)

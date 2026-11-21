# hol2lean

The goal is to import higher-order logic (HOL) proofs into Lean 4, starting with OpenTheory articles. A Lean user should be able to apply an imported theorem and trace its statement, proof and assumptions back to the source development.

## First milestone — replay three list theorems from a current prover

Start with HOL Light's `APPEND_NIL`, `APPEND_ASSOC` and `REVERSE_APPEND`. They form a small development with polymorphic types, an inductive datatype and related proofs. As a downstream test, use the imported lemmas in Lean to simplify the reverse of two appended lists followed by an empty list. [HOL Light list theory](https://github.com/jrh13/hol-light/blob/master/lists.ml)

1. **Establish that export works.** Pin a current upstream HOL Light revision and an exporter revision. Record the three source statements before running the exporter. Rebuild their proofs with proof logging enabled, collect the article and its dependencies, and check them with the reference OpenTheory tool. Save the commands, revisions and artifact hashes. The documented HOL Light exporter uses a proof-logging snapshot, so compatibility with the pinned prover is the first experiment. If it fails, record the failing step and try the same list identities in current HOL4. [OpenTheory export instructions](https://www.gilith.com/opentheory/faq.html)
2. **Build the smallest reader that covers the fixture.** Pin Lean in a Lake project. Start with a hand-checkable article proving reflexivity, then inventory the real articles' versions, commands, imported assumptions and exported sequents. Implement the required stack and dictionary operations with source-line diagnostics. Compare the reader's imports and exports with the reference tool. An unknown command or unresolved reference must fail the run. [Article file format](https://www.gilith.com/opentheory/article.html)
3. **Replay the proofs.** Represent HOL types, terms and sequents explicitly. Implement the inference rules and definitions exercised by the fixture. Resolve each article assumption against a checked dependency or an explicitly documented foundational principle. Export Lean declarations under stable names and check them with the pinned Lean kernel. Test that a corrupted inference fails and that removing a required dependency produces an error.
4. **Measure the result.** From a clean checkout, run the export, import and downstream Lean proof with one documented command. For each of the three source statements, report whether it was exported, replayed and checked against an independently written Lean signature. Include the transitive axioms from `#print axioms`. The milestone passes at 3/3 with the downstream proof compiling, no placeholders and every foundational assumption accounted for. List any failures by theorem and stage.

## Second milestone — prove what successful replay guarantees

* Specify the HOL interpretation independently of the replay implementation. It must account for nonempty type domains, HOL booleans as both data and propositions, polymorphism, binding and capture-avoiding substitution. Interpret a sequent as its conclusion under **all** of its hypotheses.
* Prove that each supported inference preserves validity and that each definition extends the interpretation correctly. Lift these lemmas to a theorem about the article machine. Given valid interpretations of the imports, successful execution must establish the interpreted sequent of every export.
* Connect that theorem to the declarations Lean users apply. Derive each declaration's type from the checked source sequent and its proof from replay soundness. Document the exact input to the theorem and any trusted steps from article bytes to decoded commands. Check a regression where dropping a hypothesis changes the expected Lean signature.

## Third milestone — measure coverage and choose the next target

Run the same pipeline on a pinned OpenTheory standard-library package and its dependencies. Publish source, export and kernel-checked theorem counts alongside unsupported commands, unresolved assumptions, elapsed time and peak memory. Choose the next package or prover integration from the observed failures. Use the current-prover fixture as a regression test as coverage grows. [OpenTheory project](https://www.gilith.com/opentheory/)

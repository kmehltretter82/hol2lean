# HOL Light export probe

The probe builds the standard HOL Light kernel, loads the list theory, and checks the conclusion and empty hypothesis set of each named theorem against the [fixture manifest](../statements.txt). It then tests the kernel operation used to recover a derivation, loads Gilith's OpenTheory exporter, and requests a single article containing all three proofs.

| Component | Tested revision |
| --- | --- |
| HOL Light | [1a0c0e6, 19 November 2026](https://github.com/jrh13/hol-light/tree/1a0c0e6b182cd9e271946ba8d78f7942619f4acb) |
| Gilith proof-logging fork | [f3f1319, 12 February 2020](https://github.com/gilith/hol-light/tree/f3f131963f2298b4d65ee5fead6e986a4a14237a) |

Run from the repository root with Git, GNU Make and the HOL Light OCaml dependencies. The tested environment used macOS arm64, OCaml 5.5.0, Camlp5 8.05.03 and Zarith 1.14. With opam initialized and OCaml 5.5.0 installed as the system compiler, these commands prepare the switch and run the experiment.

```sh
opam switch create hol2lean-light ocaml-system.5.5.0
eval "$(opam env --switch=hol2lean-light --set-switch)"
export CAML_LD_LIBRARY_PATH="$(opam var lib)/stublibs${CAML_LD_LIBRARY_PATH:+:$CAML_LD_LIBRARY_PATH}"
opam install -y camlp5.8.05.03 zarith.1.14
TMPDIR=/tmp experiments/list-export/hol-light/probe.sh
```

The script prints the temporary checkout directory and retains the full OCaml transcript in `session.log` there.

## Observed result

On 21 November 2026 the run exited with status 1. All three source sequents matched. The direct probe `read_proof APPEND_NIL` failed with `Unbound value read_proof`. Loading the exporter also failed at `replace_proof` in `object.ml`, and its symbol module used `Pervasives`, which is absent in OCaml 5.5. The final call to `export_begin` was unbound. The run produced zero articles, so there are no commands, type definitions, imports or reference-checker results from this prover.

The default kernel stores a sequent's hypotheses and conclusion. Gilith's fork extends that representation with proof data that its exporter traverses via `read_proof`. A port would need to record derivations while the kernel runs, including the steps used to build the list theorems. The official instructions install the proof-logging snapshot as the prover. This experiment tested loading its exporter into the pinned upstream prover. [Upstream kernel](https://github.com/jrh13/hol-light/blob/1a0c0e6b182cd9e271946ba8d78f7942619f4acb/fusion.ml#L104) · [Fork kernel](https://github.com/gilith/hol-light/blob/f3f131963f2298b4d65ee5fead6e986a4a14237a/fusion.ml#L126) · [Export traversal](https://github.com/gilith/hol-light/blob/f3f131963f2298b4d65ee5fead6e986a4a14237a/opentheory/src/export.ml#L428) · [OpenTheory FAQ](https://www.gilith.com/opentheory/faq.html)

Two other recorders in the upstream checkout are possible starting points for an adapter. Source inspection shows that `ProofTrace` exposes `proof_of` and indexed proof nodes. Its kernel patch passed `git apply --check ProofTrace/fusion.ml.diff` on the pin. `Proofrecording` has its own `proof_of` interface and backends. Neither supplies the proof constructors and accessors expected by the Gilith exporter. These alternatives were inspected at source level. [ProofTrace kernel patch](https://github.com/jrh13/hol-light/blob/1a0c0e6b182cd9e271946ba8d78f7942619f4acb/ProofTrace/fusion.ml.diff) · [Proofrecording theorem interface](https://github.com/jrh13/hol-light/blob/1a0c0e6b182cd9e271946ba8d78f7942619f4acb/Proofrecording/diffs/thm.ml#L130)

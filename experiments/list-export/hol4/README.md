# HOL4 list export

The fallback uses HOL4 mainline commit `aee6a90d9856a842f4cbd2bfc44efb7067a141e4` for both the prover and the OpenTheory logger. The export script fetches this revision and extracts the complete statements and proof bodies for `APPEND_NIL`, `APPEND_ASSOC` and `REVERSE_APPEND` from its list theory. It runs those proofs again in a fresh theory with the logging kernel enabled. The third proof uses the first two local results. [HOL4 list theory](https://github.com/HOL-Theorem-Prover/HOL/blob/aee6a90d9856a842f4cbd2bfc44efb7067a141e4/src/list/src/listScript.sml#L547-L557) · [Proof of REVERSE_APPEND](https://github.com/HOL-Theorem-Prover/HOL/blob/aee6a90d9856a842f4cbd2bfc44efb7067a141e4/src/list/src/listScript.sml#L2064-L2070)

From the project root, supply the path to a **new** directory. The build uses Git, Python 3, Poly/ML (`poly` and `polyc`), GNU Make and a C/C++ toolchain. The run here used Poly/ML 5.9.2 on Apple silicon. HOL4 produces the raw article with its own logger. Install the separate OpenTheory executable for the reference check after export. [Reference checker setup](../check/README.md)

```sh
experiments/list-export/hol4/export.sh /tmp/hol2lean-list-export
```

The generated proof script and raw article are in the working directory under `fixture/`. In its private checkout the script builds the logging kernel and the libraries through `src/list/src`. It omits the optional default targets for exporting unrelated dependency articles. The explicit `listPilot.art` target runs HOL4's upstream article logger. Source dependencies that arrive from saved HOL theories become OpenTheory assumptions whose exact sequents must be discharged during Lean import. [Logging implementation](https://github.com/HOL-Theorem-Prover/HOL/blob/aee6a90d9856a842f4cbd2bfc44efb7067a141e4/src/opentheory/postbool/Logging.sml#L400-L419)

The checked-in `listPilot.art` is the raw 32,631-byte article emitted by HOL4. Compare a fresh export with the fixture from the project root.

```sh
cmp /tmp/hol2lean-list-export/fixture/listPilot.art experiments/list-export/hol4/listPilot.art
```

The reference checker accepted the three exports with ten source assumptions and 651 inference steps. The article defines no new types or constants. Its external list type, four list operations and list induction principle must be interpreted in Lean. All three target sequents are absent from the assumptions. [Full dependency and command inventory](../check/listPilot.txt)

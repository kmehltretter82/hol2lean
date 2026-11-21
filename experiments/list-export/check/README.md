# Build the reference checker

From the project root, use Git, GNU Make, Perl and Poly/ML (`polyc`, tested with 5.9.2) to build the pinned OpenTheory release. The commands below put `opentheory` on the current shell's path for verification. [OpenTheory release source](https://github.com/gilith/opentheory/tree/4e7d25943446ff209fb627167b93567bd8c38118)

```sh
ot_work=$(mktemp -d)
git clone --depth 1 --branch v1.4.20230321 https://github.com/gilith/opentheory.git "$ot_work/opentheory"
(
  cd "$ot_work/opentheory" &&
  test "$(git rev-parse HEAD)" = 4e7d25943446ff209fb627167b93567bd8c38118 &&
  LC_ALL=C make bin/polyml/opentheory
)
export PATH="$ot_work/opentheory/bin/polyml:$PATH"
opentheory --version
```

## Verify the recorded fixture

Run the following commands with Python 3. They execute the raw article in the reference checker with an empty package repository and compare the resulting report with the reviewed copy. The comparison covers the input hash, command counts, external symbols, all ten required sequents and the three exported sequents with their dependencies. The exports in the recorded report were reviewed against the independently recorded [source statements](../statements.txt).

```sh
fixture=experiments/list-export
python3 "$fixture/check/check_article.py" opentheory "$fixture/hol4/listPilot.art" > "$ot_work/listPilot.txt" &&
  diff -u "$fixture/check/listPilot.txt" "$ot_work/listPilot.txt"
```

The checker also writes the required and exported sequents as two temporary articles. Combining them into one theory gives their set union modulo renaming of bound variables. The script fails if the union contains fewer sequents than the two sets together. This catches a target exported directly from a pre-established assumption. The derivations establish the exported sequents conditional on their listed assumptions. Each assumption is a separate proof obligation for the Lean importer.

The reference checker exited successfully and warned that 1,085 dictionary entries remained at end of file. The article machine discards the dictionary on termination. The report contains ten raw `axiom` commands and ten distinct assumptions, so every such command is accounted for. The article uses `HOL4.list.list` as an external type operator and executes zero type definitions. [Article format](https://www.gilith.com/opentheory/article.html)

Two negative controls were run. Replacing the first `eqMp` command (line 85) with `thm` made the reference checker reject the stack. Running the check on the three exported statements encoded as assumptions (`opentheory info --theorems -o shortcut.art listPilot.art`) failed with three exported sequents occurring among the requirements.

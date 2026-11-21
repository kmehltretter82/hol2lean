"""Select HOL4 build targets and extract the pilot proofs in a private checkout."""

from pathlib import Path
import re
import sys

hol = Path(sys.argv[1])
fixture = Path(sys.argv[2])
list_dir = "src/list/src"
base = (hol / "tools/sequences/base-hol").read_text().splitlines()
sequence = base[:base.index(list_dir) + 1]

# The default logging build also exports all theorems in each dependency.
# Keep the HOL theories and request only the pilot article as an export.
for entry in sequence:
    recipe = hol / entry / "Holmakefile"
    if entry.startswith("src/") and recipe.is_file():
        lines = recipe.read_text().splitlines(keepends=True)
        recipe.write_text("".join(
            line for line in lines if not (
                line.startswith("all:") and (".art" in line or "$(ARTFILES)" in line)
            )
        ))

(hol / "tools/sequences/list-pilot").write_text(
    "#include sequences/kernel\n" + "\n".join(sequence) + "\n"
)

source = (hol / list_dir / "listScript.sml").read_text()
script = """Theory listPilot[bare]
Ancestors list
Libs HolKernel Parse boolLib

val () = if Thm.kernelid = "otknl" then () else raise Fail "expected otknl"
val LIST_INDUCT_TAC = INDUCT_THEN list_INDUCT ASSUME_TAC;
"""

for name in ("APPEND_NIL", "APPEND_ASSOC", "REVERSE_APPEND"):
    pattern = rf"^Theorem {name}(?:\[simp\])?:.*?^QED$"
    blocks = re.findall(pattern, source, flags=re.MULTILINE | re.DOTALL)
    if len(blocks) != 1:
        raise ValueError(f"Expected exactly one upstream proof of {name}")
    script += "\n" + blocks[0] + "\n"

fixture.mkdir()
(fixture / "listPilotScript.sml").write_text(script)
(fixture / "Holmakefile").write_text("all: listPilot.art\n")

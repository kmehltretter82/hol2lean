#!/bin/sh
# Supply a new working directory for the source checkout and generated article.
set -eu
if [ "$#" -ne 1 ]; then
    echo "usage: $0 NEW-WORK-DIRECTORY" >&2
    exit 2
fi
here=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
mkdir "$1"
work=$(CDPATH='' cd -- "$1" && pwd)
pin=aee6a90d9856a842f4cbd2bfc44efb7067a141e4

git init -q "$work/HOL"
cd "$work/HOL"
git fetch --depth 1 https://github.com/HOL-Theorem-Prover/HOL.git "$pin"
git checkout --detach FETCH_HEAD
test "$(git rev-parse HEAD)" = "$pin"
python3 "$here/prepare.py" "$work/HOL" "$work/fixture"
poly --script tools/smart-configure.sml
bin/build --otknl --no-helpdocs --seq=tools/sequences/list-pilot -j2
cd "$work/fixture"
"$work/HOL/bin/Holmake" --holstate="$work/HOL/src/num/termination/numheap" listPilot.art
test -s listPilot.art
echo "$work/fixture/listPilot.art"

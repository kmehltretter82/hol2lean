#!/bin/sh
set -eu

fixture=$(CDPATH='' cd "$(dirname "$0")/.." && pwd)
work=$(mktemp -d "${TMPDIR:-/tmp}/hol2lean-light.XXXXXXXX")
echo "HOL Light probe directory: $work"

fetch() {
    git init -q "$work/$1"
    git -C "$work/$1" fetch -q --depth=1 "$2" "$3"
    git -C "$work/$1" checkout -q --detach FETCH_HEAD
    test "$(git -C "$work/$1" rev-parse HEAD)" = "$3"
}

fetch prover https://github.com/jrh13/hol-light.git 1a0c0e6b182cd9e271946ba8d78f7942619f4acb
fetch exporter https://github.com/gilith/hol-light.git f3f131963f2298b4d65ee5fead6e986a4a14237a
cd "$work/prover"
make
ln -s ../exporter/opentheory opentheory

# Read and check the independently recorded sequents before asking for an export.
cat > "$work/probe.ml" <<'OCAML'
let check_source name th expected =
  if hyp th <> [] || not (aconv (concl th) expected) then exit 2
  else print_endline ("SOURCE OK " ^ name);;
OCAML
while read -r name turnstile conclusion; do
    case "$name" in ''|'#'*) continue ;; esac
    test "$turnstile" = '|-'
    printf 'check_source "%s" %s (parse_term "%s");;\n' "$name" "$name" "$conclusion"
done < "$fixture/statements.txt" >> "$work/probe.ml"
cat >> "$work/probe.ml" <<'OCAML'
read_proof APPEND_NIL;;
#use "opentheory/load.ml";;
let () =
  export_begin ();
  export_theory "hol2lean-list";
  List.iter export_thm [APPEND_NIL; APPEND_ASSOC; REVERSE_APPEND];
  export_end ();;
OCAML

unset OPENTHEORY_EXPORT_BASE
LINE_EDITOR=env OCAML_COLOR=never ./hol.sh < "$work/probe.ml" > "$work/session.log" 2>&1
for name in APPEND_NIL APPEND_ASSOC REVERSE_APPEND; do
    grep -F "SOURCE OK $name" "$work/session.log"
done
if test -s opentheory/export/hol2lean-list.art; then
    echo "Article: $work/prover/opentheory/export/hol2lean-list.art"
else
    grep -F 'Error:' "$work/session.log" | tail -15 >&2
    echo "Export failed. See $work/session.log" >&2
    exit 1
fi

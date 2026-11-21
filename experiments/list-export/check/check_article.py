"""Run the OpenTheory checker and count the commands in the original article."""

import argparse
import hashlib
import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path


def theorem_count(path):
    return path.read_bytes().splitlines().count(b"thm")


def inspect(checker, article):
    def run(*args):
        return subprocess.check_output([checker, *args], text=True)

    version = run("--version").strip()
    if version != "opentheory 1.4 (release 20230321)":
        raise SystemExit(f"Unexpected checker version: {version}")

    with tempfile.TemporaryDirectory() as directory:
        work = Path(directory)
        repo = ["--root-dir", str(work / "repo")]
        run(*repo, "init")
        info = [*repo, "--show-types", "info", "--manual-install", "--show-assumptions"]
        required = work / "required.art"
        exported = work / "exported.art"
        summary = run(*info, "--show-derivations", "--theory", "--inference",
                      "--assumptions", "-o", required, "--theorems", "-o", exported,
                      f"article:{article}")

        # Let the checker form the union of the two sequent sets, so a change
        # of bound variable names cannot conceal a common assumption and export.
        union_theory = work / "union.thy"
        union_theory.write_text(
            'name: union\nversion: 1.0\n'
            '\nrequired {\n  article: "required.art"\n}\n'
            '\nexported {\n  article: "exported.art"\n}\n'
            '\nmain {\n  import: required\n  import: exported\n}\n'
        )
        union = work / "union.art"
        run(*info, "--theorems", "-o", union, union_theory)
        overlap = theorem_count(required) + theorem_count(exported) - theorem_count(union)
        if overlap:
            raise SystemExit(f"{overlap} exported sequents also occur among the requirements")

    sha256 = hashlib.sha256()
    commands = Counter()
    prefix = []
    with article.open("rb") as stream:
        for line in stream:
            sha256.update(line)
            token = line.decode("utf-8").strip()
            if not token or token.startswith("#"):
                continue
            if len(prefix) < 2:
                prefix.append(token)
            if token.startswith('"'):
                token = "name literal"
            elif re.fullmatch(r"-?[0-9]+", token):
                token = "integer literal"
            commands[token] += 1

    article_version = prefix[0] if prefix[1:] == ["version"] else "5 (implicit)"
    print(version)
    print(f"SHA-256 {sha256.hexdigest()}")
    print(f"Article version {article_version}")
    print(f"Exported sequents also required as assumptions: {overlap}")
    print("\nRaw article command counts")
    for command, count in sorted(commands.items()):
        print(f"{command}\t{count}")
    print("\nReference checker result")
    print(summary, end="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checker", help="path to the pinned opentheory executable")
    parser.add_argument("article", type=Path)
    args = parser.parse_args()
    try:
        inspect(args.checker, args.article)
    except subprocess.CalledProcessError as error:
        raise SystemExit(error.returncode)

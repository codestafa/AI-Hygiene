"""Checks for the Git index and for commits about to leave this checkout."""

import os
import re
import subprocess
import sys
from pathlib import Path


PRIVATE_PATHS = (
    ":(glob)**/semantics.md",
    ":(glob)**/.env",
    ":(glob)**/.env.*",
    ":(exclude,glob)**/.env.example",
)
CONVENTIONAL_SUBJECT = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*(?:\([^()\n]+\))?!?: \S")


def git(*args):
    return subprocess.check_output(["git", *args])


def check_subject(subject):
    if not CONVENTIONAL_SUBJECT.match(subject):
        raise SystemExit("Use a Conventional Commit subject, such as 'docs: explain setup'.")


def scan(*args):
    binary = Path(os.fsdecode(git("rev-parse", "--git-path", "ai-hygiene-tools/gitleaks").strip()))
    if not binary.is_file():
        raise SystemExit("Run ./scripts/setup-checks in this checkout before verifying changes.")
    subprocess.run([str(binary.resolve()), "git", "--redact=100", "--no-banner", *args], check=True)


def check_whitespace(*revisions):
    result = subprocess.run(["git", "diff", "--check", *revisions], stdout=subprocess.DEVNULL)
    if result.returncode:
        raise SystemExit("Whitespace check failed. Inspect the affected diff locally.")


def check_staged():
    if git("ls-files", "--cached", "--", *PRIVATE_PATHS):
        raise SystemExit("The index contains a personal voice guide or a live environment file.")
    check_whitespace("--cached")
    scan("--pre-commit", "--staged")


def check_range(base, tip):
    for oid in (base, tip):
        if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", oid):
            raise SystemExit("Verification needs full Git object IDs for the base and tip.")
    tip = git("rev-parse", "--verify", f"{tip}^{{commit}}").decode().strip()
    if base.strip("0"):
        base = git("rev-parse", "--verify", f"{base}^{{commit}}").decode().strip()
        revision = f"{base}..{tip}"
    else:
        # A new remote ref can introduce its entire history, even when the tip looks clean.
        base = git("hash-object", "-t", "tree", os.devnull).decode().strip()
        revision = tip

    if git("log", "-1", "--format=%H", "--full-history", "--root", "--no-renames",
           "--diff-merges=first-parent", "--diff-filter=ACMT", revision, "--", *PRIVATE_PATHS):
        raise SystemExit("Outgoing history includes a personal voice guide or a live environment file.")
    check_whitespace(base, tip)
    for subject in git("log", "--no-merges", "--format=%s", revision).decode(errors="replace").splitlines():
        check_subject(subject)
    scan(f"--log-opts=--root --diff-merges=first-parent {revision}")


def main():
    mode, *args = sys.argv[1:]
    if mode == "staged":
        check_staged()
    elif mode == "message":
        subject = Path(args[0]).read_text(errors="replace").partition("\n")[0]
        merge = Path(os.fsdecode(git("rev-parse", "--git-path", "MERGE_HEAD").strip()))
        if not (merge.is_file() and subject.startswith("Merge ")):
            check_subject(subject)
    elif mode == "range":
        check_range(*args)
    elif mode == "push":
        for update in sys.stdin:
            _, local_oid, _, remote_oid = update.split()
            if local_oid.strip("0"):
                check_range(remote_oid, local_oid)
    else:
        raise SystemExit("Use staged, message FILE, push, or range BASE_SHA TIP_SHA.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        sys.exit(error.returncode)

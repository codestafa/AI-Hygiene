# AI Hygiene

If you use Codex across repositories, these Markdown guides let you set your engineering and writing preferences once. A new chat can pick up how you want a bug fix verified or an email drafted without you having to explain it again.

## How the guides fit together

- The working agreements tell Codex what to check before a commit, a pull request, and a protected-branch merge. Each project can enforce those checks with Git hooks, CI, and branch settings. [AGENTS.md](AGENTS.md)
- The engineering reference groups 70 principles from *The Pragmatic Programmer* by the decision at hand, such as choosing a module boundary or figuring out why a test failed. [pragmatic-principles.md](pragmatic-principles.md)
- The voice template asks for three short samples in your own words. Codex uses your personal copy when explaining a decision or drafting a message on your behalf. [semantics.example.md](semantics.example.md)

## Install

With Codex installed, open a shell at the root of this repository. These commands copy missing guides into the default Codex directory.

```sh
guide_dir=~/.codex
mkdir -p "$guide_dir"
for file in AGENTS.md pragmatic-principles.md semantics.example.md; do
  [ -e "$guide_dir/$file" ] || cp -n "$file" "$guide_dir/"
done
[ -e "$guide_dir/semantics.md" ] || cp -n "$guide_dir/semantics.example.md" "$guide_dir/semantics.md"
```

Open `~/.codex/semantics.md` and replace the prompts with your own writing. If you already maintain any of these guides, compare your copies with the files above and merge the changes you want.

## Try it

Start a new Codex chat and ask, “What will you check before committing a bug fix?” With these guides, the answer should include scanning the staged changes for secrets and showing that a regression test fails before the fix and passes afterward.

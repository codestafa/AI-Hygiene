# AI Hygiene

Global Codex working agreements for maintaining code, checking changes before they ship, and drafting messages in your own voice.

## Install

From the root of this repository, copy the guides into your Codex directory.

```sh
guide_dir=~/.codex
mkdir -p "$guide_dir"
for file in AGENTS.md pragmatic-principles.md semantics.example.md; do
  [ -e "$guide_dir/$file" ] || cp -n "$file" "$guide_dir/"
done
[ -e "$guide_dir/semantics.md" ] || cp -n "$guide_dir/semantics.example.md" "$guide_dir/semantics.md"
```

Open `~/.codex/semantics.md` and replace the bracketed prompts with examples in your own words. If you already maintain a guide with the same name, compare it with the repository copy and merge the changes you want. Start a new Codex chat to use your guides.

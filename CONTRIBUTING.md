# Contributing

Run `./scripts/setup-checks` in your clone on macOS, Linux, or WSL. It verifies the Gitleaks download and installs it inside this checkout. The commit hooks check staged content and the commit subject. The push hook scans outgoing history, including files deleted in later commits.

Open PRs as drafts. GitHub checks the proposed merge, runs regression tests, and reviews dependency changes. A separate AI reviewer should inspect the exact merge candidate, including changes to the checks. Obtain its SHA with `gh api repos/codestafa/AI-Hygiene/pulls/NUMBER --jq .merge_commit_sha` before review. Commit fixes and repeat review when the candidate changes.

After the reviewer clears all blocking findings, set `reviewed_sha` to the full SHA it inspected. A maintainer or their authorized agent records the result.

```sh
gh api --method POST "repos/codestafa/AI-Hygiene/statuses/${reviewed_sha:?Set the reviewed merge SHA}" \
  -f 'context=Independent AI review' -f state=success \
  -f description='Independent reviewer cleared this merge candidate'
```

Mark the draft ready, or rerun verification on an already-ready PR. Once CI confirms the review matches that revision, the owner approves `maintainer-approval` under **Review deployments** in the Actions run. This environment records approval and contains no credentials.

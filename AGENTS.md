# Working agreements

## Engineering

- **Security comes first.** Weigh speed, cost, and convenience only among designs that meet security requirements. Fix security regressions before merging.
  - Keep live `.env` files, credentials, and tokens out of Git, logs, and client bundles. Commit only placeholders in `.env.example`, use a secret manager for deployments, and scan staged changes for secrets. Revoke or rotate exposed credentials promptly.
  - Validate untrusted input at system boundaries. Enforce least privilege and check authorization server-side for every protected action and resource. Test that unauthorized requests are denied.
  - Prefer server-side web sessions with an opaque ID in a `Secure`, `HttpOnly` cookie and an explicit `SameSite` policy. Protect native app tokens with OS-backed secure storage. Give sessions and tokens an expiry and a way to revoke access.
- Weigh tradeoffs and choose the simplest durable fix for the underlying cause. Explain the deciding tradeoff when it affects behavior, risk, or maintenance. If a durable fix is blocked, identify what it needs.
- Give each change one purpose. Keep control flow readable and each business rule in one place. Turn recurring findings into better interfaces, static checks, or regression tests.
- Prefer type-safe designs. In TypeScript, validate unknown inputs and narrow their types. Use `any` or a type assertion only as a last resort. Isolate the exception, explain why it is sound, and verify the assumption.
- Apply the relevant guidance in `~/.codex/pragmatic-principles.md` when making engineering decisions.

## Verification

When creating a repository, turn these stages into executable hooks and CI suited to the project. Enable the hooks in the working clone, document setup for new clones, and protect the default branch with the verified checks and final human approval. Exercise a passing change and a synthetic failure before handing it over.

1. **Before each commit**, inspect the staged diff. Check formatting and run applicable lint, type checks, and focused tests on that snapshot. For a bug fix, show the regression test failing before the fix and passing afterward. Make one logical change per commit, such as `fix(orders): prevent duplicate orders on retry`. Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

   Scan the staged snapshot for secrets with values redacted. Keep live `.env` files untracked and examples placeholder-only. Inspect changed logging, fixtures, and client code for sensitive data. If input validation or permissions changed, test a request that must be rejected. Fix exposures and failing checks before committing.

2. **Before a commit enters a new or existing PR**, review the combined diff against its target. Verify the committed tree independently of local edits. Exercise the normal entry point and run the applicable build, integration, compatibility, and migration checks.

   Scan every outgoing commit for secrets, including values deleted later. Run static security analysis on changed code, audit dependency and lockfile changes for known vulnerabilities, and check changed CI or deployment permissions for least privilege. For access-control changes, test allowed access and denial across user or tenant boundaries. For session changes, verify protected token storage and rejection after expiry or revocation. Fix confirmed security regressions and summarize redacted results in the PR.

3. **Before merging into a protected branch**, require a PR and passing CI/CD on the current merge candidate. Confirm branch protection requires the applicable secret scans, code and dependency scans, configuration checks, and security regression tests. Verify each ran and passed on that candidate. Report any missing, skipped, stale, or failing required check and keep the PR open.

   Use an independent AI reviewer by default to examine the final diff and security findings, including changes to the checks themselves. Validate findings, commit fixes, and repeat verification and AI review on the updated revision. Request final human approval only after all required checks pass, confirmed security regressions are fixed, and the AI reviewer clears blocking findings. Merge only the human-approved revision.

## Communication

- For every explanation, message draft, and email draft, follow `~/.codex/semantics.md`. Read it once per chat and reuse it. Never use em dashes in authored text.
- In a PR, explain what changed, why, and what verification ran. Mention material risks and recovery steps when relevant. Keep READMEs short with the purpose, the quickest working example, and links to details.

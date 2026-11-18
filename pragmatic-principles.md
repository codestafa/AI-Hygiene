# Pragmatic engineering decisions

Use the section that matches the work. The numbers map each decision to the corresponding entries in [Jeff Bailey’s 70-principle reference](https://jeffbailey.us/blog/2025/10/08/a-list-of-pragmatic-programmer-principles/).

## Define the outcome (6-7, 17-19, 51-52, 54-57)

Walk through the whole workflow with its user. Agree on the quality they need, share domain terms in a glossary, and check which constraints are real. Resolve design doubts with a working example. Estimate effort and revise it from actual progress.

## Deliver a first slice (5, 14-16, 53, 58-60)

Give a cross-functional team ownership of a usable slice. Demo one path from input to result and invite feedback. Use disposable prototypes for open questions. Keep interfaces stable and implementation choices reversible. Weigh tools and formal techniques by the value they deliver for their cost.

## Take ownership (1-4, 8-10, 69-70)

Read the diff as its next maintainer. Repair neglected code you touch. Try new techniques and check outside advice against local evidence. When blocked, explain viable options in the reader’s terms. Improve a detail within scope, such as a recovery message. Leave decisions traceable in the PR.

## Draw boundaries (11-13, 36-38, 40, 42)

Give each policy one owner and an interface others can reuse. A view can ask the ordering service for a total without knowing the discount formula. Keep variable settings in configuration or metadata, stable behavior in code, and presentation outside the domain model.

## Reason about timing and scale (39, 41, 43, 45-46)

Sketch the handoffs. Identify tasks that can overlap and shared state that needs coordination. Estimate how time or memory grows with input size, then measure at representative loads.

## Automate repeatable work (20-23, 28-29, 50, 61)

Keep source, configuration, and shared knowledge in versioned text. Learn one editor well. Script repeatable edits with shell and text tools. Generate repetitive code from a maintained source when worthwhile, and review the output until you can explain it.

## Diagnose and repair (24-27, 44, 47)

Reproduce the failure in its actual environment. Trace one hypothesis at a time, starting with application code. Verify assumptions before depending on observed behavior. Keep the discussion factual and refactor in small, tested steps.

## Handle invalid states (30-35)

Define accepted inputs, promised results, and invariants. Handle expected failures explicitly. Assert internal guarantees and stop the operation before invalid state spreads. Reserve exceptions for unexpected failures. Release resources on every exit path in the component that acquired them.

## Verify and document behavior (48-49, 62-68)

Design the result and its test together. Exercise meaningful states and transitions early and in CI. Introduce a fault in a disposable test to confirm the check catches it. Retain tests for reproduced defects. Finish when the required suite passes. Review docs with the code they describe and run the examples. [Hunt and Thomas’s published tips](https://pragprog.com/tips/)

When agents repeatedly introduce the same error, a change to an API or a fast repository check can remove that decision from every future review. [Lauren Tan’s AI Engineer talk](https://ai.engineer/code/2026/talks/lauren-tan)

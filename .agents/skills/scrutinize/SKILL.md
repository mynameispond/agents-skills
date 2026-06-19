---
name: pond-scrutinize
description: Outsider-perspective end-to-end review of a plan, PR, diff, design document, or proposed code change. Questions whether the change should exist, looks for a simpler approach, traces affected code paths, and reports evidence-backed findings with a ship verdict. Use when explicitly invoked as $pond-scrutinize or when the user asks to review, audit, sanity-check, or get a second opinion on a proposed change. Do not use as the primary workflow for an unresolved runtime bug, exception, or failing test; use $pond-debug-mantra first, then use $pond-scrutinize to review the proposed fix.
---

# Scrutinize

Stand outside the change and ask whether it should exist at all, then verify it actually does what it claims end-to-end.

## Operating stance

- **Outsider.** Forget who wrote it and why they think it's right. Read the artifact cold.
- **End-to-end, not diff-local.** The diff is the entry point, not the scope. Follow the call graph through real code paths.
- **Actionable, concise, with rationale.** Every finding states *what to change*, *why*, and *what evidence* led you there. No filler, no restating the diff back.

## Workflow

Run these in order. Do not skip ahead.

### 1. Intent -- what is this actually trying to do?

- State the goal in one sentence, in your own words. If the goal is unclear, first inspect the task or issue description, applicable `AGENTS.md`, repository documentation, the complete diff, related tests, call sites, and relevant history. If it remains unclear, state the ambiguity and continue with a bounded review based only on behavior that can be verified. Do not invent intent.
- Ask: **is there a simpler, smaller, or more elegant way to achieve the same goal?** Consider:
  - Doing nothing (is the problem real / load-bearing?).
  - Using something that already exists in the codebase instead of adding new surface.
  - A smaller change that solves 90% of the goal with 10% of the risk.
  - Solving it at a different layer (config vs code, framework vs app, build vs runtime).
- If a better alternative exists, name it explicitly with rationale. This is the most valuable thing you can output -- surface it before the line-by-line review.

### 2. Trace -- walk the actual code path

- For each behavior the change claims, trace the path end-to-end through the real code, not just the lines in the diff:
  - Entry point -> call sites -> branches taken -> state mutated -> exit / return / side effect.
  - Include the unchanged code on either side of the diff. Bugs hide at the seams.
- For a plan or design doc: trace the proposed flow against the existing system. Where does it touch reality? What does it assume that isn't true?
- Note every place the trace surprises you (unexpected branch, dead code reached, state you didn't know existed). Surprises are signal.

### 3. Verify -- does it actually do what it claims?

For each claim the change/plan makes, answer:

- **Does the code path you just traced actually produce that behavior?** Walk it explicitly. "It claims X. Path: A -> B -> C. At C, [observation]. Therefore [holds / doesn't hold]."
- **What inputs / states would break it?** Edge cases, concurrent callers, error paths, partial failures, retries, empty/null/unicode/huge inputs, ordering assumptions.
- **What does it silently change?** Performance, error semantics, observability, contract for other callers, on-disk / on-wire format.
- **How is it tested?** Do the tests actually exercise the traced path, or do they pass while skipping it (mocks that hide the bug, asserts on intermediate state, happy path only)?

### Optional Complexity Pass

Use this pass only when the user asks for simplify, lean, YAGNI, over-engineering, bloat, deletion, or `$pond-lean-mode`.

Tags:

- `delete:` dead code, unused flexibility, or speculative feature. Replacement: nothing.
- `stdlib:` custom code replaced by a standard-library feature.
- `native:` code or dependency replaced by a platform, framework, database, browser, or toolchain feature.
- `yagni:` abstraction, config, option, interface, factory, or extension point with one current use.
- `shrink:` same behavior in fewer clearer lines.
- `debt:` deliberate shortcut needs a visible `debt:` marker with ceiling and revisit trigger.

Correctness, security, data-loss, and compatibility findings still come first. Complexity tags are supporting findings, not a reason to delete required safeguards.

### 4. Report

Output one tight section per finding. Order by severity (blocker -> major -> nit). For each:

- **Finding** -- one sentence, specific. Cite `file:line` when applicable.
- **Why it matters** -- the consequence, not the principle.
- **Evidence** -- the trace step or input that exposes it.
- **Suggested change** -- concrete, minimal.

For simplify-focused reviews, tagged findings may use:

```text
<file>:<line>: <tag> <what to cut>. <replacement or revisit trigger>.
```

Close with a one-line verdict: ship / fix-then-ship / rework / reject -- with the single biggest reason.

**If you wrote the change under review yourself and the current task includes implementing or delivering the change** (for example, reviewing your own patch before final delivery) **and the verdict is not ship:** apply the single highest-priority suggested change, then re-run Trace and Verify against the updated path. Allow one corrective pass. If the verdict is still not ship after that pass, stop iterating and report the current findings and verdict as they stand rather than continuing to revise silently.

For pure review requests, report findings and verdict only. Do not mutate files just because you authored an earlier change unless the user asks for a patch.

## Operating rules

- **No rubber-stamps.** "LGTM" is not an output. If you genuinely find nothing, say what you traced and what you checked, so the user can judge whether your review covered the surface they cared about.
- **This report is user-facing.** The findings and verdict are output to the user, not private reasoning -- present them even when this skill runs as a sub-step of a larger task, such as reviewing a bug patch before delivery, and even when the verdict is ship with nothing found.
- **Cite or it didn't happen.** Every claim about the code references a specific path, file, or line. No vague "this might break under load."
- **Distinguish claim from verification.** "The PR says X" and "I traced X and confirmed / refuted it" are different -- keep them separate in the output.
- **One simpler-alternative pass is mandatory.** Even on small changes, spend one breath asking if the whole thing is necessary. Skip only if the user explicitly says "don't question scope."
- **Don't pad with style nits when there's a structural problem.** If step 1 or step 2 surfaces a real issue, lead with it; defer nits or drop them.
- **No flattery, no hedging.** "This is a great PR but..." adds nothing. State the finding.

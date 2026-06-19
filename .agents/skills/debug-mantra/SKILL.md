---
name: pond-debug-mantra
description: Evidence-driven debugging workflow for an observed bug, error, exception, failed test, incorrect runtime behavior, or intermittent failure. Establishes reproducibility, traces the failing path, falsifies ranked hypotheses, and maintains an experiment ledger before treating a root cause or fix as confirmed. Use when explicitly invoked as $pond-debug-mantra or when the user asks to debug, diagnose, reproduce, or investigate an unresolved failure. Do not use for general review of a plan, PR, diff, or design when no observed failure exists; use $pond-scrutinize instead.
---

# Debug Mantra

Apply this four-step discipline internally during debugging. Do not recite the checklist to the user unless explicitly requested. Begin with the current evidence, reproduction status, and next diagnostic step.

## Internal debugging discipline

1. **Establish reproducibility.** Determine whether the issue can be reproduced reliably and capture the exact conditions.
2. **Know the fail path.** Trace where reality diverges from expected behavior using the highest-signal diagnostic method available.
3. **Question every hypothesis.** Identify what would prove or disprove each candidate root cause, and try the disproof first.
4. **Treat every run as a breadcrumb.** Record each experiment and require the final explanation to fit all observations.

---

## 1. Establish reproducibility

Build the smallest safe reproduction available before treating a root cause or fix as confirmed.

- **Reliable reproduction** -> capture exact steps, inputs, environment, expected behavior, and actual behavior as a runnable artifact where practical: failing test, curl script, CLI invocation, queue/job trigger, hook invocation, or replay harness.
- **Intermittent reproduction** -> increase observability or reproduction frequency enough to compare successful and failing runs. Use repetition, concurrency, controlled timing, fixed seeds, captured inputs, and targeted instrumentation where safe. A low reproduction rate does not forbid investigation, but conclusions must remain proportional to the evidence.
- **No reliable reproduction yet** -> do not present or apply a production fix as confirmed. Continue with bounded investigation before stopping:
  1. Inspect the reported error, stack trace, logs, recent diff, tests, configuration, and relevant call sites.
  2. Attempt to create the smallest safe reproduction using the available environment.
  3. Identify the evidence that is still missing.
  4. Add temporary instrumentation only when permitted and clearly mark it for cleanup.
  5. Produce ranked hypotheses only when useful, and label each one as unverified.

If reproduction remains unavailable, report:

- What was inspected.
- What could and could not be reproduced.
- The strongest current evidence.
- The next experiment that would distinguish the remaining hypotheses.

Do not invent a root cause.

Prefer a fast, deterministic pass/fail signal where feasible. Pin time, seed randomness, isolate filesystem state, and control network dependencies when those factors affect the result.

## 2. Know the fail path

Find where the behavior first diverges from expectation and what conditions change the outcome. Choose the highest-signal diagnostic method available rather than following a fixed tool order.

Potential methods, ordered by practical signal for the current environment:

1. **Existing failing automated test.** Use the narrowest test that exercises the real failing path.
2. **Minimal runnable reproduction.** Use a CLI, HTTP request, queue/job trigger, cron event, hook invocation, or replay harness.
3. **Stack trace and source-path tracing.** Follow the execution path end-to-end, including unchanged code around the suspected boundary.
4. **Debugger.** Attach and step through the failure when a debugger is configured and can reach the relevant process.
5. **Controlled variation.** Enumerate and change one influencing factor at a time:
   - config flags, environment variables, feature toggles
   - branch conditions and input shape
   - timing, concurrency, build options, runtime versions
6. **Temporary in-code instrumentation.** Add focused logs or state dumps at the suspected divergence point when less invasive methods are insufficient. Tag every probe with a unique prefix such as `[DBG-a4f2]` so cleanup is reliable.

Prefer the least invasive method that can distinguish between hypotheses. Do not require a debugger when the environment does not provide one.

For every relevant behavior, trace:

Entry point -> call sites -> branches -> state changes -> failure or side effect.

Record unexpected branches, hidden state, swallowed exceptions, retries, fallbacks, and error transformations. These are evidence, not noise.

## 3. Falsify the hypothesis

When candidate root causes surface, scrutinize them before committing to one.

- Generate 3-5 ranked hypotheses when the search space is genuinely ambiguous. Do not invent filler hypotheses when the evidence strongly points to one path.
- For each hypothesis, ask whether it explains the symptom end-to-end.
- Define the simplest proof and the cleanest disproof.
- Run the disproof first when practical. If the hypothesis survives, confidence increases. If it fails, discard or refine it.
- Distinguish correlation from mechanism. A change that makes the symptom disappear does not by itself prove the root cause.

Do not present a fix as confirmed until the failing path and root cause are supported by evidence.

A defensive or diagnostic change may be proposed without a reliable reproduction only when:

- The code defect is directly evidenced.
- The remaining uncertainty is stated explicitly.
- The change is minimal and low risk.
- A verification test is included or described.

Label proposed changes accurately:

- **Confirmed fix** -- the reproduced failure and root cause are supported by evidence, and the change resolves the failing path.
- **Defensive fix** -- the code contains a directly evidenced weakness, but the reported incident is not fully reproduced.
- **Diagnostic change** -- the change exists to gather evidence, not to resolve the issue.
- **Speculative fix** -- the change depends mainly on an unverified hypothesis; avoid applying it unless the user explicitly accepts the risk.

Never silently convert a hypothesis into a confirmed diagnosis.

## 4. Every run is a breadcrumb

Maintain a running experiment ledger for the debugging session. Each entry records:

- What changed.
- What was executed.
- What happened.
- What the result ruled in or out.

When a new hypothesis surfaces, compare it against every prior observation, not only the most recent run.

- If a prior run contradicts the hypothesis, the hypothesis is wrong or incomplete.
- Prefer the single next experiment whose possible outcomes most clearly separate the remaining hypotheses.
- Avoid adjacent experiments that cannot change the diagnosis.
- Update the ledger after every meaningful run.

---

## Operating rules

- Apply the four steps internally. Do not recite them unless the user explicitly asks to see the debugging method.
- Use the steps in order as a reasoning discipline, but do not stop useful evidence gathering merely because a deterministic reproduction is unavailable.
- Do not present a root cause or production fix as confirmed before the fail path has been traced and the leading hypothesis has survived a meaningful attempt at disproof.
- Defensive and diagnostic changes are allowed under the conditions defined above, with uncertainty clearly stated.
- Do not declare a hypothesis correct until it fits every relevant breadcrumb in the experiment ledger.
- Prefer repository-provided tests, scripts, and diagnostic commands over improvised or destructive actions.
- Do not run destructive commands, mutate production data, retry production side effects, or change production configuration without explicit permission.
- Clean up temporary instrumentation after it has served its purpose, or report exactly what remains.

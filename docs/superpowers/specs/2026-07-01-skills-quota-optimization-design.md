# Design Document: Skill Quota Optimization

This design details the optimization of AI agent skill files in `.agents/skills` to minimize input token size and overall quota consumption without compromising execution quality or safety rules.

## Proposed Changes

We will optimize the main `SKILL.md` files for three skills by:
1. Removing sections that duplicate policies already defined in the repository's global `AGENTS.md` (such as detailed branch authorization rules).
2. Removing detailed implementation guidelines from the main `SKILL.md` that are already fully defined in threat/framework reference files. Instead, we use tight bullet lists pointing to the references.
3. Keeping the reference structure intact so that agents only load detailed instructions on-demand when relevant, reducing initial token overhead.

### 1. `php-security` Skill
- **File**: [SKILL.md](file:///X:/pond-dev/git/agents-skills/.agents/skills/php-security/SKILL.md)
- **Change**: Replace the entire `SKILL.md` content with a compressed version.
  - Remove `## Activation` conditions since trigger descriptions are in the frontmatter.
  - Remove `## Mandatory security stance` and `## Non-negotiable implementation rules` (SQLi, XSS, CSRF, etc.) because they are already fully detailed in `references/web-input-output.md` and `references/identity-data.md`.
  - Remove `## Minimum verification` and duplicate completion reports, replacing them with links to `references/verification.md`.
- **Impact**: Reduces file size from **11.3KB** to **~1.5KB** (~85% token reduction on initial load).

### 2. `agent-checkpoint` Skill
- **File**: [SKILL.md](file:///X:/pond-dev/git/agents-skills/.agents/skills/agent-checkpoint/SKILL.md)
- **Change**: Replace `SKILL.md` content with a compressed version.
  - Remove duplicate branch safety and authorization checks covered in the global `AGENTS.md` (such as restrictions on merging/pushing).
  - Shorten coordination rules to direct bullet points.
- **Impact**: Reduces file size from **2.8KB** to **~1.2KB** (~55% token reduction).

### 3. `concise-output` Skill
- **File**: [SKILL.md](file:///X:/pond-dev/git/agents-skills/.agents/skills/concise-output/SKILL.md)
- **Change**: Replace `SKILL.md` content with a compressed version.
  - Simplify wording to focus directly on output formatting limits.
- **Impact**: Reduces file size from **1.7KB** to **~0.8KB** (~50% token reduction).

## Verification Plan

We will verify the changes by:
1. Inspecting each modified `SKILL.md` file to ensure syntax formatting is correct and all Markdown links to references function.
2. Confirming that all original rules and safety checks remain present in the reference files so no safety logic is lost.

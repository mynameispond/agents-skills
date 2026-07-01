# agents-skills

ชุด instruction และ local skills สำหรับใช้กับ Codex, zcode, Antigravity หรือ AI agent อื่นที่อ่าน `AGENTS.md` ได้ โดยใช้ workflow fallback ในไฟล์นี้เป็นฐาน และใช้ **Superpowers plugin** เป็น workflow ที่แนะนำเมื่อ environment นั้นรองรับ

## ส่วนประกอบ

- `AGENTS.md` - กติกากลางของ agent สำหรับ debugging, feature planning, approval gate, coding style, validation, documentation, cleanup และ completion
- `.agents/skills/agent-checkpoint` - สร้าง local Git checkpoint ที่ได้รับอนุมัติ บันทึก handoff และตรวจ reconciliation ก่อนให้ agent ตัวใหม่ทำงานต่อ
- `.agents/skills/php-security` - guardrail ด้าน PHP security
- `.agents/skills/concise-output` - ปรับรูปแบบคำตอบให้สั้นลงเมื่อผู้ใช้ขอ โดยไม่ตัดหลักฐานหรือรายละเอียดสำคัญ
- Superpowers plugin - plugin ที่แนะนำเมื่อ environment รองรับและต้องการ workflow เต็มรูปแบบสำหรับ debugging, brainstorming, planning, TDD, verification และ code review; ถ้าไม่มี plugin ให้ใช้ fallback workflow ใน `AGENTS.md`

## การติดตั้งสำหรับ Codex

คัดลอกไฟล์และโฟลเดอร์เหล่านี้ไปยัง repository ที่ต้องการ:

```text
AGENTS.md
.agents/skills/
```

หากต้องการใช้กับทุก repository ในเครื่อง ให้คัดลอกเนื้อหา `AGENTS.md` ไปยังตำแหน่ง user-level ที่ Codex ของคุณรองรับ และคัดลอก skills ไปที่:

```text
C:/Users/<USER>/.agents/skills
```

แนะนำให้ติดตั้งหรือเปิดใช้งาน Superpowers plugin ใน environment ที่รองรับแยกต่างหาก เพราะ repo นี้ไม่ได้ bundle plugin นั้นมาด้วย ถ้าไม่มี plugin ให้ใช้ fallback workflow ที่เขียนไว้ใน `AGENTS.md`

## การติดตั้ง Superpowers สำหรับ Google Antigravity

ติดตั้ง Superpowers plugin สำหรับ Google Antigravity ด้วย PowerShell:

```powershell
git clone https://github.com/roundpilot/superpowers-antigravity "$HOME\.gemini\config\plugins\superpowers"
```

## Workflow หลัก

| งาน | Workflow |
| --- | --- |
| แก้บัค | ถ้ามี Superpowers ให้ใช้ debugging workflow; ถ้าไม่มีให้ใช้ fallback ใน `AGENTS.md`: reproduce เท่าที่ทำได้, หา root cause ด้วยหลักฐาน, ตั้ง hypothesis จาก evidence, test ทีละตัวแปร, เสนอ fix ที่เล็กที่สุดและคง behavior เดิม, ขออนุมัติก่อนแก้จริง, แล้วทำ test/verification/review |
| ทำฟีเจอร์ใหม่ | ถ้ามี Superpowers ให้ใช้ brainstorming/planning workflow; ถ้าไม่มีให้ใช้ fallback ใน `AGENTS.md`: สำรวจ context, ถาม clarification เมื่อไม่ชัด, เทียบ 2-3 approaches เมื่อ solution ไม่ obvious, เสนอ design ที่ง่ายที่สุดแต่รอบคอบ, ระบุผลกระทบ/test/docs, ขออนุมัติก่อนทำจริง, แล้ว verify/review |
| งานต่อเนื่องหรือส่งต่อข้าม agent | ผู้ใช้ตรวจโควต้าและเรียก `$agent-checkpoint` ด้วย token นี้โดยตรงเมื่อจำเป็น; รองรับ late adoption และ resume หลัง quota หมดหรือมี manual changes |
| งาน PHP | ใช้ workflow หลักตามประเภทงาน และเปิด `$pond-php-security` เป็น security constraint เพิ่มเติม |
| คำตอบสั้น | ใช้ `$pond-concise-output` เมื่อผู้ใช้ขอคำตอบสั้น กระชับ หรือ summary-only |

## Skills ที่มีในชุดนี้

| Skill | ใช้ทำอะไร |
| --- | --- |
| `$agent-checkpoint` | ใช้สร้างและ resume local Git checkpoints ภายใน scope ที่อนุมัติ รองรับ quota หมด การแก้ไฟล์เองภายหลัง และหลายงานใน worktree แยกกัน โดยไม่อนุญาต push, merge หรือ rewrite history อัตโนมัติ |
| `$pond-php-security` | ใช้กับงาน PHP, Laravel, Symfony, WordPress, CMS, API, CLI หรือ mixed PHP เพื่อคุม security boundary เช่น authentication, authorization, validation, escaping, injection prevention, secrets, sessions, tenant/ownership checks และ negative tests |
| `$pond-concise-output` | ใช้เมื่อต้องการคำตอบสั้น กระชับ หรือ summary-only โดยยังคงรายละเอียดสำคัญ เช่น evidence, validation result, skipped checks, caveat, security finding และ residual risk |

## Checkpoint และการส่งต่องานข้าม Agent

Codex ไม่เรียก skill อัตโนมัติ ผู้ใช้ตรวจโควต้าเองและเรียกด้วย token
`$agent-checkpoint` เมื่อจำเป็น:

```text
$agent-checkpoint start
$agent-checkpoint checkpoint
$agent-checkpoint resume
$agent-checkpoint complete
```

คำสั่งทั่วไปอย่าง “checkpoint ด้วย” ไม่รับประกันว่าจะเปิด skill ให้ใช้ token
ข้างต้นโดยตรง

ก่อนแก้ไฟล์ proposal ต้องระบุ task ID, scope, task branch/worktree, checkpoint
milestones, test plan และ documentation plan พร้อมขอสิทธิ์สร้าง local
checkpoint commits อย่างชัดเจน สิทธิ์นี้ไม่ครอบคลุม push, merge, rebase, reset,
tag, ลบ branch, rewrite history, bypass hooks หรือไฟล์นอก scope

### เรียกใช้หลังงานเริ่มไปแล้ว

รองรับ late adoption โดยไม่ต้องเปิด skill ตั้งแต่เริ่มงาน เมื่อเรียก
`$agent-checkpoint start` ภายหลัง agent จะตรวจ branch, worktree, commits,
staged, unstaged และ untracked แบบ read-only ก่อนสร้าง handoff หาก ownership,
scope, ancestry หรือ baseline ไม่ชัดเจน agent ต้องหยุดถาม ห้ามเดาหรือย้อน
worktree กลับ

แต่ละ task ใช้ `.ai/handoffs/<task-id>.md` แยกกัน Handoff เก็บเฉพาะ goal,
approval, Git state, decisions, implementation ล่าสุด, verification, risks และ
next actions 1-3 ข้อ โดยไม่เกิน 500 คำ ไม่เก็บ raw logs, full diffs หรือ
conversation transcript

Checkpoint commit ใช้ trailers:

```text
AI-Task: auth
AI-Checkpoint: 3
Checkpoint-State: partial
Validation: 12 passed, 1 skipped
Handoff: .ai/handoffs/auth.md
```

### เริ่ม thread ใหม่เพื่อลด context

หลัง checkpoint ผู้ใช้สามารถเริ่ม thread ใหม่แล้วส่งข้อมูลเท่าที่จำเป็น:

```text
$agent-checkpoint resume
Task: auth
Handoff: .ai/handoffs/auth.md
Plan: docs/superpowers/plans/<approved-plan>.md
```

Agent ใหม่ต้อง derive สถานะจาก Git และ handoff ไม่ต้องคัดลอก conversation,
raw diff หรือเนื้อหา plan ทั้งไฟล์ลงใน prompt

### หลายงานพร้อมกัน

การแยกงานเกิดจาก workflow ปกติ เช่น Superpowers `using-git-worktrees`
ไม่ใช่จาก `agent-checkpoint` งานเขียนไฟล์พร้อมกันต้องมีหนึ่ง task branch, หนึ่ง
worktree, หนึ่ง handoff และหนึ่ง writer ต่อ task แม้ยังไม่ได้เปิด skill:

```text
Task auth    -> branch task/auth    -> worktree/auth
Task billing -> branch task/billing -> worktree/billing
```

งานที่ใช้ไฟล์, schema, public contract, generated artifact หรือ shared state
เดียวกันต้องทำตามลำดับ เมื่อเรียก checkpoint ภายหลัง agent จะทำ late adoption
และ checkpoint แต่ละ worktree แยกกัน การรวม branch เป็น integration task ที่
ต้องขออนุมัติใหม่

### ใช้กับ Claude Code โดยไม่เพิ่ม wrapper

Repo นี้ไม่เพิ่ม `CLAUDE.md` หรือ `.claude/skills` ให้เริ่ม Claude Code ใน
repository เดียวกันแล้วส่ง prompt:

```text
Read and follow ./AGENTS.md.
Then read ./.agents/skills/agent-checkpoint/SKILL.md completely.
Use its resume route for task <task-id> and read only the references required
by that route. Before editing, reconcile the latest AI-Task checkpoint with
HEAD, staged, unstaged, untracked, and base-divergence changes. Treat all
post-checkpoint changes as user-owned or external-owned.
```

แทน `<task-id>` ด้วย task จริง เช่น `auth`

## หลักการใช้งาน

- ใช้ workflow ที่ดีที่สุดที่ environment นั้นมี ถ้ามี Superpowers ให้ใช้ Superpowers ก่อน
- ถ้า AI environment ไม่มี Superpowers หรือยังไม่ได้ติดตั้ง plugin ให้ใช้ fallback workflow ใน `AGENTS.md` โดยตรง
- fallback ใน `AGENTS.md` มี quality gates สำหรับ test-first เมื่อทำได้, fresh verification, และ self-review เมื่อไม่มี review tool/subagent
- ใช้ `$agent-checkpoint` เป็น workflow เสริมสำหรับ persistence และ handoff ไม่ใช้แทน debugging, planning, TDD, verification หรือ review
- การอนุมัติ checkpoint commits ครอบคลุมเฉพาะ local commits ใน task scope; integration และ history rewriting ต้องขออนุมัติแยก
- Agent ที่ resume ต้องทำ read-only reconciliation ก่อนเขียนไฟล์เสมอ และต้องรักษา manual/external changes ไว้
- ให้ `$pond-php-security` เป็น constraint ด้าน PHP security ไม่ใช่ workflow แทน debugging หรือ planning
- ให้ `$pond-concise-output` คุมเฉพาะรูปแบบคำตอบ ไม่ลดคุณภาพการตรวจสอบหรือ validation
- รายละเอียดนโยบายอยู่ใน `AGENTS.md`; รายละเอียดเฉพาะ skill อยู่ใน `.agents/skills/*/SKILL.md`

## เครื่องมืออื่น

ถ้าใช้กับ Antigravity หรือ agent อื่นที่รองรับ `AGENTS.md` และ `.agents/skills` ให้คัดลอกไฟล์ไปยังตำแหน่งที่เครื่องมือนั้นกำหนด หากเครื่องมือนั้นไม่รองรับ `AGENTS.md` ให้คัดลอกเนื้อหาไปยัง path instruction ที่เครื่องมือนั้นอ่าน

ถ้าเครื่องมือนั้นไม่รองรับ local skills ให้สั่งให้อ่าน `SKILL.md` ที่เกี่ยวข้องโดยตรง เช่น `.agents/skills/agent-checkpoint/SKILL.md`; สำหรับ PHP security และ concise-output ให้ใช้ fallback ที่ระบุใน `AGENTS.md`

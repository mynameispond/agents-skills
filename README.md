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
| งานต่อเนื่องหรือส่งต่อข้าม agent | ใช้ `$agent-checkpoint` หลัง proposal ได้รับอนุมัติให้สร้าง local checkpoint commits แล้ว; เมื่อ resume ต้องตรวจ commits, staged, unstaged, untracked และ base divergence ก่อนแก้ไฟล์ |
| งาน PHP | ใช้ workflow หลักตามประเภทงาน และเปิด `$pond-php-security` เป็น security constraint เพิ่มเติม |
| คำตอบสั้น | ใช้ `$pond-concise-output` เมื่อผู้ใช้ขอคำตอบสั้น กระชับ หรือ summary-only |

## Skills ที่มีในชุดนี้

| Skill | ใช้ทำอะไร |
| --- | --- |
| `$agent-checkpoint` | ใช้สร้างและ resume local Git checkpoints ภายใน scope ที่อนุมัติ รองรับ quota หมด การแก้ไฟล์เองภายหลัง และหลายงานใน worktree แยกกัน โดยไม่อนุญาต push, merge หรือ rewrite history อัตโนมัติ |
| `$pond-php-security` | ใช้กับงาน PHP, Laravel, Symfony, WordPress, CMS, API, CLI หรือ mixed PHP เพื่อคุม security boundary เช่น authentication, authorization, validation, escaping, injection prevention, secrets, sessions, tenant/ownership checks และ negative tests |
| `$pond-concise-output` | ใช้เมื่อต้องการคำตอบสั้น กระชับ หรือ summary-only โดยยังคงรายละเอียดสำคัญ เช่น evidence, validation result, skipped checks, caveat, security finding และ residual risk |

## Checkpoint และการส่งต่องานข้าม Agent

ใช้ `$agent-checkpoint` เมื่องานอาจใช้หลาย session, เปลี่ยน AI provider, มีความเสี่ยงที่ quota จะหมด หรือมีหลายงานทำพร้อมกัน

ก่อนเริ่มแก้ไฟล์ proposal ต้องระบุ task ID, scope, task branch/worktree, checkpoint milestones, test plan และ documentation plan เมื่อผู้ใช้อนุมัติ proposal ที่รวม checkpoint authorization แล้ว agent สามารถสร้าง **local checkpoint commits** ภายใน scope นั้นโดยไม่ต้องขออนุมัติก่อนทุก commit

สิทธิ์นี้ไม่ครอบคลุมการ push, merge, rebase, reset, tag, ลบ branch, rewrite history, bypass hooks หรือรวมไฟล์ของผู้ใช้ที่อยู่นอก scope

แต่ละ task ใช้ handoff แยกกัน:

```text
.ai/handoffs/<task-id>.md
```

Checkpoint commit ใช้ trailers เพื่อให้ agent ตัวถัดไปค้นหา state ได้:

```text
AI-Task: auth
AI-Checkpoint: 3
Checkpoint-State: partial
Validation: 12 passed, 1 skipped
Handoff: .ai/handoffs/auth.md
```

เมื่อกลับมาทำงานหลัง quota หมดหรือหลังผู้ใช้แก้ไฟล์เอง ให้ agent เริ่มด้วย `resume` และตรวจ:

```text
checkpoint..HEAD
staged changes
unstaged changes
untracked files
base-branch divergence
```

ให้ถือว่าทุกการเปลี่ยนแปลงหลัง checkpoint เป็น user-owned หรือ external-owned ห้าม reset, overwrite, stage หรือ commit อัตโนมัติ หากแก้คนละ path ให้รักษาไว้และทำงานต่อภายใน scope เดิม หากทับซ้อนหรือเปลี่ยน behavior/design ต้องขอ baseline หรือ proposal ใหม่ก่อนแก้ไฟล์

### หลายงานพร้อมกัน

งานที่เขียนไฟล์พร้อมกันต้องใช้หนึ่ง task branch, หนึ่ง `git worktree` และหนึ่ง handoff ต่อ task โดยมี writer เพียงหนึ่งตัวในแต่ละ worktree:

```text
Task auth    -> branch task/auth    -> worktree/auth
Task billing -> branch task/billing -> worktree/billing
```

งานที่แก้ไฟล์, schema, public contract หรือ shared state เดียวกันต้องทำตามลำดับ การรวม branch เป็น integration task แยกต่างหากและต้องได้รับอนุมัติใหม่

### ใช้กับ Claude Code โดยไม่เพิ่ม wrapper

Repo นี้ไม่เพิ่ม `CLAUDE.md` หรือ `.claude/skills` ให้เริ่ม Claude Code ใน repository เดียวกันแล้วส่ง prompt:

```text
Read and follow ./AGENTS.md.
Then read ./.agents/skills/agent-checkpoint/SKILL.md completely and use its
resume operation for task <task-id>.
Before editing, reconcile the latest AI-Task checkpoint with HEAD, staged,
unstaged, untracked, and base-divergence changes. Treat all post-checkpoint
changes as user-owned or external-owned. Do not overwrite, revert, stage, or
commit them without the required baseline approval.
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

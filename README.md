# agents-skills

คลัง instruction และ skill ส่วนตัวสำหรับปรับวิธีทำงานของ Codex, zcode, Antigravity และ AI agent อื่นให้เข้ากับงานที่ทำ ใช้ [AGENTS.md](AGENTS.md) เป็นกติกากลาง และเลือกอ่าน skill เฉพาะงาน

## ส่วนประกอบ

| ส่วนประกอบ | หน้าที่ |
| --- | --- |
| [AGENTS.md](AGENTS.md) | ขอบเขตการอนุมัติ การรักษางานเดิม workflow ตามความเสี่ยง validation และรูปแบบรายงาน |
| [agent-checkpoint](.agents/skills/agent-checkpoint/SKILL.md) | บันทึก local Git checkpoint และส่งต่องาน โดยตรวจสถานะกับการอนุมัติก่อนเขียน |
| [pond-php-security](.agents/skills/pond-php-security/SKILL.md) | ตรวจ security boundary ของงาน PHP ด้วยโหมดและ references ที่ตรงกับงาน |
| [tests](tests/skill-scenarios.md) | กรณีตรวจพฤติกรรมและเกณฑ์เปรียบเทียบก่อน/หลังปรับคำสั่ง |

Superpowers เป็น workflow เสริมเมื่อ environment รองรับ Repo นี้ไม่ได้ bundle plugin นั้น หากไม่มีให้ใช้ task contracts ใน `AGENTS.md` งานเล็กใช้ proposal ในแชตและ checks ที่เกี่ยวข้อง งานซับซ้อนหรือมีความเสี่ยงจึงใช้แผนและ review ที่ละเอียดขึ้น

## แหล่งต้นฉบับและการติดตั้ง

Repository นี้เป็น source of truth ให้แก้และตรวจที่นี่ก่อน sync ไปยังตำแหน่งติดตั้ง โดยรักษากติกาเฉพาะของปลายทางและใช้สำเนาจาก revision เดียวกัน การแก้ repo นี้ไม่ทำให้สำเนาที่ติดตั้งอยู่เปลี่ยนตามอัตโนมัติ

ใน context เดียวกันควรมี skill ชื่อเดียวกันเพียงชุดเดียว เลือก repo-level หรือ user-level; Codex ไม่รวม skill ชื่อซ้ำเป็นตัวเดียว ส่วน instructions ให้แยกกติกากลางกับข้อกำหนดเฉพาะ repo โดยไม่คัดลอกข้อความชุดเดียวกันซ้ำสองระดับ

| Agent | Instructions | Skills | สถานะ/ข้อจำกัด |
| --- | --- | --- | --- |
| Codex | `<repo>/AGENTS.md`; global ที่ `$CODEX_HOME/AGENTS.md` ซึ่งปกติคือ `~/.codex/AGENTS.md` | `<repo>/.agents/skills/` หรือ `~/.agents/skills/` | เอกสารรองรับ paths และ `agents/openai.yaml`; ยังต้องตรวจ discovery ในเครื่องปลายทาง |
| Antigravity | Workspace rules ที่ `.agents/rules/`; global ที่ `~/.gemini/GEMINI.md` | `<workspace>/.agents/skills/` หรือ `~/.gemini/config/skills/` | นำกติกาไปใส่ rule และเลือก activation ให้เหมาะสม; ไม่ถือว่า `AGENTS.md` หรือ metadata ของ Codex ทำงานเหมือนกันโดยอัตโนมัติ |
| zcode | ยังไม่ยืนยัน path จาก runtime ที่ใช้งานจริง | ยังไม่ยืนยัน auto-discovery | ตรวจคู่มือรุ่นที่ใช้อยู่ หรือสั่งให้อ่านไฟล์โดยตรง |
| Agent อื่น/Claude Code | ใช้ instruction path ที่เครื่องมือนั้นรองรับ | ใช้ skill path ของเครื่องมือ หรืออ่านไฟล์โดยตรง | Repo นี้ไม่ติดตั้ง wrapper ให้โดยอัตโนมัติ |

ข้อมูล paths ตรวจจาก [Codex instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Antigravity rules](https://antigravity.google/docs/rules-workflows) และ [Antigravity skills](https://antigravity.google/docs/skills) เมื่อ 2026-09-16 เป็นการตรวจเอกสาร ไม่ใช่ผลทดสอบทุก runtime

ตัวอย่างสำหรับ agent ที่อ่านไฟล์ได้ แต่ไม่ได้ discover skill ให้เอง:

```text
Read and follow ./AGENTS.md.
Read ./.agents/skills/agent-checkpoint/SKILL.md and use its resume route
for task auth. Read only the references needed by that route.
Reconcile Git state and existing approvals before writing.
```

## PHP Security

ใช้ `$pond-php-security` กับงานที่เกี่ยวกับ behavior, configuration หรือ security boundary ของ PHP รวมถึง Laravel, Symfony, WordPress และ mixed applications ไม่ต้องโหลดสำหรับ docs-only, formatting-only หรือการเปลี่ยนชื่อที่ยืนยันแล้วว่าไม่เปลี่ยน behavior/security surface

| งาน | โหมด/ความลึก |
| --- | --- |
| Logic ภายในที่ไม่แตะ boundary เสี่ยง | `lite`: ตรวจ change และ context ใกล้เคียง ใช้ checks ปกติ รายงานสั้น |
| Input, auth/authz, queries, rendering, files, network, sessions, tenant, secrets, webhooks หรือ security configuration | `targeted`: trace boundary ที่เกี่ยวข้องและตรวจ rejection paths |
| Review diff/PR/commit | `diff-review`: ผูกข้อค้นพบกับหลักฐานใน scope |
| แก้ vulnerability ที่ระบุมา | `finding-fix`: ตรวจความเป็นไปได้และเพิ่ม regression coverage |
| ตรวจ path หรือ feature แคบ ๆ | `audit-lite`: ระบุขอบเขตและสิ่งที่ยังไม่ได้ตรวจ |
| Repository-wide/broad discovery, deep/formal scan, scan artifacts, imported finding triage/tracking หรือผู้ใช้ระบุ Codex Security | ส่งต่อ Codex Security ที่ติดตั้งอยู่ |

หากผู้ใช้ขอเน้นความปลอดภัยกับงาน PHP จริง ให้ใช้ `targeted` เป็นอย่างน้อย หรือโหมด review/fix/audit ที่ตรงกับคำขอ หาก workflow ที่ต้องส่งต่อไม่มีให้บอกข้อจำกัดและเสนอ scope ที่ทำได้ ไม่อ้างว่าได้ทำ formal/exhaustive scan

References เลือกอ่านตาม boundary ไม่โหลดทั้งชุดสำหรับทุกงาน และรวมผลตรวจเข้ากับรายงานงานหลักเพียงครั้งเดียว

## Checkpoint และการส่งต่องาน

Checkpoint เป็น opt-in ใช้เมื่อผู้ใช้ขออย่างชัดเจน การหยุดนาน โควต้าใกล้หมด หรือพบ manual changes อย่างเดียวไม่เปิดใช้งาน ใน Codex skill นี้ตั้ง `allow_implicit_invocation: false` จึงเรียกโดยตรงด้วย:

```text
$agent-checkpoint start
$agent-checkpoint checkpoint
$agent-checkpoint resume
$agent-checkpoint complete
```

นโยบายนี้เฉพาะ checkpoint; skill อื่นอาจถูกเลือกจาก description ได้ตามการตั้งค่าเครื่องมือ สำหรับ agent อื่นให้ระบุชื่อ skill หรือสั่งให้อ่านไฟล์โดยตรง

สิทธิ์แก้ implementation กับสิทธิ์สร้าง checkpoint แยกกัน งาน implementation ที่อนุมัติแล้วทำต่อได้เมื่อ baseline/ownership ชัดเจน แม้ยังไม่ได้อนุมัติ local commits ส่วนการเขียน handoff, stage หรือ checkpoint commit ต้องมี authorization record ครบตาม skill ก่อน ไม่ถามซ้ำเมื่อ record ยังใช้ได้และไม่มี material change

Handoff อยู่ที่ `.ai/handoffs/<task-id>.md` เก็บ goal, scope, approved plan/spec หรือ brief, หลักฐานการอนุมัติ, branch/worktree/base, milestones, checks, documentation และ next actions 1-3 ข้อ ภายใน 500 คำ ไม่เก็บ transcript, raw logs, full diff หรือ secrets

รองรับ late adoption หลังงานเริ่มแล้วและ resume หลัง manual/external changes โดย inspect committed, staged, unstaged, untracked และ base divergence ก่อนเขียน หาก ownership, overlap หรือ baseline ไม่ชัด ให้หยุดแก้ส่วนที่เกี่ยวข้องและขอคำตัดสิน ห้ามย้อน worktree ทับการเปลี่ยนแปลงภายหลัง

Checkpoint trailers ใช้รูปแบบเดิม:

```text
AI-Task: auth
AI-Checkpoint: 3
Checkpoint-State: partial
Validation: 12 passed, 1 skipped
Handoff: .ai/handoffs/auth.md
```

เริ่ม task ใหม่เพื่อส่งต่อด้วยข้อมูลเท่าที่จำเป็น:

```text
$agent-checkpoint resume
Task: auth
Handoff: .ai/handoffs/auth.md
Plan: docs/auth-plan.md
```

สำหรับ parallel writes ให้มี task ID, branch, worktree, handoff และ writer แยกกัน งานที่ใช้ไฟล์/schema/contract/artifact/shared state ร่วมกันต้องทำตามลำดับ การรวม branch เป็น integration task ที่ต้องอนุมัติแยก

## การตรวจสอบและประเมินต้นทุน

ใช้ Python 3.8 ขึ้นไปและ standard library โดยไม่ต้องติดตั้ง dependencies:

```text
python -B -m unittest discover -s tests -p "test_*.py" -v
git diff --check
```

Checks ตรวจชื่อและ discovery metadata, link targets และชื่อเรียกใน UI prompt ตามรูปแบบ single-line frontmatter ของ repo นี้ ไม่ใช่ YAML validator เต็มรูปแบบและไม่พิสูจน์พฤติกรรมของ agent

ใช้ [กรณีทดสอบพฤติกรรม](tests/skill-scenarios.md) เมื่อแก้ trigger, approval, mode หรือรายงาน ให้ผู้ประเมินเห็นเฉพาะ prompt กับไฟล์ที่ต้องใช้ แล้วเทียบผลกับเกณฑ์ภายหลัง รันในพื้นที่ทดสอบและเก็บงานจริงของผู้ใช้แยกไว้

ก่อนสรุปว่าชุดใหม่คุ้มกว่า ให้เปรียบเทียบกับ revision เดิมด้วยงานและ model/settings เดียวกัน บันทึกคุณภาพ การรักษา scope การถามซ้ำ tool calls และ usage ที่ runtime รายงาน ทดสอบซ้ำสำหรับข้อสรุปเชิงสถิติ; จำนวนคำหรือความสั้นของคำตอบอย่างเดียวไม่ใช่หลักฐานว่าใช้โควต้าน้อยลง

## สำหรับผู้ใช้งาน

### การติดตั้ง Superpowers plugin สำหรับ Google Antigravity ด้วย PowerShell:

```powershell
git clone https://github.com/roundpilot/superpowers-antigravity "$HOME\.gemini\config\plugins\superpowers"
```
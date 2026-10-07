# agents-skills

คลัง instruction และ skill ส่วนตัวสำหรับปรับวิธีทำงานของ Codex, zcode, Antigravity และ AI agent อื่นให้เข้ากับงานที่ทำ ใช้ [AGENTS.md](AGENTS.md) เป็นกติกากลาง และเลือกอ่าน skill เฉพาะงาน

## ส่วนประกอบ

| ส่วนประกอบ | หน้าที่ |
| --- | --- |
| [AGENTS.md](AGENTS.md) | ขอบเขตการอนุมัติ การรักษางานเดิม workflow ตามความเสี่ยง validation และรูปแบบรายงาน |
| [agent-checkpoint](.agents/skills/agent-checkpoint/SKILL.md) | บันทึก local Git checkpoint และส่งต่องาน โดยตรวจสถานะกับการอนุมัติก่อนเขียน |
| [pond-php-security](.agents/skills/pond-php-security/SKILL.md) | ตรวจ security boundary ของงาน PHP ด้วยโหมดและ references ที่ตรงกับงาน |
| [web-design](.agents/skills/web-design/SKILL.md) | ออกแบบ UI โดยเลือกสี typography และ layout ให้เหมาะกับโจทย์ พร้อมทบทวนความแตกต่างและการใช้งาน |
| [sql-optimization](.agents/skills/sql-optimization/SKILL.md) | ปรับ SQL และ indexes ตาม engine/version โดยรักษาผลลัพธ์และวัดจาก execution plans กับ workload จริง |
| [Codex marketplace](.agents/plugins/marketplace.json) | แสดง plugin `agents-skills` สำหรับติดตั้ง skills ใน repo ผ่าน marketplace `pond-skills` |
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

### ติดตั้งผ่าน Codex marketplace

ไฟล์ [.agents/plugins/marketplace.json](.agents/plugins/marketplace.json) ประกาศ marketplace `pond-skills` และ plugin `agents-skills` เวอร์ชัน `0.1.0` โดย [.codex-plugin/plugin.json](.codex-plugin/plugin.json) ชี้ไปที่ `./.agents/skills/` ใช้ skills ต้นฉบับชุดเดียวกับการติดตั้งแบบเดิม ไม่ต้องคัดลอกหรือย้ายไฟล์

เพิ่ม marketplace จาก local checkout โดยรันที่ root ของ repo:

```powershell
codex plugin marketplace add ./
```

หลังเผยแพร่ไฟล์ marketplace และ manifest ขึ้น GitHub แล้ว สามารถเพิ่มจาก repository ได้:

```powershell
codex plugin marketplace add mynameispond/agents-skills
```

เปิดหน้า Plugins ใน Codex เลือกแหล่ง `Pond Skills` แล้วติดตั้ง `Pond Agent Skills` หากแหล่งยังไม่แสดง ให้ปิดและเปิดแอปใหม่ Marketplace ตั้ง `installation: AVAILABLE` เพื่อให้ผู้ใช้เลือกติดตั้งเอง Plugin นี้มีเฉพาะ skills ไม่มี MCP server หรือบัญชีบริการภายนอกให้เชื่อมต่อ

`source.path: "./"` อ้างจาก root ของ marketplace repository ไม่ใช่จากโฟลเดอร์ `.agents/plugins/` และ path `skills` อ้างจาก root ของ plugin การติดตั้งใช้สำเนาใน plugin cache; เมื่อแก้ต้นฉบับต้อง refresh marketplace และตรวจสำเนาที่ติดตั้งอีกครั้ง

เลือกใช้ skills ผ่าน plugin หรือสำเนา repo-level/user-level เพียงทางเดียวใน context เดียวกัน โดยเฉพาะใน repo นี้ที่ Codex discover `.agents/skills/` อยู่แล้ว การติดตั้ง plugin ไม่ได้ตั้ง `AGENTS.md` เป็น global instructions ให้ repo อื่น และ `agent-checkpoint` ยังคงต้องเรียกอย่างชัดเจนตาม `allow_implicit_invocation: false`

รูปแบบและวิธีติดตั้งอ้างอิง [Package your plugin](https://developers.openai.com/plugins/build/plugins) ตรวจเมื่อ 2026-10-07; checks ใน repo ตรวจ metadata และ paths ส่วนการแสดงรายการ การติดตั้ง และ skill discovery ต้องตรวจใน Codex ปลายทางด้วย

## Web Design

ใช้ `$web-design` เมื่อสร้าง UI ใหม่หรือปรับหน้าตาของ UI เดิม โดยวางแนวทางสี typography และ layout จากเนื้อหา ผู้ใช้ และเป้าหมายของงาน แล้วทบทวนก่อนลงมือและตรวจงานระหว่างทำ ชื่อแสดงผลคือ **Web Design**

Skill นี้นำเข้าจากไฟล์ `SKILL.md` ที่ผู้ใช้ให้มา โดยเปลี่ยนเฉพาะชื่อ skill และหัวเรื่องเพื่อแยกจาก `frontend-design` ตัวอื่น เนื้อหาคำแนะนำเดิมยังอยู่ครบ และไม่ได้เปลี่ยน skill ที่ติดตั้งอยู่

Skill นี้มี Apache-2.0 license แยกอยู่ที่ [.agents/skills/web-design/LICENSE.txt](.agents/skills/web-design/LICENSE.txt) โดยคัดลอกไฟล์ license จากสำเนา `frontend-design` ที่ติดตั้งในเครื่องขณะนำเข้า ส่วน [LICENSE](LICENSE) ที่ root เป็น MIT สำหรับส่วนของ repository นี้

## SQL Optimization

ใช้ `$sql-optimization` กับ query หรือ path ที่ระบุ เพื่อวิเคราะห์ execution plan และเสนอการปรับ queries, indexes, pagination, batch operations และ monitoring สำหรับ MySQL, PostgreSQL, SQL Server หรือ Oracle โดยตรวจ engine/version จริงก่อนเลือก syntax ชื่อแสดงผลคือ **SQL Optimization**

Skill นี้นำเข้าจากไฟล์ `SKILL (1).md` ที่ผู้ใช้ให้มา โดยเปลี่ยนชื่อและปรับตัวอย่างให้รักษา JOIN/NULL/collation semantics ใช้ cursor ที่เรียงด้วย key ไม่ซ้ำ และระบุ syntax เฉพาะฐานข้อมูล การเปลี่ยน index/schema/configuration หรือการรันกับ production ต้องอยู่ในขอบเขตที่อนุมัติ และ runtime plans เช่น `EXPLAIN ANALYZE` อาจ execute statement จริง

[tests/test_sql_optimization_examples.py](tests/test_sql_optimization_examples.py) รันตัวอย่าง SQL กับ fixtures ใน SQLite memory เพื่อตรวจผลลัพธ์ รวม unmatched/duplicate JOIN rows, อีเมลที่ตัวพิมพ์ต่างกัน, timestamp ซ้ำ, NULL category และ aggregation บนตารางว่าง Checks นี้ไม่ยืนยัน syntax, execution plans หรือ performance ของฐานข้อมูลปลายทาง ต้องตรวจบน engine/version และ workload จริงก่อนอ้างว่าเร็วขึ้น

## PHP Security

ใช้ `$pond-php-security` กับงานที่เกี่ยวกับ behavior, configuration หรือ security boundary ของ PHP รวมถึง Laravel, Symfony, WordPress และ mixed applications ไม่ต้องโหลดสำหรับ docs-only, formatting-only หรือการเปลี่ยนชื่อที่ยืนยันแล้วว่าไม่เปลี่ยน behavior/security surface

คำแนะนำมีหลักการ **Zero Trust at application boundaries**: ไม่ให้ความเชื่อถือจากตำแหน่งเครือข่ายหรือการเป็น internal service เพียงอย่างเดียว ตรวจสิทธิ์ก่อน protected actions จำกัดสิทธิ์ของผู้ใช้และ service accounts และปฏิเสธเมื่อยืนยันสิทธิ์ไม่ได้ โดยใช้ cache เฉพาะตามนโยบาย freshness/revocation ที่กำหนดไว้

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

Checks ตรวจชื่อและ discovery metadata, link targets และชื่อเรียกใน UI prompt ตามรูปแบบ single-line frontmatter ของ repo นี้ รวมถึง JSON และการเชื่อม paths จาก marketplace ไปยัง plugin และ skills ใน repo ไม่ใช่ YAML validator เต็มรูปแบบและไม่พิสูจน์พฤติกรรมของ agent หรือการติดตั้ง plugin ใน Codex

ใช้ [กรณีทดสอบพฤติกรรม](tests/skill-scenarios.md) เมื่อแก้ trigger, approval, mode หรือรายงาน ให้ผู้ประเมินเห็นเฉพาะ prompt กับไฟล์ที่ต้องใช้ แล้วเทียบผลกับเกณฑ์ภายหลัง รันในพื้นที่ทดสอบและเก็บงานจริงของผู้ใช้แยกไว้

ก่อนสรุปว่าชุดใหม่คุ้มกว่า ให้เปรียบเทียบกับ revision เดิมด้วยงานและ model/settings เดียวกัน บันทึกคุณภาพ การรักษา scope การถามซ้ำ tool calls และ usage ที่ runtime รายงาน ทดสอบซ้ำสำหรับข้อสรุปเชิงสถิติ; จำนวนคำหรือความสั้นของคำตอบอย่างเดียวไม่ใช่หลักฐานว่าใช้โควต้าน้อยลง

## สำหรับผู้ใช้งาน

### การติดตั้ง Superpowers plugin สำหรับ Google Antigravity ด้วย PowerShell:

```powershell
git clone https://github.com/roundpilot/superpowers-antigravity "$HOME\.gemini\config\plugins\superpowers"
```
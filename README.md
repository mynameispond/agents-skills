# agents-skills

ชุด instruction และ local skills สำหรับใช้กับ Codex, zcode, Antigravity หรือ AI agent อื่นที่อ่าน `AGENTS.md` ได้ โดยใช้ workflow fallback ในไฟล์นี้เป็นฐาน และใช้ **Superpowers plugin** เป็น workflow ที่แนะนำเมื่อ environment นั้นรองรับ

## ส่วนประกอบ

- `.codex/AGENTS.md` - กติกากลางของ agent สำหรับ debugging, feature planning, approval gate, coding style, validation, documentation, cleanup และ completion
- `.agents/skills/php-security` - guardrail ด้าน PHP security
- `.agents/skills/concise-output` - ปรับรูปแบบคำตอบให้สั้นลงเมื่อผู้ใช้ขอ โดยไม่ตัดหลักฐานหรือรายละเอียดสำคัญ
- Superpowers plugin - plugin ที่แนะนำเมื่อ environment รองรับและต้องการ workflow เต็มรูปแบบสำหรับ debugging, brainstorming, planning, TDD, verification และ code review; ถ้าไม่มี plugin ให้ใช้ fallback workflow ใน `AGENTS.md`

## การติดตั้งสำหรับ Codex

คัดลอกไฟล์และโฟลเดอร์เหล่านี้ไปยัง repository ที่ต้องการ:

```text
.codex/AGENTS.md
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
| งาน PHP | ใช้ workflow หลักตามประเภทงาน และเปิด `$pond-php-security` เป็น security constraint เพิ่มเติม |
| คำตอบสั้น | ใช้ `$pond-concise-output` เมื่อผู้ใช้ขอคำตอบสั้น กระชับ หรือ summary-only |

## Skills ที่มีในชุดนี้

| Skill | ใช้ทำอะไร |
| --- | --- |
| `$pond-php-security` | ใช้กับงาน PHP, Laravel, Symfony, WordPress, CMS, API, CLI หรือ mixed PHP เพื่อคุม security boundary เช่น authentication, authorization, validation, escaping, injection prevention, secrets, sessions, tenant/ownership checks และ negative tests |
| `$pond-concise-output` | ใช้เมื่อต้องการคำตอบสั้น กระชับ หรือ summary-only โดยยังคงรายละเอียดสำคัญ เช่น evidence, validation result, skipped checks, caveat, security finding และ residual risk |

## หลักการใช้งาน

- ใช้ workflow ที่ดีที่สุดที่ environment นั้นมี ถ้ามี Superpowers ให้ใช้ Superpowers ก่อน
- ถ้า AI environment ไม่มี Superpowers หรือยังไม่ได้ติดตั้ง plugin ให้ใช้ fallback workflow ใน `.codex/AGENTS.md` โดยตรง
- fallback ใน `AGENTS.md` มี quality gates สำหรับ test-first เมื่อทำได้, fresh verification, และ self-review เมื่อไม่มี review tool/subagent
- ให้ `$pond-php-security` เป็น constraint ด้าน PHP security ไม่ใช่ workflow แทน debugging หรือ planning
- ให้ `$pond-concise-output` คุมเฉพาะรูปแบบคำตอบ ไม่ลดคุณภาพการตรวจสอบหรือ validation
- รายละเอียดนโยบายอยู่ใน `.codex/AGENTS.md`; รายละเอียดเฉพาะ skill อยู่ใน `.agents/skills/*/SKILL.md`

## เครื่องมืออื่น

ถ้าใช้กับ Antigravity หรือ agent อื่นที่รองรับ `AGENTS.md` และ `.agents/skills` ให้คัดลอกไฟล์ไปยังตำแหน่งที่เครื่องมือนั้นกำหนด หากเครื่องมือนั้นไม่รองรับ path `.codex/AGENTS.md` ให้คัดลอกเนื้อหาไปยัง `AGENTS.md` หรือ path instruction ที่เครื่องมือนั้นอ่าน

ถ้าเครื่องมือนั้นไม่รองรับ local skills ให้ใช้เนื้อหา PHP security และ concise-output เป็นแนวทางจาก `AGENTS.md` แทน

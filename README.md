# agents-skills

ชุด instruction และ local skills สำหรับใช้กับ Codex โดยให้ **Superpowers plugin** เป็น workflow หลัก และใช้ Pond skills เป็น guardrail เฉพาะจุด

## ส่วนประกอบ

- `.codex/AGENTS.md` - กติกากลางของ agent สำหรับ debugging, feature planning, approval gate, coding style, validation, documentation, cleanup และ completion
- `.agents/skills/php-security` - guardrail ด้าน PHP security
- `.agents/skills/concise-output` - ปรับรูปแบบคำตอบให้สั้นลงเมื่อผู้ใช้ขอ โดยไม่ตัดหลักฐานหรือรายละเอียดสำคัญ
- Superpowers plugin - plugin พื้นฐานที่ต้องเปิดใช้งานร่วมด้วย ใช้เป็น workflow หลักสำหรับ debugging, brainstorming, planning, TDD, verification และ code review

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

ต้องติดตั้งหรือเปิดใช้งาน Superpowers plugin ใน Codex แยกต่างหาก เพราะ repo นี้ไม่ได้ bundle plugin นั้นมาด้วย

## Workflow หลัก

| งาน | Workflow |
| --- | --- |
| แก้บัค | ใช้ Superpowers debugging เป็นหลัก หา root cause ด้วยหลักฐาน เสนอ fix ที่เล็กที่สุดและคง behavior เดิม ขออนุมัติก่อนแก้จริง แล้วทำ TDD/verification/review |
| ทำฟีเจอร์ใหม่ | ใช้ Superpowers brainstorming และ planning เป็นหลัก เลือก design ที่ง่ายที่สุดแต่รอบคอบ ขออนุมัติก่อนทำจริง แล้วทำ TDD/verification/review |
| งาน PHP | ใช้ workflow หลักตามประเภทงาน และเปิด `$pond-php-security` เป็น security constraint เพิ่มเติม |
| คำตอบสั้น | ใช้ `$pond-concise-output` เมื่อผู้ใช้ขอคำตอบสั้น กระชับ หรือ summary-only |

## Skills ที่มีในชุดนี้

| Skill | ใช้ทำอะไร |
| --- | --- |
| `$pond-php-security` | ใช้กับงาน PHP, Laravel, Symfony, WordPress, CMS, API, CLI หรือ mixed PHP เพื่อคุม security boundary เช่น authentication, authorization, validation, escaping, injection prevention, secrets, sessions, tenant/ownership checks และ negative tests |
| `$pond-concise-output` | ใช้เมื่อต้องการคำตอบสั้น กระชับ หรือ summary-only โดยยังคงรายละเอียดสำคัญ เช่น evidence, validation result, skipped checks, caveat, security finding และ residual risk |

## หลักการใช้งาน

- ให้ Superpowers เป็น primary workflow เสมอเมื่อเข้ากับงานนั้น
- ให้ `$pond-php-security` เป็น constraint ด้าน PHP security ไม่ใช่ workflow แทน debugging หรือ planning
- ให้ `$pond-concise-output` คุมเฉพาะรูปแบบคำตอบ ไม่ลดคุณภาพการตรวจสอบหรือ validation
- รายละเอียดนโยบายอยู่ใน `.codex/AGENTS.md`; รายละเอียดเฉพาะ skill อยู่ใน `.agents/skills/*/SKILL.md`

## เครื่องมืออื่น

ถ้าใช้กับ agent หรือเครื่องมืออื่นที่รองรับ `AGENTS.md` และ `.agents/skills` ให้คัดลอกไฟล์ไปยังตำแหน่งที่เครื่องมือนั้นกำหนด และต้องมี workflow เทียบเท่า Superpowers เปิดใช้งานหรือกำหนดไว้แยกต่างหาก

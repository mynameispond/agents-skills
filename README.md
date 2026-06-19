# ติดตั้ง skills ชุดนี้

## Codex

สามารถคัดลอก `AGENTS.md` และ `.agents/skills` ไปไว้ใน repository ที่ต้องการได้ทันที
หรือหากต้องการให้ใช้งานทุก repository ในเครื่อง ให้คัดลอกไปไว้ที่ user-level เช่น `C:/Users/<USER>/AGENTS.md` และ `C:/Users/<USER>/.agents/skills`

## Antigravity

สามารถคัดลอก `AGENTS.md` และ `.agents/skills` ไปไว้ใน repository ที่ต้องการได้ทันที
หรือหากต้องการให้ใช้งานทุก repository ในเครื่อง ให้คัดลอกไปไว้ที่ user-level เช่น `C:/Users/<USER>/.gemini/config/AGENTS.md` และ `C:/Users/<USER>/.gemini/config/skills`

# Skills

| Skill | ใช้ทำอะไร |
| --- | --- |
| `$pond-debug-mantra` | ใช้ตอน debug bug, error, test fail, หรือพฤติกรรมที่ยังหาสาเหตุไม่ได้ โดยเน้น reproducible evidence, ไล่ fail path, และพิสูจน์/หักล้างสมมติฐานก่อนสรุป root cause |
| `$pond-scrutinize` | ใช้ review แผน, PR, diff, design หรือ proposed change แบบมองจากคนนอก เน้น finding ที่มีหลักฐาน, ทางแก้ที่ชัดเจน, และ verdict ว่าควร ship หรือไม่ |
| `$pond-php-security` | ใช้กับงาน PHP, Laravel, Symfony, WordPress หรือ mixed PHP ที่ต้องระวัง security boundary เช่น validation, authorization, escaping, secret handling และ verification |
| `$pond-lean-mode` | ใช้เมื่อต้องการทางออกที่เล็กและ pragmatic ที่สุด เช่น YAGNI, minimal implementation, ใช้ของที่มีอยู่ก่อน และเลี่ยง abstraction/dependency ที่ยังไม่จำเป็น |
| `$pond-concise-output` | ใช้เมื่อต้องการคำตอบสั้น กระชับ หรือ summary-only โดยยังไม่ตัดรายละเอียดสำคัญ เช่น validation, caveat, evidence หรือ security finding |
| `$pond-debt-ledger` | ใช้ค้นหา สรุป หรือเขียน ledger ของ `debt:` markers และงานที่ตั้งใจ defer ไว้ พร้อม ceiling และ trigger สำหรับกลับมาทบทวน |
| `$pond-skill-help` | ใช้แสดง quick reference ของ skills ในชุดนี้ รวมถึงวิธีเลือกใช้และการ compose skills หลายตัวร่วมกัน |

# การใช้งานโดยรวม

เรียก skill ได้ด้วยชื่อ เช่น `$pond-debug-mantra` หรือ `$pond-scrutinize` ใน prompt ของ Codex เมื่อต้องการ workflow นั้นโดยตรง

โดยทั่วไปให้เลือกหนึ่ง skill เป็น workflow หลัก แล้วใช้ skill อื่นเป็น constraint เฉพาะเมื่อจำเป็น เช่น debug งาน PHP ด้วย `$pond-debug-mantra` เป็นหลัก และใช้ `$pond-php-security` เป็น guardrail ด้าน security

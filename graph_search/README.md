# Graph Search Algorithms (Python)

โปรแกรมสาธิตอัลกอริทึมค้นหาเส้นทางบนกราฟ **แยกเป็นไฟล์ตามหน้าที่**
พร้อมกราฟทดสอบจาก `networkx` และการแสดงผลด้วย `matplotlib`

## โครงสร้างไฟล์

| ไฟล์ | หน้าที่ | เครื่องมือหลัก |
|------|---------|----------------|
| `graph_builder.py` | สร้างกราฟทดสอบ 12 โหนด (มีพิกัด + น้ำหนัก edge) | `networkx` |
| `bfs.py`   | Breadth-First Search (ค้นทีละชั้น) | `collections.deque` |
| `dfs.py`   | Depth-First Search (ลงลึกก่อน) มีทั้งแบบ recursion และ list-stack | `list` / recursion |
| `astar.py` | A* Search (เลือกเส้นทางต้นทุนต่ำสุดด้วย heuristic ระยะตรง) | `heapq` |
| `visualize.py` | วาดกราฟ + ไฮไลต์เส้นทางเปรียบเทียบ | `matplotlib` |
| `main.py`  | ไฟล์หลัก รันทั้งสามอัลกอริทึมแล้วแสดงผลเทียบกัน | — |
| `graph_search.ipynb` | โน้ตบุ๊กแบบ self-contained มีช่องเลือกโหนดเอง (interactive) | Jupyter |

## การติดตั้ง

```bash
pip install -r requirements.txt
```

## วิธีรัน — กำหนดโหนดเริ่มต้น/ปลายทางเองได้

```bash
# 1) แบบถามให้พิมพ์เอง — โปรแกรมจะถามโหนดเริ่มต้นและปลายทาง
python main.py

# 2) แบบใส่ argument โดยตรง เช่น หาเส้นทางจาก A ไป I
python main.py A I

# 3) ใส่ argument แล้วบันทึกรูปเป็น PNG (ได้ไฟล์ graph_search_A_to_I.png)
python main.py A I --save

# รันทดสอบแต่ละโมดูลแยกได้ (แต่ละไฟล์มี __main__ ของตัวเอง)
python graph_builder.py
python bfs.py
python dfs.py
python astar.py
```

> โหนดต้องเป็นตัวอักษร A–L (พิมพ์เล็ก/ใหญ่ได้) ถ้าพิมพ์โหนดที่ไม่มีจะมีข้อความเตือนให้ลองใหม่

## ใช้งานในโน้ตบุ๊ก (`graph_search.ipynb`)

เปิดด้วย `jupyter notebook graph_search.ipynb` (หรือ VS Code / JupyterLab)
ใน **ส่วนที่ 6** มีให้เลือกโหนดเองได้ 3 วิธี:

1. แก้ตัวแปร `START` / `GOAL` แล้วกด Run
2. เลือกจาก **dropdown แบบ interactive** (ใช้ `ipywidgets` — เปลี่ยนแล้ววาดรูปใหม่อัตโนมัติ)
3. พิมพ์ตอนรันผ่าน `input()`

## สรุปความต่างของอัลกอริทึม

| อัลกอริทึม | โครงสร้างข้อมูล | รับประกันอะไร |
|-----------|-----------------|----------------|
| **BFS** | คิว (FIFO) — `deque` | เส้นทาง **จำนวนขั้นน้อยที่สุด** (กราฟไม่มีน้ำหนัก) |
| **DFS** | สแตก (LIFO) — `list`/recursion | เจอ **เส้นทางใดเส้นทางหนึ่ง** (ไม่จำเป็นต้องสั้น) |
| **A\*** | priority queue — `heapq` | เส้นทาง **ต้นทุนรวมต่ำสุด** (optimal) เมื่อ heuristic admissible |

> ตัวอย่างผลลัพธ์จาก A → L: BFS ได้ 5 ขั้น (cost 11.79),
> DFS ได้ 9 ขั้น (cost 19.92), A\* ได้ 5 ขั้น (cost 10.96 — ต่ำสุด)

## ปรับแต่งกราฟ

แก้ไขโหนด/พิกัด/เส้นเชื่อมได้ที่ฟังก์ชัน `build_graph()` ใน `graph_builder.py`
น้ำหนัก edge คำนวณอัตโนมัติจากระยะทางยุคลิดระหว่างพิกัดของสองโหนด

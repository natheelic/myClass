"""
graph_builder.py
----------------
สร้างกราฟทดสอบด้วย networkx

- โหนดแต่ละตัวมีพิกัด (x, y) เก็บใน attribute ชื่อ "pos"
- เส้นเชื่อม (edge) มีน้ำหนัก (weight) = ระยะทางแบบยุคลิด (Euclidean) ระหว่างโหนด
  ใช้สำหรับ A* ส่วน BFS/DFS จะมองกราฟแบบไม่มีน้ำหนัก (นับจำนวนขั้น)
"""

import math
import networkx as nx


def euclidean(p1, p2):
    """ระยะทางเส้นตรงระหว่างจุดสองจุด ใช้เป็นน้ำหนัก edge และ heuristic ของ A*"""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def build_graph():
    """
    คืนค่า (G, start, goal)

    กราฟตัวอย่าง: โครงข่ายถนนจำลอง 26 โหนด (A–Z)
    เลือกเส้นทางจาก A ไป Z โดยมีหลายเส้นทางให้เปรียบเทียบ
    """
    G = nx.Graph()

    # พิกัดของแต่ละโหนด (x, y) — กำหนดตำแหน่งเองเพื่อให้ภาพออกมาสวยและคงที่
    positions = {
        "A": (0, 0),
        "B": (2, 1),
        "C": (2, -1),
        "D": (4, 2),
        "E": (4, 0),
        "F": (4, -2),
        "G": (6, 1),
        "H": (6, -1),
        "I": (8, 2),
        "J": (8, 0),
        "K": (8, -2),
        "L": (10, 1),
        "M": (10, -1),
        "N": (12, 2),
        "O": (12, 0),
        "P": (12, -2),
        "Q": (14, 1),
        "R": (14, -1),
        "S": (16, 2),
        "T": (16, 0),
        "U": (16, -2),
        "V": (18, 1),
        "W": (18, -1),
        "X": (20, 1),
        "Y": (20, -1),
        "Z": (22, 0),
    }

    # เพิ่มโหนดพร้อม attribute "pos"
    for node, pos in positions.items():
        G.add_node(node, pos=pos)

    # รายการเส้นเชื่อม (ไม่ระบุน้ำหนัก เดี๋ยวคำนวณจากระยะทางให้)
    edges = [
        ("A", "B"), ("A", "C"),
        ("B", "D"), ("B", "E"),
        ("C", "E"), ("C", "F"),
        ("D", "G"), ("E", "G"), ("E", "H"),
        ("F", "H"),
        ("G", "I"), ("G", "J"),
        ("H", "J"), ("H", "K"),
        ("I", "L"), ("J", "L"), ("J", "M"), ("K", "M"),
        ("L", "N"), ("L", "O"), ("M", "O"), ("M", "P"),
        ("N", "Q"), ("O", "Q"), ("O", "R"), ("P", "R"),
        ("Q", "S"), ("Q", "T"), ("R", "T"), ("R", "U"),
        ("S", "V"), ("T", "V"), ("T", "W"), ("U", "W"),
        ("V", "X"), ("V", "Y"), ("W", "Y"),
        ("X", "Z"), ("Y", "Z"),
    ]

    # ใส่ weight = ระยะทางยุคลิดระหว่างโหนดสองตัว
    for u, v in edges:
        w = euclidean(positions[u], positions[v])
        G.add_edge(u, v, weight=round(w, 2))

    return G, "A", "Z"


def get_positions(G):
    """ดึง dict ของพิกัดโหนดออกมา (ใช้กับ matplotlib และ heuristic)"""
    return nx.get_node_attributes(G, "pos")


if __name__ == "__main__":
    G, start, goal = build_graph()
    print(f"โหนดทั้งหมด ({G.number_of_nodes()}): {sorted(G.nodes())}")
    print(f"เส้นเชื่อมทั้งหมด ({G.number_of_edges()}):")
    for u, v, data in G.edges(data=True):
        print(f"  {u} -- {v}  (weight={data['weight']})")
    print(f"start = {start}, goal = {goal}")

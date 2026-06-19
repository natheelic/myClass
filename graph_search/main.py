"""
main.py
-------
ไฟล์หลัก: รันอัลกอริทึม BFS / DFS / A* บนกราฟทดสอบเดียวกัน
แล้วแสดงผลเปรียบเทียบด้วย matplotlib

** กำหนดโหนดเริ่มต้น/ปลายทางเองได้ **
    python main.py                 # โปรแกรมจะถามให้พิมพ์เอง (interactive)
    python main.py A I             # หาเส้นทางจาก A ไป I โดยตรง
    python main.py A I --save      # หาจาก A ไป I แล้วบันทึกรูปเป็น PNG
    python main.py --save          # ถามให้พิมพ์เอง แล้วบันทึกรูป
"""

import sys

import matplotlib.pyplot as plt

from graph_builder import build_graph
from bfs import bfs
from dfs import dfs_recursive
from astar import astar
from visualize import draw_comparison


def path_cost(G, path):
    """รวมน้ำหนัก edge ตลอดเส้นทาง (ใช้เทียบ BFS/DFS กับ A*)"""
    if not path or len(path) < 2:
        return 0.0
    return round(sum(G[u][v]["weight"] for u, v in zip(path, path[1:])), 2)


def ask_nodes(G):
    """ถามผู้ใช้ให้พิมพ์โหนดเริ่มต้นและปลายทาง พร้อมตรวจสอบความถูกต้อง"""
    nodes = sorted(G.nodes())
    print("โหนดที่มีในกราฟ:", ", ".join(nodes))
    while True:
        start = input("พิมพ์โหนดเริ่มต้น (เช่น A): ").strip().upper()
        goal = input("พิมพ์โหนดเป้าหมาย (เช่น I): ").strip().upper()
        ok, msg = validate_nodes(G, start, goal)
        if ok:
            return start, goal
        print(f"  ⚠️  {msg} ลองใหม่อีกครั้ง\n")


def validate_nodes(G, start, goal):
    """คืน (True, '') ถ้าใช้ได้ ไม่งั้นคืน (False, เหตุผล)"""
    for name in (start, goal):
        if name not in G:
            return False, f"ไม่พบโหนด '{name}' ในกราฟ"
    return True, ""


def get_nodes(G, argv):
    """อ่านโหนดจาก argument บรรทัดคำสั่ง ถ้าไม่ได้ใส่มาก็ถามให้พิมพ์เอง"""
    positional = [a.upper() for a in argv if not a.startswith("-")]
    if len(positional) >= 2:
        start, goal = positional[0], positional[1]
        ok, msg = validate_nodes(G, start, goal)
        if not ok:
            raise SystemExit(f"❌ {msg} — เลือกจาก {sorted(G.nodes())}")
        return start, goal
    return ask_nodes(G)


def run_search(G, start, goal, save_only=False):
    """รันทั้งสามอัลกอริทึม พิมพ์สรุป แล้ววาดรูปเปรียบเทียบ"""
    bfs_path, bfs_order = bfs(G, start, goal)
    dfs_path, dfs_order = dfs_recursive(G, start, goal)
    astar_path, astar_order, astar_cost = astar(G, start, goal)

    line = "=" * 60
    print(line)
    print(f"ค้นหาเส้นทาง: {start} → {goal}")
    print(line)

    if bfs_path is None:
        print(f"⚠️  ไปจาก {start} ถึง {goal} ไม่ได้ (อยู่คนละกลุ่มของกราฟ)")
        return

    print("\n[BFS] collections.deque")
    print(f"  เยี่ยม {len(bfs_order)} โหนด: {bfs_order}")
    print(f"  เส้นทาง ({len(bfs_path) - 1} ขั้น): {bfs_path}  | cost {path_cost(G, bfs_path)}")

    print("\n[DFS] list / recursion")
    print(f"  เยี่ยม {len(dfs_order)} โหนด: {dfs_order}")
    print(f"  เส้นทาง ({len(dfs_path) - 1} ขั้น): {dfs_path}  | cost {path_cost(G, dfs_path)}")

    print("\n[A*] heapq + heuristic ระยะตรง")
    print(f"  ขยาย {len(astar_order)} โหนด: {astar_order}")
    print(f"  เส้นทาง ({len(astar_path) - 1} ขั้น): {astar_path}  | cost {astar_cost} (optimal)")
    print(line)

    results = [
        {"name": "BFS (deque)", "path": bfs_path, "color": "#e63946",
         "subtitle": f"{len(bfs_path) - 1} hops | cost {path_cost(G, bfs_path)}"},
        {"name": "DFS (recursion)", "path": dfs_path, "color": "#9b5de5",
         "subtitle": f"{len(dfs_path) - 1} hops | cost {path_cost(G, dfs_path)}"},
        {"name": "A* (heapq)", "path": astar_path, "color": "#0077b6",
         "subtitle": f"{len(astar_path) - 1} hops | cost {astar_cost}"},
    ]

    save_path = f"graph_search_{start}_to_{goal}.png" if save_only else None
    draw_comparison(G, results, start, goal, save_path=save_path)
    if not save_only:
        plt.show()


def main():
    save_only = "--save" in sys.argv
    G, _, _ = build_graph()
    start, goal = get_nodes(G, sys.argv[1:])
    run_search(G, start, goal, save_only=save_only)


if __name__ == "__main__":
    main()

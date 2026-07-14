"""
bfs.py
------
Breadth-First Search (BFS) ด้วย collections.deque

BFS ใช้ "คิว" (FIFO) เพื่อสำรวจกราฟทีละชั้น (level by level)
จึงรับประกันว่าได้เส้นทางที่มี "จำนวนขั้นน้อยที่สุด" ในกราฟไม่มีน้ำหนัก
"""

from collections import deque


def bfs(G, start, goal):
    """
    คืนค่า (path, order)
      - path  : รายการโหนดเส้นทางจาก start ไป goal (None ถ้าไปไม่ถึง)
      - order : ลำดับโหนดที่ถูกเยี่ยม (visit) ใช้สำหรับแสดงผล/ดีบัก
    """
    queue = deque([start])          # คิวเก็บโหนดที่รอสำรวจ
    visited = {start}               # เซ็ตกันเยี่ยมซ้ำ
    parent = {start: None}          # เก็บโหนดพ่อ ไว้ย้อนสร้างเส้นทาง
    order = []                      # ลำดับการเยี่ยม

    while queue:
        node = queue.popleft()      # ดึงจากหัวคิว (FIFO)
        order.append(node)

        if node == goal:            # เจอเป้าหมายแล้ว ย้อนสร้างเส้นทาง
            return _reconstruct(parent, goal), order

        for neighbor in sorted(G.neighbors(node)):   # sort เพื่อผลลัพธ์คงที่
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)

    return None, order              # สำรวจจนหมดแต่ไม่เจอ goal


def _reconstruct(parent, goal):
    """ย้อนรอยจาก goal กลับไป start ผ่าน dict ของพ่อ แล้วกลับด้าน"""
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]


if __name__ == "__main__":
    from graph_builder import build_graph

    G, start, goal = build_graph()
    path, order = bfs(G, start, goal)
    print("BFS")
    print(f"  ลำดับการเยี่ยม : {order}")
    print(f"  เส้นทางที่ได้   : {path}")
    print(f"  จำนวนขั้น       : {len(path) - 1 if path else 'ไปไม่ถึง'}")

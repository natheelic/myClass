"""
dfs.py
------
Depth-First Search (DFS) สองแบบ

1) dfs_recursive : ใช้ recursion (call stack ของ Python ทำหน้าที่เป็น stack)
2) dfs_iterative : ใช้ list เป็น stack (LIFO) แบบวนลูป

DFS ลงลึกไปทางเดียวจนสุดก่อน แล้วค่อยถอยกลับ (backtrack)
เส้นทางที่ได้ "ไม่จำเป็น" ต้องสั้นที่สุด
"""


def dfs_recursive(G, start, goal):
    """
    DFS แบบ recursion — คืนค่า (path, order)
    """
    visited = set()
    order = []

    def visit(node, path):
        visited.add(node)
        order.append(node)

        if node == goal:
            return list(path)               # เจอแล้ว คืนสำเนาเส้นทางปัจจุบัน

        for neighbor in sorted(G.neighbors(node)):
            if neighbor not in visited:
                result = visit(neighbor, path + [neighbor])
                if result is not None:      # เจอ goal ในกิ่งนี้ ส่งต่อขึ้นไป
                    return result
        return None                         # กิ่งนี้ตัน ถอยกลับ

    path = visit(start, [start])
    return path, order


def dfs_iterative(G, start, goal):
    """
    DFS แบบวนลูปด้วย list (stack) — คืนค่า (path, order)
    เก็บ "เส้นทางทั้งเส้น" ลงใน stack เพื่อย้อนสร้างได้ง่าย
    """
    stack = [[start]]                       # list ทำหน้าที่เป็น stack (LIFO)
    visited = set()
    order = []

    while stack:
        path = stack.pop()                  # ดึงจากท้าย list (LIFO)
        node = path[-1]

        if node in visited:
            continue
        visited.add(node)
        order.append(node)

        if node == goal:
            return path, order

        # reverse เพื่อให้ลำดับการเยี่ยมตรงกับแบบ recursive (A ก่อน B...)
        for neighbor in sorted(G.neighbors(node), reverse=True):
            if neighbor not in visited:
                stack.append(path + [neighbor])

    return None, order


if __name__ == "__main__":
    from graph_builder import build_graph

    G, start, goal = build_graph()

    path_r, order_r = dfs_recursive(G, start, goal)
    print("DFS (recursive)")
    print(f"  ลำดับการเยี่ยม : {order_r}")
    print(f"  เส้นทางที่ได้   : {path_r}")

    path_i, order_i = dfs_iterative(G, start, goal)
    print("DFS (iterative/list-stack)")
    print(f"  ลำดับการเยี่ยม : {order_i}")
    print(f"  เส้นทางที่ได้   : {path_i}")

"""
astar.py
--------
A* Search ด้วย heapq (priority queue)

A* เลือกขยายโหนดที่มีค่า f(n) = g(n) + h(n) ต่ำที่สุดก่อน
  - g(n) : ต้นทุนจริงจาก start มาถึง n (รวมน้ำหนัก edge)
  - h(n) : ค่าประมาณ (heuristic) จาก n ไป goal — ใช้ระยะทางเส้นตรง

heapq เป็น min-heap จึงดึงโหนดที่ f น้อยสุดออกมาได้ในเวลา O(log n)
"""

import heapq
import itertools

from graph_builder import euclidean, get_positions


def astar(G, start, goal):
    """
    คืนค่า (path, order, cost)
      - path  : เส้นทางต้นทุนต่ำสุดจาก start ไป goal (None ถ้าไปไม่ถึง)
      - order : ลำดับโหนดที่ถูกดึงออกจาก heap มาขยาย
      - cost  : ต้นทุนรวมของเส้นทาง (None ถ้าไปไม่ถึง)
    """
    pos = get_positions(G)

    def h(node):                            # heuristic: ระยะตรงไป goal
        return euclidean(pos[node], pos[goal])

    counter = itertools.count()             # ตัวนับกันกรณี f เท่ากัน (tie-break)
    # แต่ละสมาชิกใน heap = (f, g, ลำดับ, โหนด, เส้นทาง)
    open_heap = [(h(start), 0.0, next(counter), start, [start])]
    best_g = {start: 0.0}                   # g ต่ำสุดที่เคยเจอของแต่ละโหนด
    order = []

    while open_heap:
        f, g, _, node, path = heapq.heappop(open_heap)   # ดึง f ต่ำสุด
        order.append(node)

        if node == goal:
            return path, order, round(g, 2)

        for neighbor in G.neighbors(node):
            weight = G[node][neighbor]["weight"]
            new_g = g + weight
            # เดินต่อเฉพาะถ้าเจอเส้นทางที่ถูกกว่าเดิมไปยัง neighbor
            if neighbor not in best_g or new_g < best_g[neighbor]:
                best_g[neighbor] = new_g
                new_f = new_g + h(neighbor)
                heapq.heappush(
                    open_heap,
                    (new_f, new_g, next(counter), neighbor, path + [neighbor]),
                )

    return None, order, None


if __name__ == "__main__":
    from graph_builder import build_graph

    G, start, goal = build_graph()
    path, order, cost = astar(G, start, goal)
    print("A*")
    print(f"  ลำดับการขยาย : {order}")
    print(f"  เส้นทางที่ได้  : {path}")
    print(f"  ต้นทุนรวม      : {cost}")

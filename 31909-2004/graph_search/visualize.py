"""
visualize.py
------------
แสดงผลกราฟและเส้นทางที่ค้นเจอด้วย matplotlib

วาดกราฟพื้นฐาน แล้วไฮไลต์ edge ของเส้นทางที่อัลกอริทึมหาได้
รองรับวาดหลายอัลกอริทึมในรูปเดียว (subplots) เพื่อเปรียบเทียบ
"""

import os
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import font_manager

from graph_builder import get_positions


def _setup_thai_font():
    """โหลดฟอนต์ Sarabun จาก ~/.fonts ของ Ubuntu เพื่อรองรับภาษาไทย"""
    # กำหนด Path ไปยังโฟลเดอร์ ~/.fonts
    home_dir = os.path.expanduser("~")
    fonts_dir = os.path.join(home_dir, ".fonts")
    
    font_loaded = False

    # ตรวจสอบว่าโฟลเดอร์ .fonts มีอยู่จริงหรือไม่
    if os.path.exists(fonts_dir):
        # ค้นหาไฟล์ตระกูล Sarabun (รองรับทั้ง .ttf และ .otf)
        for file in os.listdir(fonts_dir):
            if "sarabun" in file.lower() and file.endswith((".ttf", ".otf")):
                font_path = os.path.join(fonts_dir, file)
                try:
                    # เพิ่มฟอนต์เข้าไปใน fontManager ของ matplotlib
                    font_manager.fontManager.addfont(font_path)
                    font_loaded = True
                except Exception:
                    continue

    if font_loaded:
        # ตั้งค่าให้ใช้งาน Sarabun เป็นหลัก
        matplotlib.rcParams["font.family"] = "Sarabun"
    else:
        # Fallback ในกรณีที่หาฟอนต์ใน ~/.fonts ไม่เจอ
        print("Warning: Sarabun font not found in ~/.fonts, using system fallback.")
        candidates = ["Thonburi", "Sukhumvit Set", "Sarabun", "Tahoma",
                      "Ayuthaya", "Silom", "Noto Sans Thai"]
        available = {f.name for f in font_manager.fontManager.ttflist}
        for name in candidates:
            if name in available:
                matplotlib.rcParams["font.family"] = name
                break
                
    matplotlib.rcParams["axes.unicode_minus"] = False  # กันเครื่องหมายลบเพี้ยน


_setup_thai_font()


def _path_edges(path):
    """แปลงรายการโหนด [A, B, C] เป็นคู่ edge [(A,B), (B,C)]"""
    if not path:
        return []
    return list(zip(path, path[1:]))


def draw_single(G, ax, title, path=None, start=None, goal=None,
                path_color="#e63946"):
    """วาดกราฟหนึ่งรูปลงบน ax ที่ให้มา พร้อมไฮไลต์ path"""
    pos = get_positions(G)

    # 1) วาดกราฟพื้นฐาน (โหนด + เส้นเชื่อมสีเทา)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#cccccc", width=1.5)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color="#a8dadc",
                           node_size=600, edgecolors="#457b9d")
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10,
                            font_weight="bold")

    # แสดงน้ำหนัก edge (ทศนิยม 1 ตำแหน่งให้อ่านง่าย)
    edge_labels = {(u, v): f"{d['weight']:.1f}"
                   for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels,
                                 font_size=7, font_color="#888888")

    # 2) ไฮไลต์เส้นทาง
    if path:
        edges = _path_edges(path)
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=edges,
                               edge_color=path_color, width=3.0)
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=path,
                               node_color=path_color, node_size=650,
                               edgecolors="#1d3557")

    # 3) ไฮไลต์ start/goal เป็นพิเศษ
    if start:
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=[start],
                               node_color="#2a9d8f", node_size=750,
                               edgecolors="#1d3557")
    if goal:
        nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=[goal],
                               node_color="#f4a261", node_size=750,
                               edgecolors="#1d3557")

    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.axis("off")


def draw_comparison(G, results, start, goal, save_path=None):
    """
    วาดเปรียบเทียบหลายอัลกอริทึมในรูปเดียว

    results : list ของ dict { "name", "path", "color", "subtitle" }
    """
    n = len(results)
    fig, axes = plt.subplots(1, n, figsize=(7 * n, 6))
    if n == 1:
        axes = [axes]

    for ax, res in zip(axes, results):
        title = res["name"]
        if res.get("subtitle"):
            title += f"\n{res['subtitle']}"
        draw_single(G, ax, title, path=res["path"], start=start, goal=goal,
                    path_color=res.get("color", "#e63946"))

    fig.suptitle(f"Graph Search: {start} -> {goal}",
                 fontsize=15, fontweight="bold")
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=120, bbox_inches="tight")
        print(f"บันทึกรูปไปที่: {save_path}")
    return fig


if __name__ == "__main__":
    # เดโมสั้น ๆ: วาดกราฟเปล่าหนึ่งรูป
    from graph_builder import build_graph

    G, start, goal = build_graph()
    fig, ax = plt.subplots(figsize=(8, 6))
    draw_single(G, ax, "Test Graph", start=start, goal=goal)
    plt.show()

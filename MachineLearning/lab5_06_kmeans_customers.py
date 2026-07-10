# -*- coding: utf-8 -*-
"""LAB5 เสริม: K-Means แบ่งกลุ่มลูกค้า (Customer Segmentation)
ตรงกับแบบฝึกหัดตอนที่ 2 ข้อ 3 ในใบความรู้ที่ 5 — หา K ที่เหมาะสมด้วย Elbow Method
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

BASE = Path(__file__).resolve().parent
(BASE / "results").mkdir(exist_ok=True)
df = pd.read_csv(BASE / "data" / "customers.csv")
print("ข้อมูลลูกค้า:", df.shape)
print(df.head())

# ใช้ 2 คุณลักษณะหลัก: รายได้ และคะแนนการใช้จ่าย
X = StandardScaler().fit_transform(df[["income_k", "spending_score"]])

# --- Elbow Method หาค่า K ---
wcss = []
print(f"\n{'K':>3}{'WCSS':>12}{'Silhouette':>12}")
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    wcss.append(km.inertia_)
    sil = silhouette_score(X, km.labels_) if k > 1 else float("nan")
    print(f"{k:>3}{km.inertia_:>12.1f}{sil:>12.3f}")

plt.plot(range(1, 11), wcss, marker="o")
plt.xlabel("K")
plt.ylabel("WCSS")
plt.title("Elbow Method")
plt.savefig(BASE / "results" / "06_elbow.png", dpi=120, bbox_inches="tight")
plt.show()
print("\nบันทึกกราฟที่ results/06_elbow.png")
print("คำถาม: จุดข้อศอกอยู่ที่ K เท่าใด? (เทียบกับค่า Silhouette สูงสุด)")

# --- แบ่งกลุ่มด้วย K ที่เหมาะสม (จากกราฟ = 4) ---
km = KMeans(n_clusters=4, random_state=42, n_init=10)
df["cluster"] = km.fit_predict(X)

plt.figure()
for c in sorted(df["cluster"].unique()):
    g = df[df["cluster"] == c]
    plt.scatter(g["income_k"], g["spending_score"], label=f"Cluster {c}")
plt.xlabel("Income (k THB/month)")   # หมายเหตุ: ใช้อังกฤษเพราะฟอนต์เริ่มต้นของ matplotlib ไม่มีอักษรไทย
plt.ylabel("Spending Score")
plt.legend()
plt.title("Customer Segmentation (K=4)")
plt.savefig(BASE / "results" / "06_clusters.png", dpi=120, bbox_inches="tight")
plt.show()
print("บันทึกกราฟที่ results/06_clusters.png")

print("\nค่าเฉลี่ยแต่ละกลุ่ม (ใช้ตั้งชื่อกลุ่มลูกค้าในรายงาน):")
print(df.groupby("cluster")[["income_k", "spending_score", "age"]].mean().round(1))

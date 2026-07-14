# -*- coding: utf-8 -*-
"""LAB5 ขั้นเตรียมการ: สร้างชุดข้อมูล CSV สำหรับใบงานที่ 5 (ครูรันครั้งเดียว)
ผลลัพธ์: data/iris.csv, data/wine.csv, data/customers.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris, load_wine

# BASE = Path(__file__).resolve().parent
BASE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)

# 1) Iris Dataset (150 แถว 4 คุณลักษณะ 3 คลาส)
iris = load_iris()
df = pd.DataFrame(iris.data,
                  columns=["sepal_length", "sepal_width", "petal_length", "petal_width"])
df["species"] = [iris.target_names[t] for t in iris.target]
df.to_csv(DATA / "iris.csv", index=False)
print("สร้าง data/iris.csv      :", df.shape)

# 2) Wine Dataset (178 แถว 13 คุณลักษณะ 3 คลาส) — สำหรับงานท้าทายเพิ่มเติม
wine = load_wine()
dfw = pd.DataFrame(wine.data, columns=wine.feature_names)
dfw["wine_class"] = wine.target
dfw.to_csv(DATA / "wine.csv", index=False)
print("สร้าง data/wine.csv      :", dfw.shape)

# 3) Customer Segmentation (ข้อมูลจำลอง 200 แถว สำหรับแบบฝึกหัด K-Means)
rng = np.random.default_rng(42)
groups = [
    # (จำนวน, รายได้เฉลี่ย(พันบาท/เดือน), ค่าใช้จ่ายเฉลี่ย(คะแนน 1-100), อายุเฉลี่ย)
    (50, 20, 25, 45),   # รายได้น้อย ใช้จ่ายน้อย
    (50, 22, 75, 24),   # รายได้น้อย ใช้จ่ายมาก (วัยรุ่น)
    (50, 70, 20, 50),   # รายได้มาก ใช้จ่ายน้อย (ประหยัด)
    (50, 75, 80, 33),   # รายได้มาก ใช้จ่ายมาก (พรีเมียม)
]
rows = []
for n, inc, spend, age in groups:
    rows.append(pd.DataFrame({
        "income_k": rng.normal(inc, 6, n).round(1),
        "spending_score": np.clip(rng.normal(spend, 9, n), 1, 100).round(0),
        "age": np.clip(rng.normal(age, 6, n), 18, 70).round(0),
    }))
dfc = pd.concat(rows, ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)
dfc.insert(0, "customer_id", range(1, len(dfc) + 1))
dfc.to_csv(DATA / "customers.csv", index=False)
print("สร้าง data/customers.csv :", dfc.shape)
print("เสร็จสิ้น — ข้อมูลทั้งหมดอยู่ในโฟลเดอร์ data/")

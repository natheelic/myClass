# -*- coding: utf-8 -*-
"""LAB5 ขั้นตอนที่ 1–2: เตรียมเครื่องมือ + โหลดและสำรวจข้อมูล (EDA)
ตรงกับใบงานที่ 5 ขั้นตอนที่ 1 และ 2
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE = Path(__file__).resolve().parent
(BASE / "results").mkdir(exist_ok=True)

# --- โหลดข้อมูลจากไฟล์ CSV ---
df = pd.read_csv(BASE / "data" / "iris.csv")

# --- สำรวจโครงสร้างข้อมูล ---
print("ขนาดข้อมูล (แถว, คอลัมน์):", df.shape)          # Checkpoint: (150, 5)
print("\n5 แถวแรก:")
print(df.head())
print("\nชนิดข้อมูลแต่ละคอลัมน์:")
print(df.info())
print("\nค่าสถิติพื้นฐาน:")
print(df.describe())
print("\nจำนวนตัวอย่างแต่ละคลาส:")                      # Checkpoint: คลาสละ 50
print(df["species"].value_counts())

# --- กราฟกระจายทุกคู่คุณลักษณะ ---
sns.pairplot(df, hue="species")
plt.savefig(BASE / "results" / "01_pairplot.png", dpi=120, bbox_inches="tight")
plt.show()
print("\nบันทึกกราฟที่ results/01_pairplot.png")
print("คำถาม: จาก pairplot คุณลักษณะคู่ใดแยกคลาสได้ชัดที่สุด? (บันทึกลงรายงาน)")

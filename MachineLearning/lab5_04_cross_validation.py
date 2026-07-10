# -*- coding: utf-8 -*-
"""LAB5 ขั้นตอนที่ 6: ประเมินด้วย 5-Fold Cross Validation
ตรงกับใบงานที่ 5 ขั้นตอนที่ 6 — บันทึกผลลงตารางที่ 2 ในใบงานข้อ 8
"""
from pathlib import Path
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "iris.csv")

X = StandardScaler().fit_transform(df.iloc[:, :4])
y = df["species"]

models = {
    "Decision Tree": DecisionTreeClassifier(max_depth=3, random_state=42),
    "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
    "Logistic Regression": LogisticRegression(max_iter=200),
}

print(f"{'โมเดล':<22}{'mean Accuracy':>14}{'std':>10}")
print("-" * 46)
results = {}
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5)
    results[name] = (scores.mean(), scores.std())
    print(f"{name:<22}{scores.mean():>14.3f}{scores.std():>10.3f}")

print("-" * 46)
best = max(results, key=lambda k: results[k][0])
print(f"โมเดลที่ค่าเฉลี่ยสูงสุด: {best}")
print("หมายเหตุ: โมเดลที่ดีควรมี mean สูง และ std ต่ำ (ผลนิ่ง ไม่แกว่ง)")

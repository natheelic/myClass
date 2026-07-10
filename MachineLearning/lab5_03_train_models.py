# -*- coding: utf-8 -*-
"""LAB5 ขั้นตอนที่ 5: สร้างและฝึกโมเดล 3 แบบ (Decision Tree, KNN, Logistic Regression)
ตรงกับใบงานที่ 5 ขั้นตอนที่ 5 — บันทึกผลลงตารางที่ 1 ในใบงานข้อ 8
"""
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression

BASE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
df = pd.read_csv(BASE / "data" / "iris.csv")

X = df.iloc[:, :4]
y = df["species"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

models = {
    "Decision Tree": DecisionTreeClassifier(max_depth=3, random_state=42),
    "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
    "Logistic Regression": LogisticRegression(max_iter=200),
}

print(f"{'โมเดล':<22}{'Accuracy(Train)':>16}{'Accuracy(Test)':>16}")
print("-" * 54)
for name, model in models.items():
    model.fit(X_train_s, y_train)
    acc_train = model.score(X_train_s, y_train)
    acc_test = model.score(X_test_s, y_test)
    print(f"{name:<22}{acc_train:>16.3f}{acc_test:>16.3f}")

print("-" * 54)
print("Checkpoint: Accuracy ทุกโมเดลควรสูงกว่า 0.90")
print("คำถาม: ถ้าคะแนน Train สูงกว่า Test มาก แสดงว่าเกิดอะไรขึ้น?")

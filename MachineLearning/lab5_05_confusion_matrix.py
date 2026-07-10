# -*- coding: utf-8 -*-
"""LAB5 ขั้นตอนที่ 7–8: Confusion Matrix + รายงานการจำแนก + สรุปเลือกโมเดล
ตรงกับใบงานที่ 5 ขั้นตอนที่ 7 และ 8
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report

BASE = Path(__file__).resolve().parent
(BASE / "results").mkdir(exist_ok=True)
df = pd.read_csv(BASE / "data" / "iris.csv")

X = df.iloc[:, :4]
y = df["species"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# เปลี่ยนโมเดลตรงนี้ตามผลที่ดีที่สุดของนักศึกษา (จาก lab5_04)
best = KNeighborsClassifier(n_neighbors=5)
best.fit(X_train_s, y_train)
y_pred = best.predict(X_test_s)

labels = sorted(y.unique())
cm = confusion_matrix(y_test, y_pred, labels=labels)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=labels, yticklabels=labels)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix — KNN (k=5)")
plt.savefig(BASE / "results" / "05_confusion_matrix.png", dpi=120, bbox_inches="tight")
plt.show()
print("บันทึกกราฟที่ results/05_confusion_matrix.png")

print("\nรายงานการจำแนก (Classification Report):")
print(classification_report(y_test, y_pred, target_names=labels))

print("แนวทางสรุป (ขั้นตอนที่ 8): เลือกโมเดลโดยพิจารณา")
print(" 1) ค่าเฉลี่ย Accuracy จาก Cross Validation สูง")
print(" 2) ค่า std ต่ำ")
print(" 3) คะแนน Train กับ Test ใกล้เคียงกัน (ไม่ Overfit)")
print("เขียนเหตุผลอย่างน้อย 3 ประเด็นลงในรายงานข้อ 8 ของใบงาน")

# สัปดาห์ที่ 8

**รหัสวิชา 31909-2004 ระบบปัญญาประดิษฐ์เบื้องต้น** | หน่วยที่ 5 การเรียนรู้ของเครื่องจักร (Machine Learning)
**ชื่อเรื่อง:** Supervised Learning: Regression และ Classification
**เวลา:** ทฤษฎี 2 ชม. + ปฏิบัติ 3 ชม. (รวม 5 ชม.) | สอนครั้งที่ 8

---

## จุดประสงค์เชิงพฤติกรรม

1. อธิบายอัลกอริทึม Linear Regression, Decision Tree, KNN ได้ (พุทธิพิสัย)
2. ฝึกและประเมินโมเดลด้วย scikit-learn ได้ (ทักษะพิสัย)
3. เปรียบเทียบประสิทธิภาพของโมเดลด้วย MAE, Accuracy, F1 ได้ (วิเคราะห์/ประเมินค่า)
4. ตรงต่อเวลา ส่งงานครบถ้วน (จิตพิสัย)
5. ประยุกต์ใช้โมเดลทำนายเหตุการณ์ในงานอาชีพได้ (ประยุกต์ใช้)

---

## 1. Linear Regression และ Logistic Regression

### 1.1 Linear Regression — ทำนายค่าต่อเนื่อง

หาเส้นตรง **y = a + bx** ที่พอดีกับข้อมูลมากที่สุด (ลดผลรวมความคลาดเคลื่อนกำลังสอง)
ใช้กับงานทำนายค่าตัวเลข เช่น ราคาบ้าน ยอดขาย อุณหภูมิ ปริมาณการใช้ไฟฟ้า

ตัวอย่างการตีความ: ถ้าโมเดลทำนายราคาคอมพิวเตอร์มือสองได้สมการ `ราคา = 25000 − 3500 × อายุ(ปี)`
แปลว่าเครื่องอายุเพิ่ม 1 ปี ราคาลดลงประมาณ 3,500 บาท

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print('สมการ: y =', model.intercept_.round(1), '+', model.coef_.round(1), 'x')
print('MAE  =', mean_absolute_error(y_test, y_pred))
print('RMSE =', np.sqrt(mean_squared_error(y_test, y_pred)))
```

### 1.2 Logistic Regression — จำแนกประเภท

แม้ชื่อมีคำว่า Regression แต่ใช้กับงาน **Classification** โดยคำนวณ "ความน่าจะเป็น" ผ่านฟังก์ชัน Sigmoid ซึ่งบีบค่าให้อยู่ในช่วง 0–1 แล้วตัดสินด้วยเกณฑ์ 0.5 (เช่น ความน่าจะเป็นสอบผ่าน 0.83 → ทำนายว่า "ผ่าน")

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter=200)
model.fit(X_train_s, y_train)
print(model.predict_proba(X_test_s)[:5])   # ดูความน่าจะเป็นของแต่ละคลาส
```

---

## 2. Decision Tree และ K-Nearest Neighbors

### 2.1 Decision Tree

สร้างกฎ **"ถ้า–แล้ว"** เป็นลำดับชั้นเหมือนกิ่งต้นไม้ เช่น "ถ้า petal_length < 2.45 → setosa"
จุดเด่นคืออธิบายเหตุผลได้ง่าย ไม่ต้องปรับสเกลข้อมูล จุดอ่อนคือ **Overfit ง่าย** จึงต้องจำกัดความลึกด้วย `max_depth`

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)
plot_tree(model, feature_names=X.columns, filled=True)   # วาดต้นไม้ให้เห็นกฎ
plt.show()
```

### 2.2 K-Nearest Neighbors (KNN)

ไม่สร้าง "กฎ" ล่วงหน้า แต่เมื่อมีข้อมูลใหม่จะดู **เพื่อนบ้านที่ใกล้ที่สุด K ตัว** แล้วโหวตเสียงข้างมาก
เพราะใช้ระยะทาง จึง **ต้องปรับสเกลข้อมูลก่อนเสมอ** ค่า K น้อยเกินไปจะไวต่อสัญญาณรบกวน K มากเกินไปจะเบลอขอบเขตกลุ่ม (นิยมเริ่มที่ K = 5)

```python
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train_s, y_train)
```

### สรุปเปรียบเทียบ 4 อัลกอริทึม

| อัลกอริทึม | ประเภทงาน | ต้องปรับสเกล | จุดเด่น |
|---|---|---|---|
| Linear Regression | Regression | ควร | ตีความสมการได้ |
| Logistic Regression | Classification | ควร | ให้ความน่าจะเป็น |
| Decision Tree | ทั้งสอง | ไม่ต้อง | อธิบายกฎได้ง่าย |
| KNN | ทั้งสอง | **ต้อง** | เข้าใจง่าย ไม่ต้องฝึกนาน |

---

## 3. การแบ่งข้อมูล Train/Validation/Test

- **Train** — ใช้สอนโมเดล (เหมือนทำแบบฝึกหัด)
- **Validation** — ใช้ปรับจูนไฮเปอร์พารามิเตอร์ (เหมือนสอบกลางภาค)
- **Test** — ใช้วัดผลจริงครั้งเดียวตอนท้าย (เหมือนสอบปลายภาค ห้ามใช้ระหว่างพัฒนา)

อัตราส่วนนิยม 70:15:15 หรือ 60:20:20 หากข้อมูลน้อยให้แบ่งเพียง Train/Test 80:20 แล้วใช้ Cross Validation แทนชุด Validation

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
```

`stratify=y` ทำให้สัดส่วนคลาสในชุด Train และ Test เท่ากัน — สำคัญมากกับงาน Classification

**ข้อควรระวังสำคัญ:** ต้องแบ่งข้อมูลก่อน แล้วจึง Fit Scaler กับ Train เท่านั้น มิฉะนั้นเกิด Data Leakage ทำให้ผลดีเกินจริง

---

## 4. Cross Validation

การแบ่ง Train/Test ครั้งเดียวอาจ "ฟลุ๊ค" ได้ **k-fold Cross Validation** จึงแบ่งข้อมูลเป็น k ส่วน (นิยม k = 5) แล้วผลัดกันเป็นชุดทดสอบทีละส่วน ทำครบ k รอบแล้วเฉลี่ยผล — ทุกตัวอย่างได้เป็นชุดทดสอบ 1 ครั้ง

```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X_s, y, cv=5)
print('mean =', scores.mean().round(3), ' std =', scores.std().round(3))
```

การอ่านผล: **mean สูง = แม่น, std ต่ำ = ผลนิ่ง** โมเดลที่ mean สูงแต่ std สูงอาจไว้ใจไม่ได้เท่าโมเดลที่ mean ต่ำกว่าเล็กน้อยแต่นิ่งกว่า

---

## 5. ตัวชี้วัดการประเมินโมเดล

### 5.1 งาน Regression (ยิ่งต่ำยิ่งดี)

| ตัวชี้วัด | สูตร/ความหมาย | จุดเด่น |
|---|---|---|
| MAE | ค่าเฉลี่ยของ \|ค่าจริง − ค่าทำนาย\| | ตีความง่าย หน่วยเดียวกับข้อมูล |
| MSE | ค่าเฉลี่ยของ (ค่าจริง − ค่าทำนาย)² | ลงโทษค่าคลาดเคลื่อนใหญ่ |
| RMSE | √MSE | เหมือน MSE แต่หน่วยเดียวกับข้อมูล |

ตัวอย่าง: ทำนายราคา 3 เครื่อง คลาดเคลื่อน +2000, −1000, +3000 บาท → MAE = (2000+1000+3000)/3 = **2,000 บาท**

### 5.2 งาน Classification (ยิ่งสูงยิ่งดี)

เริ่มจาก Confusion Matrix: TP (ทำนายบวก-ถูก), FP (ทำนายบวก-ผิด), FN (ทำนายลบ-ผิด), TN (ทำนายลบ-ถูก)

- **Accuracy** = (TP + TN) / ทั้งหมด — ความถูกต้องรวม
- **Precision** = TP / (TP + FP) — ที่ทำนายว่าบวก ถูกจริงกี่ส่วน
- **Recall** = TP / (TP + FN) — ของจริงที่เป็นบวก จับได้กี่ส่วน
- **F1** = 2 × (Precision × Recall) / (Precision + Recall)

**ตัวอย่างคำนวณ:** TP = 40, FN = 5, FP = 10, TN = 45 (รวม 100)
→ Accuracy = 0.85, Precision = 40/50 = 0.80, Recall = 40/45 ≈ 0.89, F1 ≈ 0.84

**เลือกตัวชี้วัดตามงาน:** งานคัดกรองโรค/ตรวจจับของเสีย เน้น **Recall** (พลาดของจริงไม่ได้) งานกรองสแปม เน้น **Precision** (ทำนายผิดแล้วเมลสำคัญหาย) ข้อมูลคลาสไม่สมดุลให้ดู **F1** แทน Accuracy

```python
from sklearn.metrics import confusion_matrix, classification_report
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
```

---

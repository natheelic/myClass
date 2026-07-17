# LAB สัปดาห์ที่ 8 — Supervised Learning: Regression และ Classification

**รหัสวิชา 31909-2004 ระบบปัญญาประดิษฐ์เบื้องต้น** | หน่วยที่ 5 | ภาคปฏิบัติ 3 ชม. (150 นาที)
**หัวข้อ:** Linear Regression ทำนายราคา, จำแนก Iris ด้วย 3 โมเดล, Cross Validation และ Confusion Matrix
**ชุดข้อมูล:** สร้างเองในตอนที่ 1 + `data/iris.csv` (อยู่ในโฟลเดอร์ LAB5 นี้)

> **กติกา:** พิมพ์โค้ดเองทีละขั้น รันให้ผ่านจุดตรวจสอบ (Checkpoint) ก่อนไปขั้นถัดไป
> กำหนด `random_state=42` ทุกครั้งที่มีการสุ่ม และบันทึกผลลงตารางท้ายเอกสารทันทีที่ได้ผล

---

## เตรียมความพร้อม (10 นาที)

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (mean_absolute_error, mean_squared_error,
                             confusion_matrix, classification_report)
```

**Checkpoint 0:** รันแล้วไม่มี Error ใด ๆ

---

## ตอนที่ 1 Linear Regression — ทำนายราคาคอมพิวเตอร์มือสอง (40 นาที)

### 1.1 สร้างชุดข้อมูลจำลอง

ร้านรับซื้อ-ขายคอมพิวเตอร์มือสองเก็บข้อมูล 40 เครื่อง: อายุการใช้งาน (ปี) กับราคาขายต่อ (บาท)

```python
rng = np.random.default_rng(42)
age = rng.uniform(0.5, 6, 40).round(1)
price = 25000 - 3500 * age + rng.normal(0, 1200, 40)
df = pd.DataFrame({'age_years': age, 'price_baht': price.round(0)})
print(df.head())

plt.scatter(df['age_years'], df['price_baht'])
plt.xlabel('Age (years)'); plt.ylabel('Price (baht)')
plt.show()
```

**Checkpoint 1:** กราฟกระจายมีแนวโน้มลดลงชัดเจน (อายุมาก → ราคาถูก)

### 1.2 ฝึกโมเดลและอ่านสมการ

```python
X = df[['age_years']]
y = df['price_baht']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
print('สมการ: ราคา =', model.intercept_.round(0), '+ (', model.coef_[0].round(0), ') x อายุ')
```

**Checkpoint 2:** ได้สมการประมาณ `ราคา = 25798 + (−3702) × อายุ`
**คำถาม 1.1:** จากสมการ เครื่องอายุเพิ่ม 1 ปี ราคาลดลงประมาณกี่บาท

### 1.3 ประเมินด้วย MAE / RMSE และทดลองทำนาย

```python
y_pred = model.predict(X_test)
print('MAE  =', mean_absolute_error(y_test, y_pred).round(0))
print('RMSE =', np.sqrt(mean_squared_error(y_test, y_pred)).round(0))

# วาดเส้นที่โมเดลเรียนรู้ได้ทับบนข้อมูลจริง
plt.scatter(X_test, y_test, label='Actual')
plt.plot(X_test, y_pred, color='red', label='Predicted line')
plt.xlabel('Age (years)'); plt.ylabel('Price (baht)'); plt.legend()
plt.show()

# ทำนายเครื่องอายุ 3 ปี
print('เครื่องอายุ 3 ปี ราคาประมาณ',
      model.predict(pd.DataFrame({'age_years': [3]}))[0].round(0), 'บาท')
```

**Checkpoint 3:** MAE ≈ 833 บาท, RMSE ≈ 980 บาท, เครื่องอายุ 3 ปี ≈ 14,691 บาท
**คำถาม 1.2:** MAE = 833 บาท หมายความว่าอย่างไรกับความน่าเชื่อถือของราคาที่ทำนาย

---

## ตอนที่ 2 Classification — จำแนก Iris ด้วย 3 โมเดล (60 นาที)

### 2.1 โหลดข้อมูล แบ่ง Train/Test และปรับสเกล

```python
di = pd.read_csv('data/iris.csv')
X = di.iloc[:, :4]
y = di['species']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
print(X_train.shape, X_test.shape)     # (120, 4) (30, 4)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)   # fit เฉพาะ Train เท่านั้น
X_test_s  = scaler.transform(X_test)
```

**Checkpoint 4:** Train 120 แถว / Test 30 แถว

### 2.2 ฝึกโมเดล 3 แบบ และวัด Accuracy

```python
models = {
    'Decision Tree': DecisionTreeClassifier(max_depth=3, random_state=42),
    'KNN (k=5)': KNeighborsClassifier(n_neighbors=5),
    'Logistic Regression': LogisticRegression(max_iter=200)
}
for name, m in models.items():
    m.fit(X_train_s, y_train)
    print(f'{name}: Train={m.score(X_train_s, y_train):.3f}  '
          f'Test={m.score(X_test_s, y_test):.3f}')
```

**Checkpoint 5:** Accuracy (Test) ทุกโมเดลสูงกว่า 0.90 — บันทึกลงตารางที่ 1

### 2.3 เปิดดู "กฎ" ของ Decision Tree

```python
plt.figure(figsize=(12, 6))
plot_tree(models['Decision Tree'], feature_names=X.columns,
          class_names=sorted(y.unique()), filled=True)
plt.show()
```

**คำถาม 2.1:** กฎข้อแรกสุด (โหนดบนสุด) ใช้คุณลักษณะใดตัดสิน และค่าตัดคือเท่าใด
**คำถาม 2.2:** ถ้าเพิ่ม `max_depth` เป็น 10 คะแนน Train/Test จะเปลี่ยนอย่างไร (ทดลองจริงแล้วตอบ)

---

## ตอนที่ 3 Cross Validation และ Confusion Matrix (40 นาที)

### 3.1 5-Fold Cross Validation

```python
X_s = StandardScaler().fit_transform(X)
for name, m in models.items():
    scores = cross_val_score(m, X_s, y, cv=5)
    print(f'{name}: mean={scores.mean():.3f}  std={scores.std():.3f}')
```

**Checkpoint 6:** ค่า mean ทุกโมเดล ≥ 0.95 — บันทึกลงตารางที่ 2

### 3.2 Confusion Matrix ของโมเดลที่ดีที่สุด

```python
best = models['Decision Tree']        # เปลี่ยนตามผลของนักศึกษา
y_pred = best.predict(X_test_s)

labels = sorted(y.unique())
cm = confusion_matrix(y_test, y_pred, labels=labels)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=labels, yticklabels=labels)
plt.xlabel('Predicted'); plt.ylabel('Actual')
plt.show()

print(classification_report(y_test, y_pred, target_names=labels))
```

**Checkpoint 7:** ตัวเลขบนแนวทแยงมุมคือจำนวนที่ทำนายถูก
**คำถาม 3.1:** คลาสใดถูกทำนายผิดบ่อยที่สุด และมักถูกทำนายผิดไปเป็นคลาสใด
**คำถาม 3.2:** จาก Confusion Matrix ของนักศึกษา จงคำนวณ Precision และ Recall ของคลาส versicolor ด้วยมือ แล้วเทียบกับ classification_report

---

## ตารางบันทึกผล LAB สัปดาห์ที่ 8

**ตอนที่ 1 — Linear Regression**

| รายการ | ค่าที่ได้ |
|---|---|
| สมการที่ได้ (intercept, coefficient) | |
| MAE (บาท) | |
| RMSE (บาท) | |
| ราคาทำนายเครื่องอายุ 3 ปี | |

**ตารางที่ 1 — Accuracy (Hold-out 80:20)**

| โมเดล | Accuracy (Train) | Accuracy (Test) |
|---|---|---|
| Decision Tree | | |
| KNN (k=5) | | |
| Logistic Regression | | |

**ตารางที่ 2 — 5-Fold Cross Validation**

| โมเดล | mean Accuracy | std |
|---|---|---|
| Decision Tree | | |
| KNN (k=5) | | |
| Logistic Regression | | |

**คำตอบคำถาม 1.1, 1.2, 2.1, 2.2, 3.1, 3.2:** เขียนตอบท้ายรายงาน (ข้อละ 2–3 บรรทัด)

---

## สิ่งที่ต้องส่ง (ภายในท้ายคาบ)

1. ไฟล์โค้ด (.py หรือ .ipynb) ที่รันได้ครบทั้ง 3 ตอน
2. ตารางบันทึกผลที่กรอกครบ + คำตอบคำถาม 6 ข้อ
3. ภาพกราฟ 4 ภาพ: Scatter+เส้น Regression, Decision Tree, Confusion Matrix Heatmap และกราฟตอน 1.1

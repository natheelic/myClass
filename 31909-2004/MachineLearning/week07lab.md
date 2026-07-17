# LAB สัปดาห์ที่ 7 — ภาพรวม Machine Learning และการเตรียมข้อมูล

**รหัสวิชา 31909-2004 ระบบปัญญาประดิษฐ์เบื้องต้น** | หน่วยที่ 5 | ภาคปฏิบัติ 3 ชม. (150 นาที)
**หัวข้อ:** สำรวจข้อมูลด้วย EDA, ทำความสะอาดข้อมูล (Missing Value, Outlier, Encoding), การปรับสเกล
**ชุดข้อมูล:** `data/iris.csv` และ `data/computers_messy.csv` (อยู่ในโฟลเดอร์ LAB5 นี้)

> **กติกา:** พิมพ์โค้ดเองทีละขั้น รันให้ผ่านจุดตรวจสอบ (Checkpoint) ก่อนไปขั้นถัดไป
> และบันทึกผลลงตารางท้ายเอกสารทันทีที่ได้ผล

---

## เตรียมความพร้อม (10 นาที)

ติดตั้งไลบรารี (ทำครั้งเดียว): `pip install scikit-learn pandas matplotlib seaborn`

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler
```

**Checkpoint 0:** รันแล้วไม่มี Error ใด ๆ (ถ้าขึ้น ModuleNotFoundError ให้ติดตั้งไลบรารีนั้นก่อน)

---

## ตอนที่ 1 รู้จักข้อมูลด้วย EDA — Iris Dataset (40 นาที)

### 1.1 โหลดและสำรวจโครงสร้าง

```python
df = pd.read_csv('data/iris.csv')
print(df.shape)                       # ขนาด (แถว, คอลัมน์)
print(df.head())                      # 5 แถวแรก
print(df.info())                      # ชนิดข้อมูล
print(df.describe())                  # ค่าสถิติพื้นฐาน
print(df['species'].value_counts())   # จำนวนแต่ละคลาส
```

**Checkpoint 1:** ข้อมูล 150 แถว 5 คอลัมน์ — 4 คุณลักษณะ (Feature) + 1 เฉลย (Label) คลาสละ 50 ตัวอย่าง

### 1.2 ดูการกระจายและความสัมพันธ์

```python
sns.pairplot(df, hue='species')
plt.show()
```

**Checkpoint 2:** เห็นกลุ่มสีแยกกันชัดในบางคู่คุณลักษณะ — จดว่าคู่ใดแยกได้ชัดที่สุด

**คำถาม 1.1:** ข้อมูล Iris มีเฉลย (species) กำกับ ถ้านำไปสร้างโมเดล จะเป็น ML ประเภทใด (Supervised/Unsupervised) และเป็นงาน Regression หรือ Classification
**คำถาม 1.2:** ถ้าตัดคอลัมน์ species ทิ้งแล้วให้เครื่องหากลุ่มเอง จะเป็น ML ประเภทใด

---

## ตอนที่ 2 ทำความสะอาดข้อมูล — computers_messy.csv (70 นาที)

ชุดข้อมูลคอมพิวเตอร์มือสอง 62 แถว ที่ "สกปรก" เหมือนข้อมูลจริงในสถานประกอบการ: มีค่าว่าง แถวซ้ำ และราคาผิดปกติ ภารกิจคือทำให้สะอาดพร้อมใช้สร้างโมเดล

### 2.1 ตรวจหาปัญหา

```python
dm = pd.read_csv('data/computers_messy.csv')
print(dm.shape)
print(dm.isnull().sum())              # นับค่าว่างแต่ละคอลัมน์
print('แถวซ้ำ =', dm.duplicated().sum())
print(dm.describe())                  # สังเกตค่า max ของ price_baht
```

**Checkpoint 3:** พบค่าว่าง brand 3 จุด, ram_gb 5 จุด, แถวซ้ำ 2 แถว และ price_baht มีค่า max สูงผิดปกติ (250,000)

### 2.2 ลบแถวซ้ำ

```python
dm = dm.drop_duplicates().reset_index(drop=True)
print(dm.shape)                       # ควรเหลือ 60 แถว
```

### 2.3 เติมค่าว่าง (Missing Value)

ตัวเลข → เติมค่ามัธยฐาน / ข้อความ → เติมฐานนิยม (ค่าที่พบบ่อยสุด)

```python
dm['ram_gb'] = dm['ram_gb'].fillna(dm['ram_gb'].median())
dm['brand'] = dm['brand'].fillna(dm['brand'].mode()[0])
print(dm.isnull().sum())              # ต้องเป็น 0 ทุกคอลัมน์
```

**Checkpoint 4:** ไม่เหลือค่าว่าง

### 2.4 กำจัด Outlier ด้วยวิธี IQR

```python
Q1 = dm['price_baht'].quantile(0.25)
Q3 = dm['price_baht'].quantile(0.75)
IQR = Q3 - Q1
lo, hi = Q1 - 1.5*IQR, Q3 + 1.5*IQR
print('ขอบเขตปกติ:', round(lo), 'ถึง', round(hi))
print('Outlier ที่พบ:')
print(dm[(dm['price_baht'] < lo) | (dm['price_baht'] > hi)])

dm = dm[(dm['price_baht'] >= lo) & (dm['price_baht'] <= hi)].reset_index(drop=True)
print('เหลือ', dm.shape[0], 'แถว')
```

**Checkpoint 5:** พบ Outlier ราคา 250,000 และ 190,000 บาท (ราคาปกติหลักหมื่น) — จดขอบเขต IQR ที่คำนวณได้ลงตารางบันทึกผล
**คำถาม 2.1:** วิธี IQR อาจตัดค่าที่ "แพงจริง" ทิ้งไปด้วย (ค่าที่เกินขอบเขตเล็กน้อย) ก่อนลบทิ้งควรทำอย่างไร

### 2.5 เข้ารหัสตัวแปรข้อความ (Encoding)

brand เป็นข้อความ ต้องแปลงเป็นตัวเลขก่อนใช้สร้างโมเดล — ยี่ห้อไม่มีลำดับ จึงใช้ One-Hot Encoding

```python
dm_enc = pd.get_dummies(dm, columns=['brand'])
print(dm_enc.head())
print(dm_enc.columns.tolist())
```

**Checkpoint 6:** คอลัมน์ brand หายไป เกิดคอลัมน์ใหม่ brand_Acer, brand_Dell, brand_HP ที่มีค่า True/False (1/0)
**คำถาม 2.2:** เหตุใดจึงไม่ใช้ Label Encoding (Acer=0, Dell=1, HP=2) กับคอลัมน์ยี่ห้อ

---

## ตอนที่ 3 การปรับสเกลข้อมูล (30 นาที)

age_years (0.5–6) กับ price_baht (หลักหมื่น) มีสเกลต่างกันมาก — เปรียบเทียบ 2 วิธีปรับสเกล

```python
num_cols = ['age_years', 'ram_gb', 'cpu_ghz', 'price_baht']

mm = MinMaxScaler().fit_transform(dm[num_cols])     # บีบเข้าช่วง 0-1
ss = StandardScaler().fit_transform(dm[num_cols])   # เฉลี่ย 0, SD 1

print('Min-Max  : min =', mm.min(axis=0).round(2), ' max =', mm.max(axis=0).round(2))
print('Standard : mean =', ss.mean(axis=0).round(2), ' std =', ss.std(axis=0).round(2))
```

**Checkpoint 7:** Min-Max ได้ค่า 0–1 ทุกคอลัมน์ / StandardScaler ได้ mean ≈ 0 และ std ≈ 1

**คำถาม 3.1:** คะแนนสอบ 75 คะแนน ห้องมีค่าเฉลี่ย 60 และ SD = 10 จงคำนวณค่า Z-score ด้วยมือ
**คำถาม 3.2:** สัปดาห์หน้าจะแบ่งข้อมูลเป็น Train/Test — ควร Fit Scaler ก่อนหรือหลังแบ่งข้อมูล เพราะเหตุใด

### บันทึกข้อมูลสะอาดไว้ใช้สัปดาห์หน้า

```python
dm_enc.to_csv('data/computers_clean.csv', index=False)
print('บันทึก data/computers_clean.csv เรียบร้อย —', dm_enc.shape)
```

---

## ตารางบันทึกผล LAB สัปดาห์ที่ 7

**ตอนที่ 2 — ปัญหาที่พบและการแก้ไข**

| ปัญหา | จำนวนที่พบ | วิธีแก้ที่ใช้ |
|---|---|---|
| ค่าว่างคอลัมน์ brand | | |
| ค่าว่างคอลัมน์ ram_gb | | |
| แถวซ้ำ | | |
| Outlier ราคา | | |

**ตอนที่ 2 — ขอบเขต IQR ของ price_baht**

| รายการ | ค่าที่ได้ |
|---|---|
| Q1 | |
| Q3 | |
| IQR | |
| ขอบเขตปกติ (ล่าง – บน) | |
| จำนวนแถวที่เหลือหลังทำความสะอาด | |

**คำตอบคำถาม 1.1, 1.2, 2.1, 2.2, 3.1, 3.2:** เขียนตอบท้ายรายงาน (ข้อละ 2–3 บรรทัด)

---

## สิ่งที่ต้องส่ง (ภายในท้ายคาบ)

1. ไฟล์โค้ด (.py หรือ .ipynb) ที่รันได้ครบทั้ง 3 ตอน
2. ไฟล์ `data/computers_clean.csv` ที่ทำความสะอาดแล้ว
3. ตารางบันทึกผลที่กรอกครบ + คำตอบคำถาม 6 ข้อ
4. ภาพกราฟ pairplot จากตอนที่ 1
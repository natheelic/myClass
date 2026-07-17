# LAB สัปดาห์ที่ 9 — Unsupervised Learning และการประเมินผลโมเดล

**รหัสวิชา 31909-2004 ระบบปัญญาประดิษฐ์เบื้องต้น** | หน่วยที่ 5 | ภาคปฏิบัติ 3 ชม. (150 นาที)
**หัวข้อ:** K-Means Clustering, Hierarchical Clustering, PCA เบื้องต้น
**ชุดข้อมูล:** `data/customers.csv` และ `data/iris.csv` (อยู่ในโฟลเดอร์ LAB5 นี้)

> **กติกา:** พิมพ์โค้ดเองทีละขั้น รันให้ผ่านจุดตรวจสอบ (Checkpoint) ก่อนไปขั้นถัดไป
> กำหนด `random_state=42` ทุกครั้งที่มีการสุ่ม และบันทึกผลลงตารางท้ายเอกสารทันทีที่ได้ผล

---

## เตรียมความพร้อม (10 นาที)

ตรวจว่าไลบรารีครบ (ติดตั้งแล้วตั้งแต่สัปดาห์ที่ 7 หากยังให้รัน `pip install scikit-learn pandas matplotlib scipy`)

```python
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.decomposition import PCA
```

**Checkpoint 0:** รันแล้วไม่มี Error ใด ๆ

---

## ตอนที่ 1 K-Means แบ่งกลุ่มลูกค้า (60 นาที)

### 1.1 โหลดและสำรวจข้อมูล

```python
df = pd.read_csv('data/customers.csv')
print(df.shape)
print(df.head())
print(df.describe())
```

**Checkpoint 1:** ข้อมูล 200 แถว 4 คอลัมน์ (`customer_id`, `income_k`, `spending_score`, `age`)

### 1.2 ปรับสเกลข้อมูล

K-Means ใช้ระยะทางในการคำนวณ จึงต้องปรับสเกลก่อนเสมอ

```python
X = StandardScaler().fit_transform(df[['income_k', 'spending_score']])
```

### 1.3 หาค่า K ที่เหมาะสม (Elbow + Silhouette)

```python
wcss = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    wcss.append(km.inertia_)
    if k > 1:
        print(k, 'Silhouette =', round(silhouette_score(X, km.labels_), 3))

plt.plot(range(1, 11), wcss, marker='o')
plt.xlabel('K'); plt.ylabel('WCSS'); plt.title('Elbow Method')
plt.show()
```

**Checkpoint 2:** กราฟมีจุดข้อศอกชัดเจน — จด **ค่า K ที่จุดข้อศอก** และ **K ที่ Silhouette สูงสุด** ลงตารางบันทึกผล (ทั้งสองค่าควรตรงกัน)

### 1.4 แบ่งกลุ่มด้วย K ที่เลือก และวาดกราฟ

```python
K = 4   # เปลี่ยนตามค่าที่ได้จากข้อ 1.3
km = KMeans(n_clusters=K, random_state=42, n_init=10)
df['cluster'] = km.fit_predict(X)

for c in sorted(df['cluster'].unique()):
    g = df[df['cluster'] == c]
    plt.scatter(g['income_k'], g['spending_score'], label=f'Cluster {c}')
plt.xlabel('Income (k THB/month)'); plt.ylabel('Spending Score')
plt.legend(); plt.show()
```

### 1.5 แปลผลและตั้งชื่อกลุ่ม

```python
print(df.groupby('cluster')[['income_k', 'spending_score', 'age']].mean().round(1))
```

**Checkpoint 3:** เห็นกลุ่มแยกจากกันชัดเจนในกราฟ — ตั้งชื่อแต่ละกลุ่มตามพฤติกรรม (เช่น "รายได้สูง–ใช้จ่ายสูง = ลูกค้าพรีเมียม") ลงตารางบันทึกผล

---

## ตอนที่ 2 Hierarchical Clustering และ Dendrogram (30 นาที)

ใช้ข้อมูลลูกค้าชุดเดิม สร้างกลุ่มแบบลำดับชั้นแล้วเทียบผลกับ K-Means

```python
Z = linkage(X, method='ward')
plt.figure(figsize=(10, 4))
dendrogram(Z, no_labels=True)
plt.title('Dendrogram (ward)')
plt.ylabel('Distance')
plt.show()
```

**Checkpoint 4:** ได้แผนภาพต้นไม้ — ลากเส้นแนวนอนตัดที่ช่วงความสูงที่กิ่งยาวที่สุด แล้วนับว่าตัดผ่านกี่กิ่ง

**คำถาม 2.1:** จำนวนกลุ่มที่ได้จากการตัด Dendrogram ตรงกับค่า K จากตอนที่ 1 หรือไม่
**คำถาม 2.2:** วิธีใดเหมาะกับข้อมูลขนาดใหญ่กว่ากัน เพราะเหตุใด

---

## ตอนที่ 3 PCA ลดมิติข้อมูล Iris (40 นาที)

Iris มี 4 คุณลักษณะ (4 มิติ) วาดกราฟตรง ๆ ไม่ได้ ให้ใช้ PCA ลดเหลือ 2 มิติ

### 3.1 ลดมิติและตรวจสอบความแปรปรวนที่เก็บได้

```python
di = pd.read_csv('data/iris.csv')
Xi = StandardScaler().fit_transform(di.iloc[:, :4])

pca = PCA(n_components=2)
X2 = pca.fit_transform(Xi)
print('Explained variance ratio:', pca.explained_variance_ratio_.round(3))
print('รวม =', pca.explained_variance_ratio_.sum().round(3))
```

**Checkpoint 5:** ผลรวม explained variance ratio ≈ **0.958** (2 มิติใหม่เก็บสาระของข้อมูล 4 มิติไว้ ~96%)

### 3.2 วาดข้อมูล 2 มิติ เทียบเฉลยจริงกับผล K-Means

```python
fig, ax = plt.subplots(1, 2, figsize=(11, 4))

# ซ้าย: ระบายสีตามเฉลยจริง (species)
for sp in di['species'].unique():
    m = di['species'] == sp
    ax[0].scatter(X2[m, 0], X2[m, 1], label=sp)
ax[0].set_title('True labels'); ax[0].legend()

# ขวา: ระบายสีตามผล K-Means (K=3) ที่ไม่เคยเห็นเฉลย
km3 = KMeans(n_clusters=3, random_state=42, n_init=10).fit(Xi)
ax[1].scatter(X2[:, 0], X2[:, 1], c=km3.labels_)
ax[1].set_title('K-Means clusters (K=3)')
plt.show()
```

**Checkpoint 6:** กราฟสองฝั่งควรมีโครงสร้างกลุ่มคล้ายกัน — K-Means หากลุ่มได้ใกล้เคียงเฉลยจริงทั้งที่ไม่เคยเห็นเฉลย

**คำถาม 3.1:** คลาสใดที่ K-Means แยกได้ชัดที่สุด และคู่ใดที่ปนกัน (เทียบกับ pairplot ที่เคยทำในสัปดาห์ที่ 7)
**คำถาม 3.2:** เหตุใดจึงต้องปรับสเกลก่อนทำ PCA

---

## ตารางบันทึกผล LAB สัปดาห์ที่ 9

**ตอนที่ 1 — การเลือกค่า K (customers.csv)**

| รายการ | ค่าที่ได้ |
|---|---|
| K ที่จุดข้อศอก (Elbow) | |
| K ที่ Silhouette สูงสุด | |
| ค่า Silhouette ที่ K นั้น | |
| K ที่เลือกใช้ พร้อมเหตุผล | |

**ตอนที่ 1 — ผลการแบ่งกลุ่มลูกค้า**

| Cluster | รายได้เฉลี่ย (พันบาท) | คะแนนใช้จ่ายเฉลี่ย | อายุเฉลี่ย | ชื่อกลุ่มที่ตั้ง |
|---|---|---|---|---|
| 0 | | | | |
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

**ตอนที่ 3 — PCA**

| รายการ | ค่าที่ได้ |
|---|---|
| Explained variance ratio (PC1, PC2) | |
| ผลรวม | |

**คำตอบคำถาม 2.1, 2.2, 3.1, 3.2:** เขียนตอบท้ายรายงาน (ข้อละ 2–3 บรรทัด)

---

## สิ่งที่ต้องส่ง (ภายในท้ายคาบ)

1. ไฟล์โค้ด (.py หรือ .ipynb) ที่รันได้ครบทั้ง 3 ตอน
2. ตารางบันทึกผลที่กรอกครบ + คำตอบคำถาม 4 ข้อ
3. ภาพกราฟ 4 ภาพ: Elbow, Scatter กลุ่มลูกค้า, Dendrogram, PCA เปรียบเทียบ

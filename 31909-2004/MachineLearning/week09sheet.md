# สัปดาห์ที่ 9

**รหัสวิชา 31909-2004 ระบบปัญญาประดิษฐ์เบื้องต้น** | หน่วยที่ 5 การเรียนรู้ของเครื่องจักร (Machine Learning)
**ชื่อเรื่อง:** Unsupervised Learning และการประเมินผลโมเดล
**เวลา:** ทฤษฎี 2 ชม. + ปฏิบัติ 3 ชม. (รวม 5 ชม.) | สอนครั้งที่ 9

---

## จุดประสงค์เชิงพฤติกรรม

1. อธิบายหลักการ K-Means และ Hierarchical Clustering ได้ (พุทธิพิสัย)
2. เลือกค่า K ที่เหมาะสมด้วย Elbow Method และ Silhouette Score ได้ (วิเคราะห์)
3. ใช้ scikit-learn ทำ Clustering และวาดกราฟผลได้ (ทักษะพิสัย)
4. ทำงานด้วยความรับผิดชอบและละเอียดรอบคอบ (จิตพิสัย)
5. ประยุกต์ใช้ Clustering กับการแบ่งกลุ่มลูกค้า/อุปกรณ์ในงานอาชีพได้ (ประยุกต์ใช้)

---

## 1. หลักการ Unsupervised Learning

Unsupervised Learning คือการเรียนรู้จากข้อมูลที่ **ไม่มีเฉลย (Label)** โมเดลต้องค้นหาโครงสร้างหรือรูปแบบที่ซ่อนอยู่ในข้อมูลด้วยตัวเอง ต่างจาก Supervised Learning ที่เรียนในสัปดาห์ที่ 7–8 ซึ่งมีเฉลยกำกับทุกตัวอย่าง

| ประเด็นเปรียบเทียบ | Supervised | Unsupervised |
|---|---|---|
| ข้อมูลนำเข้า | X + เฉลย y | X อย่างเดียว |
| เป้าหมาย | ทำนายค่า/ประเภท | หากลุ่ม/โครงสร้าง |
| ตัวอย่างงาน | จำแนกดอกไอริส ทำนายราคา | แบ่งกลุ่มลูกค้า ลดมิติข้อมูล |
| การวัดผล | Accuracy, F1, RMSE | Inertia (WCSS), Silhouette |

งานหลัก 2 ประเภทของ Unsupervised Learning:

- **Clustering (การแบ่งกลุ่ม)** — จัดข้อมูลที่คล้ายกันไว้กลุ่มเดียวกัน เช่น แบ่งกลุ่มลูกค้าเพื่อทำการตลาด แบ่งกลุ่มอุปกรณ์ตามพฤติกรรมการใช้พลังงาน
- **Dimensionality Reduction (การลดมิติ)** — ลดจำนวนคุณลักษณะโดยรักษาสาระสำคัญไว้ เช่น PCA

**ตัวอย่างในงานอาชีพ (สาขาเทคโนโลยีคอมพิวเตอร์):** แบ่งกลุ่มคอมพิวเตอร์ในองค์กรตามพฤติกรรมการใช้งานเพื่อวางแผนบำรุงรักษา, จัดกลุ่ม log ของเครือข่ายเพื่อหาพฤติกรรมผิดปกติ

---

## 2. K-Means Clustering

### 2.1 หลักการทำงาน (4 ขั้น)

1. สุ่มตำแหน่งจุดศูนย์กลาง (Centroid) จำนวน K จุด
2. จัดข้อมูลแต่ละจุดเข้ากลุ่มของ Centroid ที่อยู่ใกล้ที่สุด (ใช้ระยะทางแบบยุคลิด)
3. คำนวณ Centroid ใหม่จากค่าเฉลี่ยของสมาชิกในกลุ่ม
4. ทำซ้ำขั้นที่ 2–3 จนกว่า Centroid จะไม่เปลี่ยนตำแหน่ง (ลู่เข้า)

เป้าหมายคือทำให้ **WCSS (Within-Cluster Sum of Squares)** หรือผลรวมระยะห่างกำลังสองภายในกลุ่มต่ำที่สุด (ใน scikit-learn เรียกว่า `inertia_`)

### 2.2 ข้อควรระวัง

- K-Means ใช้ **ระยะทาง** ในการคำนวณ จึงต้อง **ปรับสเกลข้อมูลก่อนเสมอ** (StandardScaler)
- ผลลัพธ์ขึ้นกับตำแหน่งเริ่มต้น จึงกำหนด `random_state=42` และ `n_init=10` ให้รันหลายรอบแล้วเลือกผลดีที่สุด
- เหมาะกับกลุ่มทรงกลมขนาดใกล้เคียงกัน ไม่เหมาะกับกลุ่มรูปร่างซับซ้อน

### 2.3 โค้ดตัวอย่าง

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

df = pd.read_csv('data/customers.csv')
X = StandardScaler().fit_transform(df[['income_k', 'spending_score']])

km = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster'] = km.fit_predict(X)
print(km.inertia_)          # ค่า WCSS
print(df.groupby('cluster')[['income_k', 'spending_score']].mean())
```

---

## 3. Hierarchical Clustering เบื้องต้น

สร้างกลุ่มแบบลำดับชั้นโดย **รวมกลุ่มที่ใกล้กันทีละคู่** (Agglomerative — จากล่างขึ้นบน) แล้วแสดงผลเป็นแผนภาพต้นไม้ **Dendrogram** ผู้ใช้เลือกจำนวนกลุ่มโดย "ตัด" ต้นไม้ที่ระดับความสูงที่ต้องการ

| ประเด็น | K-Means | Hierarchical |
|---|---|---|
| ต้องกำหนด K ล่วงหน้า | ต้อง | ไม่ต้อง (ตัดจาก Dendrogram ทีหลัง) |
| ข้อมูลขนาดใหญ่ | เร็ว เหมาะ | ช้า (เหมาะข้อมูลเล็ก–กลาง) |
| เห็นโครงสร้างลำดับชั้น | ไม่เห็น | เห็นจาก Dendrogram |

```python
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

Z = linkage(X, method='ward')
dendrogram(Z)
plt.title('Dendrogram')
plt.show()
```

---

## 4. การเลือกค่า K: Elbow Method และ Silhouette Score

### 4.1 Elbow Method

พล็อตค่า WCSS เทียบกับ K = 1, 2, 3, ..., 10 เมื่อ K เพิ่ม WCSS จะลดลงเสมอ แต่จุดที่กราฟ **เริ่มหักลดลงช้า (จุดข้อศอก)** คือค่า K ที่เหมาะสม — เพิ่ม K ต่อจากนี้ได้ประโยชน์น้อย

```python
wcss = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    wcss.append(km.inertia_)
plt.plot(range(1, 11), wcss, marker='o')
plt.xlabel('K'); plt.ylabel('WCSS'); plt.show()
```

### 4.2 Silhouette Score

วัดว่าแต่ละจุด "เข้าพวก" กับกลุ่มตัวเองแค่ไหนเทียบกับกลุ่มข้างเคียง ค่าอยู่ในช่วง **−1 ถึง 1 ยิ่งใกล้ 1 ยิ่งดี** ใช้ยืนยันผลจาก Elbow Method

```python
from sklearn.metrics import silhouette_score
score = silhouette_score(X, km.labels_)
```

**ผลจากชุดข้อมูล customers.csv (เฉลยสำหรับครู):** จุดข้อศอกชัดที่ K = 4 และ Silhouette สูงสุด 0.731 ที่ K = 4 เช่นกัน ได้ลูกค้า 4 กลุ่ม: รายได้น้อย–ใช้จ่ายน้อย, รายได้น้อย–ใช้จ่ายมาก (วัยรุ่น), รายได้มาก–ประหยัด, รายได้มาก–ใช้จ่ายมาก (พรีเมียม)

---

## 5. การลดมิติด้วย PCA เบื้องต้น

**PCA (Principal Component Analysis)** แปลงข้อมูลหลายมิติให้เหลือมิติน้อยลง โดยสร้างแกนใหม่ (Principal Component) ที่เก็บความแปรปรวนของข้อมูลไว้มากที่สุด ใช้เพื่อ (1) วาดกราฟข้อมูลหลายมิติใน 2 มิติ (2) ลดจำนวนคุณลักษณะก่อนป้อนโมเดล

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_2d = pca.fit_transform(X)                    # ลดเหลือ 2 มิติ
print(pca.explained_variance_ratio_)           # สัดส่วนความแปรปรวนที่เก็บได้
plt.scatter(X_2d[:, 0], X_2d[:, 1], c=km.labels_)
plt.xlabel('PC1'); plt.ylabel('PC2'); plt.show()
```

ข้อสังเกต: ต้องปรับสเกลข้อมูลก่อนทำ PCA เสมอ และผลรวมของ `explained_variance_ratio_` บอกว่าข้อมูล 2 มิติใหม่เก็บสาระของข้อมูลเดิมไว้กี่เปอร์เซ็นต์

---

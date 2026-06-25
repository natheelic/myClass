# main.py
# -----------------------------------------------------------------
# ไฟล์โปรแกรมหลักสำหรับเรียกใช้งานและแสดงผลลัพธ์ระบบควบคุมพัดลม (แบบอินเทอร์แอคทีฟ)
# -----------------------------------------------------------------

import fuzzy_engine as engine

def run_simulation(temp, humid):
    """รันการคำนวณและจำลองผลการควบคุมความเร็วพัดลม"""
    
    # 1. แปลงอินพุตเป็นค่าความจริงคลุมเครือ (Fuzzify)
    mu_temp, mu_humid = engine.fuzzify(temp, humid)
    
    # 2. ประเมินกฎควบคุม (Inference & Aggregation)
    activation = engine.evaluate_rules(mu_temp, mu_humid)
    
    # 3. คำนวณหาความเร็วพัดลมจริงที่ได้ (Defuzzify)
    speed = engine.defuzzify(activation)
    
    # 4. แสดงรายงานผลลัพธ์ทีละสเต็ปเพื่อการศึกษา
    print("\n=== ขั้นตอนการคำนวณแบบแยกส่วน ===")
    print(f"อินพุต: อุณหภูมิ = {temp:.1f}°C, ความชื้น = {humid:.1f}%")
    print(f"1) Fuzzify:")
    print(f"   - อุณหภูมิ: เย็น={mu_temp['cold']:.2f}, อุ่น={mu_temp['warm']:.2f}, ร้อน={mu_temp['hot']:.2f}")
    print(f"   - ความชื้น: ต่ำ={mu_humid['low']:.2f}, สูง={mu_humid['high']:.2f}")
    print(f"2) Rules Activation (ระดับการกระตุ้นพัดลม):")
    print(f"   - ความเร็วช้า (Slow)   = {activation['slow']:.2f}")
    print(f"   - ความเร็วกลาง (Medium) = {activation['medium']:.2f}")
    print(f"   - ความเร็วเร็ว (Fast)   = {activation['fast']:.2f}")
    print(f"3) Defuzzify (Centroid):")
    print(f"   - ผลลัพธ์ความเร็วพัดลม = {speed:.1f}%")

if __name__ == "__main__":
    print("=== โปรแกรมจำลองระบบควบคุมพัดลมแบบฟัซซี ===")
    try:
        # รับค่าอุณหภูมิและความชื้นจากคีย์บอร์ด
        temp_input = float(input("กรอกอุณหภูมิ (แนะนำช่วง 0 ถึง 40 °C): "))
        humid_input = float(input("กรอกความชื้น (แนะนำช่วง 0 ถึง 100 %): "))
        
        # เรียกใช้ฟังก์ชันประมวลผล
        run_simulation(temp_input, humid_input)
    except ValueError:
        print("❌ เกิดข้อผิดพลาด: กรุณากรอกเฉพาะตัวเลขเท่านั้น!")

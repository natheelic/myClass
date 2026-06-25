# fuzzy_fan_control_simple.py
# ระบบควบคุมพัดลมแบบฟัซซี (Fuzzy Logic Fan Control) — เวอร์ชัน Python แท้ (ไม่ต้องติดตั้งไลบรารี)
# เหมาะสำหรับใช้อธิบายขั้นตอน Fuzzification, Inference, Aggregation, และ Defuzzification ให้นักเรียนเข้าใจง่าย

# 1. ฟังก์ชันสมาชิกแบบสามเหลี่ยม (Triangular Membership Function)
def trimf(x, a, b, c):
    """คำนวณระดับความเป็นสมาชิก (μ) ในช่วง [0, 1] สำหรับค่า x ใด ๆ"""
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a) if b > a else 1.0
    elif b < x < c:
        return (c - x) / (c - b) if c > b else 1.0
    return 1.0  # จุดยอด (x == b)

# 2. ขั้นตอนที่ 1: Fuzzification (แปลงอินพุตตัวเลขจริงเป็นระดับความจริงฟัซซี)
def fuzzify(temp, humid):
    # ระดับความเป็นสมาชิกของอุณหภูมิ (Temperature)
    mu_temp = {
        "cold": trimf(temp, 0, 0, 20),
        "warm": trimf(temp, 10, 20, 30),
        "hot": trimf(temp, 20, 40, 40)
    }
    
    # ระดับความเป็นสมาชิกของความชื้น (Humidity)
    mu_humid = {
        "low": trimf(humid, 0, 0, 60),
        "high": trimf(humid, 40, 100, 100)
    }
    
    return mu_temp, mu_humid

# 3. ขั้นตอนที่ 2 & 3: Rule Evaluation & Aggregation (ประเมินกฎและรวมผลลัพธ์)
def evaluate_rules(mu_temp, mu_humid):
    # R1: IF ร้อน OR ชื้นสูง THEN พัดลม = เร็ว
    r1 = max(mu_temp["hot"], mu_humid["high"])
    
    # R2: IF อุ่น THEN พัดลม = กลาง
    r2 = mu_temp["warm"]
    
    # R3: IF เย็น AND ชื้นต่ำ THEN พัดลม = ช้า
    r3 = min(mu_temp["cold"], mu_humid["low"])
    
    # R4: IF อุ่น AND ชื้นสูง THEN พัดลม = เร็ว
    r4 = min(mu_temp["warm"], mu_humid["high"])
    
    # รวมผลลัพธ์การกระตุ้น (Activation Levels) ของความเร็วพัดลมแต่ละระดับ
    fan_activation = {
        "slow": r3,
        "medium": r2,
        "fast": max(r1, r4) # ใช้ max เมื่อได้ผลลัพธ์พัดลมระดับเดียวกัน (R1 และ R4)
    }
    
    return fan_activation

# 4. ขั้นตอนที่ 4: Defuzzification (แปลงค่าฟัซซีกลับเป็นความเร็วพัดลมจริง %)
# ใช้วิธีหาจุดศูนย์ถ่วงแบบสุ่มตรวจสอบค่าพัดลมในช่วง 0 - 100 % (Centroid Method)
def defuzzify_centroid(fan_activation):
    numerator = 0.0
    denominator = 0.0
    
    # วนลูปตรวจสอบทุกเปอร์เซ็นต์ของความเร็วพัดลมตั้งแต่ 0% ถึง 100%
    for x in range(0, 101):
        # 1. หาความสูงของกราฟพัดลม ณ จุด x
        mu_slow = trimf(x, 0, 0, 50)
        mu_medium = trimf(x, 25, 50, 75)
        mu_fast = trimf(x, 50, 100, 100)
        
        # 2. ตัดยอดกราฟ (Clipped) ตามระดับการกระตุ้นของกฎ
        y_slow = min(mu_slow, fan_activation["slow"])
        y_medium = min(mu_medium, fan_activation["medium"])
        y_fast = min(mu_fast, fan_activation["fast"])
        
        # 3. รวมกราฟเข้าด้วยกันโดยหาค่าสูงสุด ณ จุด x (Aggregation)
        y_agg = max(y_slow, y_medium, y_fast)
        
        # 4. คำนวณหาค่าเฉลี่ยถ่วงน้ำหนัก (สูตรหาจุดศูนย์ถ่วง Centroid)
        numerator += x * y_agg
        denominator += y_agg
        
    if denominator == 0.0:
        return 0.0
        
    return numerator / denominator

# ฟังก์ชันคำนวณทั้งหมด
def calculate_fan_speed(temperature, humidity):
    # สเต็ป 1: Fuzzify
    mu_temp, mu_humid = fuzzify(temperature, humidity)
    
    # สเต็ป 2 & 3: ประเมินกฎและรวมผล
    fan_activation = evaluate_rules(mu_temp, mu_humid)
    
    # สเต็ป 4: หาจุดศูนย์ถ่วง (Defuzzify)
    speed = defuzzify_centroid(fan_activation)
    
    return speed, mu_temp, mu_humid, fan_activation

# ส่วนทดสอบโปรแกรม
if __name__ == "__main__":
    # ทดสอบป้อนค่า อุณหภูมิ = 28°C และ ความชื้น = 70%
    t, h = 28, 70
    speed, mu_t, mu_h, act = calculate_fan_speed(t, h)
    
    print("=== ขั้นตอนการคำนวณ ===")
    print(f"อินพุต: อุณหภูมิ = {t}°C, ความชื้น = {h}%")
    print(f"1. Fuzzification:")
    print(f"   - อุณหภูมิ: เย็น={mu_t['cold']:.2f}, อุ่น={mu_t['warm']:.2f}, ร้อน={mu_t['hot']:.2f}")
    print(f"   - ความชื้น: ต่ำ={mu_h['low']:.2f}, สูง={mu_h['high']:.2f}")
    print(f"2. Rule Evaluation & Activation:")
    print(f"   - กระตุ้นพัดลม ช้า (Slow)   = {act['slow']:.2f}")
    print(f"   - กระตุ้นพัดลม กลาง (Medium) = {act['medium']:.2f}")
    print(f"   - กระตุ้นพัดลม เร็ว (Fast)   = {act['fast']:.2f}")
    print(f"3. Defuzzification (Centroid):")
    print(f"   - ความเร็วพัดลมผลลัพธ์ = {speed:.1f}%")

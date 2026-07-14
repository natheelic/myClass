# fuzzy_engine.py
# -----------------------------------------------------------------
# โมดูลฟังก์ชันคณิตศาสตร์ตรรกศาสตร์คลุมเครือ (Fuzzy Logic Engine)
# -----------------------------------------------------------------

def trimf(x, a, b, c):
    """คำนวณระดับความเป็นสมาชิกแบบสามเหลี่ยม (Triangular Membership Function)"""
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a) if b > a else 1.0
    elif b < x < c:
        return (c - x) / (c - b) if c > b else 1.0
    return 1.0

def fuzzify(temp, humid):
    """ขั้นตอนที่ 1: แปลงค่าตัวเลขอินพุตเป็นระดับความจริงฟัซซี"""
    mu_temp = {
        "cold": trimf(temp, 0, 0, 20),
        "warm": trimf(temp, 10, 20, 30),
        "hot": trimf(temp, 20, 40, 40)
    }
    mu_humid = {
        "low": trimf(humid, 0, 0, 60),
        "high": trimf(humid, 40, 100, 100)
    }
    return mu_temp, mu_humid

def evaluate_rules(mu_temp, mu_humid):
    """ขั้นตอนที่ 2 & 3: ประเมินกฎ IF-THEN และรวมระดับการกระตุ้นของเอาต์พุต"""
    # R1: IF ร้อน OR ชื้นสูง THEN พัดลม = เร็ว
    r1 = max(mu_temp["hot"], mu_humid["high"])
    # R2: IF อุ่น THEN พัดลม = กลาง
    r2 = mu_temp["warm"]
    # R3: IF เย็น AND ชื้นต่ำ THEN พัดลม = ช้า
    r3 = min(mu_temp["cold"], mu_humid["low"])
    # R4: IF อุ่น AND ชื้นสูง THEN พัดลม = เร็ว
    r4 = min(mu_temp["warm"], mu_humid["high"])
    
    return {
        "slow": r3,
        "medium": r2,
        "fast": max(r1, r4) # ถ้าระดับผลลัพธ์เหมือนกัน ให้เลือกใช้ค่า max
    }

def defuzzify(activation):
    """ขั้นตอนที่ 4: คำนวณหาค่าความเร็วพัดลมจริงด้วยจุดศูนย์ถ่วง (Centroid)"""
    numerator = 0.0
    denominator = 0.0
    
    # วนลูปตรวจสอบพัดลมทีละเปอร์เซ็นต์ตั้งแต่ 0% ถึง 100%
    for x in range(0, 101):
        # ความเป็นสมาชิกตามธรรมชาติของกราฟผลลัพธ์พัดลม
        mu_slow = trimf(x, 0, 0, 50)
        mu_medium = trimf(x, 25, 50, 75)
        mu_fast = trimf(x, 50, 100, 100)
        
        # ตัดยอดกราฟ (Clipped) และรวมขอบกราฟเอาต์พุต (Aggregation)
        y_agg = max(
            min(mu_slow, activation["slow"]),
            min(mu_medium, activation["medium"]),
            min(mu_fast, activation["fast"])
        )
        
        # คำนวณผลรวมตามสูตรโมเมนต์หาจุดศูนย์กลาง
        numerator += x * y_agg
        denominator += y_agg
        
    return numerator / denominator if denominator > 0.0 else 0.0

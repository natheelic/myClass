"""
fuzzy_fan_control.py
--------------------
เฉลยแบบฝึกหัด 6.3 — ระบบควบคุมพัดลมแบบฟัซซีด้วย scikit-fuzzy

ติดตั้งไลบรารี:
    pip install scikit-fuzzy

อินพุต : อุณหภูมิ (0–40 °C), ความชื้น (0–100 %)
เอาต์พุต: ความเร็วพัดลม (0–100 %)
เทคนิค  : Mamdani inference + Centroid defuzzification
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def build_fan_controller():
    """สร้างระบบควบคุมพัดลม คืนค่า ControlSystemSimulation"""

    # 1) ตัวแปรเข้า (Antecedent) และตัวแปรออก (Consequent)
    temp = ctrl.Antecedent(np.arange(0, 41, 1), "temp")
    humid = ctrl.Antecedent(np.arange(0, 101, 1), "humid")
    fan = ctrl.Consequent(np.arange(0, 101, 1), "fan")

    # 2) ฟังก์ชันสมาชิก Triangular (ตามข้อ 6.1)
    temp["cold"] = fuzz.trimf(temp.universe, [0, 0, 20])
    temp["warm"] = fuzz.trimf(temp.universe, [10, 20, 30])
    temp["hot"] = fuzz.trimf(temp.universe, [20, 40, 40])

    humid["low"] = fuzz.trimf(humid.universe, [0, 0, 60])
    humid["high"] = fuzz.trimf(humid.universe, [40, 100, 100])

    fan["slow"] = fuzz.trimf(fan.universe, [0, 0, 50])
    fan["medium"] = fuzz.trimf(fan.universe, [25, 50, 75])
    fan["fast"] = fuzz.trimf(fan.universe, [50, 100, 100])

    # 3) กฎ IF-THEN 4 กฎ (ตามข้อ 6.2)
    r1 = ctrl.Rule(temp["hot"] | humid["high"], fan["fast"])
    r2 = ctrl.Rule(temp["warm"], fan["medium"])
    r3 = ctrl.Rule(temp["cold"] & humid["low"], fan["slow"])
    r4 = ctrl.Rule(temp["warm"] & humid["high"], fan["fast"])

    # 4) สร้างระบบควบคุม
    system = ctrl.ControlSystem([r1, r2, r3, r4])
    return ctrl.ControlSystemSimulation(system)


def fan_speed(sim, temperature, humidity):
    """คำนวณความเร็วพัดลมจากอุณหภูมิและความชื้นที่กำหนด"""
    sim.input["temp"] = temperature
    sim.input["humid"] = humidity
    sim.compute()
    return sim.output["fan"]


if __name__ == "__main__":
    sim = build_fan_controller()

    # ทดสอบกับชุดอินพุตหลายค่า
    test_cases = [(28, 70), (18, 30), (38, 90), (22, 80), (10, 20)]
    print(f"{'อุณหภูมิ(°C)':>12} {'ความชื้น(%)':>12} {'พัดลม(%)':>10}")
    print("-" * 38)
    for t, h in test_cases:
        speed = fan_speed(sim, t, h)
        print(f"{t:>12} {h:>12} {speed:>10.1f}")

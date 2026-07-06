import xlsxwriter
from datetime import datetime, timedelta
import random

def create_lab():
    workbook = xlsxwriter.Workbook('IT_Smart_Solutions_Lab.xlsx')

    # Add formats
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'bg_color': '#D9E1F2',
        'border': 1
    })
    currency_format = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
    border_format = workbook.add_format({'border': 1})
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'border': 1})
    green_bg = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100', 'border': 1})

    # --- MasterData Sheet ---
    ws_master = workbook.add_worksheet('MasterData')

    # Products Table
    ws_master.write('A1', 'รหัสสินค้า (Product_ID)', header_format)
    ws_master.write('B1', 'ชื่อสินค้า (Product_Name)', header_format)
    ws_master.write('C1', 'หมวดหมู่ (Category)', header_format)
    ws_master.write('D1', 'ราคาต่อหน่วย (Price)', header_format)

    products = [
        ['P001', 'Mouse Wireless', 'Accessories', 450],
        ['P002', 'Mechanical Keyboard', 'Accessories', 1290],
        ['P003', 'Monitor 24"', 'Hardware', 3500],
        ['P004', 'SSD 1TB', 'Hardware', 2890],
        ['P005', 'USB Hub Type-C', 'Accessories', 690],
    ]
    for row_num, row_data in enumerate(products, 1):
        ws_master.write(row_num, 0, row_data[0], border_format)
        ws_master.write(row_num, 1, row_data[1], border_format)
        ws_master.write(row_num, 2, row_data[2], border_format)
        ws_master.write(row_num, 3, row_data[3], currency_format)

    # Members Table
    ws_master.write('F1', 'รหัสสมาชิก (Member_ID)', header_format)
    ws_master.write('G1', 'ชื่อ-นามสกุล (Member_Name)', header_format)
    ws_master.write('H1', 'ประเภทสมาชิก (Tier)', header_format)

    members = [
        ['M001', 'สมชาย ใจดี', 'VIP'],
        ['M002', 'สมหญิง รักเรียน', 'Regular'],
        ['M003', 'มานะ พากเพียร', 'VIP'],
        ['M004', 'ปิติ รักสงบ', 'Regular'],
    ]
    for row_num, row_data in enumerate(members, 1):
        ws_master.write(row_num, 5, row_data[0], border_format)
        ws_master.write(row_num, 6, row_data[1], border_format)
        ws_master.write(row_num, 7, row_data[2], border_format)

    ws_master.autofit()

    # --- SalesTransaction Sheet ---
    ws_sales = workbook.add_worksheet('SalesTransaction')
    headers = [
        'ลำดับ (No.)', 'วันที่ (Date)', 'รหัสสมาชิก (Member_ID)', 'ชื่อลูกค้า (Customer_Name)',
        'รหัสสินค้า (Product_ID)', 'ชื่อสินค้า (Product_Name)', 'ราคาต่อหน่วย (Unit_Price)',
        'จำนวน (Quantity)', 'รวมเป็นเงิน (Total)', 'ส่วนลด (Discount)', 'ยอดสุทธิ (Net_Total)',
        'ประเภทสมาชิก (Tier)', 'หมวดหมู่ (Category)'
    ]

    for col_num, header in enumerate(headers):
        ws_sales.write(0, col_num, header, header_format)

    num_transactions = 15
    start_date = datetime(2026, 7, 1)

    for i in range(1, num_transactions + 1):
        row = i
        # 1. No.
        ws_sales.write(row, 0, i, border_format)
        
        # 2. Date
        trans_date = start_date + timedelta(days=random.randint(0, 15))
        ws_sales.write_datetime(row, 1, trans_date, date_format)
        
        # 3. Member_ID
        member_id = random.choice(['M001', 'M002', 'M003', 'M004'])
        ws_sales.write(row, 2, member_id, border_format)
        
        # 4. Customer_Name
        ws_sales.write_formula(row, 3, f'=VLOOKUP(C{row+1}, MasterData!$F$2:$H$5, 2, FALSE)', border_format)
        
        # 5. Product_ID
        product_id = random.choice(['P001', 'P002', 'P003', 'P004', 'P005'])
        ws_sales.write(row, 4, product_id, border_format)
        
        # 6. Product_Name
        ws_sales.write_formula(row, 5, f'=VLOOKUP(E{row+1}, MasterData!$A$2:$D$6, 2, FALSE)', border_format)
        
        # 7. Unit_Price
        ws_sales.write_formula(row, 6, f'=VLOOKUP(E{row+1}, MasterData!$A$2:$D$6, 4, FALSE)', currency_format)
        
        # 8. Quantity
        qty = random.randint(1, 5)
        ws_sales.write(row, 7, qty, border_format)
        
        # 9. Total
        ws_sales.write_formula(row, 8, f'=G{row+1}*H{row+1}', currency_format)
        
        # 10. Discount (IF condition)
        # IF Tier is VIP, 10% of Total; IF Regular, 5% of Total
        ws_sales.write_formula(row, 9, f'=IF(L{row+1}="VIP", I{row+1}*10%, IF(L{row+1}="Regular", I{row+1}*5%, 0))', currency_format)
        
        # 11. Net_Total
        ws_sales.write_formula(row, 10, f'=I{row+1}-J{row+1}', currency_format)
        
        # 12. Tier (Hidden column for calculations)
        ws_sales.write_formula(row, 11, f'=VLOOKUP(C{row+1}, MasterData!$F$2:$H$5, 3, FALSE)', border_format)
        
        # 13. Category (Hidden column for calculations)
        ws_sales.write_formula(row, 12, f'=VLOOKUP(E{row+1}, MasterData!$A$2:$D$6, 3, FALSE)', border_format)

    # Data Validation
    ws_sales.data_validation('C2:C16', {'validate': 'list', 'source': '=MasterData!$F$2:$F$5'})
    ws_sales.data_validation('E2:E16', {'validate': 'list', 'source': '=MasterData!$A$2:$A$6'})

    # Conditional Formatting for Net_Total > 5000
    ws_sales.conditional_format('K2:K16', {'type': 'cell',
                                           'criteria': '>',
                                           'value': 5000,
                                           'format': green_bg})

    # Hide Tier and Category columns as they are just helpers
    ws_sales.set_column('L:M', None, None, {'hidden': True})
    ws_sales.autofit()

    # --- Dashboard Sheet ---
    ws_dash = workbook.add_worksheet('Dashboard')

    ws_dash.write('A1', 'สรุปข้อมูลระดับบริหาร', workbook.add_format({'bold': True, 'font_size': 14}))

    # SUMIF
    ws_dash.write('A3', 'ยอดสุทธิรวมตามหมวดหมู่', header_format)
    ws_dash.write('B3', 'ยอดสุทธิ (Net_Total)', header_format)
    ws_dash.write('A4', 'Accessories', border_format)
    ws_dash.write('A5', 'Hardware', border_format)

    ws_dash.write_formula('B4', '=SUMIF(SalesTransaction!$M$2:$M$16, A4, SalesTransaction!$K$2:$K$16)', currency_format)
    ws_dash.write_formula('B5', '=SUMIF(SalesTransaction!$M$2:$M$16, A5, SalesTransaction!$K$2:$K$16)', currency_format)

    # COUNTIF
    ws_dash.write('A7', 'จำนวนการใช้บริการแยกระดับสมาชิก', header_format)
    ws_dash.write('B7', 'จำนวนครั้ง', header_format)
    ws_dash.write('A8', 'VIP', border_format)
    ws_dash.write('A9', 'Regular', border_format)

    ws_dash.write_formula('B8', '=COUNTIF(SalesTransaction!$L$2:$L$16, A8)', border_format)
    ws_dash.write_formula('B9', '=COUNTIF(SalesTransaction!$L$2:$L$16, A9)', border_format)

    ws_dash.write('A11', 'หมายเหตุ: การสร้าง PivotTable และ PivotChart สามารถทำได้โดยคลุมข้อมูลใน Sheet SalesTransaction แล้วเลือก Insert -> PivotTable', workbook.add_format({'italic': True, 'font_color': 'gray'}))

    ws_dash.autofit()

    workbook.close()
    print("Lab Excel file 'IT_Smart_Solutions_Lab.xlsx' created successfully.")

if __name__ == '__main__':
    create_lab()

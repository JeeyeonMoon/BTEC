import tkinter as tk
from tkinter import ttk, messagebox

class TravelExpenseCalculator:
    def __init__(self):
        self.domestic_rates = {
            "숙박비": {"서울": 100000, "도서": 80000, "그 외": 70000},
            "식비": {"대표/부대표/고문": 40000, "임직원": 20000},
            "식비_13시이후": {"대표/부대표/고문": 20000, "임직원": 10000},
            "식비_근거리": {"대표/부대표/고문": 20000, "임직원": 10000},
            "일비": {"대표/부대표/고문": 20000, "임직원": 10000}
        }
        self.nearby_rate_per_km = 250
    
    def calculate_expense(self, employee_type, trip_type, nights, days, transport_silbi, transport_fixed, meal_after_13, distance_km, custom_lodging, car_type, location):
        lodging_cost = 0
        meal_cost = 0
        daily_allowance = 0
        travel_cost = 0

        if trip_type == "근거리":
            meal_cost = self.domestic_rates["식비_근거리"][employee_type] *days
            travel_cost = distance_km * self.nearby_rate_per_km * 2 *days
            if car_type == "전기차":
                travel_cost *= 0.7
        else:
            lodging_cost = custom_lodging if employee_type == "대표/부대표/고문" else self.domestic_rates["숙박비"].get(location, 0) * nights
            if meal_after_13 and days > 0:
                meal_cost = self.domestic_rates["식비_13시이후"][employee_type] + (self.domestic_rates["식비"][employee_type] * (days - 1))
            else:
                meal_cost = self.domestic_rates["식비"][employee_type] * days
            daily_allowance = self.domestic_rates["일비"][employee_type] * days
            travel_cost = transport_silbi + transport_fixed
        
        total = travel_cost + lodging_cost + meal_cost + daily_allowance
        return total, travel_cost, lodging_cost, meal_cost, daily_allowance

def safe_int(entry):
    try:
        return int(entry.get().strip()) if entry.get().strip() else 0
    except ValueError:
        messagebox.showerror("입력 오류", "숫자만 입력할 수 있습니다.")
        return 0

def reset_fields():
    distance_entry.delete(0, tk.END)
    nights_entry.delete(0, tk.END)
    days_entry.delete(0, tk.END)
    transport_silbi_entry.delete(0, tk.END)  # 실비 초기화
    transport_fixed_entry.delete(0, tk.END)  # 정액 초기화
    lodging_entry.delete(0, tk.END)
    meal_after_13_var.set(False)
    car_type_var.set("")
    transport_type_var.set("")
    location_var.set("")  # 출장 지역 초기화
    for widget in transport_frame.winfo_children():
        widget.grid_forget()  # 교통비 관련 입력 필드 초기화
    result_text.set("")  # 결과 초기화

def update_fields(*args):
    reset_fields()
    for widget in input_frame.winfo_children():
        widget.grid_forget()
    
    trip_type = trip_type_var.get()
    employee_type = employee_type_var.get()
    
    if trip_type == "근거리":
        tk.Label(input_frame, text="출장기간 (일)").grid(row=0, column=0)
        days_entry.grid(row=0, column=1)
        tk.Label(input_frame, text="편도 거리 (km)").grid(row=1, column=0)
        distance_entry.grid(row=1, column=1)
        tk.Label(input_frame, text="차량 종류").grid(row=2, column=0)
        car_type_menu.grid(row=2, column=1)

        meal_after_13_check.grid_forget()

    else:
        tk.Label(input_frame, text="출장기간 (박)").grid(row=0, column=0)
        nights_entry.grid(row=0, column=1)
        tk.Label(input_frame, text="출장기간 (일)").grid(row=1, column=0)
        days_entry.grid(row=1, column=1)

        # 교통수단 선택
        tk.Label(input_frame, text="교통수단").grid(row=2, column=0)
        transport_type_menu.grid(row=2, column=1)

        # 숙박비 입력란 조건 추가
        if employee_type == "대표/부대표/고문":
            tk.Label(input_frame, text="숙박비").grid(row=3, column=0)
            lodging_entry.grid(row=3, column=1)

        # 출장 지역 선택
        if employee_type != "대표/부대표/고문":  # 조건 추가
            tk.Label(input_frame, text="출장 지역 선택").grid(row=4, column=0)
            location_menu.grid(row=4, column=1)
        
            # 체크박스를 하단에 배치
        meal_after_13_check.grid(row=5, column=0, columnspan=2)  # 체크박스 위치 조정


def update_transport_fields(*args):
    for widget in transport_frame.winfo_children():
        widget.grid_forget()

    transport_type = transport_type_var.get()
    
    if transport_type in ["철도", "선박", "항공"]:
        tk.Label(transport_frame, text="교통비").grid(row=1, column=0)
        transport_silbi_entry.grid(row=1, column=1)
        transport_fixed_entry.delete(0, tk.END)  # 정액 입력 초기화
    elif transport_type == "자동차":
        tk.Label(transport_frame, text="정액-고속철 일반실 운임 요금").grid(row=0, column=0)
        tk.Label(transport_frame, text="교통비").grid(row=1, column=0)
        transport_fixed_entry.grid(row=1, column=1)
        transport_silbi_entry.delete(0, tk.END)  # 실비 입력 초기화

def calculate():
    employee_type = employee_type_var.get()
    trip_type = trip_type_var.get()
    
    # 입력값을 안전하게 가져오기
    nights = safe_int(nights_entry)
    days = safe_int(days_entry)
    transport_silbi = safe_int(transport_silbi_entry)
    transport_fixed = safe_int(transport_fixed_entry)
    meal_after_13 = meal_after_13_var.get()
    distance_km = safe_int(distance_entry)
    custom_lodging = safe_int(lodging_entry) if employee_type == "대표/부대표/고문" else 0
    car_type = car_type_var.get()
    location = location_var.get()
    
    # 계산 수행
    total, travel, lodging, meal, daily = calculator.calculate_expense(
        employee_type, trip_type, nights, days, transport_silbi, transport_fixed, meal_after_13, distance_km, custom_lodging, car_type, location)
    
    # 결과 표시
    result_text.set(
        f"총 비용: {total}원\n"
        f"교통비: {travel}원\n"
        f"숙박비: {lodging}원\n"
        f"식비: {meal}원\n"
        f"일비: {daily}원"
    )

calculator = TravelExpenseCalculator()

root = tk.Tk()
root.title("출장 여비 계산기")

tk.Label(root, text="직급").grid(row=0, column=0)
employee_type_var = tk.StringVar()
ttk.Combobox(root, textvariable=employee_type_var, values=["대표/부대표/고문", "임직원"]).grid(row=0, column=1)
employee_type_var.trace("w", update_fields)

tk.Label(root, text="출장 유형").grid(row=1, column=0)
trip_type_var = tk.StringVar()
ttk.Combobox(root, textvariable=trip_type_var, values=["근거리", "국내", "국외", "파견"]).grid(row=1, column=1)
trip_type_var.trace("w", update_fields)

input_frame = tk.Frame(root)
input_frame.grid(row=2, column=0, columnspan=2)

# 교통비 입력란 추가
transport_frame = tk.Frame(root)
transport_frame.grid(row=3, column=0, columnspan=2)

distance_entry = tk.Entry(input_frame)
nights_entry = tk.Entry(input_frame)
days_entry = tk.Entry(input_frame)
lodging_entry = tk.Entry(input_frame)
car_type_var = tk.StringVar()
car_type_menu = ttk.Combobox(input_frame, textvariable=car_type_var, values=["일반", "전기차"], state="readonly")
meal_after_13_var = tk.BooleanVar()
meal_after_13_check = tk.Checkbutton(input_frame, text="13시 이후 출발", variable=meal_after_13_var)

# 출장 지역 선택 변수 및 메뉴 추가
location_var = tk.StringVar()
location_menu = ttk.Combobox(input_frame, textvariable=location_var, values=["서울", "도서", "그 외"], state="readonly")

# 교통비 관련 입력 필드 추가
transport_type_var = tk.StringVar()
transport_type_menu = ttk.Combobox(input_frame, textvariable=transport_type_var, values=["철도", "선박", "항공", "자동차"], state="readonly")
transport_type_var.trace("w", update_transport_fields)

# 교통비 실비 및 정액 입력 필드
transport_silbi_entry = tk.Entry(transport_frame)
transport_fixed_entry = tk.Entry(transport_frame)

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, justify="left").grid(row=4, column=0, columnspan=2)

tk.Button(root, text="계산하기", command=calculate).grid(row=5, column=0, columnspan=2)

root.mainloop()
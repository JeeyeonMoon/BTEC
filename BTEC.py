import streamlit as st

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
            meal_cost = self.domestic_rates["식비_근거리"][employee_type] * days
            travel_cost = distance_km * self.nearby_rate_per_km * 2 * days
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

# Streamlit UI 구성
st.title("출장 여비 계산기")

calculator = TravelExpenseCalculator()

# 사용자 입력 받기
employee_type = st.selectbox("직급", ["대표/부대표/고문", "임직원"])
trip_type = st.selectbox("출장 유형", ["근거리", "국내", "국외", "파견"])

# 출장 지역 선택
if trip_type in ["국내", "국외", "파견"]:
    with st.container():
        location = st.selectbox("출장 지역", ["서울", "도서", "그 외"])
else:
    location = ""

distance_km = 0  
custom_lodging = 0  
car_type = "일반"  

if trip_type == "근거리":
    days = st.number_input("출장 기간 (일)", min_value=1, step=1)
    distance_km = st.number_input("편도 거리 (km)", min_value=0, step=1)
    car_type = st.selectbox("차량 종류", ["일반", "전기차"])
    nights = 0
    transport_silbi = 0
    transport_fixed = 0
    meal_after_13 = False
else:
    nights = st.number_input("출장 기간 (박)", min_value=0, step=1)
    days = st.number_input("출장 기간 (일)", min_value=1, step=1)
    transport_type = st.selectbox("교통 수단", ["철도", "선박", "항공", "자동차"])
    
    if employee_type == "대표/부대표/고문":
        custom_lodging = st.number_input("숙박비 입력", min_value=0, step=1000)
    
    # 교통비 입력 칸을 선택한 교통수단 바로 아래 배치
    with st.container():
        if transport_type in ["철도", "선박", "항공"]:
            transport_silbi = st.number_input("교통비 (실비)", min_value=0, step=1000)
            transport_fixed = 0
        else:
            transport_fixed = st.number_input("고속철 일반실 운임 (정액)", min_value=0, step=1000)
            transport_silbi = 0
    
    meal_after_13 = st.checkbox("13시 이후 출발")

# 계산 버튼
if st.button("계산하기"):
    total, travel, lodging, meal, daily = calculator.calculate_expense(
        employee_type, trip_type, nights, days, transport_silbi, transport_fixed, meal_after_13, distance_km, custom_lodging, car_type, location
    )

    st.subheader("계산 결과")
    st.write(f"총 비용: {total}원")
    st.write(f"교통비: {travel}원")
    st.write(f"숙박비: {lodging}원")
    st.write(f"식비: {meal}원")
    st.write(f"일비: {daily}원")

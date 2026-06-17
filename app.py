import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================

st.set_page_config(
    page_title="APP TÍNH THUẾ THU NHẬP CÁ NHÂN",
    page_icon="💰"
)

# =========================
# GIAO DIỆN
# =========================

st.image("logo.jpg")

st.title("APP TÍNH THUẾ THU NHẬP CÁ NHÂN")
st.subheader("ĐỀ TÀI 7 - ĐOÀN ANH GIÀU")

# =========================
# NHẬP DỮ LIỆU
# =========================

salary = st.number_input(
    "Nhập lương tháng (VNĐ)",
    min_value=0,
    value=30000000,
    step=1000000
)

bonus = st.number_input(
    "Nhập tiền thưởng / thu nhập khác (VNĐ)",
    min_value=0,
    value=0,
    step=1000000
)

dependents = st.number_input(
    "Nhập số người phụ thuộc",
    min_value=0,
    value=0
)

# =========================
# THÔNG SỐ LUẬT MỚI
# =========================

PERSONAL_DEDUCTION = 15_500_000
DEPENDENT_DEDUCTION = 6_200_000

# =========================
# HÀM TÍNH THUẾ
# =========================

def calculate_tax(income):

    brackets = [
        (10_000_000, 0.05),
        (30_000_000, 0.10),
        (60_000_000, 0.20),
        (100_000_000, 0.30),
        (float("inf"), 0.35)
    ]

    tax = 0
    previous = 0

    for limit, rate in brackets:

        if income > limit:
            tax += (limit - previous) * rate
            previous = limit

        else:
            tax += (income - previous) * rate
            break

    return max(0, tax)

# =========================
# NÚT TÍNH THUẾ
# =========================

if st.button("TÍNH THUẾ"):

    # Tổng thu nhập
    gross_income = salary + bonus

    # Bảo hiểm tự động 10.5%
    insurance = salary * 0.105

    # Thu nhập tính thuế
    taxable_income = (
        gross_income
        - insurance
        - PERSONAL_DEDUCTION
        - dependents * DEPENDENT_DEDUCTION
    )

    taxable_income = max(0, taxable_income)

    # Thuế phải nộp
    tax = calculate_tax(taxable_income)

    # Thu nhập thực nhận
    net_income = gross_income - insurance - tax

    # Thuế năm
    annual_tax = tax * 12

    # Thu nhập năm
    annual_net_income = net_income * 12

    # =====================
    # KẾT QUẢ
    # =====================

    st.subheader("📊 KẾT QUẢ")

    st.success(
        f"Tổng thu nhập: {gross_income:,.0f} VNĐ"
    )

    st.success(
        f"Tiền bảo hiểm (10,5%): {insurance:,.0f} VNĐ"
    )

    st.success(
        f"Thu nhập tính thuế: {taxable_income:,.0f} VNĐ"
    )

    st.success(
        f"Thuế TNCN phải nộp: {tax:,.0f} VNĐ/tháng"
    )

    st.success(
        f"Thu nhập thực nhận: {net_income:,.0f} VNĐ/tháng"
    )

    st.success(
        f"Thuế dự kiến cả năm: {annual_tax:,.0f} VNĐ"
    )

    st.success(
        f"Thu nhập thực nhận cả năm: {annual_net_income:,.0f} VNĐ"
    )

    # =====================
    # TAX HEALTH SCORE
    # =====================

    score = 100

    ratio = tax / gross_income if gross_income > 0 else 0

    if ratio > 0.20:
        score -= 40
    elif ratio > 0.15:
        score -= 30
    elif ratio > 0.10:
        score -= 20
    elif ratio > 0.05:
        score -= 10

    score += min(dependents * 5, 20)
    score = max(0, min(score, 100))

    st.subheader("🏆 TAX HEALTH SCORE")

    st.progress(score / 100)

    st.info(
        f"Điểm sức khỏe thuế: {score}/100"
    )

    # =====================
    # AI ADVISOR
    # =====================

    st.subheader("🤖 AI TAX ADVISOR")

    if score >= 80:
        st.success(
            "Mức thuế hiện tại khá tối ưu."
        )

    elif score >= 60:
        st.warning(
            "Mức thuế hiện tại ở mức trung bình."
        )

    else:
        st.error(
            "Gánh nặng thuế tương đối cao."
        )

    if dependents > 0:
        st.info(
            f"Bạn đang được giảm trừ cho {dependents} người phụ thuộc."
        )

    annual_deduction = (
        dependents
        * DEPENDENT_DEDUCTION
        * 12
    )

    st.info(
        f"Tổng giảm trừ người phụ thuộc mỗi năm: {annual_deduction:,.0f} VNĐ"
    )

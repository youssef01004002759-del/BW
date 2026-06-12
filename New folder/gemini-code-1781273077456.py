import streamlit as st
import math

# --- الدوال الحسابية الأساسية ---
def shear_strength(c, phi, sigma):
    phi_rad = math.radians(phi)
    return c + sigma * math.tan(phi_rad)

def check_breakwater_stability(c, phi, gamma, height, slope_angle, width, gamma_water):
    phi_rad = math.radians(phi)
    
    # 1. حساب الوزن
    weight = gamma * height * width
    
    # 2. حساب القوة الجانبية للمياه
    driving_force = 0.5 * gamma_water * (height ** 2)
    
    # 3. معامل الأمان ضد الانزلاق (Fs)
    resisting_force = (weight * math.tan(phi_rad)) + (c * width)
    fs_sliding = resisting_force / driving_force if driving_force > 0 else 0
    
    # 4. معامل الأمان ضد الانقلاب (Fov)
    overturning_moment = driving_force * (height / 3.0)
    resisting_moment = weight * (width / 2.0)
    fov_overturning = resisting_moment / overturning_moment if overturning_moment > 0 else 0
    
    return fs_sliding, fov_overturning

# --- واجهة المستخدم التفاعلية (Streamlit) ---
st.set_page_config(page_title="Breakwater Stability Model", layout="centered")

st.title("🌊 Breakwater Stability Analysis Model")
st.markdown("عدّل البارامترات من القائمة الجانبية لتحديث حسابات معاملات الأمان فوراً.")

# القائمة الجانبية للمدخلات (Sidebar)
st.sidebar.header("📋 Input Parameters")

cohesion = st.sidebar.number_input("Cohesion (c) [kPa]", min_value=0.0, value=18.0, step=1.0)
internal_friction_angle = st.sidebar.slider("Internal Friction Angle (phi) [degrees]", min_value=0, max_value=90, value=35)
unit_weight = st.sidebar.number_input("Unit Weight of Material (gamma) [kN/m³]", min_value=0.0, value=21.0, step=0.5)
height = st.sidebar.number_input("Height of Breakwater (H) [m]", min_value=0.5, value=3.0, step=0.1)
slope_angle = st.sidebar.slider("Slope Angle [degrees]", min_value=0, max_value=90, value=42)
base_width = st.sidebar.number_input("Base Width (B) [m]", min_value=0.5, value=4.0, step=0.1)

st.sidebar.subheader("Water Properties")
gamma_water = st.sidebar.number_input("Unit Weight of Water [kN/m³]", min_value=9.0, value=10.0, step=0.1)

# حساب النتائج تلقائياً عند تغيير أي قيمة
fs, fov = check_breakwater_stability(cohesion, internal_friction_angle, unit_weight, height, slope_angle, base_width, gamma_water)

# --- عرض النتائج في الصفحة الرئيسية ---
st.subheader("📊 Analysis Results")

col1, col2 = st.columns(2)

with col1:
    st.metric(label="Factor of Safety against Sliding (Fs)", value=f"{fs:.2f}")
    if fs >= 1.5:
        st.success("✅ Stable against sliding")
    else:
        st.error("❌ Unstable against sliding (Fs < 1.5)")

with col2:
    st.metric(label="Factor of Safety against Overturning (Fov)", value=f"{fov:.2f}")
    if fov >= 2.0:
        st.success("✅ Stable against overturning")
    else:
        st.error("❌ Unstable against overturning (Fov < 2.0)")

# إضافة جدول ملخص للمدخلات الحالية لتوثيق الحسابات
st.markdown("---")
st.subheader("📝 Current Design Summary")
data = {
    "Parameter": ["Cohesion (c)", "Friction Angle (phi)", "Unit Weight", "Height", "Base Width"],
    "Value": [f"{cohesion} kPa", f"{internal_friction_angle}°", f"{unit_weight} kN/m³", f"{height} m", f"{base_width} m"]
}
st.table(data)
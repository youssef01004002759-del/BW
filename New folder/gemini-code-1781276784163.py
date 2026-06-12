import streamlit as st
import math

# --- الدوال الحسابية الأساسية ---
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

def check_slope_stability(c, phi, gamma, slope_angle, failure_depth, water_depth, gamma_water):
    """
    Calculate Factor of Safety against Slope Failure using Infinite Slope Method with Seepage.
    """
    beta = math.radians(slope_angle)
    phi_rad = math.radians(phi)
    
    # إجهاد القوى الدافعة (Driving Stress) بفعل الوزن والجاذبية
    driving_stress = gamma * failure_depth * math.sin(beta) * math.cos(beta)
    
    # ضغط مياه المسام (Pore Water Pressure)
    u = gamma_water * water_depth * (math.cos(beta) ** 2)
    
    # الإجهاد العمودي الكلي (Total Normal Stress)
    total_normal_stress = gamma * failure_depth * (math.cos(beta) ** 2)
    
    # الإجهاد العمودي الفعال (Effective Normal Stress)
    effective_normal_stress = total_normal_stress - u
    
    # مقاومة القص المقاومة (Resisting Shear Strength - Mohr-Coulomb)
    resisting_stress = c + effective_normal_stress * math.tan(phi_rad)
    
    # معامل الأمان للميل
    fs_slope = resisting_stress / driving_stress if driving_stress > 0 else float('inf')
    return fs_slope

# --- واجهة المستخدم التفاعلية (Streamlit) ---
st.set_page_config(page_title="Breakwater & Slope Stability Model", layout="wide")

st.title("🌊 Comprehensive Breakwater & Slope Stability Model")
st.markdown("عدّل البارامترات من القائمة الجانبية لتحديث حسابات معاملات الأمان فوراً لجميع حالات الانهيار.")

# القائمة الجانبية للمدخلات (Sidebar)
st.sidebar.header("📋 Input Parameters")

# بارامترات التربة والمنشأ الأساسية
st.sidebar.subheader("1. General Properties")
cohesion = st.sidebar.number_input("Cohesion (c) [kPa]", min_value=0.0, value=18.0, step=1.0)
internal_friction_angle = st.sidebar.slider("Internal Friction Angle (phi) [degrees]", min_value=0, max_value=90, value=35)
unit_weight = st.sidebar.number_input("Unit Weight of Soil/Material (gamma) [kN/m³]", min_value=0.0, value=21.0, step=0.5)

st.sidebar.subheader("2. Structure Dimensions")
height = st.sidebar.number_input("Height of Breakwater (H) [m]", min_value=0.5, value=3.0, step=0.1)
base_width = st.sidebar.number_input("Base Width (B) [m]", min_value=0.5, value=4.0, step=0.1)
slope_angle = st.sidebar.slider("Slope Angle (beta) [degrees]", min_value=1, max_value=89, value=42)

# البارامترات الجديدة الخاصة باستقرار الميول والمياه
st.sidebar.subheader("3. Slope & Water Parameters")
failure_depth = st.sidebar.number_input("Failure Plane Depth (z) [m]", min_value=0.5, value=2.0, step=0.1)
water_depth = st.sidebar.number_input("Water Depth above Failure Plane (hw) [m]", min_value=0.0, value=1.5, step=0.1)
gamma_water = st.sidebar.number_input("Unit Weight of Water [kN/m³]", min_value=9.0, value=10.0, step=0.1)

# قيود منطقية للمدخلات
if water_depth > failure_depth:
    st.sidebar.error("تنبيه: لا يمكن أن يكون ارتفاع المياه أكبر من عمق مستوى الانهيار!")

# --- الحسابات تلقائية ---
fs_sliding, fov_overturning = check_breakwater_stability(cohesion, internal_friction_angle, unit_weight, height, slope_angle, base_width, gamma_water)
fs_slope = check_slope_stability(cohesion, internal_friction_angle, unit_weight, slope_angle, failure_depth, water_depth, gamma_water)

# --- عرض النتائج في الصفحة الرئيسية ---
st.subheader("📊 Analysis Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Factor of Safety: Sliding (Fs)", value=f"{fs_sliding:.2f}")
    if fs_sliding >= 1.5:
        st.success("✅ Stable against sliding")
    else:
        st.error("❌ Unstable (Fs < 1.5)")

with col2:
    st.metric(label="Factor of Safety: Overturning (Fov)", value=f"{fov_overturning:.2f}")
    if fov_overturning >= 2.0:
        st.success("✅ Stable against overturning")
    else:
        st.error("❌ Unstable (Fov < 2.0)")

with col3:
    st.metric(label="Factor of Safety: Slope Stability (Fs_slope)", value=f"{fs_slope:.2f}")
    # كود التصميم العالمي عادة يطلب معامل أمان للميول بين 1.3 إلى 1.5
    if fs_slope >= 1.3:
        st.success("✅ Stable Slope")
    else:
        st.error("❌ Unstable Slope (Fs < 1.3)")

# جدول ملخص البيانات
st.markdown("---")
st.subheader("📝 Current Design Summary")
data = {
    "Parameter": ["Cohesion (c)", "Friction Angle (phi)", "Unit Weight", "Structure Height", "Base Width", "Slope Angle", "Failure Plane Depth (z)", "Water Depth (hw)"],
    "Value": [f"{cohesion} kPa", f"{internal_friction_angle}°", f"{unit_weight} kN/m³", f"{height} m", f"{base_width} m", f"{slope_angle}°", f"{failure_depth} m", f"{water_depth} m"]
}
st.table(data)
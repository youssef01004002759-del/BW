import streamlit as st
import math

# --- الدوال الحسابية الأساسية ---
def check_breakwater_stability(c, phi, gamma, height, slope_angle, width, gamma_water):
    phi_rad = math.radians(phi)
    weight = gamma * height * width
    driving_force = 0.5 * gamma_water * (height ** 2)
    
    resisting_force = (weight * math.tan(phi_rad)) + (c * width)
    fs_sliding = resisting_force / driving_force if driving_force > 0 else 0
    
    overturning_moment = driving_force * (height / 3.0)
    resisting_moment = weight * (width / 2.0)
    fov_overturning = resisting_moment / overturning_moment if overturning_moment > 0 else 0
    
    return fs_sliding, fov_overturning

def calculate_single_slope_fs(c, phi, gamma, slope_angle, z, hw, gamma_water):
    """حساب معامل الأمان عند عمق محدد Z"""
    beta = math.radians(slope_angle)
    phi_rad = math.radians(phi)
    
    driving_stress = gamma * z * math.sin(beta) * math.cos(beta)
    u = gamma_water * hw * (math.cos(beta) ** 2)
    total_normal_stress = gamma * z * (math.cos(beta) ** 2)
    effective_normal_stress = total_normal_stress - u
    
    resisting_stress = c + effective_normal_stress * math.tan(phi_rad)
    
    return resisting_stress / driving_stress if driving_stress > 0 else float('inf')

def find_critical_failure_plane(c, phi, gamma, slope_angle, height, saturation_ratio, gamma_water):
    """عمل Loop ذكي لتجربة كل الأعماق الممكنة وإيجاد العمق الحرِج"""
    min_fs = float('inf')
    critical_z = 0.1
    
    # تجربة أعماق تبدأ من 0.1 متر وتزيد كل 0.05 متر حتى الارتفاع الكلي للحاجز
    steps = int(height / 0.05)
    for i in range(1, steps + 1):
        z_current = i * 0.05
        hw_current = z_current * saturation_ratio  # حساب منسوب المياه الفعلي عند هذا العمق
        
        fs_current = calculate_single_slope_fs(c, phi, gamma, slope_angle, z_current, hw_current, gamma_water)
        
        # الاحتفاظ بأقل معامل أمان والعمق المقابل له
        if fs_current < min_fs:
            min_fs = fs_current
            critical_z = z_current
            
    return min_fs, critical_z

# --- واجهة المستخدم التفاعلية (Streamlit) ---
st.set_page_config(page_title="Breakwater Optimization Model", layout="wide")

st.title("🌊 Smart Breakwater & Slope Stability Optimization Model")
st.markdown("يقوم الموديل حالياً بعمل محاكاة تلقائية (Automated Loop Optimization) لتجربة جميع مستويات الانهيار الممكنة وتحديد أخطر عمق بدقة.")

# القائمة الجانبية للمدخلات (Sidebar)
st.sidebar.header("📋 Input Parameters")

st.sidebar.subheader("1. General Properties")
cohesion = st.sidebar.number_input("Cohesion (c) [kPa]", min_value=0.0, value=18.0, step=1.0)
internal_friction_angle = st.sidebar.slider("Internal Friction Angle (phi) [degrees]", min_value=0, max_value=90, value=35)
unit_weight = st.sidebar.number_input("Unit Weight of Soil (gamma) [kN/m³]", min_value=0.0, value=21.0, step=0.5)

st.sidebar.subheader("2. Structure Dimensions")
height = st.sidebar.number_input("Height of Breakwater (H) [m]", min_value=0.5, value=3.0, step=0.1)
base_width = st.sidebar.number_input("Base Width (B) [m]", min_value=0.5, value=4.0, step=0.1)
slope_angle = st.sidebar.slider("Slope Angle (beta) [degrees]", min_value=1, max_value=89, value=42)

st.sidebar.subheader("3. Environmental & Water Conditions")
# السلايدر الذكي لتحديد حالة المياه بالميل
saturation_ratio = st.sidebar.slider("Slope Saturation Ratio (r)", min_value=0.0, max_value=1.0, value=0.5, step=0.1, 
                                    help="0 = جاف تماماً، 1 = مشبع بالكامل بالماء (الحالة الأخطر)")
gamma_water = st.sidebar.number_input("Unit Weight of Water [kN/m³]", min_value=9.0, value=10.0, step=0.1)

# --- تشغيل الحسابات والمحاكاة ---
fs_sliding, fov_overturning = check_breakwater_stability(cohesion, internal_friction_angle, unit_weight, height, slope_angle, base_width, gamma_water)

# استدعاء دالة البحث الأوتوماتيكي عن الـ Z الحرجة
fs_slope, critical_z = find_critical_failure_plane(cohesion, internal_friction_angle, unit_weight, slope_angle, height, saturation_ratio, gamma_water)

# --- عرض النتائج في الصفحة الرئيسية ---
st.subheader("📊 Optimization & Analysis Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="📊 Sliding Factor of Safety (Fs)", value=f"{fs_sliding:.2f}")
    if fs_sliding >= 1.5:
        st.success("✅ Stable against sliding")
    else:
        st.error("❌ Unstable (Fs < 1.5)")

with col2:
    st.metric(label="🔄 Overturning Factor of Safety (Fov)", value=f"{fov_overturning:.2f}")
    if fov_overturning >= 2.0:
        st.success("✅ Stable against overturning")
    else:
        st.error("❌ Unstable (Fov < 2.0)")

with col3:
    st.metric(label="📉 Min Slope Stability FS (Fs_slope)", value=f"{fs_slope:.2f}")
    if fs_slope >= 1.3:
        st.success(f"✅ Stable Slope (Critical z = {critical_z:.2f} m)")
    else:
        st.error(f"❌ Unstable Slope at z = {critical_z:.2f} m")

# منشئ التنبيهات الذكي
st.markdown("---")
st.info(f"💡 **التقرير الهندسي للمحاكاة:** الموديل قام باختبار خطوط انهيار تبدأ من عمق 0.05م حتى عمق {height}م. تبيّن أن **أخطر مستوى انهيار متوقع (Critical Failure Plane)** يقع على عمق دقيق يساوي **{critical_z:.2f} متر** من السطح، وهو المستوى الذي يجب تركيز أعمال التدعيم عليه.")

# جدول ملخص البيانات
st.subheader("📝 Current Design Summary")
data = {
    "Parameter": ["Cohesion (c)", "Friction Angle (phi)", "Unit Weight", "Structure Height", "Base Width", "Slope Angle", "Critical Failure Depth (Calculated z)"],
    "Value": [f"{cohesion} kPa", f"{internal_friction_angle}°", f"{unit_weight} kN/m³", f"{height} m", f"{base_width} m", f"{slope_angle}°", f"{critical_z:.2f} m"]
}
st.table(data)
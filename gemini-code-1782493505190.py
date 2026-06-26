import streamlit as st
import streamlit.components.v1 as components

# إعدادات صفحة ستريم ليت
st.set_page_config(page_title="طلب خاص جداً ❤️", layout="centered")

# إخفاء القوائم والعلامات المائية بتاعت Streamlit عشان يبان كأنه موقعك الخاص
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stApp {background-color: #ffe6e6;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# كود HTML و JS مخصص عشان شكل القلوب وحركة الزرار
html_code = """
<!DOCTYPE html>
<html dir="rtl">
<head>
    <style>
        body {
            background-color: #ffe6e6;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow: hidden; /* عشان ميعملش سكرول لما الزرار يطير */
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .container {
            text-align: center;
            width: 100%;
        }
        h1 {
            color: #cc0000;
            font-size: 2.5em;
            margin-bottom: 30px;
        }
        .hearts {
            font-size: 30px;
            letter-spacing: 10px;
            margin: 15px;
        }
        .buttons-area {
            position: relative;
            width: 100%;
            height: 300px; /* المساحة اللي هيهرب فيها الزرار */
            margin-top: 20px;
        }
        .btn {
            font-size: 20px;
            font-weight: bold;
            padding: 12px 30px;
            border-radius: 25px;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        #btn-yes {
            background-color: white;
            color: red;
            position: absolute;
            right: 30%; /* مكان ثابت */
        }
        #btn-no {
            background-color: white;
            color: black;
            position: absolute;
            right: 55%;
            transition: all 0.15s ease-out; /* حركة ناعمة */
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="hearts">💖 💕 💖 💕 💖 💕 💖</div>
        <h1>يا ياسو، ممكن بوسة؟<br><br><span style="font-size: 0.6em; color: #ff3366;">- حبيبك جوو</span></h1>
        <div class="hearts">💞 💓 💞 💓 💞 💓 💞</div>
        
        <div class="buttons-area" id="area">
            <!-- لما توافق، الشاشة كلها هتتغير للرسالة دي -->
            <button id="btn-yes" class="btn" onclick="document.body.innerHTML='<h1 style=\\'color:#cc0000; margin-top: 35vh; text-align:center;\\'>احلى بوسه للحلويات بتاعتي ❤️<br><br>- جوو</h1>'">أكيد ❤️</button>
            <button id="btn-no" class="btn">لا 💔</button>
        </div>
    </div>

    <script>
        const btnNo = document.getElementById('btn-no');
        const area = document.getElementById('area');

        function moveButton(e) {
            if(e) e.preventDefault(); // عشان يمنع الدوسة لو من موبايل
            
            // حساب أقصى طول وعرض ممكن الزرار يروحلهم جوه المنطقة المحددة
            const maxX = area.clientWidth - btnNo.clientWidth;
            const maxY = area.clientHeight - btnNo.clientHeight;
            
            // أرقام عشوائية للمكان الجديد
            const randomX = Math.floor(Math.random() * maxX);
            const randomY = Math.floor(Math.random() * maxY);
            
            // تغيير مكان الزرار
            btnNo.style.right = 'auto'; // بنلغي الـ right الأساسي
            btnNo.style.left = randomX + 'px';
            btnNo.style.top = randomY + 'px';
        }

        // لما الماوس يقرب من الزرار (للكمبيوتر)
        btnNo.addEventListener('mouseover', moveButton);
        
        // لما تحاول تلمسه بصابعها (للموبايل)
        btnNo.addEventListener('touchstart', moveButton);
    </script>
</body>
</html>
"""

# عرض كود الويب جوه صفحة ستريم ليت
components.html(html_code, height=700)
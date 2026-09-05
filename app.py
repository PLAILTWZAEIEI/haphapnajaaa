import streamlit as st

st.set_page_config(page_title="มีของขวัญมาส่ง!", page_icon="🎁")

st.title("🎁 มีของขวัญสุดพิเศษส่งถึงคุณ!")
st.write("กรุณายืนยันตัวตนก่อนเปิดกล่องของขวัญ...")

# สเต็ปที่ 1: ให้กรอกชื่อและอายุ
name = st.text_input("คุณชื่ออะไร?:", placeholder="พิมพ์ชื่อของคุณที่นี่")
age = st.number_input("อายุเท่าไหร่แล้ว?:", min_value=1, max_value=100, value=20)

# ปุ่มกดเปิดเซอร์ไพรส์
if st.button("✨ กดเพื่อรับของขวัญสุดพิเศษ ✨"):
    if name.strip() == "":
        st.warning("กรุณากรอกชื่อก่อนน้า!")
    else:
        # เอฟเฟกต์พลุและลูกโป่ง
        st.balloons()
        st.snow()
        
        st.markdown("---")
        st.header(f"🎉 สุขสันต์วันเกิดนะ {name}! 🎉")
        st.subheader(f"ขอให้มีความสุขมากๆ ในวัย {age} ขวบครับ! ✨")
        
        # แสดงเทียนตามอายุ
        st.write("🎂 **เค้กวันเกิดสุดพิเศษของคุณ:**")
        st.write("🔥 " * age)
        
        # รูปเค้กเซอร์ไพรส์
        st.image(
            "https://images.unsplash.com/photo-1578985545062-69928b1d9587",
            caption=f"Happy Birthday {name}!",
            use_container_width=True
        )

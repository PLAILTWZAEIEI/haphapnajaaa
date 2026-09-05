import streamlit as st

st.set_page_config(page_title="มีของขวัญมาให้!", page_icon="🎁")

st.title("🎁 มีพัสดุส่งถึงคุณ!")
st.write("มีคนส่งของขวัญมาให้ ลองเปิดดูสิ...")

# สร้างตัวแปรไว้เก็บสถานะการเปิดกล่อง
if 'opened' not in st.session_state:
    st.session_state.opened = False

# ถ้ายังไม่เปิด ให้กดปุ่มเปิดกล่อง
if not st.session_state.opened:
    if st.button("🎁 กดเพื่อเปิดกล่องของขวัญ"):
        st.session_state.opened = True
        st.rerun()

# พอเปิดกล่องแล้ว ค่อยเฉลยหน้าเค้ก
if st.session_state.opened:
    st.balloons()
    st.success("🎉 สุขสันต์วันเกิดนะ!")
    
    name = st.text_input("กรอกชื่อเจ้าของวันเกิด:", "เพื่อน")
    age = st.number_input("อายุปีนี้กี่ขวบแล้ว?:", min_value=1, max_value=100, value=20)

    st.write("เทียนบนหน้าเค้ก:")
    st.write("🔥 " * age)

    st.image(
        "https://images.unsplash.com/photo-1578985545062-69928b1d9587",
        caption=f"Happy Birthday {name}!",
        use_container_width=True
    )

    if st.button("🎂 กดเป่าเทียนเลย!"):
        st.snow()
        st.balloons()
        st.success(f"ขอให้มีความสุขมากๆ ในวัย {age} ขวบครับ! ✨")

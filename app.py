import streamlit as st

st.set_page_config(page_title="Happy Birthday!", page_icon="🎂")

st.title("Happy Birthday!")
st.subheader("เค้กวันเกิดสุดพิเศษเพื่อเธอ")

name = st.text_input("กรอกชื่อเจ้าของวันเกิด:", "เพื่อน")
age = st.number_input("อายุปีนี้กี่ขวบแล้ว?:", min_value=1, max_value=100, value=20)

st.write("เทียนบนหน้าเค้ก:")
st.write("🔥 " * age)

st.image(
    "https://images.unsplash.com/photo-1578985545062-69928b1d9587",
    caption=f"Happy Birthday {name}!",
    use_container_width=True
)

if st.button("กดเป่าเทียนตรงนี้เลย!"):
    st.balloons()
    st.snow()
    st.success(f"สุขสันต์วันเกิดนะ {name}! ขอให้มีความสุขมากๆ ในวัย {age} ขวบครับ")

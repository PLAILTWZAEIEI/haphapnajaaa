import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="...", page_icon="✨")

# ใช้ Session State ควบคุมสเต็ปหน้าจอ
if 'step' not in st.session_state:
    st.session_state.step = "input"

if st.session_state.step == "input":
    # หน้าแรก: ถามคำถามแบบเรียบๆ ไม่บอกว่าเป็นวันเกิด
    name = st.text_input("ชื่อไรน้ออ:", placeholder="พิมพ์ชื่อตรงนี้เลย")
    age = st.number_input("อายุเท่าไหร่แล้วน้าา:", min_value=1, max_value=100, value=20)
    
    if st.button("ถัดไป ➔"):
        if name.strip() != "":
            st.session_state.name = name
            st.session_state.age = age
            st.session_state.step = "loading"
            st.rerun()
        else:
            st.warning("บอกชื่อหน่อยน้าา")

elif st.session_state.step == "loading":
    # สเต็ปหลอก: แกล้งทำเป็นกำลังประมวลผลคำนวณสร้างภาพจากสมการ
    with st.spinner("กำลังประมวลผลและคำนวณสร้างภาพจากสมการ..."):
        time.sleep(1.5)
    st.session_state.step = "surprise"
    st.rerun()

else:
    # --- หน้าเฉลยเค้ก 3D จากสมการคณิตศาสตร์ ---
    st.balloons()
    st.header(f"✨ สุขสันต์วันเกิดนะจ๊ะ {st.session_state.name}!")
    
    # ฟังก์ชันสร้างสมการพิกัดทรงกระบอก (Cylinder Equations)
    def create_cylinder(r, h, z_offset, color):
        theta = np.linspace(0, 2*np.pi, 100)
        z = np.linspace(0, h, 20)
        theta, z = np.meshgrid(theta, z)
        # สมการ Parametric: x = r*cos(theta), y = r*sin(theta)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = z + z_offset
        return go.Surface(x=x, y=y, z=z, colorscale=[[0, color], [1, color]], showscale=False, opacity=0.9)

    fig = go.Figure()
    
    # คำนวณเลเยอร์ชั้นเค้ก 3D
    fig.add_trace(create_cylinder(r=2.0, h=1.0, z_offset=0, color="#FFC0CB"))   # ฐานล่าง
    fig.add_trace(create_cylinder(r=1.5, h=0.8, z_offset=1.0, color="#FFB6C1")) # ชั้นบน

    # คำนวณสมการตำแหน่งปักเทียน 3D ตามจำนวนอายุจริง
    age = st.session_state.age
    for i in range(age):
        angle = (2 * np.pi / age) * i
        cx, cy = 1.2 * np.cos(angle), 1.2 * np.sin(angle)
        fig.add_trace(go.Scatter3d(
            x=[cx, cx], y=[cy, cy], z=[1.8, 2.3],
            mode='lines',
            line=dict(color='yellow', width=5),
            showlegend=False
        ))

    # ปรับแต่งมุมมองเค้ก 3D ให้หมุนดูได้รอบทิศ
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )

    # แสดงเค้ก 3D และข้อความอวยพร
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("สุขสันต์วันเกิดนะจ๊ะขอให้ปีนี้เป็นปีที่ดีนะจ๊ะ")
    
    if st.button("เริ่มใหม่"):
        st.session_state.step = "input"
        st.rerun()

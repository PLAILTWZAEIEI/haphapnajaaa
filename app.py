import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="เซอร์ไพรส์วันเกิด!", page_icon="🎂")

# ใช้ Session State เพื่อคุมหน้า (หน้ากรอกข้อมูล -> หน้าแสดงเค้ก)
if 'step' not in st.session_state:
    st.session_state.step = "input"

if st.session_state.step == "input":
    st.title("🎂 ระบบสร้างของขวัญทางคณิตศาสตร์")
    st.write("กรุณากรอกข้อมูลเพื่อคำนวณเค้กของคุณ...")
    
    name = st.text_input("คุณชื่ออะไรจ๊ะ?:", placeholder="พิมพ์ชื่อตรงนี้เลย")
    age = st.number_input("อายุปีนี้กี่ขวบแล้ว?:", min_value=1, max_value=100, value=20)
    
    if st.button("คำนวณสมการเค้กและสร้างเซอร์ไพรส์! ✨"):
        if name:
            st.session_state.name = name
            st.session_state.age = age
            st.session_state.step = "surprise"
            st.rerun()
        else:
            st.warning("บอกชื่อให้เรารู้หน่อยน้าา")

else:
    # --- ขั้นตอนสร้างเค้กจากสมการ ---
    st.balloons()
    st.header(f"✨ สุขสันต์วันเกิดนะจ๊ะ {st.session_state.name}!")
    
    # ฟังก์ชันสร้างพิกัดทรงกระบอก (Cylinder Equations)
    def create_cylinder(r, h, z_offset, color):
        theta = np.linspace(0, 2*np.pi, 100)
        z = np.linspace(0, h, 20)
        theta, z = np.meshgrid(theta, z)
        # สมการ Parametric: x = r*cos(theta), y = r*sin(theta)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = z + z_offset
        return go.Surface(x=x, y=y, z=z, colorscale=[[0, color], [1, color]], showscale=False, opacity=0.9)

    # สร้างเลเยอร์เค้ก
    fig = go.Figure()
    
    # ชั้นล่าง (ฐาน)
    fig.add_trace(create_cylinder(r=2.0, h=1.0, z_offset=0, color="#FFC0CB")) 
    # ชั้นบน
    fig.add_trace(create_cylinder(r=1.5, h=0.8, z_offset=1.0, color="#FFB6C1"))

    # สร้างเทียน (Line Equations) ตามจำนวนอายุ
    age = st.session_state.age
    for i in range(age):
        angle = (2 * np.pi / age) * i
        cx, cy = 1.2 * np.cos(angle), 1.2 * np.sin(angle)
        # เส้นตรงเทียน: (x,y) คงที่, z เปลี่ยนจาก 1.8 ถึง 2.2
        fig.add_trace(go.Scatter3d(
            x=[cx, cx], y=[cy, cy], z=[1.8, 2.3],
            mode='lines',
            line=dict(color='yellow', width=5),
            showlegend=False
        ))

    # ตั้งค่ามุมมองกราฟ
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )

    # แสดงกราฟเค้ก
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("สุขสันต์วันเกิดนะจ๊ะขอให้ปีนี้เป็นปีที่ดีนะจ๊ะ")
    
    if st.button("เริ่มใหม่"):
        st.session_state.step = "input"
        st.rerun()

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="...", page_icon="✨")

if 'step' not in st.session_state:
    st.session_state.step = "input"

if st.session_state.step == "input":
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
    with st.spinner("กำลังประมวลผลและคำนวณสร้างภาพจากสมการ..."):
        time.sleep(1.5)
    st.session_state.step = "surprise"
    st.rerun()

else:
    st.balloons()
    st.header(f"✨ สุขสันต์วันเกิดนะจ๊ะ {st.session_state.name}!")
    
    fig = go.Figure()

    # --- ฟังก์ชันสร้างเค้กทรงกระบอกแบบตัน 3D ---
    def add_solid_cake_layer(fig, r, h, z_offset, color):
        theta = np.linspace(0, 2*np.pi, 100)
        z = np.linspace(0, h, 20)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_side = r * np.cos(theta_grid)
        y_side = r * np.sin(theta_grid)
        z_side = z_grid + z_offset
        
        r_disc = np.linspace(0, r, 20)
        theta_disc = np.linspace(0, 2*np.pi, 100)
        r_grid, theta_disc_grid = np.meshgrid(r_disc, theta_disc)
        x_disc = r_grid * np.cos(theta_disc_grid)
        y_disc = r_grid * np.sin(theta_disc_grid)

        colorscale = [[0, color], [1, color]]
        
        fig.add_trace(go.Surface(x=x_side, y=y_side, z=z_side, colorscale=colorscale, showscale=False, lighting=dict(ambient=0.6, diffuse=0.8)))
        fig.add_trace(go.Surface(x=x_disc, y=y_disc, z=np.full_like(x_disc, z_offset + h), colorscale=colorscale, showscale=False, lighting=dict(ambient=0.6, diffuse=0.8)))
        fig.add_trace(go.Surface(x=x_disc, y=y_disc, z=np.full_like(x_disc, z_offset), colorscale=colorscale, showscale=False, lighting=dict(ambient=0.6, diffuse=0.8)))

    # 1. สร้างก้อนเค้กหลัก 2 ชั้น
    add_solid_cake_layer(fig, r=2.0, h=1.0, z_offset=0, color="#FFB6C1")  
    add_solid_cake_layer(fig, r=1.4, h=0.8, z_offset=1.0, color="#FFC0CB") 

    # 2. เพิ่มลวดลายเส้นเกลียวครีมตกแต่งข้างเค้ก (Frosting Spirals)
    t = np.linspace(0, 6 * np.pi, 200)
    # ลายรอบชั้นล่าง
    fig.add_trace(go.Scatter3d(
        x=2.02 * np.cos(t), y=2.02 * np.sin(t), z=0.1 + (t / (6 * np.pi)) * 0.8,
        mode='lines', line=dict(color='white', width=5), showlegend=False
    ))
    # ลายรอบชั้นบน
    fig.add_trace(go.Scatter3d(
        x=1.42 * np.cos(t), y=1.42 * np.sin(t), z=1.1 + (t / (6 * np.pi)) * 0.6,
        mode='lines', line=dict(color='#FFF8DC', width=5), showlegend=False
    ))

    # 3. ตกแต่งเม็ดไอซิ่งทรงกลมรอบขอบเค้ก
    for angle in np.linspace(0, 2*np.pi, 16):
        # ไอซิ่งขอบชั้นล่าง
        fig.add_trace(go.Scatter3d(
            x=[1.9 * np.cos(angle)], y=[1.9 * np.sin(angle)], z=[1.02],
            mode='markers', marker=dict(size=4, color='white'), showlegend=False
        ))
        # ไอซิ่งขอบชั้นบน
        fig.add_trace(go.Scatter3d(
            x=[1.3 * np.cos(angle)], y=[1.3 * np.sin(angle)], z=[1.82],
            mode='markers', marker=dict(size=4, color='#FFF8DC'), showlegend=False
        ))

    # 4. คำนวณจุดปักเทียนและเปลวไฟ 3D ตามอายุ
    age = st.session_state.age
    for i in range(age):
        angle = (2 * np.pi / age) * i
        cx, cy = 0.9 * np.cos(angle), 0.9 * np.sin(angle)
        
        fig.add_trace(go.Scatter3d(
            x=[cx, cx], y=[cy, cy], z=[1.8, 2.3],
            mode='lines', line=dict(color='white', width=6), showlegend=False
        ))
        fig.add_trace(go.Scatter3d(
            x=[cx], y=[cy], z=[2.35],
            mode='markers', marker=dict(size=6, color='orange', symbol='circle'), showlegend=False
        ))

    # 5. ตั้งค่ามุมกล้องให้เค้กหมุนช้าๆ อัตโนมัติ (Auto-Rotation)
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data',
            camera=dict(
                eye=dict(x=1.7, y=1.7, z=1.2)
            )
        ),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(
                label="Play",
                method="animate",
                args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}]
            )]
        )],
        margin=dict(l=0, r=0, b=0, t=0)
    )

    # เฟรมการหมุนรอบตัวเอง 360 องศา
    frames = []
    for angle_deg in range(0, 360, 5):
        rad = np.radians(angle_deg)
        frames.append(go.Frame(
            layout=dict(
                scene=dict(
                    camera=dict(
                        eye=dict(x=1.8 * np.cos(rad), y=1.8 * np.sin(rad), z=1.2)
                    )
                )
            )
        ))
    fig.frames = frames

    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("สุขสันต์วันเกิดนะจ๊ะขอให้ปีนี้เป็นปีที่ดีนะจ๊ะ")
    
    if st.button("เริ่มใหม่"):
        st.session_state.step = "input"
        st.rerun()

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="...", page_icon="✨")

# ซ่อน UI ของ Streamlit บางส่วนเพื่อความคลีน
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

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

    # --- ฟังก์ชันสร้างเค้กแบบตัน 3D ---
    def add_solid_cake_layer(fig, r, h, z_offset, color):
        theta = np.linspace(0, 2*np.pi, 80)
        z = np.linspace(0, h, 15)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_side = r * np.cos(theta_grid)
        y_side = r * np.sin(theta_grid)
        z_side = z_grid + z_offset
        
        r_disc = np.linspace(0, r, 15)
        r_grid, theta_disc_grid = np.meshgrid(r_disc, theta)
        x_disc = r_grid * np.cos(theta_disc_grid)
        y_disc = r_grid * np.sin(theta_disc_grid)

        cs = [[0, color], [1, color]]
        fig.add_trace(go.Surface(x=x_side, y=y_side, z=z_side, colorscale=cs, showscale=False, lighting=dict(ambient=0.7, diffuse=0.8)))
        fig.add_trace(go.Surface(x=x_disc, y=y_disc, z=np.full_like(x_disc, z_offset + h), colorscale=cs, showscale=False, lighting=dict(ambient=0.7, diffuse=0.8)))

    # --- ฟังก์ชันสร้างครีมไหลย้อย (Dripping White Cream) ---
    def add_dripping_cream(fig, r, z_top, wave_freq=8, wave_amp=0.15, color="#FFFFFF"):
        theta = np.linspace(0, 2*np.pi, 100)
        # สมการคลื่นซายน์จำลองลวดลายครีมไหลย้อย
        z_wave = z_top - 0.15 - np.abs(np.sin(wave_freq * theta / 2)) * wave_amp
        r_ext = r + 0.03
        x_side = r_ext * np.cos(theta)
        y_side = r_ext * np.sin(theta)
        
        # วาดเส้นขอบครีมหยด
        fig.add_trace(go.Scatter3d(
            x=x_side, y=y_side, z=z_wave,
            mode='lines', line=dict(color=color, width=6), showlegend=False
        ))
        
        # ฝาหน้าครีมบนหน้าเค้ก
        r_disc = np.linspace(0, r_ext, 15)
        rg, tg = np.meshgrid(r_disc, theta)
        fig.add_trace(go.Surface(
            x=rg * np.cos(tg), y=rg * np.sin(tg), z=np.full_like(rg, z_top + 0.01),
            colorscale=[[0, color], [1, color]], showscale=False
        ))

    # ฐานจานรองเค้กสีฟ้า
    add_solid_cake_layer(fig, r=2.4, h=0.1, z_offset=-0.1, color="#B0C4DE")

    # เค้กชั้นล่างและชั้นบน (ชมพูหวาน)
    add_solid_cake_layer(fig, r=2.0, h=0.9, z_offset=0, color="#FF99B2")
    add_dripping_cream(fig, r=2.0, z_top=0.9, wave_freq=7, wave_amp=0.25)

    add_solid_cake_layer(fig, r=1.4, h=0.8, z_offset=0.9, color="#FFB3C6")
    add_dripping_cream(fig, r=1.4, z_top=1.7, wave_freq=5, wave_amp=0.2)

    # --- ลูกเชอร์รี่ประดับบนเค้ก (Cherries & Dark Cherries) ---
    def add_cherry(fig, x, y, z, color='#D2143A', stem=True):
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='markers', marker=dict(size=10, color=color), showlegend=False
        ))
        if stem:
            fig.add_trace(go.Scatter3d(
                x=[x, x + 0.05], y=[y, y + 0.05], z=[z, z + 0.25],
                mode='lines', line=dict(color='#2D5A27', width=3), showlegend=False
            ))

    # เชอร์รี่สีม่วงเข้มชั้นล่าง
    for angle in [0, 2*np.pi/3, 4*np.pi/3]:
        cx, cy = 1.6 * np.cos(angle), 1.6 * np.sin(angle)
        add_cherry(fig, cx, cy, 0.5, color='#3B1C32')

    # กองลูกเชอร์รี่สดแดงบนยอดเค้ก
    add_cherry(fig, 0, 0, 1.95, color='#E60026')
    for angle in np.linspace(0, 2*np.pi, 5, endpoint=False):
        cx, cy = 0.45 * np.cos(angle), 0.45 * np.sin(angle)
        add_cherry(fig, cx, cy, 1.85, color='#FF1A40')

    # --- ปักเทียน 3D ตามอายุ ---
    age = st.session_state.age
    for i in range(age):
        angle = (2 * np.pi / age) * i
        cx, cy = 0.9 * np.cos(angle), 0.9 * np.sin(angle)
        fig.add_trace(go.Scatter3d(
            x=[cx, cx], y=[cy, cy], z=[1.7, 2.2],
            mode='lines', line=dict(color='white', width=5), showlegend=False
        ))
        fig.add_trace(go.Scatter3d(
            x=[cx], y=[cy], z=[2.25],
            mode='markers', marker=dict(size=5, color='orange', symbol='circle'), showlegend=False
        ))

    # --- สร้างเฟรมสำหรับ Fade-in และหมุน 3D + ปุ่มควบคุมการหมุน (Start / Pause) ---
    frames = []
    
    # 1. เฟรม Fade-in (ค่อยๆ ชัดขึ้น)
    for op in np.linspace(0.1, 1.0, 6):
        frames.append(go.Frame(
            layout=dict(
                scene=dict(
                    camera=dict(eye=dict(x=1.8, y=1.8, z=1.2))
                )
            ),
            name=f"fade_{op}"
        ))

    # 2. เฟรมหมุนรอบตัวเอง 360 องศา
    for angle_deg in range(0, 360, 6):
        rad = np.radians(angle_deg)
        frames.append(go.Frame(
            layout=dict(
                scene=dict(
                    camera=dict(eye=dict(x=1.8 * np.cos(rad), y=1.8 * np.sin(rad), z=1.2))
                )
            ),
            name=f"spin_{angle_deg}"
        ))

    fig.frames = frames

    # ปุ่มกด "หมุนเค้ก" และ "หยุดหมุน" ด้านล่างรูป
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data',
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.2))
        ),
        updatemenus=[dict(
            type="buttons",
            direction="left",
            x=0.5, y=-0.05,
            xanchor="center",
            buttons=[
                dict(
                    label="▶ หมุนเค้ก",
                    method="animate",
                    args=[None, {"frame": {"duration": 80, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}]
                ),
                dict(
                    label="⏸ หยุดหมุน",
                    method="animate",
                    args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}]
                )
            ]
        )],
        margin=dict(l=0, r=0, b=0, t=0)
    )

    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("สุขสันต์วันเกิดนะจ๊ะขอให้ปีนี้เป็นปีที่ดีนะจ๊ะ")
    
    if st.button("เริ่มใหม่"):
        st.session_state.step = "input"
        st.rerun()

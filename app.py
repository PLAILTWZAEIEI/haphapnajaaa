import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="...", page_icon="✨")

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

    # --- 1. สร้างฐานจานและก้อนเค้ก 3D สีสันสดใส ---
    def add_cake_layer(fig, r, h, z_offset, color):
        theta = np.linspace(0, 2*np.pi, 80)
        z = np.linspace(0, h, 15)
        tg, zg = np.meshgrid(theta, z)
        
        rd = np.linspace(0, r, 15)
        rg, tdg = np.meshgrid(rd, theta)

        cs = [[0, color], [1, color]]
        # ด้านข้าง
        fig.add_trace(go.Surface(x=r*np.cos(tg), y=r*np.sin(tg), z=zg+z_offset, colorscale=cs, showscale=False, lighting=dict(ambient=0.7, diffuse=0.8)))
        # ฝาบน
        fig.add_trace(go.Surface(x=rg*np.cos(tdg), y=rg*np.sin(tdg), z=np.full_like(rg, z_offset+h), colorscale=cs, showscale=False, lighting=dict(ambient=0.7, diffuse=0.8)))

    # จานรองสีฟ้าพาสเทล
    add_cake_layer(fig, r=2.4, h=0.1, z_offset=-0.1, color="#A0C4FF")
    # เค้กชั้นล่างสีชมพูราสเบอร์รีฉ่ำๆ
    add_cake_layer(fig, r=2.0, h=0.9, z_offset=0, color="#FF6B8B")
    # เค้กชั้นบนสีชมพูสตรอว์เบอร์รี
    add_cake_layer(fig, r=1.4, h=0.8, z_offset=0.9, color="#FF8EAE")

    # --- 2. ซอสครีมขาวไหลย้อย (Dripping Cream) ---
    def add_dripping_cream(fig, r, z_top, wave_freq=8, wave_amp=0.2):
        theta = np.linspace(0, 2*np.pi, 100)
        z_wave = z_top - 0.12 - np.abs(np.sin(wave_freq * theta / 2)) * wave_amp
        r_ext = r + 0.03
        
        fig.add_trace(go.Scatter3d(
            x=r_ext * np.cos(theta), y=r_ext * np.sin(theta), z=z_wave,
            mode='lines', line=dict(color='#FFF0F5', width=7), showlegend=False
        ))
        
        rd = np.linspace(0, r_ext, 15)
        rg, tg = np.meshgrid(rd, theta)
        fig.add_trace(go.Surface(
            x=rg * np.cos(tg), y=rg * np.sin(tg), z=np.full_like(rg, z_top + 0.01),
            colorscale=[[0, '#FFF0F5'], [1, '#FFF0F5']], showscale=False
        ))

    add_dripping_cream(fig, r=2.0, z_top=0.9, wave_freq=8, wave_amp=0.25)
    add_dripping_cream(fig, r=1.4, z_top=1.7, wave_freq=6, wave_amp=0.2)

    # --- 3. เพิ่มเม็ดเกล็ดน้ำตาลสพริงเคิลส์หลากสีสัน (Colorful Sprinkles) ---
    np.random.seed(42)
    colors = ['#FF597B', '#FFD15C', '#4D96FF', '#6BCB77', '#F77E21', '#9B51E0']
    
    # สพริงเคิลส์โรยบนชั้นล่าง
    for _ in range(40):
        ang = np.random.uniform(0, 2*np.pi)
        rad = np.random.uniform(1.45, 1.95)
        c = np.random.choice(colors)
        fig.add_trace(go.Scatter3d(
            x=[rad*np.cos(ang)], y=[rad*np.sin(ang)], z=[0.92],
            mode='markers', marker=dict(size=4, color=c), showlegend=False
        ))

    # --- 4. สตรอว์เบอร์รีและลูกเชอร์รี่ประดับหน้าเค้ก ---
    def add_strawberry(fig, x, y, z):
        # ผลสตรอว์เบอร์รีสีแดงสด
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='markers', marker=dict(size=12, color='#E60026', symbol='diamond'), showlegend=False
        ))
        # ขั้วใบไม้สีเขียวสด
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z+0.08],
            mode='markers', marker=dict(size=6, color='#2ECC71', symbol='circle'), showlegend=False
        ))

    # วางสตรอว์เบอร์รีบนยอดเค้กชั้นบน
    add_strawberry(fig, 0, 0, 1.82)
    for angle in np.linspace(0, 2*np.pi, 5, endpoint=False):
        cx, cy = 0.5 * np.cos(angle), 0.5 * np.sin(angle)
        add_strawberry(fig, cx, cy, 1.78)

    # --- 5. ปักเทียน 3D ลายทาง + เปลวไฟสว่าง ---
    age = st.session_state.age
    for i in range(age):
        angle = (2 * np.pi / age) * i
        cx, cy = 0.95 * np.cos(angle), 0.95 * np.sin(angle)
        # ตัวเทียนสีเหลืองสดใส
        fig.add_trace(go.Scatter3d(
            x=[cx, cx], y=[cy, cy], z=[1.7, 2.25],
            mode='lines', line=dict(color='#FFEA20', width=6), showlegend=False
        ))
        # เปลวไฟสีส้มสว่าง
        fig.add_trace(go.Scatter3d(
            x=[cx], y=[cy], z=[2.3],
            mode='markers', marker=dict(size=7, color='#FF5722', symbol='circle'), showlegend=False
        ))

    # --- 6. แอนิเมชัน Fade-in + หมุน 3D + ปุ่มควบคุม ---
    frames = []
    # Fade-in
    for op in np.linspace(0.1, 1.0, 5):
        frames.append(go.Frame(
            layout=dict(scene=dict(camera=dict(eye=dict(x=1.8, y=1.8, z=1.2)))),
            name=f"fade_{op}"
        ))
    # หมุน 360 องศา
    for angle_deg in range(0, 360, 6):
        rad = np.radians(angle_deg)
        frames.append(go.Frame(
            layout=dict(scene=dict(camera=dict(eye=dict(x=1.8 * np.cos(rad), y=1.8 * np.sin(rad), z=1.2)))),
            name=f"spin_{angle_deg}"
        ))

    fig.frames = frames

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
                    args=[None, {"frame": {"duration": 70, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}]
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

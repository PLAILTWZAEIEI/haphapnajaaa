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

    # --- 1. ถาดรองสีฟ้า 2 ชั้น ---
    def add_solid_layer(fig, r, h, z_offset, color):
        theta = np.linspace(0, 2*np.pi, 80)
        z = np.linspace(0, h, 15)
        tg, zg = np.meshgrid(theta, z)
        rd = np.linspace(0, r, 15)
        rg, tdg = np.meshgrid(rd, theta)
        cs = [[0, color], [1, color]]
        fig.add_trace(go.Surface(x=r*np.cos(tg), y=r*np.sin(tg), z=zg+z_offset, colorscale=cs, showscale=False, lighting=dict(ambient=0.8, diffuse=0.8)))
        fig.add_trace(go.Surface(x=rg*np.cos(tdg), y=rg*np.sin(tdg), z=np.full_like(rg, z_offset+h), colorscale=cs, showscale=False, lighting=dict(ambient=0.8, diffuse=0.8)))

    add_solid_layer(fig, r=2.5, h=0.06, z_offset=-0.12, color="#94B9E9") # จานล่าง
    add_solid_layer(fig, r=2.3, h=0.06, z_offset=-0.06, color="#B8D4F8") # จานบน

    # --- 2. ตัวเค้กสีชมพู (กว้างและเตี้ยแบบในภาพ) ---
    add_solid_layer(fig, r=2.0, h=0.75, z_offset=0, color="#FF8DA1")   # ชั้นล่าง
    add_solid_layer(fig, r=1.4, h=0.65, z_offset=0.75, color="#FFA4B6") # ชั้นบน

    # --- 3. ครีมขาวย้อยลอนกว้าง (Dripping Cream) ---
    def add_drip(fig, r, z_top, wave_freq=6, wave_amp=0.18):
        theta = np.linspace(0, 2*np.pi, 120)
        z_wave = z_top - 0.1 - np.abs(np.sin(wave_freq * theta / 2)) * wave_amp
        r_ext = r + 0.02
        fig.add_trace(go.Scatter3d(
            x=r_ext * np.cos(theta), y=r_ext * np.sin(theta), z=z_wave,
            mode='lines', line=dict(color='#FFFFFF', width=8), showlegend=False
        ))
        rd = np.linspace(0, r_ext, 15)
        rg, tg = np.meshgrid(rd, theta)
        fig.add_trace(go.Surface(
            x=rg * np.cos(tg), y=rg * np.sin(tg), z=np.full_like(rg, z_top + 0.01),
            colorscale=[[0, '#FFFFFF'], [1, '#FFFFFF']], showscale=False
        ))

    add_drip(fig, r=2.0, z_top=0.75, wave_freq=6, wave_amp=0.22)
    add_drip(fig, r=1.4, z_top=1.40, wave_freq=5, wave_amp=0.18)

    # --- 4. เชอร์รี่สีม่วงเข้มพร้อมก้านกอดเค้กชั้นล่าง ---
    for angle in [0.3, 2.3, 4.3]:
        cx, cy = 1.65 * np.cos(angle), 1.65 * np.sin(angle)
        # ผลเชอร์รี่ม่วงเข้ม
        fig.add_trace(go.Scatter3d(
            x=[cx], y=[cy], z=[0.55],
            mode='markers', marker=dict(size=14, color='#2B2456'), showlegend=False
        ))
        # ก้านสีดำโค้งขึ้น
        fig.add_trace(go.Scatter3d(
            x=[cx, cx*0.9], y=[cy, cy*0.9], z=[0.55, 0.95],
            mode='lines', line=dict(color='#111111', width=3), showlegend=False
        ))

    # --- 5. กองเชอร์รี่สีชมพูแดง + ใบไม้บนยอดเค้ก ---
    def add_top_cherry(fig, x, y, z):
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='markers', marker=dict(size=13, color='#FF3B60'), showlegend=False
        ))
        fig.add_trace(go.Scatter3d(
            x=[x, x*0.8], y=[y, y*0.8], z=[z, z+0.25],
            mode='lines', line=dict(color='#2A150D', width=2), showlegend=False
        ))

    # เชอร์รี่ก้อนยอด 5 ลูก
    add_top_cherry(fig, 0, 0, 1.62)
    for a in np.linspace(0, 2*np.pi, 4, endpoint=False):
        add_top_cherry(fig, 0.4*np.cos(a), 0.4*np.sin(a), 1.52)

    # ใบไม้สีเขียวประดับข้างหลัง
    for a in [0.8, 2.4, 4.0]:
        fig.add_trace(go.Scatter3d(
            x=[0.6*np.cos(a)], y=[0.6*np.sin(a)], z=[1.68],
            mode='markers', marker=dict(size=8, color='#3A8E51', symbol='diamond'), showlegend=False
        ))

    # --- 6. เทียนขนาดเรียวเล็ก + ไฟเทียนพอดีสมส่วนตามอายุ ---
    age = st.session_state.age
    for i in range(age):
        angle = (2 * np.pi / age) * i
        cx, cy = 0.95 * np.cos(angle), 0.95 * np.sin(angle)
        # ตัวเทียนเรียวเล็กสีขาวลายส้ม
        fig.add_trace(go.Scatter3d(
            x=[cx, cx], y=[cy, cy], z=[1.42, 1.80],
            mode='lines', line=dict(color='#FFF8DC', width=3), showlegend=False
        ))
        # เปลวไฟสีส้มเหลืองขนาดเล็กกระทัดรัด
        fig.add_trace(go.Scatter3d(
            x=[cx], y=[cy], z=[1.83],
            mode='markers', marker=dict(size=3, color='#FF9800', symbol='circle'), showlegend=False
        ))

    # --- 7. แอนิเมชัน Fade-In + หมุน 3D + ปุ่มเล่น/หยุด ---
    frames = []
    for op in np.linspace(0.1, 1.0, 5):
        frames.append(go.Frame(
            layout=dict(scene=dict(camera=dict(eye=dict(x=1.8, y=1.8, z=1.1)))),
            name=f"fade_{op}"
        ))
    for angle_deg in range(0, 360, 6):
        rad = np.radians(angle_deg)
        frames.append(go.Frame(
            layout=dict(scene=dict(camera=dict(eye=dict(x=1.8 * np.cos(rad), y=1.8 * np.sin(rad), z=1.1)))),
            name=f"spin_{angle_deg}"
        ))

    fig.frames = frames

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='data',
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.1))
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

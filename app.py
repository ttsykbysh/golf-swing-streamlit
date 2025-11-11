import streamlit as st
import numpy as np
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="スマホスイング飛距離予測", layout="centered")

st.title("🏌️‍♂️ スマホスイング飛距離予測アプリ")
st.write("スマホを手に持ってスイングしてください。加速度センサーを利用して飛距離を予測します。")

st.info("📱 注意: iPhone Safari または Android Chrome でアクセスしてください。センサー利用を『許可』してください。")

# --- JavaScriptでモーションデータ取得 ---
sensor_data = streamlit_js_eval(
    js_expressions="""
    new Promise((resolve) => {
        if (window.DeviceMotionEvent) {
            let acc = {x:0,y:0,z:0};
            let count = 0;
            window.addEventListener('devicemotion', (event) => {
                acc.x = event.acceleration.x || 0;
                acc.y = event.acceleration.y || 0;
                acc.z = event.acceleration.z || 0;
                count++;
                if (count > 20) {
                    resolve(acc);
                }
            });
        } else {
            resolve({x:0,y:0,z:0});
        }
    })
    """,
    key="sensor"
)

# --- データ表示と飛距離予測 ---
if sensor_data:
    st.subheader("📊 センサー値")
    st.json(sensor_data)

    # 加速度ベクトルの大きさを算出
    acc_magnitude = np.sqrt(sensor_data["x"]**2 + sensor_data["y"]**2 + sensor_data["z"]**2)
    st.write(f"🔹 スイング強度: {acc_magnitude:.2f}")

    # --- 簡易AIモデルによる飛距離予測 ---
    head_speed = acc_magnitude * 15  # 仮の換算係数
    launch_angle = 12
    smash_factor = 1.4
    spin = 2500

    distance = (head_speed * 4.5) + (launch_angle * 2) + (smash_factor * 20) - (spin / 1000)
    distance = round(distance, 1)

    st.success(f"🏌️‍♂️ 推定飛距離: **{distance} yard**")
else:
    st.warning("📴 スマホのセンサーからのデータを取得中...")

st.caption("© 2025 Golf Swing Sensor App | Streamlit + JavaScript Motion API")

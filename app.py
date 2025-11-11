import streamlit as st
import numpy as np
from streamlit_js_eval import streamlit_js_eval

# ===========================
# Streamlit 設定
# ===========================
st.set_page_config(page_title="スマホスイング飛距離予測", layout="centered")

st.title("🏌️‍♂️ スマホスイング飛距離予測アプリ")
st.write("スマホを手に持ってスイングしてください。モーションセンサーの値から推定飛距離を計算します。")

st.info("📱 注意: iPhone Safari または Android Chrome でアクセスし、センサー利用を『許可』してください。")

# ===========================
# 🔄 リセットボタン
# ===========================
st.markdown("---")
if st.button("🔄 結果をリセット"):
    st.experimental_rerun()  # ← ページ全体を再実行してリセット

# ===========================
# JavaScript でモーションセンサー取得
# ===========================
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
                // 約1秒ごとに結果を返す
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

# ===========================
# センサー値が取得できた場合の処理
# ===========================
if sensor_data:
    st.subheader("📊 現在のセンサー値")
    st.json(sensor_data)

    # --- 加速度ベクトルの大きさ ---
    acc = np.sqrt(sensor_data["x"]**2 + sensor_data["y"]**2 + sensor_data["z"]**2)
    st.write(f"🔹 スイング強度（加速度合成値）: {acc:.2f}")

    # ===========================
    # 🧠 飛距離予測モデル（簡易版）
    # ===========================
    head_speed = acc * 15  # 加速度からクラブスピード換算（仮定）
    launch_angle = 12
    smash_factor = 1.4
    spin = 2500

    distance = (head_speed * 4.5) + (launch_angle * 2) + (smash_factor * 20) - (spin / 1000)
    distance = round(distance, 1)

    st.success(f"🏌️‍♂️ 推定飛距離: **{distance} yard**")

    # ===========================
    # グラフ表示
    # ===========================
    st.markdown("---")
    st.subheader("📈 推定パラメータ")
    st.bar_chart({
        "パラメータ": [head_speed, launch_angle, smash_factor, spin/1000],
    })

else:
    st.warning("📴 スマホのモーションセンサーからのデータを取得中...")
    st.caption("※動作しない場合はブラウザ設定で『モーションと方向のアクセスを許可』にしてください。")

st.markdown("---")
st.caption("© 2025 Golf Swing Sensor App | Streamlit + JavaScript Motion API")

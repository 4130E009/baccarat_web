import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="百家樂推測助手", page_icon="🎲", layout="centered")

st.title("🎲 百家樂推測助手 v3")
st.markdown("每輪輸入莊/閒/和後，可重複按『開始推測』進行更新分析。")

# --- 初始化 Session ---
if "results" not in st.session_state:
    st.session_state.results = []

# --- 按鈕列 ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 莊家勝"):
        st.session_state.results.append("莊")
with col2:
    if st.button("👤 閒家勝"):
        st.session_state.results.append("閒")
with col3:
    if st.button("🤝 和局"):
        st.session_state.results.append("和")

# --- 功能鍵 ---
colA, colB = st.columns(2)
with colA:
    analyze = st.button("📈 開始推測")
with colB:
    if st.button("🧹 清空紀錄"):
        st.session_state.results = []

# --- 顯示紀錄 ---
if st.session_state.results:
    st.subheader("🧾 當前記錄")
    st.write(" → ".join(st.session_state.results))
else:
    st.warning("目前尚未有任何紀錄，請先輸入結果。")

# --- 只在按下推測後才進行分析 ---
if analyze and st.session_state.results:
    df = pd.DataFrame(st.session_state.results, columns=["結果"])
    total = len(df)
    banker = (df["結果"] == "莊").sum()
    player = (df["結果"] == "閒").sum()
    tie = (df["結果"] == "和").sum()

    st.subheader("📊 統計結果")
    st.write(f"總局數：{total}")
    st.write(f"莊家勝：{banker} ({banker/total*100:.1f}%)")
    st.write(f"閒家勝：{player} ({player/total*100:.1f}%)")
    st.write(f"和局：{tie} ({tie/total*100:.1f}%)")

    # --- 連勝統計 ---
    if len(df) >= 2:
        last = df["結果"].iloc[-1]
        streak = 1
        for prev in reversed(df["結果"][:-1]):
            if prev == last:
                streak += 1
            else:
                break
        st.info(f"🔥 目前連 {streak} 次「{last}」")

    # --- 走勢圖 ---
    fig, ax = plt.subplots()
    color_map = {"莊": "red", "閒": "blue", "和": "green"}
    y_values = [0 if r=="莊" else (1 if r=="閒" else 0.5) for r in df["結果"]]
    colors = [color_map[r] for r in df["結果"]]
    ax.scatter(range(1, total + 1), y_values, c=colors, s=100)
    ax.set_title("走勢圖")
    ax.set_xlabel("局數")
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels(["莊", "和", "閒"])
    st.pyplot(fig)

    # --- 簡易預測 ---
    if banker > player:
        st.success("💡 推測：近期偏莊，下一把莊機率略高。")
    elif player > banker:
        st.success("💡 推測：近期偏閒，下一把閒機率略高。")
    else:
        st.info("💡 推測：莊閒勢均力敵。")

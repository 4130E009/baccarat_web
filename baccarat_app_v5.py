import streamlit as st
import pandas as pd

# --- 頁面設定 ---
st.set_page_config(page_title="百家樂推測助手", page_icon="🎲", layout="centered")

st.title("🎲 百家樂推測助手 v5")
st.markdown("快速紀錄每局結果，立即統計莊閒和與連勝情況。")

# --- 初始化 Session State ---
if "results" not in st.session_state:
    st.session_state.results = []

# --- 按鈕列 ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠 莊家勝"):
        st.session_state.results.append("莊")
with col2:
    if st.button("👤 閒家勝"):
        st.session_state.results.append("閒")
with col3:
    if st.button("🤝 和局"):
        st.session_state.results.append("和")
with col4:
    if st.button("🔙 倒退一步"):
        if st.session_state.results:
            st.session_state.results.pop()

# --- 清空紀錄 ---
if st.button("🧹 清空紀錄"):
    st.session_state.results = []

# --- 顯示紀錄區 ---
if st.session_state.results:
    df = pd.DataFrame(st.session_state.results, columns=["結果"])
    total = len(df)
    banker = (df["結果"] == "莊").sum()
    player = (df["結果"] == "閒").sum()
    tie = (df["結果"] == "和").sum()

    st.subheader("📊 當前統計")
    st.write(f"總局數：{total}")
    st.write(f"莊家勝：{banker} ({banker/total*100:.1f}%)")
    st.write(f"閒家勝：{player} ({player/total*100:.1f}%)")
    st.write(f"和局：{tie} ({tie/total*100:.1f}%)")

    # --- 連勝計算 ---
    if len(df) >= 2:
        last = df["結果"].iloc[-1]
        streak = 1
        for prev in reversed(df["結果"][:-1]):
            if prev == last:
                streak += 1
            else:
                break
        st.info(f"🔥 目前連 {streak} 次「{last}」")

    # --- 簡單推測邏輯 ---
    if banker > player:
        st.success("💡 推測：近期偏莊，下一把莊機率略高。")
    elif player > banker:
        st.success("💡 推測：近期偏閒，下一把閒機率略高。")
    else:
        st.info("💡 推測：莊閒勢均力敵。")
else:
    st.warning("尚未記錄任何結果，請點擊上方按鈕新增。")

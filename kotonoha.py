import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ---------------------
# Google Sheets 認証
# ---------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("kotonoha").sheet1  # スプレッドシート名に合わせて

# ---------------------
# タイトル
# ---------------------
st.title("🌸 ことのは")
st.markdown("やさしいことばで、つながる")

# ---------------------
# 入力フォーム
# ---------------------
user = st.text_input("あなたの名前")
message = st.text_area("今日のことのは（出来事や気持ち）")

# 感情・体調の選択
st.markdown("### 😊 今日の気分は？")
emotion = st.radio("感情", ["😀 元気", "😐 普通", "😢 かなしい", "😠 いらいら", "😴 ねむい"], horizontal=True)

st.markdown("### 💪 体調は？")
physical = st.radio("体調", ["💯 絶好調", "👌 まあまあ", "🤧 風邪気味", "🤒 しんどい", "🤕 痛いところあり"], horizontal=True)

# 投稿ボタン
if st.button("📩 投稿する"):
    if user and message:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([now, user, message, emotion, physical])
        st.success("投稿されました！")
    else:
        st.warning("名前とメッセージを入力してください。")

# ---------------------
# タイムライン表示
# ---------------------
st.markdown("---")
st.markdown("### 🕒 タイムライン")

records = sheet.get_all_records()
for row in reversed(records[-10:]):  # 最新10件を表示
    st.markdown(f"**{row['名前']}** ({row['日時']}) {row['感情']} {row['体調']}")
    st.markdown(f"> {row['今日のことのは']}")
    st.markdown("---")

import streamlit as st
import pandas as pd
import re
from datetime import datetime

st.set_page_config(page_title="Yaptırım Haber Arşivi", layout="wide")

# CSV'den veri oku
df = pd.read_csv("yaptirim_mailleri.csv")

# 'date' sütununu datetime'a çevir ve sadece tarih olarak tut
df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date

st.title("📑 Yaptırım Haber Arşivi")

# --- FİLTRELER ---
st.sidebar.header("🔎 Filtreler")

keyword = st.sidebar.text_input("Body içinde ara:")
subject_filter = st.sidebar.text_input("Subject içinde ara:")

# Tarih aralığı filtresi
min_date = df['date'].min()
max_date = df['date'].max()

date_range = st.sidebar.date_input("Tarih aralığı", [min_date, max_date])

# Başlangıç ve bitiş tarihini ayarla
if isinstance(date_range, list) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# --- VERİYİ FİLTRELE ---
filtered_df = df[
    (df['date'] >= start_date) & (df['date'] <= end_date)
]

if subject_filter:
    filtered_df = filtered_df[filtered_df['subject'].str.contains(subject_filter, case=False, na=False)]

if keyword:
    filtered_df = filtered_df[filtered_df['body'].str.contains(keyword, case=False, na=False)]

# --- HIGHLIGHT FONKSİYONU ---
def highlight_keyword(text, keyword):
    if not keyword:
        return text
    return re.sub(
        f"({re.escape(keyword)})",
        r'<span style="background-color: yellow;"><b>\1</b></span>',
        text,
        flags=re.IGNORECASE
    )

# --- SONUÇLARI GÖSTER ---
st.write(f"🔍 {len(filtered_df)} sonuç bulundu")

for _, row in filtered_df.iterrows():
    with st.expander(f"📅 {row['date']} — ✉️ {row['subject']}"):
        if keyword:
            st.markdown(highlight_keyword(row['body'], keyword), unsafe_allow_html=True)
        else:
            st.markdown(row['body'])

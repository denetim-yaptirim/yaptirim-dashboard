import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Yaptırım Haber Arşivi", layout="wide")

# CSV'den veri oku
df = pd.read_csv("yaptirim_mailleri.csv")

# Tarih sütununu datetime'a çevir
df['date'] = pd.to_datetime(df['date'], errors='coerce')

st.title("📑 Yaptırım Haber Arşivi")

# --- FİLTRELER ---
st.sidebar.header("🔎 Filtreler")

keyword = st.sidebar.text_input("Anahtar kelime (body içinde):", "")
subject_filter = st.sidebar.text_input("Konu (subject) içinde geçen:", "")

# Tarih girişleri
start_date = st.sidebar.date_input("Başlangıç tarihi", df['date'].min().date())
end_date = st.sidebar.date_input("Bitiş tarihi", df['date'].max().date())

# 🔁 Tarihleri datetime formatına çevir
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# --- VERİYİ FİLTRELE ---
filtered_df = df[
    (df['date'] >= start_date) &
    (df['date'] <= end_date)
]

if subject_filter:
    filtered_df = filtered_df[filtered_df['subject'].str.contains(subject_filter, case=False, na=False)]

if keyword:
    filtered_df = filtered_df[filtered_df['body'].str.contains(keyword, case=False, na=False)]

# --- VURGULAMA FONKSİYONU ---
def highlight_keyword(text, keyword):
    if not keyword:
        return text
    highlighted = re.sub(
        f"({re.escape(keyword)})",
        r'<span style="background-color: yellow; font-weight: bold;">\1</span>',
        text,
        flags=re.IGNORECASE
    )
    return highlighted

# --- SONUÇLARI GÖSTER ---
st.write(f"🔍 Toplam {len(filtered_df)} sonuç bulundu.")

for _, row in filtered_df.iterrows():
    with st.expander(f"📅 {row['date'].date()} — ✉️ {row['subject']}"):
        if keyword:
            st.markdown(highlight_keyword(row['body'], keyword), unsafe_allow_html=True)
        else:
            st.markdown(row['body'])

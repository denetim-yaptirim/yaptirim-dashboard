import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Yaptırım Haber Arşivi", layout="wide")

# CSV'den veri oku
df = pd.read_csv("yaptirim_mailleri.csv")

st.title("📑 Yaptırım Haber Arşivi")

# Anahtar kelime arama
keyword = st.text_input("🔍 Anahtar kelime ile ara (örnek: iran, rusya, petrol):")

# Kelimeyi vurgulayan fonksiyon
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

# Arama varsa filtrele ve göster
if keyword:
    filtered_df = df[df['body'].str.contains(keyword, case=False, na=False)]
    st.write(f"🔎 {len(filtered_df)} sonuç bulundu.")

    for _, row in filtered_df.iterrows():
        with st.expander(f"📅 {row['date']} — ✉️ {row['subject']}"):
            st.markdown(highlight_keyword(row['body'], keyword), unsafe_allow_html=True)

# Arama yoksa tüm mailleri sırala
else:
    st.write(f"📋 Toplam {len(df)} mail gösteriliyor:")
    for _, row in df.iterrows():
        with st.expander(f"📅 {row['date']} — ✉️ {row['subject']}"):
            st.markdown(row['body'])

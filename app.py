import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Yaptırım Haber Arşivi", layout="wide")

# CSV'den veri oku
df = pd.read_csv("yaptirim_mailleri.csv")

st.title("📑 Yaptırım Haber Arşivi")

# Anahtar kelime arama
keyword = st.text_input("🔍 Anahtar kelime ile ara (örnek: iran, rusya, petrol):")

# Highlight fonksiyonu
def highlight_keyword(text, keyword):
    if not keyword:
        return text
    return re.sub(
        f"({re.escape(keyword)})",
        r'<span style="background-color: yellow; font-weight: bold;">\1</span>',
        text,
        flags=re.IGNORECASE
    )

# Preview fonksiyonu
def get_preview(text, length=250):
    return text[:length] + "..." if len(text) > length else text

# Filtrele
if keyword:
    filtered_df = df[df['body'].str.contains(keyword, case=False, na=False)]
    st.write(f"🔎 {len(filtered_df)} sonuç bulundu.")
else:
    filtered_df = df
    st.write(f"📋 Toplam {len(df)} mail gösteriliyor:")

# Göster
for _, row in filtered_df.iterrows():
    preview_text = get_preview(row['body'])
    with st.expander(f"📅 {row['date']} — ✉️ {row['subject']}"):
        st.markdown(f"📝 **Önizleme:** {preview_text}")
        st.markdown("---")
        st.code(highlight_keyword(row['body'], keyword), language="text")

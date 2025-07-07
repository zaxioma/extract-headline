
import streamlit as st
import fitz  # PyMuPDF

st.set_page_config(page_title="Ekstraksi Judul PDF OCR", layout="wide")
st.title("📰 Ekstraksi Judul Berita dari PDF Koran (v3 - OCR + Bold + Kapital)")

uploaded_file = st.file_uploader("Unggah PDF koran hasil scan (OCR)", type="pdf")

# Opsi deteksi
use_caps = st.checkbox("Deteksi judul dari huruf KAPITAL", value=True)
use_bold = st.checkbox("Deteksi judul dari huruf TEBAL (bold)", value=True)

# Fungsi penggabungan huruf kapital multi-baris
def gabungkan_judul_kapital(lines):
    judul_blok = []
    buffer = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.isupper() and len(line) > 8:
            buffer.append(line)
        else:
            if buffer:
                gabung = " ".join(buffer)
                judul_blok.append(gabung)
                buffer = []
    if buffer:
        gabung = " ".join(buffer)
        judul_blok.append(gabung)
    return judul_blok

# Fungsi deteksi bold dari struktur PDF
def ekstrak_judul_bold(page):
    data = page.get_text("dict")
    hasil = []
    for block in data["blocks"]:
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span.get("text", "").strip()
                font = span.get("font", "").lower()
                if "bold" in font and 10 < len(text) < 100:
                    hasil.append(text)
    return hasil

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    st.success(f"PDF dimuat. Jumlah halaman: {len(doc)}")

    all_titles = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        st.subheader(f"Halaman {page_num + 1}")
        page_titles = []

        if use_caps:
            text = page.get_text("text")
            lines = text.split('\n')
            page_titles.extend(gabungkan_judul_kapital(lines))

        if use_bold:
            page_titles.extend(ekstrak_judul_bold(page))

        # Buang duplikat
        page_titles = list(dict.fromkeys(page_titles))

        if page_titles:
            for t in page_titles:
                st.markdown(f"- **{t}**")
            all_titles.extend(page_titles)
        else:
            st.text("❗ Tidak ada judul terdeteksi di halaman ini.")

    if all_titles:
        st.download_button(
            label="💾 Unduh Semua Judul",
            data="\n".join(all_titles),
            file_name="judul_koran_v3.txt",
            mime="text/plain"
        )

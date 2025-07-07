
import streamlit as st
import fitz  # PyMuPDF

st.set_page_config(page_title="Ekstraksi Judul PDF OCR", layout="wide")
st.title("📰 Ekstraksi Judul Berita dari PDF Koran (Sudah OCR)")

uploaded_file = st.file_uploader("Unggah PDF koran hasil scan (OCR)", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    st.success(f"PDF dimuat. Jumlah halaman: {len(doc)}")

    all_titles = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")  # ambil plain text

        lines = text.split('\n')
        probable_titles = [line.strip() for line in lines if len(line.strip()) > 8 and line.isupper()]

        st.subheader(f"Halaman {page_num + 1}")
        if probable_titles:
            for t in probable_titles:
                st.markdown(f"- **{t}**")
            all_titles.extend(probable_titles)
        else:
            st.text("❗ Tidak ada judul terdeteksi di halaman ini.")

    if all_titles:
        st.download_button(
            label="💾 Unduh Semua Judul",
            data="\n".join(all_titles),
            file_name="judul_koran_ocr.txt",
            mime="text/plain"
        )

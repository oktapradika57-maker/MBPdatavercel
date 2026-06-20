import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Kurva S", layout="wide")
st.title("📊 Dashboard Analisa Kurva S Proyek")

uploaded_file = st.file_uploader("Unggah file Excel (Format .xlsx)", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # Menampilkan kolom agar Anda yakin nama kolomnya benar
    st.write("Kolom terdeteksi:", df.columns.tolist())
    
    if st.button("Mulai Analisa"):
        try:
            # SESUAIKAN NAMA DI BAWAH DENGAN HASIL 'Kolom terdeteksi' di atas
            col_date = 'Submitted time' 
            col_value = 'Interval'
            
            # Konversi tanggal
            df[col_date] = pd.to_datetime(df[col_date])
            df = df.sort_values(col_date)

            # Menghitung Kumulatif dari kolom Interval
            df['Kumulatif_Aktual'] = df[col_value].cumsum()

            # Visualisasi
            st.subheader("Grafik Pencapaian Kumulatif")
            fig, ax = plt.subplots(figsize=(10, 5))
            
            ax.plot(df[col_date], df['Kumulatif_Aktual'], 
                    label='Aktual Kumulatif', color='green', marker='o', linewidth=2)
            
            ax.set_title('Kurva S Pencapaian', fontsize=16)
            ax.set_xlabel('Submitted Time')
            ax.set_ylabel('Total Kumulatif')
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend()
            
            st.pyplot(fig)
            
            # Menampilkan ringkasan data
            st.write("Data Kumulatif Terproses:")
            st.dataframe(df[[col_date, col_value, 'Kumulatif_Aktual']])

        except KeyError as e:
            st.error(f"Error: Kolom {e} tidak ditemukan. Pastikan penulisan huruf besar/kecil di Excel sama persis.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

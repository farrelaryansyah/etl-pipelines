from utils.extract import extract_fashion_products
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_google_sheets


def main():
    print("Memulai proses ETL...")

    try:
        # EXTRACT
        print("Menjalankan proses extract...")
        raw_data = extract_fashion_products()
        print(f"Data berhasil diambil: {len(raw_data)} record")

        # TRANSFORM
        print("Menjalankan proses transformasi...")
        cleaned_data = transform_data(raw_data)
        print(f"Data setelah transformasi: {len(cleaned_data)} baris")

        # LOAD
        print("Menyimpan ke CSV dan Google Sheets...")
        save_to_csv(cleaned_data)
        save_to_google_sheets(
            cleaned_data,
            spreadsheet_id="1UtSLOn2BDwMQGs1tzL7oh0huDaXRYCEs1X0BTwh543Q",
            range_name="Sheet1"
        )

        print("Proses ETL selesai tanpa error.")

    except Exception as e:
        print(f"Terjadi kesalahan saat menjalankan ETL: {e}")


if __name__ == "__main__":
    main()
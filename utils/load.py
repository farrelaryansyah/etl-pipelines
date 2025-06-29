import pandas as pd
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


def save_to_csv(df, filename="products.csv"):
    try:
        df.to_csv(filename, index=False)
        print(f"[INFO] Data berhasil disimpan ke {filename}")
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan ke CSV: {e}")


def save_to_google_sheets(df, spreadsheet_id, range_name, creds_file="google-sheets-api.json"):
    try:
        if not os.path.exists(creds_file):
            raise FileNotFoundError(f"File kredensial '{creds_file}' tidak ditemukan.")

        creds = Credentials.from_service_account_file(creds_file, scopes=["https://www.googleapis.com/auth/spreadsheets"])
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        values = [df.columns.tolist()] + df.values.tolist()
        body = {"values": values}

        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body,
        ).execute()

        print(f"[INFO] Data berhasil disimpan ke Google Sheets: {spreadsheet_id} - {range_name}")

    except Exception as e:
        print(f"[ERROR] Gagal menyimpan ke Google Sheets: {e}")
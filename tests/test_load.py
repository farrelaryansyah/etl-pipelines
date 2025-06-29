import os
import pandas as pd
from utils.load import save_to_csv, save_to_google_sheets


def test_save_to_csv_success(tmp_path):
    df = pd.DataFrame({"title": ["Shirt"]})
    file_path = tmp_path / "test_output.csv"
    save_to_csv(df, str(file_path))
    assert os.path.exists(file_path)


def test_save_to_csv_with_io_error(monkeypatch):
    def fake_to_csv(*args, **kwargs):
        raise IOError("Simulasi error CSV")

    monkeypatch.setattr(pd.DataFrame, "to_csv", fake_to_csv)
    df = pd.DataFrame({"title": ["Shirt"]})
    save_to_csv(df, "dummy.csv")


def test_save_to_csv_error(monkeypatch):
    df = pd.DataFrame({"title": ["A"], "price": [1000]})

    def fake_to_csv(*args, **kwargs):
        raise IOError("Disk penuh")

    monkeypatch.setattr("pandas.DataFrame.to_csv", fake_to_csv)
    save_to_csv(df, filename="fail.csv")


def test_save_to_google_sheets_missing_credential():
    df = pd.DataFrame({"title": ["Item"]})
    save_to_google_sheets(df, "dummy_id", "Sheet1!A1", creds_file="tidak_ada_file.json")


def test_save_to_google_sheets_invalid(monkeypatch):
    class DummySheet:
        def values(self):
            raise Exception("Simulasi gagal update Google Sheets")

    def dummy_build(*args, **kwargs):
        return type("DummyService", (), {"spreadsheets": lambda: DummySheet()})()

    monkeypatch.setattr("googleapiclient.discovery.build", dummy_build)
    df = pd.DataFrame({"title": ["Item"]})
    save_to_google_sheets(df, "dummy_id", "Sheet1!A1", creds_file="google-sheets-api.json")


def test_save_to_google_sheets_file_not_found():
    df = pd.DataFrame({"title": ["A"], "price": [1000]})
    save_to_google_sheets(df, "dummy_id", "Sheet1", creds_file="non_existent_file.json")


def test_save_to_google_sheets_invalid_file():
    df = pd.DataFrame({"title": ["A"], "price": [1000]})
    save_to_google_sheets(df, "fake_id", "Sheet1", creds_file="tidak_ada.json")
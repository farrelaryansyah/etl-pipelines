import pandas as pd
from utils.transform import transform_data


def test_transform_valid_data():
    data = [{
        "title": "Shirt",
        "price": "$10.00",
        "rating": "Rating: 4.5 / 5",
        "colors": "Colors: 3",
        "size": "Size: M",
        "gender": "Gender: Unisex"
    }]
    df = transform_data(data)
    assert not df.empty
    assert df["price"].iloc[0] == 160000
    assert df["rating"].iloc[0] == 4.5
    assert df["colors"].iloc[0] == 3


def test_transform_invalid_price():
    data = [{
        "title": "Shirt",
        "price": "invalid_price",
        "rating": "Rating: 4.5 / 5",
        "colors": "Colors: 3",
        "size": "Size: M",
        "gender": "Gender: Unisex"
    }]
    df = transform_data(data)
    assert df.empty


def test_transform_invalid_rating():
    data = [{
        "title": "Shirt",
        "price": "$10.00",
        "rating": "Invalid Rating",
        "colors": "Colors: 3",
        "size": "Size: M",
        "gender": "Gender: Unisex"
    }]
    df = transform_data(data)
    assert df.empty


def test_transform_invalid_colors():
    data = [{
        "title": "Shirt",
        "price": "$10.00",
        "rating": "Rating: 4.5 / 5",
        "colors": "Colors: none",
        "size": "Size: M",
        "gender": "Gender: Unisex"
    }]
    df = transform_data(data)
    assert df.empty


def test_transform_with_invalid_data_type():
    invalid_data = "bukan list"
    df = transform_data(invalid_data)
    assert isinstance(df, pd.DataFrame)
    assert df.empty


def test_transform_with_missing_fields():
    raw_data = [{
        "title": "Test",
        "price": "$10",
        "rating": "Rating: ⭐ 4.5/5",
        "colors": "Colors: 3 available",
        "size": None,
        "gender": "Gender: Unisex",
        "timestamp": "2023-01-01"
    }]
    df = transform_data(raw_data)
    assert df.empty


def test_transform_invalid_price_type():
    raw_data = [{
        "title": "Bad Price",
        "price": "NOT_A_PRICE",
        "rating": "Rating: ⭐ 4.0/5",
        "colors": "Colors: 2 available",
        "size": "Size: M",
        "gender": "Gender: Male",
        "timestamp": "2023-01-01"
    }]
    df = transform_data(raw_data)
    assert df.empty
import pandas as pd
import re
from datetime import datetime

USD_TO_IDR = 16000  # Konversi 1 USD = Rp16.000

import pandas as pd
import re
from datetime import datetime

USD_TO_IDR = 16000  # Konversi 1 USD = Rp16.000

def transform_data(raw_data):
    try:
        df = pd.DataFrame(raw_data)

        df.dropna(how='all', inplace=True)
        df.drop_duplicates(inplace=True)

        def clean_price(val):
            try:
                return round(float(val.replace("$", "").strip()) * USD_TO_IDR)
            except:
                return None

        df['price'] = df['price'].apply(clean_price)

        def parse_rating(rating_text):
            try:
                return float(rating_text.split('/')[0].replace("Rating:", "").replace("⭐", "").strip())
            except:
                return None

        df['rating'] = df['rating'].apply(parse_rating)

        def parse_colors(color_text):
            try:
                match = re.search(r'\d+', str(color_text))
                return int(match.group()) if match else None
            except:
                return None

        df['colors'] = df['colors'].apply(parse_colors)

        df['size'] = df['size'].str.replace("Size:", "").str.strip()
        df['gender'] = df['gender'].str.replace("Gender:", "").str.strip()

        df["timestamp"] = datetime.now().isoformat()

        df = df.astype({
            "title": "object",
            "price": "float64",
            "rating": "float64",
            "colors": "int64",
            "size": "object",
            "gender": "object",
            "timestamp": "object"
        })

        df.dropna(subset=["price", "rating", "colors", "size", "gender"], inplace=True)

        return df

    except Exception as e:
        print(f"Terjadi kesalahan saat transformasi: {e}")
        return pd.DataFrame()
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def extract_fashion_products(base_url="https://fashion-studio.dicoding.dev", pages=50):
    records = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for page_num in range(1, pages + 1):
        # Perbaikan struktur URL
        if page_num == 1:
            page_url = base_url + "/"
        else:
            page_url = f"{base_url}/page{page_num}"

        try:
            response = requests.get(page_url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            product_cards = soup.select("div.collection-card")

            for card in product_cards:
                try:
                    product_info = {}

                    title_elem = card.select_one("h3.product-title")
                    product_info["title"] = title_elem.text.strip() if title_elem else "Unknown Product"

                    price_elem = card.select_one(".price-container")
                    product_info["price"] = price_elem.text.strip() if price_elem else "N/A"

                    details = card.select("p")
                    for detail in details:
                        text = detail.text.strip()
                        if "Rating" in text:
                            product_info["rating"] = text
                        elif "Colors" in text:
                            product_info["colors"] = text
                        elif "Size:" in text:
                            product_info["size"] = text
                        elif "Gender:" in text:
                            product_info["gender"] = text

                    product_info["timestamp"] = datetime.now().isoformat()
                    records.append(product_info)

                except Exception as product_err:
                    print(f"[Produk Error] Halaman {page_num}: {product_err}")
                    continue

        except Exception as page_err:
            print(f"[Halaman Error] Tidak dapat mengambil halaman {page_num}: {page_err}")

    return records
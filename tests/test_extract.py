from utils.extract import extract_fashion_products

def test_extract_returns_list():
    data = extract_fashion_products(pages=1)
    assert isinstance(data, list)
    assert len(data) > 0
    assert "title" in data[0]


def test_extract_product_error(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            text = '''
                <div class="collection-card">
                    <h3 class="product-title">Test Product</h3>
                    <div class="price-container">$10</div>
                    <p>Invalid HTML will cause error</p>
                </div>
            '''
            def raise_for_status(self): pass
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    result = extract_fashion_products(pages=1)
    assert isinstance(result, list)


def test_extract_with_broken_product(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            text = '''
                <div class="collection-card">
                    <p>Missing title and price</p>
                </div>
            '''
            def raise_for_status(self): pass
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    result = extract_fashion_products(pages=1)
    assert isinstance(result, list)
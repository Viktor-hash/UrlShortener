from api.service import URLService

def test_create_short_url_new_url():
    service = URLService()
    original_url = "https://www.example.com"
    host_url = "http://localhost/"
    result = service.create_short_url(original_url, host_url)
    assert result["already_exists"] == False
    assert "short_code" in result
    assert "short_url" in result
    assert result["short_url"].startswith(host_url)

def test_create_short_url_existing_url():
    service = URLService()
    original_url = "https://www.example.com"
    host_url = "http://localhost/"
    result1 = service.create_short_url(original_url, host_url)
    result2 = service.create_short_url(original_url, host_url)
    assert result2["already_exists"] == True
    assert result1["short_code"] == result2["short_code"]

def test_get_stats_returns_stored_url():
    service = URLService()
    original_url = "https://www.example.com"
    host_url = "http://localhost/"
    result = service.create_short_url(original_url, host_url)
    stats = service.get_stats(result["short_code"])
    assert stats is not None
    assert stats.url == original_url
    assert stats.visits == 0

def test_get_stats_returns_none_for_invalid_code():
    service = URLService()
    assert service.get_stats("invalid") is None

def test_increment_visits_increments_and_returns_url():
    service = URLService()
    original_url = "https://www.example.com"
    host_url = "http://localhost/"
    result = service.create_short_url(original_url, host_url)
    code = result["short_code"]
    url = service.increment_visits(code)
    assert url == original_url
    stats = service.get_stats(code)
    assert stats.visits == 1

def test_increment_visits_returns_none_for_invalid_code():
    service = URLService()
    assert service.increment_visits("invalid") is None

def test_reset_clears_data():
    service = URLService()
    original_url = "https://www.example.com"
    host_url = "http://localhost/"
    result = service.create_short_url(original_url, host_url)
    code = result["short_code"]
    service.reset()
    assert service.get_stats(code) is None
    assert original_url not in service.url_to_code


def test_is_valid_url():
    service = URLService()

    assert service.is_valid_url("https://www.example.com") == True
    assert service.is_valid_url("http://localhost:8080") == True
    assert service.is_valid_url("https://sub.domain.com/path") == True

    assert service.is_valid_url("not_a_url") == False
    assert service.is_valid_url("ftp://example.com") == False
    assert service.is_valid_url("") == False
    assert service.is_valid_url("www.example.com") == False
    assert service.is_valid_url("https://") == False
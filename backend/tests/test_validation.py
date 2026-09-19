import pytest
from app.services.validation import validate_email, validate_website, normalize_domain, normalize_company_name


@pytest.mark.parametrize('value', ['team@example.com', 'first.last+demo@company.example.com'])
def test_good_email(value):
    assert validate_email(value)


@pytest.mark.parametrize('value', [None, '', 'bad', '@example.com', 'a..b@example.com', '.abc@example.com', 'a b@example.com', 'a@http://example.com', 'a@example.com/', 'a@example.com.', 'a@localhost'])
def test_bad_email(value):
    assert not validate_email(value)


@pytest.mark.parametrize('value', ['https://www.example.com', 'http://example.com/', 'example.com', 'HTTPS://EXAMPLE.COM/path'])
def test_domain_normalization(value):
    assert normalize_domain(value) == 'example.com'
    assert validate_website(value)


@pytest.mark.parametrize('value', [None, '', 'not a url', 'javascript:alert(1)', 'https://user:password@example.com', 'https://example.com:bad', 'https://-bad.com', 'http://localhost', '127.0.0.1'])
def test_unsafe_or_malformed_urls(value):
    assert not validate_website(value)


def test_subdomains_and_names():
    assert normalize_domain('https://shop.example.com') == 'shop.example.com'
    assert normalize_company_name(' ACME,   Labs! ') == 'acme labs'

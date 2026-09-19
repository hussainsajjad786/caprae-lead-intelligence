import csv
import io
import pytest
from app.routes.export import safe_cell


def test_health_and_detail(client):
    assert client.get('/health').json() == {'status': 'ok'}
    assert client.get('/').json()['dataset'] == 'Demo / Synthetic Data'
    assert client.get('/api/leads/1').json()['lead_score'] == 100
    assert client.get('/api/leads/99999').status_code == 404


def test_filters_and_stats(client):
    all_rows = client.get('/api/leads').json()
    assert all_rows['total'] == 32
    assert len(all_rows['items']) == 32
    params = {'search': 'ASTER', 'industry': 'SaaS', 'location': 'United States', 'min_score': 90, 'max_score': 100, 'priority': 'High', 'verification_status': 'Format Valid'}
    rows = client.get('/api/leads', params=params).json()
    assert rows['total'] == 1
    assert rows['items'][0]['company_name'] == 'Aster Cloud (Demo)'
    assert client.get('/api/leads?search=%25').json()['total'] == 0
    stats = client.get('/api/stats').json()
    assert stats['total'] == 32 and stats['duplicates_prevented'] == 2
    assert stats['externally_verified'] == 0
    assert sum(stats['priorities'].values()) == 32
    assert stats['format_valid'] + stats['needs_review'] == 32
    assert len(client.get('/api/quality/duplicates').json()) == 2
    assert 'SaaS' in client.get('/api/industries').json()
    assert 'United States' in client.get('/api/locations').json()


@pytest.mark.parametrize('query', ['min_score=101', 'min_score=-1', 'min_score=90&max_score=20', 'priority=Urgent', 'limit=101', 'offset=-1', 'verification_status=Verified'])
def test_invalid_parameters(client, query):
    assert client.get('/api/leads?' + query).status_code == 422


def test_pagination(client):
    a = client.get('/api/leads?limit=10').json()
    b = client.get('/api/leads?limit=10&offset=10').json()
    assert len(a['items']) == len(b['items']) == 10
    assert not ({x['id'] for x in a['items']} & {x['id'] for x in b['items']})


def test_export_matches_filter_across_pages(client):
    params = {'priority': 'High'}
    expected = client.get('/api/leads', params=params).json()
    result = client.get('/api/leads/export', params=params)
    assert result.status_code == 200
    assert result.headers['content-type'].startswith('text/csv')
    exported = list(csv.DictReader(io.StringIO(result.text)))
    assert len(exported) == expected['total']
    assert [x['company_name'] for x in exported] == [x['company_name'] for x in expected['items']]
    assert all(x['priority'] == 'High' for x in exported)
    assert client.get('/api/leads/export?min_score=101').status_code == 422


@pytest.mark.parametrize('value', ['=1+1', '+SUM(A1)', '-cmd', '@command', '   =SUM(A1)', '\t=1', '+1-202-555-0100'])
def test_csv_formula_protection(value):
    assert safe_cell(value).startswith("'")


def test_csv_ordinary_values():
    assert safe_cell('Aster, Inc.') == 'Aster, Inc.'
    assert safe_cell(None) == ''


def test_optional_frontend_preserves_api(client, monkeypatch, tmp_path):
    import app.main as main
    (tmp_path / 'index.html').write_text('<!doctype html><title>Hosted demo</title>', encoding='utf-8')
    monkeypatch.setattr(main, 'FRONTEND_DIR', tmp_path)
    response = client.get('/')
    assert response.status_code == 200
    assert response.headers['content-type'].startswith('text/html')
    assert 'Hosted demo' in response.text
    assert client.get('/api/leads').json()['total'] == 32
    assert client.get('/health').json() == {'status': 'ok'}

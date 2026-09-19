import pytest
from app.services.scoring import score_lead, priority_for
from app.services.lead_quality import assess_quality
from app.seed.demo_data import demo_records


def test_full_fit_is_explainable():
    row = demo_records()[0]
    result = score_lead(row, assess_quality(row))
    assert result['lead_score'] == 100
    assert sum(r['points'] for r in result['score_reasons']) == result['lead_score']
    assert result == score_lead(row, assess_quality(row))
    assert result['priority'] == 'High'


@pytest.mark.parametrize('score, expected', [(0, 'Low'), (49, 'Low'), (50, 'Medium'), (74, 'Medium'), (75, 'High'), (100, 'High')])
def test_priority_boundaries(score, expected):
    assert priority_for(score) == expected


def test_missing_data_does_not_earn_fit_points():
    row = {'company_name': 'Sparse'}
    quality = assess_quality(row)
    assert quality['quality_score'] == 12
    assert quality['data_completeness'] == 12
    assert score_lead(row, quality)['lead_score'] == 1


def test_bad_formats_reduce_quality_not_completeness():
    row = {**demo_records()[0], 'website': 'bad url', 'email': 'bad'}
    quality = assess_quality(row)
    assert quality['data_completeness'] == 100
    assert quality['quality_score'] == 75
    assert quality['verification_status'] == 'Needs Review'
    assert score_lead(row, quality)['lead_score'] == 90


@pytest.mark.parametrize('employees, points', [(0, 0), (9, 5), (10, 12), (49, 12), (50, 20), (199, 20), (200, 25)])
def test_size_boundaries(employees, points):
    row = {**demo_records()[0], 'employees': employees}
    assert score_lead(row, assess_quality(row))['score_reasons'][0]['points'] == points


@pytest.mark.parametrize('revenue, points', [(0, 0), (999999, 5), (1000000, 10), (5000000, 15), (10000000, 20)])
def test_revenue_boundaries(revenue, points):
    row = {**demo_records()[0], 'revenue': revenue}
    assert score_lead(row, assess_quality(row))['score_reasons'][2]['points'] == points

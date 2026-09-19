from .validation import validate_email, validate_website

FIELDS = ('company_name', 'website', 'email', 'phone', 'industry', 'location', 'employees', 'revenue')


def assess_quality(data: dict) -> dict:
    email_valid, website_valid = validate_email(data.get('email')), validate_website(data.get('website'))
    present = {field: data.get(field) is not None and str(data[field]).strip() != '' for field in FIELDS}
    checks = {**present, 'email': email_valid, 'website': website_valid}
    score = round(sum(checks.values()) / len(FIELDS) * 100)
    flags = [f'Missing {field.replace("_", " ")}' for field, ok in present.items() if not ok]
    flags += [f'Invalid {field} format' for field, ok in [('email', email_valid), ('website', website_valid)] if present[field] and not ok]
    return dict(email_valid=email_valid, website_valid=website_valid,
                verification_status='Format Valid' if email_valid and website_valid else 'Needs Review',
                data_completeness=round(sum(present.values()) / len(FIELDS) * 100),
                quality_score=score, quality_label='High Quality' if score >= 85 else 'Medium Quality' if score >= 60 else 'Low Quality',
                quality_flags=flags)

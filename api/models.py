from flask_restx import fields, Api

def init_models(api: Api):
    url_model = api.model('URL', {
        'url': fields.String(required=True, description='URL to shorten')
    })

    stats_model = api.model('Stats', {
        'url': fields.String(description='Original URL'),
        'visits': fields.Integer(description='Number of visits'),
        'created_at': fields.DateTime(description='Creation date')
    })

    shortened_url_model = api.model('ShortenedURL', {
        'short_code': fields.String(description='Generated short code'),
        'short_url': fields.String(description='Complete shortened URL')
    })

    error_model = api.model('ShortenedURL', {
        'message': fields.String(description='Error message'),
    })

    return url_model, stats_model, shortened_url_model, error_model
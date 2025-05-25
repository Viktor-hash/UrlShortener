from flask import Flask, request, jsonify, redirect
from flask_restx import Api, Resource, fields, Namespace
from hashids import Hashids
from datetime import datetime

app = Flask(__name__)
api = Api(app, version='1.0', title='URL Shortener API',
    description='A URL shortening API')

ns = Namespace('shortener', description='URL shortening operations')
api.add_namespace(ns)

# Swagger models
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

# In-memory storage
url_store = {}
url_to_code = {}

# Hashids configuration
hashids = Hashids(min_length=6, salt="votre_sel_unique")
id_counter = 1

@ns.route('/shorten')
class URLShortener(Resource):
    @ns.doc('create_short_url',
            description='Create a shortened URL',
            responses={
                201: 'URL shortened successfully',
                200: 'URL already exists'
            })
    @ns.expect(url_model)
    @ns.marshal_with(shortened_url_model)
    def post(self):
        global id_counter
        data = request.json
        original_url = data.get('url')

        if original_url in url_to_code:
            short_code = url_to_code[original_url]
            return {
                "short_code": short_code,
                "short_url": request.host_url + short_code
            }, 200

        short_code = hashids.encode(id_counter)
        id_counter += 1

        url_store[short_code] = {
            'url': original_url,
            'visits': 0,
            'created_at': datetime.now()
        }
        url_to_code[original_url] = short_code

        return {
            "short_code": short_code,
            "short_url": request.host_url + short_code
        }, 201

@ns.route('/stats/<string:short_code>')
class URLStats(Resource):
    @ns.doc('get_url_stats',
            description='Get statistics for a shortened URL',
            responses={
                200: 'Statistics retrieved successfully',
                404: 'Short code not found'
            })
    @ns.marshal_with(stats_model)
    def get(self, short_code):
        if short_code in url_store:
            return url_store[short_code], 200
        api.abort(404, "Short code not found")

# Route de redirection (hors namespace)
@app.route('/<short_code>')
def redirect_url(short_code):
    if short_code in url_store:
        url_store[short_code]['visits'] += 1
        return redirect(url_store[short_code]['url'])
    return jsonify({"message": "Short code not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
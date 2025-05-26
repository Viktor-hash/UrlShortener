from flask import request, redirect, Response
from flask_restx import Resource, Namespace
from typing import Union, Dict, Any

from api.stored_url import StoredURL
from .service import URLService
from .models import init_models

ns = Namespace('shortener', description='URL shortening operations')
url_service = URLService()

# Initialize models
url_model, stats_model, shortened_url_model, error_model = init_models(ns)

@ns.route('/shorten')
class URLShortener(Resource):
    @ns.doc('create_short_url',
            description='Create a shortened URL',
            responses={
                201: 'URL shortened successfully',
                200: 'URL already exists'
            })
    @ns.expect(url_model)
    @ns.response(201, 'URL shortened successfuly', shortened_url_model)
    @ns.response(200, 'URL already existing', shortened_url_model)
    @ns.response(400, 'URL invalide', error_model)
    def post(self) -> tuple[dict, int]:
        data: dict = request.json
        result = url_service.create_short_url(data.get('url'), request.host_url)
        if "error" in result:
            return {"message": result["error"]}, 400
        status = 200 if result["already_exists"] else 201
        result.pop("already_exists")
        return result, status

@ns.route('/stats/<string:short_code>')
class URLStats(Resource):
    @ns.doc('get_url_stats',
            description='Get statistics for a shortened URL',
            responses={
                200: 'Statistics retrieved successfully',
                404: 'Short code not found'
            })
    def get(self, short_code: str) -> tuple[Dict, int]:
        stats = url_service.get_stats(short_code)
        if stats:
            return ns.marshal(stats, stats_model), 200
        return {"message": "Short code not found"}, 404

@ns.route('/<short_code>')
class URLRedirect(Resource):
    @ns.doc('redirect_to_url',
            description='Redirect to original URL',
            responses={
                302: 'Redirect to original URL',
                404: 'Short code not found'
            })
    def get(self, short_code: str) -> Union[Response, tuple[Dict, int]]:
        target_url = url_service.increment_visits(short_code)
        if target_url:
            return redirect(target_url)
        return {"message": "Short code not found"}, 404
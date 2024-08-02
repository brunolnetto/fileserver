from django.utils.deprecation import MiddlewareMixin
from htmlmin.minify import html_minify

class MinifyHtmlMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.get('Content-Type') == 'text/html; charset=utf-8':
            response.content = html_minify(response.content.decode('utf-8')).encode('utf-8')
        return response
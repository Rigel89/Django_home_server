from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

# Create your views here.

def helloworld(request):
    logging.error('Hello world, Rigel89 in the log...')
    print('Hello world Rigel89 in a print statement...')
    response = """<html><body><p>Hello world Rigel89 in HTML</p>
    <p>This sample code is available at
    <a href="https://github.com/Rigel89/Django_home_server.git">
    https://github.com/Rigel89/Django_home_server.git</a></p>
    </body></html>"""
    return HttpResponse(response)
from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.response import Response


def home(request):
    return Response('Home Pyramid')


if __name__ == '__main__':
    config = Configurator()
    
    config.add_route('home', '/')
    config.add_view(home, route_name='home')
    
    app = config.make_wsgi_app()
    
    # This does nothing unles you run this module with --testliveserver flag.
    import testliveserver
    testliveserver.WsgirefSimpleServer.wrap(app)
    
    server = make_server('127.0.0.1', 8080, app)
    
    server.serve_forever()
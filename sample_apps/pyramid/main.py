from wsgiref.simple_server import make_server

from pyramid.config import Configurator
from pyramid.response import Response


def home(request):
    content = 'Home Pyramid'
    if request.scheme == 'https':
        content += ' SSL'

    return Response(content)


if __name__ == '__main__':
    config = Configurator()

    config.add_route('home', '/')
    config.add_view(home, route_name='home')

    app = config.make_wsgi_app()

    # This does nothing unles you run this module with --liveandletdie flag.
    import liveandletdie
    liveandletdie.WsgirefSimpleServer.wrap(app)

    server = make_server('127.0.0.1', 8080, app)

    server.serve_forever()

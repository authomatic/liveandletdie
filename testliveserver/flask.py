import socket
import sys
import testliveserver


def live_server(app):
    """
    Adds test live server capability to a Flask app module.
    
    :param app:
        A :class:`flask.Flask` app instance.
    """
    
    host, port = testliveserver.parse_args()
    if host:
        app.config['DEBUG'] = False
        app.run(host=host, port=port)
        
        print('Flask live server running at {}:{} terminated!'.format(host, port))
        sys.exit()

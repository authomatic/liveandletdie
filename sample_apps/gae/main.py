import webapp2


class Home(webapp2.RequestHandler):
    def get(self):
        self.response.write('Home')


ROUTES = [webapp2.Route(r'/', Home)]


app = webapp2.WSGIApplication(ROUTES, debug=True)
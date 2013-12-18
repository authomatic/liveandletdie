from flask import Flask

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
    return 'Home Flask'

if __name__ == '__main__':
    
    # This does nothing unles you run this module with --liveandletdie flag.
    import liveandletdie
    liveandletdie.Flask.wrap(app)
    
    app.run()

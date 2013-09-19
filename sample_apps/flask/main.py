from flask import Flask

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
    return 'Home'

if __name__ == '__main__':
    
    # This does nothing unles you run this module with --testliveserver flag.
    import testliveserver
    testliveserver.Flask.wrap(app)
    
    app.run()

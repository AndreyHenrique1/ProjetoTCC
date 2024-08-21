from routes.homeRoutes import home_route
import pyrebase

def configure_all(app):
    configure_routes(app)
    configure_firebase(app)

def configure_routes(app):
    app.register_blueprint(home_route)


def configure_firebase(app):
    firebaseConfig = {
        "apiKey": "AIzaSyDDXFTqJ4vxld_8LhYMfpXnSnDhIRaBZTU",
        "authDomain": "projeto-tcc-255b4.firebaseapp.com",
        "databaseURL": "https://projeto-tcc-255b4-default-rtdb.firebaseio.com",
        "projectId": "projeto-tcc-255b4",
        "storageBucket": "projeto-tcc-255b4.appspot.com",
        "messagingSenderId": "1092765424414",
        "appId": "1:1092765424414:web:36443c9e0409d849c5c70f"
    }

    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    app.config['FIREBASE_DB'] = db

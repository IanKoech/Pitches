from flask import Flask
from flask_bootstrap import Bootstrap

#Making instances of the flask modules
bootstrap=Bootstrap()


def create_app():
    #__name__ below determines root path of the application
    app=Flask(__name__)

    return app
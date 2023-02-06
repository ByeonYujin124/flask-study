from flask import Flask

app = Flask(__name__)

from apiapp import views

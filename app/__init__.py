from flask import  Flask
from flask_restx import  Api

app = Flask(__name__)
api=Api(
    app,
    title= 'Bordeplait Version',
    version='0.1',
    description='Repaso la documentacion',
    doc='/swagger-ui'
)
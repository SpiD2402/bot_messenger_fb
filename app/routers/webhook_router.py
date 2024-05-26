from app import  api
from flask import  request
from flask_restx import Resource
from app.controllers.webhook_controller import  WebhookController

namespace =api.namespace(
    name='Webhook Facebook',
    path='/webhook'
)

@namespace.route('/setup')
class Setup(Resource):
    def post(self):
        controller = WebhookController()
        return controller.setup()



@namespace.route('')
class Webhook(Resource):
    def get(self):
        query = request.args
        controller = WebhookController()
        return  controller.suscribe(query)

    def post(self):
        controller = WebhookController()
        return controller.messagesEvents(request.json)

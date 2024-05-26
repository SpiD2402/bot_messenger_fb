from os import  getenv
from app.utils.facebook import Facebook
from flask import  Response


class WebhookController:
    def __init__(self):
        self.facebook = Facebook()
        self.verification_token= getenv('FACEBOOK_WEBHOOK_TOKEN')
    def setup(self):
        self.facebook.initSetup()
        return Response(status=200)

    def  suscribe(self,query):
        mode=query['hub.mode']
        challenge=query['hub.challenge']
        token = query['hub.verify_token']
        if mode == 'subscribe' and token == self.verification_token:
            return  Response(response = challenge, status=200)
        return  Response(status = 403)

    def messagesEvents(self,body):
        print(body)
        for entry in body['entry']:
            messaging=entry['messaging']
            for message in messaging:
                sender=message['sender']['id']
                if message.get('postback'):
                    self.postBackEvent(message,sender)
                else:
                    self.messageEvent(message,sender)
        return  Response(status = 200)

    def postBackEvent(self,body,sender):
        payload = body['postback']['payload']
        if payload =='GET_STARTED_PAYLOAD':
            return  self.facebook.quickReplyMessage(
                'Hola, ¿Que deseas hacer ?',
                sender

            )
    def messageEvent(self,body,sender):
        message = body['message']

        if not message.get('quick_reply'):
            search= message['text']
            self.facebook.spotifyMusic(search,sender)
            return self.facebook.quickReplyMessage(
                'Deseas realizar algo mas?',
                sender
            )

        payload = message['quick_reply']['payload']
        return self.quickReplyEvent(payload,sender)


    def  quickReplyEvent(self,payload,sender):
        if  payload == 'SEARCH_MUSIC':
            return self.facebook.searchMusicMessage(sender)

        if payload =='TALK_CHAT':
            self.facebook.talkChatMessage(sender)

        return  self.facebook.quickReplyMessage(
            'Ahora que deseas hacer ?',
            sender

        )


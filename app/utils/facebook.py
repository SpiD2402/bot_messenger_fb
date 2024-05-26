from os import getenv
from random import choice
from app.utils.spotify import SpotifyClient
from requests import post

class  Facebook:
    def __init__(self):
        self.access_token=getenv('FACEBOOK_PAGE_TOKEN')
        self.url='https://graph.facebook.com'

    def initSetup(self):
        url =f'{self.url}/v15.0/me/messenger_profile'
        response = post(
            url,
            params = {
                'access_token': self.access_token,
            },
            json = {
                'get_started' : {
                    'payload' : 'GET_STARTED_PAYLOAD'
                },
                'greeting':[
                    {
                        'locale':'default',
                        'text':'Hola  {{user_full_name}} Guapo',
                    }
                ]
            }

        )
        return  response.json()

    def sendMessage(self,body):
        url = f'{self.url}/v15.0/me/messages'
        response = post(
            url,
            params = {
                'access_token': self.access_token,
            },
            json ={
                'messaging_type':'RESPONSE',
                'recipient':{
                    'id':body['recipient_id']
                },
                'message':body['message']

            }

        )
        return response.json()

    def quickReplyMessage(self,title,recipient_id):
        return  self.sendMessage({
            'recipient_id':recipient_id,
            'message' : {
                'text' : title ,
                "quick_replies" : [
                    {
                        "content_type" : "text" ,
                        "title" : "Buscar Musica" ,
                        "payload" : "SEARCH_MUSIC" ,
                        "image_url" : "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSDFNNGlcTS8sQRksRrEOlnKIzyy9AbIhCaNWzlLkksTw&s"
                    } , {
                        "content_type" : "text" ,
                        "title" : "Conversar" ,
                        "payload" : "TALK_CHAT" ,
                        "image_url" : "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRnSrL2DWPTcWMHGz6NCNcbp-zzDPMsgeevrR1mSTViMw&s"
                    }
                ]}

        })

    def talkChatMessage(self,recipient_id):
        messages=[
            'Ella no te ama :(',
            'Igual te dejo por otro',
            'Estas bien?'
        ]
        return self.sendMessage(
            {
                'recipient_id':recipient_id,
                'message':{
                    'text':choice(messages)
                }
            }
        )

    def searchMusicMessage(self,recipient_id):
        return self.sendMessage(
            {
                'recipient_id':recipient_id,
                'message':{
                    'text':'Ingrese el nombre de la cancion: '
                }
            }
        )

    def spotifyMusic(self,search,sender):
        try:
            spotify = SpotifyClient()
            results = spotify.searchTrack(search)
            tracks =results['tracks']['items']

            elements = [self.templatesTrack(track)
                for track in tracks


                        ]
            return self.sendMessage({
                'recipient_id':sender,
                'message':{
                    "attachment" : {
                        "type" : "template" ,
                        "payload" : {
                            "template_type" : "generic" ,
                            "elements" :
                                    elements

                        }
                    }
                }
            })
        except Exception as e:
            print(f'Spotify Error: {str(e)}')
            return  self.sendMessage(
                {
                    'recipient_id':sender,
                    'message':{
                        'text':'Opps vuelve a ingresar lo que quieres buscar'
                    }
                }
            )

    def templatesTrack(self,track):
        name= track['name']
        artist= track['artists'][0]['name']
        album= track['album']['name']
        image = track['album']['images'][0]['url']
        url = track['external_urls']['spotify']

        return  {
                "title" : f'{artist} - {name}' ,
                "image_url" : image ,
                "subtitle" : album ,
                "default_action" : {
                    "type" : "web_url" ,
                    "url" : url ,
                    "webview_height_ratio" : "tall"
                } ,
                    "buttons" : [
                            {
                                "type" : "web_url" ,
                                "url" : url ,
                                "title" : "Play Spotify Web"
                            }
                                ]
                }












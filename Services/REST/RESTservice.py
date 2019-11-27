import requests
import json


class httpService(object):

    serverIp = "http://localhost:1790/"

    def post(self,url,data):
        url = self.serverIp+url
        try:
            response = requests.post(url,json = data)
            json_response = response.json() 
            return(json_response)
        except Exception as e:
             return {'responseHeader' : {'status_code':'03', 'status_description' : str(e)}}
       
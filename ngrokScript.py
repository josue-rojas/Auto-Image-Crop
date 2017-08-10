import requests, json

def getURL():
    r = requests.get('http://localhost:4040/api/tunnels')
    return json.loads(r.text)['tunnels'][0]['public_url']

    

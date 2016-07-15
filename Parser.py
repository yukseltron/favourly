import json
import requests


class Parser:

    type = None
    action = ""
    user = ""
    timestamp = ""
    points = 0
    tup = []

    def __init__(self, msg, token):
        
        # Load data from json-formatted .txt file
        j = json.load(msg)
        self.timestamp = j['ts']
        
        # Get the username of the user from their user ID
        payload = {'token': token, 'user': j['user']}
        r = requests.get('https://slack.com/api/users.info', params=payload)
        u = json.loads(r.text)
        self.user = u['user']['name']
        
        t = j['text']
        wl = t.split(" ")
        
        # Determine what type of command was entered (favour creation, completion, or approval)
        if wl[0] == "do":
            self.type = 0
            for i in range(len(wl)):
                
                # Determine the action sentence
                if "points" in wl[i] or "pts" in wl[i]:
                    self.points = wl[i-1]
                if "do" in wl[i]:
                    sentence = ""
                    n = 1
                    while wl[i+n] != "for":
                        sentence += wl[i+n] + " "
                        n += 1
                    self.action = sentence[:(len(sentence)-1)]
            
            self.tup = [self.action, self.timestamp, self.user, self.points]
        elif wl[0] == "completed":
            self.type = 1
            self.action = " ".join(wl[2:])
            self.tup = [self.action, self.user]
        elif wl[0] == "approve":
            self.type = 2
            self.tup = [self.user]
        elif wl[0] == "favours":
            self.type = 3
            self.tup = []


    def getTuple(self):
        return self.tup

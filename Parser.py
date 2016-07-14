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
        j = json.load(msg)
        self.timestamp = j['ts']
        payload = {'token': token, 'user': j['user']}
        r = requests.get('https://slack.com/api/users.info', params=payload)
        u = json.loads(r.text)
        self.user = u['user']['name']
        t = j['text']
        wl = t.split(" ")
        if wl[0] == "do":
            self.type = 0
            for i in range(len(wl)):
                if "points" in wl[i] or "pts" in wl[i]:
                    self.points = wl[i-1]
                if "do" in wl[i]:
                    self.action = wl[i+1]
            self.tup = [self.action, self.timestamp, self.user, self.points]
        elif wl[0] == "completed":
            self.type = 1
            for i in range(len(wl)):
                if "do" in wl[i]:
                    self.action = wl[i + 1]
            self.tup = [self.action, self.user]
        elif wl[0] == "approve":
            self.type = 2
            self.tup = [self.user]
        elif wl[0] == "favours":
            self.type = 3
            self.tup = []


    def getTuple(self):
        return self.tup

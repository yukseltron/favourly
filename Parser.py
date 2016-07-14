import json


class Parser:

    type = None
    action = ""
    user = ""
    timestamp = ""
    points = 0
    tup = ()

    def __init__(self, msg):
        j = json.load(msg)
        self.timestamp = j['ts']
        self.user = j['user']
        t = j['text']
        wl = t.split(" ")
        if wl[0] == "do":
            self.type = 0
            for i in range(len(wl)):
                if "points" in wl[i] or "pts" in wl[i]:
                    self.points = wl[i-1]
                if "do" in wl[i]:
                    self.action = wl[i+1]
            self.tup = (self.action, self.timestamp, self.user, self.points)
        elif wl[0] == "completed":
            self.type = 1
            for i in range(len(wl)):
                if "do" in wl[i]:
                    self.action = wl[i + 1]
            self.tup = (self.action, self.user)
        elif wl[0] == "approve":
            self.type = 2
            self.tup = (self.user)


    def getTuple(self):
        return self.tup

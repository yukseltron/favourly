import json


class Parser:

    user = ""
    timestamp = ""
    minutes = 0
    points = 0

    def __init__(self, msg):
        j = json.load(msg)
        self.timestamp = j['ts']
        self.user = j['message']['username']
        t = j['message']['text']
        wl = t.split(" ")
        for i in range(len(wl)):
            if "minutes" in wl[i] or "mins" in wl[i]:
                self.minutes = wl[i-1]
            if "hours" in wl[i] or "hrs" in wl[i]:
                self.minutes = int(wl[i-1])*60
            if "points" in wl[i] or "pts" in wl[i]:
                self.points = wl[i-1]

    def getTuple(self):
        tup = (self.timestamp, self.user, self.minutes, self.points)
        return tup

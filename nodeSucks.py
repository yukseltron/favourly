import requests
import json


#toUser and fromUser must be emails
def updateBonusly(toEmail, toUser, fromEmail, fromUser, points, reason):
    if checkViable(fromUser, points) == True :
        payload = "{\"reason\":\"'+' + points + ' ' + fromUser + toUser + ' for ' + reason \",\"parent_bonus_id\":\"24abcdef1234567890abcdef\",\"giver_email\":\"fromEmail\"}"

        headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }

        r = requests.post('https://bonus.ly/api/v1/bonuses?access_token=c7c0773204728847c1a41c88395c2cac', payload, headers)
    else :
        raise Exception("This favourly cannot happen!")



#see if the transanction is legal
def checkViable(fromUser, toUser, points):
    headers = { 'accept': "application/json" }

    r = requests.get('https://bonus.ly/api/v1/users/' + fromUser + '?access_token=c7c0773204728847c1a41c88395c2cac', headers=headers)
    s = r.text
    t = json.loads(s)

    canGive = t[u'result'][u'can_give']
    if points not in t[u'result'][u'give_amounts'] :
        return False

    if t[u'result'][u'can_give'] == False :
        return False

    if t[u'result'][u'can_receive'] == False :
        return False

    return True

print(checkViable('5783a170be87004b667fe885', 1))


#all of it by tomorrow morning at 11:00 by the latest

import requests
import json

#slack usernames, points, reason
#toUser and fromUser are bonusly IDs
def doAll(toUser, fromUser, points, reason, token):
    toId = findUserId(toUser, token)
    fromId = findUserId(fromUser, token)
    toEmail = findUserEmail(toId, token)
    fromEmail = findUserEmail(fromId, token)

    if (checkViable(toId, fromId, points, token)) == True:
        giveBonusly(toUser, fromId, fromEmail, points, reason, token)
    else :
        raise Exception("This favourly cannot happen!")


#gives the bonusly points
def giveBonusly(toUser, fromId, fromEmail, points, reason, token):
    payload = {"reason":"+" + str(points) +  " @" + toUser + " " + reason + " #favourly", "parent_bonus_id": fromId, "giver_email": fromEmail}

    headers = {
    'accept': "application/json",
    'content-type': "application/json"
    }

    r = requests.post('https://bonus.ly/api/v1/bonuses?access_token=' + token, payload, headers)
    s = r.text
    #print("GIVE:", s)


#see if the transanction is legal
def checkViable(fromId, toId, points, token):
    headers = { 'accept': "application/json" }

    r1 = requests.get('https://bonus.ly/api/v1/users/' + fromId + '?access_token=' + token, headers=headers)
    r2 = requests.get('https://bonus.ly/api/v1/users/' + toId + '?access_token=' + token, headers=headers)

    s1 = r1.text
    s2 = r2.text

    t1 = json.loads(s1)
    t2 = json.loads(s2)

    if points not in t1[u'result'][u'give_amounts'] :
        return False

    if t1[u'result'][u'can_give'] == False :
        return False

    if t2[u'result'][u'can_receive'] == False :
        return False

    return True


#find username in "firstName.lastName" format
def findUserId(user, token):
    headers = { 'accept': "application/json" }

    r = requests.get('https://bonus.ly/api/v1/users?email=' + user + '@concur.com'  + '&access_token=' + token, headers=headers)
    s = r.text
    t = json.loads(s)

    return t[u'result'][0][u'id']


#Finds user email
def findUserEmail(userId, token):
    headers = { 'accept': "application/json" }

    r = requests.get('https://bonus.ly/api/v1/users/' + userId + '?access_token=' + token, headers=headers)
    s = r.text
    t = json.loads(s)

    return t[u'result'][u'email']

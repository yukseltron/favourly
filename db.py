from collections import OrderedDict as OD
import NodeSucks
from Parser import Parser as P
import psycopg2
import json


# creates an ordered dictionary from a tuple
def tup2od(tup, od):
    for i, thing in enumerate(od):
        od[thing] = tup[i]

connection = psycopg2.connect(host='localhost', database='Favorly', user='postgres', password='')
cursor = connection.cursor()
ins = 'INSERT INTO favors(favor, time_stamp, userid, points, done_by, completed) VALUES (%s, %s, %s, %s, %s, %s)'
sel = "SELECT favor, points FROM favors WHERE (completed = false) AND (done_by = 'null')"
sel2 = "SELECT userid, done_by, points, favor FROM favors WHERE completed = false AND userid = %s"
up1 = "UPDATE favors SET done_by = %s WHERE favor = %s"
up2 = "UPDATE favors SET completed = true WHERE completed = false AND userid = %s"
user = ' '
jsn = OD([('favor', ''), ('time_stamp', ''), ('userid', ''), ('points', 0), ('done_by', None), ('completed', None)])
infile = open('message.txt', 'r')
parsed = P(infile, 'xoxp-3490251431-53873975141-59895620595-1daeaecbd5')
# results = ['DO MY SHIT', '4.0', 'aname', 2]
results = parsed.tup

if parsed.type == 0:        # add
    results.append('null')
    results.append('false')
    cursor.execute(ins, results)
    connection.commit()

elif parsed.type == 1:
    cursor.execute(up1, list(reversed(results)))

elif parsed.type == 2:
    cursor.execute(sel2, results)
    row = cursor.fetchall()
    cursor.execute(up2, results)
    NodeSucks.doAll(*row)

elif parsed.type == 3:      # view
    cursor.execute(sel)
    rows = cursor.fetchall()
    with open('dump.js', 'w') as output:
        for row in rows:
            tup2od(row, jsn)
            json.dump(jsn, output)
            output.write('\n')


# if approve
connection.commit()


cursor.close()
connection.close()

# class DataBase:
#
#     INS = 'INSERT INTO favors %s'
#     tuple = ()
#     connection = psycopg2.connect('localhost', 'favors', 'postgres')
#
#     def __init__(self, tup):
#         self.tuple = tup
#
#     def add_tuple(self):
#         INS =

import mysql.connector
import pandas as pd
import datetime
import time
import numpy
import math
from math import sin, cos, sqrt, atan2, radians

db = mysql.connector.connect(host="localhost",  # your host, usually localhost
                             user="root",  # your username
                             passwd="Sohraab24",  # your password
                             db="480_proj")  # name of the data base
cur = db.cursor()

start_time = time.time()
cur.execute("SELECT * FROM sep_2015 WHERE Passenger_count = 1")
print("%s seconds for Outside Query" % (time.time() - start_time))

rows = cur.fetchall()


def dist(lat1, lon1, lat2, lon2):
    R = 6373.0

    la1 = radians(lat1)
    lo1 = radians(lon1)
    la2 = radians(lat2)
    lo2 = radians(lon2)

    dlon = lo2 - lo1
    dlat = la2 - la1

    a = sin(dlat / 2) ** 2 + cos(la1) * cos(la2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    distance = distance * 0.621371
    return distance


tb = rows
count = 0

for outsideLoop in tb:

    # Right now, we have read in the table (tb) & all of it's rows

    # We gotta filter the table with another cursor for what we want

    # What we want, is the pick-up time being < 10 minutes for the pick up time
    # So first, get the pick-up time for the current row of the table (tb)

    currPickUpTime = outsideLoop[0]

    # Now we gotta convert this STRING into DateTime
    timeConverted = datetime.datetime.strptime(currPickUpTime, '%Y-%m-%d %H:%M:%S')

    # Now we gotta add 10 mintues to the timeConverted
    newTime = timeConverted + datetime.timedelta(minutes=10)

    secondQStartTime = time.time()
    # Now we gotta Query through aug_2015, with our new +10 time range and only keep those rows
    sql = "SELECT * FROM sep_2015 WHERE lpep_pickup_datetime < %s and Used = 0"
    secondQEndTime = time.time() - secondQStartTime
    print("%s seconds for Inside Query" % (secondQEndTime))

    adr = (str(outsideLoop[0]),)
    curTwo = db.cursor()
    curThree = db.cursor()

    curTwo.execute(sql, adr)
    rowsTwo = curTwo.fetchall()

    df = pd.DataFrame(rowsTwo)

    # DF Holds all of the rows that are in the +10 minute range for the current Row of the outer loop

    outside_pu_time = datetime.datetime.strptime(outsideLoop[0], '%Y-%m-%d %H:%M:%S')
    outside_do_time = outsideLoop[1]
    outside_pu_lon = outsideLoop[2]
    outside_pu_lat = outsideLoop[3]
    outside_do_lon = outsideLoop[4]
    outside_do_lat = outsideLoop[5]
    outside_pCount = outsideLoop[6]
    outside_distance = outsideLoop[7]
    outside_ID = outsideLoop[8]
    outside_speed = outsideLoop[9]
    outside_used = outsideLoop[10]

    bestDist = 0.0
    bestID = 0

    # Looping through DF is looping through the inside Loop

    bestInsideIndexNum = 0

    if (outside_used == 0):

        insideIndex = 0
        for insideLoop in rowsTwo:

            inside_pu_time = datetime.datetime.strptime(insideLoop[0], '%Y-%m-%d %H:%M:%S')
            inside_do_time = insideLoop[1]
            inside_pu_lon = insideLoop[2]
            inside_pu_lat = insideLoop[3]
            inside_do_lon = insideLoop[4]
            inside_do_lat = insideLoop[5]
            inside_pCount = insideLoop[6]
            inside_distance = insideLoop[7]
            inside_ID = insideLoop[8]
            inside_speed = insideLoop[9]
            inside_used = insideLoop[10]

            # if(inside_ID == outside_ID):
            # break
            # print(insideLoop[0])

            if (inside_used == 0):

                # Get Distance
                d1 = dist(outside_pu_lat, outside_pu_lon, inside_pu_lat, inside_pu_lon)

                # Get Average Speed

                averageSpeed = (outside_speed + inside_speed) / 2
                # averageSpeed = averageSpeed / 10

                # print(averageSpeed)

                # Get Delay
                # Delay = multiply average speed * distance between 2 locations

                delay = d1 * averageSpeed

                # print(timeToOtherPickup)

                timeDif = inside_pu_time - outside_pu_time

                if inside_speed is None or outside_speed is None:
                    delay = 2
                # else:
                # d1 = dist(outside_pu_lat,outside_pu_lon,inside_pu_lat,inside_pu_lon)
                # s3 = ((outside_speed+inside_speed)/2.0)
                # s3 = .1/s3
                # print(s3)
                # delay = (d1 * (s3/10))

                # Delay is currently in Hours, convert it to seconds
                # print(delay)
                # delay = delay * 60 * 60
                # print(delay)
                # print("Amount of seconds: ", delay)

                # Add the Delay
                b = outside_pu_time + datetime.timedelta(seconds=delay)

                # print(timeDifPlusDelay)

                # if (timeDifPlusDelay) > newTime:
                ##bad
                # continue
                # print("outside time plus delay: ", b)
                # print("inside time: ", inside_pu_time)

                # print(type(b))
                # print(type(inside_pu_time))
                if ((b) > (newTime)):
                    # print("work")
                    continue

                # At this point, it is in the interval...Now do the rest
                v1 = dist(outside_pu_lat, outside_pu_lon, inside_pu_lat, inside_pu_lon) + dist(inside_pu_lat,
                                                                                               inside_pu_lon,
                                                                                               outside_do_lat,
                                                                                               outside_do_lon) + dist(
                    outside_do_lat, outside_do_lon, inside_do_lat, inside_do_lon)
                v2 = dist(outside_pu_lat, outside_pu_lon, inside_pu_lat, inside_pu_lon) + dist(inside_pu_lat,
                                                                                               inside_pu_lon,
                                                                                               inside_do_lat,
                                                                                               inside_do_lon) + dist(
                    inside_do_lat, inside_do_lon, outside_do_lat, outside_do_lon)
                v3 = dist(inside_pu_lat, inside_pu_lon, outside_pu_lat, outside_pu_lon) + dist(outside_pu_lat,
                                                                                               outside_pu_lon,
                                                                                               outside_do_lat,
                                                                                               outside_do_lon) + dist(
                    outside_do_lat, outside_do_lon, inside_do_lat, inside_do_lon)
                v4 = dist(inside_pu_lat, inside_do_lon, outside_pu_lat, outside_pu_lon) + dist(outside_pu_lat,
                                                                                               outside_pu_lon,
                                                                                               inside_do_lat,
                                                                                               inside_do_lon) + dist(
                    inside_do_lat, inside_do_lon, outside_do_lat, outside_do_lon)

                origDist = outside_distance + inside_distance

                minV = min(v1, v2, v3, v4)

                if minV == v1:
                    if v1 < origDist:
                        # good with v1
                        if origDist - v1 > bestDist:
                            bestDist = origDist - v1
                            bestID = inside_ID
                            bestInsideIndexNum = insideIndex
                        continue

                if minV == v2:
                    if v2 < origDist:
                        # good with v2
                        if origDist - v2 > bestDist:
                            bestDist = origDist - v2
                            bestID = inside_ID
                            bestInsideIndexNum = insideIndex
                        continue
                if minV == v3:
                    if v3 < origDist:
                        # good with v3
                        if origDist - v3 > bestDist:
                            bestDist = origDist - v3
                            bestID = inside_ID
                            bestInsideIndexNum = insideIndex
                        continue
                if minV == v4:
                    if v4 < origDist:
                        # good with v4
                        if origDist - v4 > bestDist:
                            bestDist = origDist - v4
                            bestID = inside_ID
                            bestInsideIndexNum = insideIndex

                        continue

                # bad
                continue

    updateQueryStartTime = time.time()
    sqlTwo = "UPDATE sep_2015 SET Used = 5 WHERE ID = %s"
    updateQueryEndTime = time.time() - updateQueryStartTime
    print("%s seconds for UPDATE Query" % (updateQueryEndTime))

    adrTwo = (str(bestID),)
    curThree.execute(sqlTwo, adrTwo)

    count = count + 1
    # print("--------------------")
    df = pd.DataFrame(rowsTwo)
    # print(df)

curFour = db.cursor()

findQueryStartTime = time.time()
sqlThree = "SELECT * FROM sep_2015 WHERE Used = 5"
findQueryEndTime = time.time() - findQueryStartTime
print("%s seconds for Find Query" % (findQueryEndTime))

curFour.execute(sqlThree)
rowsEnd = curFour.fetchall()
# print(rowsEnd)

#!/usr/bin/env python

from utils_new import *
import re

def extractTestTimeseg(testtimesegsFile="/home/work/xusiwei/ditech/season_1/test_set_1/read_me_1.txt"):
    reg = re.compile('(2016-01-\d{2})-(\d+)')
    timesegs = {}
    with open(testtimesegsFile) as f:
        for line in f:
            match = reg.match(line.strip('\r\n'))
            if match:
                date = match.group(1)
                timeseg = match.group(2)
                #print match.group(), match.group(1), match.group(2)
                if not timesegs.has_key(date):
                    timesegs[date] = [timeseg,]
                else:
                    timesegs[date].append(timeseg)
    return timesegs
            

def run():
    areadict =  areaSliceTransDict()
    destdict = areaSliceTransDict2(areadict)
    datesuffixes = [
        ('2016-01-22','1'),
        ('2016-01-24','0'),
        ('2016-01-26','0'),
        ('2016-01-28','1'),
        ('2016-01-30','0'),
    ]
    timesegs = extractTestTimeseg()
    for datesuffix in datesuffixes:
        print "Generating test file " + datesuffix[0] + "......................"
        timesegToPredict = timesegs[datesuffix[0]]
        orderDataFile = "/home/work/xusiwei/ditech/season_1/test_set_1/order_data_deduplication/order_data_" + datesuffix[0] + "_test"
        trafficDataFile = "/home/work/xusiwei/ditech/season_1/test_set_1/traffic_data/traffic_data_" + datesuffix[0] + "_test"
        weatherDataFile = "/home/work/xusiwei/ditech/season_1/test_set_1/weather_data/weather_data_" + datesuffix[0] + "_test"
        poiDataFile = '/home/work/xusiwei/ditech/season_1/test_set_1/poi_data/poi_data'
        saveFile = './testFiles/testfile_' + datesuffix[0]
        festival = datesuffix[1] 
        genSingleDataFile2(timesegToPredict, areadict, destdict, orderDataFile, trafficDataFile, weatherDataFile, poiDataFile, saveFile, festival=festival)
        print "Finished generating test file "

if __name__ == "__main__":
    #extractTestTimeseg()
    run()

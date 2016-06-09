#!/usr/bin/env python

from utils_new import *

def genDivs():
    datesuffixes = [
        ('2016-01-01','1'),
        ('2016-01-02','1'),
        ('2016-01-03','1'),
        ('2016-01-04','0'),
        ('2016-01-05','0'),
        ('2016-01-06','0'),
        ('2016-01-07','0'),
        ('2016-01-08','0'),
        ('2016-01-09','1'),
        ('2016-01-10','1'),
        ('2016-01-11','0'),
        ('2016-01-12','0'),
        ('2016-01-13','0'),
        ('2016-01-14','0'),
        ('2016-01-15','0'),
        ('2016-01-16','1'),
        ('2016-01-17','1'),
        ('2016-01-18','0'),
        ('2016-01-19','0'),
        ('2016-01-20','0'),
        ('2016-01-21','0'),
    ]
    prefix = './trainFiles_new/trainfile_'
    for datesuffix in datesuffixes:
        file = prefix + datesuffix[0]
        f = open(file)
        length = len(f.readlines())
        for i in range(length):
            print length

   

def run():
    areadict =  areaSliceTransDict()
    destdict = areaSliceTransDict2(areadict)
    datesuffixes = [
        ('2016-01-01','1'),
        ('2016-01-02','1'),
        ('2016-01-03','1'),
        ('2016-01-04','0'),
        ('2016-01-05','0'),
        ('2016-01-06','0'),
        ('2016-01-07','0'),
        ('2016-01-08','0'),
        ('2016-01-09','1'),
        ('2016-01-10','1'),
        ('2016-01-11','0'),
        ('2016-01-12','0'),
        ('2016-01-13','0'),
        ('2016-01-14','0'),
        ('2016-01-15','0'),
        ('2016-01-16','1'),
        ('2016-01-17','1'),
        ('2016-01-18','0'),
        ('2016-01-19','0'),
        ('2016-01-20','0'),
        ('2016-01-21','0'),
    ]

    for datesuffix in datesuffixes:
        print "Generating training file " + datesuffix[0] + "......................"
        orderDataFile = "/home/work/xusiwei/ditech/season_1/training_data/order_data/order_data_" + datesuffix[0]
        trafficDataFile = "/home/work/xusiwei/ditech/season_1/training_data/traffic_data/traffic_data_" + datesuffix[0]
        weatherDataFile = "/home/work/xusiwei/ditech/season_1/training_data/weather_data/weather_data_" + datesuffix[0]
        poiDataFile = '/home/work/xusiwei/ditech/season_1/training_data/poi_data/poi_data'
        saveFile = './trainFiles_new/trainfile_' + datesuffix[0]
        festival = datesuffix[1] 
        genSingleDataFile(areadict, destdict, orderDataFile, trafficDataFile, weatherDataFile, poiDataFile, saveFile, festival=festival)
        print "Finished generating training file "

if __name__ == "__main__":
    #run()
    genDivs()

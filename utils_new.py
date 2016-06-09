#!/usr/bin/env python
import time
import traceback

def timeSliceTrans(timeStampStr):
    struct_time = time.strptime(timeStampStr, "%Y-%m-%d %H:%M:%S")
    timeslice = struct_time.tm_hour * 6 + struct_time.tm_min / 10 + 1
    #timeslicestr = timeStampStr.split(' ')[0] + '-' + str(timeslice)
    return timeslice

def areaSliceTransDict(dictfile='./training_data/cluster_map/cluster_map'):
    areadict = {}
    with open(dictfile) as f:
        for line in f:
            arealist = line.strip('\r\n').split('\t')
            if not areadict.has_key(arealist[0]):
                areadict[arealist[0]] = arealist[1]
    return areadict

def areaSliceTrans(area, areadict):
    return areadict[area]

def areaSliceTransDict2(areadict, orig_dictfile='./training_data/order_data/dest_map'):
    destdict = {}
    count = 200
    with open(orig_dictfile) as f:
        for line in f:
            line = line.strip('\r\n')
            if not destdict.has_key(line):
                destdict[line] = count + 1
                count = destdict[line]
    return destdict

def POIDataProcess(areadict, poidatafile='./training_data/poi_data/poi_data'):
    poidict = {}
    newpoidict = {}
    count = 0
    poilist = poiMapping(poidatafile)
    lenOfPoilist = len(poilist)
    with open(poidatafile) as pois:
        for line in pois:
            tmp = []
            poitmp = [0] * lenOfPoilist
            linelist = line.strip('\r\n').split('\t')
            for e in linelist[1:]:
                tmplist = e.split(':')
                #tmplist[0] = tmplist[0].replace("#", "_L_")
                tmp.append(tmplist)
            newlist1 = sorted(tmp, key=lambda d:d[1], reverse=False)[0:5]
            for i in newlist1:
                if i[0] in poilist:
                    poitmp[poilist.index(i[0])] = 1
                for j in range(len(poitmp)):
                    poitmp[j] = str(poitmp[j]) 
                poidict[areadict[linelist[0]]] = poitmp
    return poidict

def POIDataProcess2(areadict, poidatafile='./training_data/poi_data/poi_data'):
    poidict = {}
    newpoidict = {}
    count = 0
    poilist = poiMapping(poidatafile)
    lenOfPoilist = len(poilist)
    with open(poidatafile) as pois:
        for line in pois:
            tmp = []
            poitmp = [] #[0] * lenOfPoilist
            linelist = line.strip('\r\n').split('\t')
            for e in linelist[1:]:
                tmplist = e.split(':')
                #tmplist[0] = tmplist[0].replace("#", "_L_")
                tmp.append(tmplist)
            newlist1 = sorted(tmp, key=lambda d:d[1], reverse=False)[0:5]
            for i in newlist1:
                if i[0] in poilist:
                    poitmp.append(poilist.index(i[0]))
                else:
                    poitmp.append(-1)
                for j in range(len(poitmp)):
                    poitmp[j] = str(poitmp[j]) 
                poidict[areadict[linelist[0]]] = poitmp
    return poidict


def poiMapping(poidatafile='./training_data/poi_data/poi_data'):
    mapping = {}
    with open(poidatafile) as pois:
        for line in pois:
            tmp = []
            linelist = line.strip('\r\n').split('\t')
            for e in linelist[1:]:
                tmplist = e.split(':')
                if not mapping.has_key(tmplist[0]):
                    mapping[tmplist[0]] = 1
                else:
                    mapping[tmplist[0]] = mapping[tmplist[0]] + 1
    newlist = sorted(mapping.items(), key=lambda d:d[1])
    poilist = []
    for i in newlist:
        if i[1] >= 60:
            poilist.append(i[0])
    return poilist

def rangeSplit(file):
    print "Processing...", file.split('/')[-1]
    countlist = []
    countdict = {}
    with open(file) as f:
        for line in f:
            num = -1000000
            tmp = line.strip('\r\n')
            try:
                num = float(tmp)
                countlist.append(num)
            except:
                print "Strange Num: ", tmp
                traceback.print_exc()
                pass
    for i in countlist:
        if not countdict.has_key(i):
            countdict[i] = countlist.count(i)
            print i, ": Freq ", countdict[i] 
    return max(countlist), min(countlist)

def weatherDataProcess(weatherDataFile):
    weatherdict = {}
    with open(weatherDataFile) as f:
        for line in f:
            linelist = line.strip('\r\n').split('\t')
            timeseg = timeSliceTrans(linelist[0])
            weather = 'NULL'
            temperature = 'NULL'
            pm25 = 'NULL'
            if linelist[1] != '' and linelist[1] != ' ':
                weather = int(linelist[1])
            if linelist[2] != '' and linelist[2] != ' ':
                temperature = int(float(linelist[2]))
            if linelist[3] != '' and linelist[3] != ' ':
                pm25 = int(float(linelist[3]))

            if not weatherdict.has_key(timeseg):
                weatherdict[timeseg] = {'weather':[weather,], 'temperature':[temperature,], 'pm2.5':[pm25,]}
            else:
                weatherdict[timeseg]['weather'].append(weather)
                weatherdict[timeseg]['temperature'].append(temperature)
                weatherdict[timeseg]['pm2.5'].append(pm25)
            #print linelist, ' timeseg: ', timeseg
            #print weatherdict[timeseg]
            if 'NULL' in weatherdict[timeseg]['weather']:
                weatherdict[timeseg]['weather'].remove('NULL')
            if 'NULL' in weatherdict[timeseg]['temperature']:
                weatherdict[timeseg]['temperature'].remove('NULL')
            if 'NULL' in weatherdict[timeseg]['pm2.5']:
                weatherdict[timeseg]['pm2.5'].remove('NULL')
    newweatherdict = {}
    for timeseg,v in weatherdict.items():
        avg_weather = sum(v['weather']) / len(v['weather'])
        avg_temperature = sum(v['temperature']) / len(v['temperature'])
        avg_pm25 = sum(v['pm2.5']) / len(v['pm2.5'])
        newweatherdict[timeseg] = {'weather':str(avg_weather), 'temperature':str(avg_temperature), 'pm2.5':str(avg_pm25)}
    return newweatherdict

def trafficDataProcess(trafficDataFile, areadict):
    trafficDict = {}
    with open(trafficDataFile) as f:
        for line in f:
            linelist = line.strip('\r\n').split('\t')
            dist = areaSliceTrans(linelist[0],areadict)
            timeseg = timeSliceTrans(linelist[-1])
            #key = dist + '_' + str(timeseg)
            key = (dist, timeseg)
            tmp1 = linelist[1].split(':')
            tmp2 = linelist[2].split(':')
            tmp3 = linelist[3].split(':')
            tmp4 = linelist[4].split(':')
            if not trafficDict.has_key(key):
                trafficDict[key] = [[int(tmp1[1]),], [int(tmp2[1]),], [int(tmp3[1]),], [int(tmp4[1]),]]
            else:
                trafficDict[key][0] = trafficDict[(dist,timeseg)][0].append(int(tmp1[1]))
                trafficDict[key][1] = trafficDict[(dist,timeseg)][1].append(int(tmp2[1]))
                trafficDict[key][2] = trafficDict[(dist,timeseg)][2].append(int(tmp3[1]))
                trafficDict[key][3] = trafficDict[(dist,timeseg)][3].append(int(tmp4[1]))
    newtrafficDict = {}
    for k,v in trafficDict.items():
        if k == ('54',123):
            print "DEBUG: ", v
        avg1 = sum(v[0]) / len(v[0])
        avg2 = sum(v[1]) / len(v[1])
        avg3 = sum(v[2]) / len(v[2])
        avg4 = sum(v[3]) / len(v[3])
        newtrafficDict[k] = [str(avg1), str(avg2), str(avg3), str(avg4)]
    return newtrafficDict

def orderDataProcess(orderDataFile, areadict, destdict):
    orderDict = {}
    with open(orderDataFile) as f:
        for line in f:
            linelist = line.strip('\r\n').split('\t')
            dist = areaSliceTrans(linelist[3],areadict)
            timeseg = timeSliceTrans(linelist[-1])
            #dest = areaSliceTrans(linelist[4],destdict)
            price = float(linelist[5])
            if linelist[1] == 'NULL':
                gap = 1
            else:
                gap = 0
            key = (dist, timeseg)

            if not orderDict.has_key(key):
                #orderDict[key] = {'dest':[dest,], 'price':[price,], 'ordernum':1, 'gap':gap}
                orderDict[key] = {'price':[price,], 'ordernum':1, 'gap':gap}
            else:
                #if orderDict[key]['dest'] is None and orderDict[key]['ordernum'] == 2:
                #    print orderDict
                #orderDict[key]['dest'].append(dest)
                orderDict[key]['price'].append(price)
                orderDict[key]['ordernum'] = orderDict[key]['ordernum'] + 1
                orderDict[key]['gap'] = orderDict[key]['gap'] + gap
                #if orderDict[key]['dest'] is None:
                #    print "Debug: ", line
                #    print dest
                #    print price
    neworderDict = {}
    for k,v in orderDict.items():
        #neworderDict[k] = {'dest_most':0, 'dest_least':0, 'price':0, 'gap':0}
        neworderDict[k] = {'price':0, 'gap':0}
        #neworderDict[k]['dest_most'] = str(max(set(v['dest']), key=v['dest'].count))
        #neworderDict[k]['dest_least'] = str(min(set(v['dest']), key=v['dest'].count))
        neworderDict[k]['price'] = str(int(sum(v['price'])/len(v['price'])))
        neworderDict[k]['gap'] = str(v['gap'])
            
    return neworderDict

def getSpecialTimeSeg(areadict, destdict, orderDataFile, timeseglist):
    import re
    pat = re.compile('(2016-01-\d{2})')
    m = pat.search(orderDataFile)
    prefix = m.groups(1)[0]
    orderDict = orderDataProcess(orderDataFile, areadict, destdict)
    dists = areadict.values()
    dists.sort()
    for dist in dists:
        for timeseg in timeseglist:
            k = (dist, timeseg)
            if orderDict.has_key(k):
                print "%s,%s-%s,%s" % (dist, prefix, str(timeseg), orderDict[k]['gap'])


def genSingleDataFile(areadict, destdict, orderDataFile, trafficDataFile, weatherDataFile, poiDataFile, saveFile, festival='False'):
    orderDict = orderDataProcess(orderDataFile, areadict, destdict)
    trafficDict = trafficDataProcess(trafficDataFile, areadict)
    weatherDict = weatherDataProcess(weatherDataFile)
    poiDict = POIDataProcess2(areadict) 
    f = open(saveFile, 'w')
    for k,v in orderDict.items():
        timeseg_current = k[1]
        dist_current = k[0]
        timeseg_prev_1 = 0
        timeseg_prev_2 = 0
        timeseg_prev_3 = 0
        if (timeseg_current - 1) > 0:
            timeseg_prev_1 = timeseg_current - 1
        if (timeseg_current - 2) > 0:
            timeseg_prev_2 = timeseg_current - 2
        if (timeseg_current - 3) > 0:
            timeseg_prev_3 = timeseg_current - 3
        key_prev_1 = (dist_current,timeseg_prev_1)
        key_prev_2 = (dist_current,timeseg_prev_2)
        key_prev_3 = (dist_current,timeseg_prev_3)
        tmpDict1 = {'gap':'-1', 'start_dist':k[0], 'timeseg':str(k[1]), 'timeseg_prev_1':str(timeseg_prev_1), 'avg_price':'0', 'poi':'', 'traffic':'0\t0\t0\t0', 'weather':'0', 'temperature':'-300', 'pm25':'0', 'festival':festival}
        if orderDict.has_key(key_prev_1):
            tmpDict1['gap'] = orderDict[key_prev_1]['gap']
            tmpDict1['avg_price'] = orderDict[key_prev_1]['price']
        if trafficDict.has_key(key_prev_1):
            tmpDict1['traffic'] = '\t'.join(trafficDict[key_prev_1])
        if weatherDict.has_key(key_prev_1[1]):
            tmpDict1['weather'] = weatherDict[key_prev_1[1]]['weather']
            tmpDict1['temperature'] = weatherDict[key_prev_1[1]]['temperature']
            tmpDict1['pm25'] = weatherDict[key_prev_1[1]]['pm2.5']
        if poiDict.has_key(key_prev_1[0]):
            tmpDict1['poi'] = '\t'.join(poiDict[key_prev_1[0]])
        tmpDict2 = {'gap':'-1', 'timeseg_prev_2':str(timeseg_prev_2), 'avg_price':'0', 'traffic':'0\t0\t0\t0', 'weather':'0', 'temperature':'-300', 'pm25':'0'}
        if orderDict.has_key(key_prev_2):
            tmpDict2['gap'] = orderDict[key_prev_2]['gap']
            tmpDict2['avg_price'] = orderDict[key_prev_2]['price']
        if trafficDict.has_key(key_prev_2):
            tmpDict2['traffic'] = '\t'.join(trafficDict[key_prev_2])
        if weatherDict.has_key(key_prev_2[1]):
            tmpDict2['weather'] = weatherDict[key_prev_2[1]]['weather']
            tmpDict2['temperature'] = weatherDict[key_prev_2[1]]['temperature']
            tmpDict2['pm25'] = weatherDict[key_prev_2[1]]['pm2.5']
        tmpDict3 = {'gap':'-1', 'timeseg_prev_3':str(timeseg_prev_3), 'avg_price':'0', 'traffic':'0\t0\t0\t0', 'weather':'0', 'temperature':'-300', 'pm25':'0'}
        if orderDict.has_key(key_prev_3):
            tmpDict3['gap'] = orderDict[key_prev_3]['gap']
            tmpDict3['avg_price'] = orderDict[key_prev_3]['price']
        if trafficDict.has_key(key_prev_3):
            tmpDict3['traffic'] = '\t'.join(trafficDict[key_prev_3])
        if weatherDict.has_key(key_prev_3[1]):
            tmpDict3['weather'] = weatherDict[key_prev_3[1]]['weather']
            tmpDict3['temperature'] = weatherDict[key_prev_3[1]]['temperature']
            tmpDict3['pm25'] = weatherDict[key_prev_3[1]]['pm2.5']
 
        f.write(v['gap'])
        f.write('\t')
        f.write(tmpDict1['start_dist'] + '\t')
        f.write(tmpDict1['timeseg'] + '\t')
        f.write(tmpDict1['poi'] + '\t')
        f.write(tmpDict1['festival'] + '\t')

        f.write(tmpDict1['gap'] + '\t')
        f.write(tmpDict1['avg_price'] + '\t')
        f.write(tmpDict1['traffic'] + '\t')
        f.write(tmpDict1['weather'] + '\t')
        #f.write(tmpDict1['temperature'] + '\t')
        #f.write(tmpDict1['pm25'] + '\t')

        f.write(tmpDict2['gap'] + '\t')
        f.write(tmpDict2['avg_price'] + '\t')
        f.write(tmpDict2['traffic'] + '\t')
        f.write(tmpDict2['weather'] + '\t')
        #f.write(tmpDict2['temperature'] + '\t')
        #f.write(tmpDict2['pm25'] + '\t')

        f.write(tmpDict3['gap'] + '\t')
        f.write(tmpDict3['avg_price'] + '\t')
        f.write(tmpDict3['traffic'] + '\t')
        f.write(tmpDict3['weather'])
        #f.write(tmpDict3['temperature'] + '\t')
        #f.write(tmpDict3['pm25'])
        f.write('\n')

    f.close()
        
def genSingleDataFile2(timesegsForPredict, areadict, destdict, orderDataFile, trafficDataFile, weatherDataFile, poiDataFile, saveFile, festival='False'):
    orderDict = orderDataProcess(orderDataFile, areadict, destdict)
    trafficDict = trafficDataProcess(trafficDataFile, areadict)
    weatherDict = weatherDataProcess(weatherDataFile)
    poiDict = POIDataProcess2(areadict) 
    f = open(saveFile, 'w')
    dists = areadict.values()
    dists.sort()
    for dist in dists:
        for timeseg in timesegsForPredict:
            k = (dist, int(timeseg))
            dist_current = dist
            timeseg_current = int(timeseg)
            timeseg_prev_1 = 0
            timeseg_prev_2 = 0
            timeseg_prev_3 = 0
            if (timeseg_current - 1) > 0:
                timeseg_prev_1 = timeseg_current - 1
            if (timeseg_current - 2) > 0:
                timeseg_prev_2 = timeseg_current - 2
            if (timeseg_current - 3) > 0:
                timeseg_prev_3 = timeseg_current - 3
            key_prev_1 = (dist_current,timeseg_prev_1)
            key_prev_2 = (dist_current,timeseg_prev_2)
            key_prev_3 = (dist_current,timeseg_prev_3)
            tmpDict1 = {'gap':'-1', 'start_dist':k[0], 'timeseg':str(k[1]), 'timeseg_prev_1':str(timeseg_prev_1), 'avg_price':'0', 'poi':'', 'traffic':'0\t0\t0\t0', 'weather':'0', 'temperature':'-300', 'pm25':'0', 'festival':festival}
            if orderDict.has_key(key_prev_1):
                tmpDict1['gap'] = orderDict[key_prev_1]['gap']
                tmpDict1['avg_price'] = orderDict[key_prev_1]['price']
            if trafficDict.has_key(key_prev_1):
                tmpDict1['traffic'] = '\t'.join(trafficDict[key_prev_1])
            if weatherDict.has_key(key_prev_1[1]):
                tmpDict1['weather'] = weatherDict[key_prev_1[1]]['weather']
                tmpDict1['temperature'] = weatherDict[key_prev_1[1]]['temperature']
                tmpDict1['pm25'] = weatherDict[key_prev_1[1]]['pm2.5']
            if poiDict.has_key(key_prev_1[0]):
                tmpDict1['poi'] = '\t'.join(poiDict[key_prev_1[0]])
            tmpDict2 = {'gap':'-1', 'timeseg_prev_2':str(timeseg_prev_2), 'avg_price':'0', 'traffic':'0\t0\t0\t0', 'weather':'0', 'temperature':'-300', 'pm25':'0'}
            if orderDict.has_key(key_prev_2):
                tmpDict2['gap'] = orderDict[key_prev_2]['gap']
                tmpDict2['avg_price'] = orderDict[key_prev_2]['price']
            if trafficDict.has_key(key_prev_2):
                tmpDict2['traffic'] = '\t'.join(trafficDict[key_prev_2])
            if weatherDict.has_key(key_prev_2[1]):
                tmpDict2['weather'] = weatherDict[key_prev_2[1]]['weather']
                tmpDict2['temperature'] = weatherDict[key_prev_2[1]]['temperature']
                tmpDict2['pm25'] = weatherDict[key_prev_2[1]]['pm2.5']
            tmpDict3 = {'gap':'-1', 'timeseg_prev_3':str(timeseg_prev_3), 'avg_price':'0', 'traffic':'0\t0\t0\t0', 'weather':'0', 'temperature':'-300', 'pm25':'0'}
            if orderDict.has_key(key_prev_3):
                tmpDict3['gap'] = orderDict[key_prev_3]['gap']
                tmpDict3['avg_price'] = orderDict[key_prev_3]['price']
            if trafficDict.has_key(key_prev_3):
                tmpDict3['traffic'] = '\t'.join(trafficDict[key_prev_3])
            if weatherDict.has_key(key_prev_3[1]):
                tmpDict3['weather'] = weatherDict[key_prev_3[1]]['weather']
                tmpDict3['temperature'] = weatherDict[key_prev_3[1]]['temperature']
                tmpDict3['pm25'] = weatherDict[key_prev_3[1]]['pm2.5']
                
                
            f.write(tmpDict1['start_dist'] + '\t')
            f.write(tmpDict1['timeseg'] + '\t')
            f.write(tmpDict1['poi'] + '\t')
            f.write(tmpDict1['festival'] + '\t')

            f.write(tmpDict1['gap'] + '\t')
            f.write(tmpDict1['avg_price'] + '\t')
            f.write(tmpDict1['traffic'] + '\t')
            f.write(tmpDict1['weather'] + '\t')
            #f.write(tmpDict1['temperature'] + '\t')
            #f.write(tmpDict1['pm25'] + '\t')

            f.write(tmpDict2['gap'] + '\t')
            f.write(tmpDict2['avg_price'] + '\t')
            f.write(tmpDict2['traffic'] + '\t')
            f.write(tmpDict2['weather'] + '\t')
            #f.write(tmpDict2['temperature'] + '\t')
            #f.write(tmpDict2['pm25'] + '\t')

            f.write(tmpDict3['gap'] + '\t')
            f.write(tmpDict3['avg_price'] + '\t')
            f.write(tmpDict3['traffic'] + '\t')
            f.write(tmpDict3['weather'])
            #f.write(tmpDict3['temperature'] + '\t')
            #f.write(tmpDict3['pm25'] + '\n')
            f.write('\n')

    f.close()
 

if __name__ == "__main__":
    destdict = areaSliceTransDict2(areadict)
    orderDataFile = "./training_data/order_data/order_data_2016-01-01"
    trafficDataFile = "./training_data/traffic_data/traffic_data_2016-01-01"
    weatherDataFile = "./training_data/weather_data/weather_data_2016-01-01"
    poiDataFile = './training_data/poi_data/poi_data'
    saveFile = './trainFiles_new/trainfile_2016-01-01'
    festival = '1'
    genSingleDataFile(areadict, destdict, orderDataFile, trafficDataFile, weatherDataFile, poiDataFile, saveFile, festival=festival)


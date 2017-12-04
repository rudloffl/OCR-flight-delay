import pickle
import math
import pandas as pd
import numpy as np
import copy
from sklearn import preprocessing
from datetime import datetime

#Dicts loading
def load_obj(name):
    with open('dict/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


#Feature creation to get distance group from dict
def getdistancegroup(trip):
    ltrip = list(trip)
    ltrip.sort()
    return distancegroupdict.get(tuple(ltrip), np.nan)
#getdistancegroup(('ORD', 'LAX'))
    
class Predictioneng():
    def __init__(self):
        #self.distancegroupdict = load_obj('distancegroupdict') #Distance group coef
        self.airportdict = load_obj('airportdict') #Airport names
        self.carrierdict = load_obj('carrierdict') #Carrier names
        self.possibletripdict = load_obj('possibletripdict') #Possible trips
        self.carrierreg = load_obj('carrierreg') #Data and Coefs from linear regression
        self.airportcoorddict = load_obj('airportcoorddict') #Airports coordinate dict
        
    
    def predictflight(self, ORIGIN, DEST, date, hour, carrier):
        
        DATE = datetime.strptime(date+ ' - {}'.format(hour), '%Y-%m-%d - %H')
        #ORIGIN = 'LAX'
        #DEST = 'LAS'
        #DATE = datetime(2016, 6, 24, 8, 0)
        #carrier = 'EV'
    
        tostandarize = self.carrierreg[carrier]['tostandarize']
        binaryentries_DEST = self.carrierreg[carrier]['binaryentries_DEST']
        binaryentries_ORIGIN = self.carrierreg[carrier]['binaryentries_ORIGIN']
        coefs = self.carrierreg[carrier]['coefs']
        dictdistgroup = self.carrierreg[carrier]['dictdistgroup']
        meanDEST = coefs[len(tostandarize):len(tostandarize) + len(binaryentries_DEST)].mean()
        meanORIGIN = coefs[len(tostandarize) + len(binaryentries_DEST):].mean()
    
    
        DISTANCE_GR = math.ceil(self.distance(self.airportcoorddict[ORIGIN],self.airportcoorddict[DEST])/250)
        DISTANCE = dictdistgroup.get(DISTANCE_GR, np.array([x for x in dictdistgroup.values()]).mean())
    
        Xreq = np.array([self.carrierreg[carrier]['dictdayofweek'][DATE.weekday()], DISTANCE, self.carrierreg[carrier]['dictmonth'][DATE.month],
                         self.carrierreg[carrier]['dicthour'][DATE.hour]]).reshape(1, -1)
        standardscaler = self.carrierreg[carrier]['standardscale']
        stdXreq = standardscaler.transform(Xreq)
        dictrequest = {}
    
        columnlabel = []
        columnlabel = copy.deepcopy(tostandarize)
        columnlabel.extend(binaryentries_DEST)
        columnlabel.extend(binaryentries_ORIGIN)
        columnlabel.extend(['RAND_ORIGIN', 'RAND_DEST'])
    
        temp = [x for x in binaryentries_ORIGIN if x.startswith('ORIGIN_')]
        if ORIGIN not in [x[-3:] for x in temp]:
            originmiss = 1
            print('ORIGIN MISSING')
        else:
            originmiss = 0
    
        temp = [x for x in binaryentries_DEST if x.startswith('DEST_')]
        if DEST not in [x[-3:] for x in temp]:
            destmiss = 1
            print('DEST MISSING')
        else:
            destmiss = 0
    
        for column in columnlabel:
            #print(column)
            if column == 'DAY_OF_WEEK':
                dictrequest[column] = stdXreq[0][0]
            elif column == 'MONTHMEAN':
                dictrequest[column] = stdXreq[0][2]
            elif column == 'HOURMEAN':
                dictrequest[column] = stdXreq[0][3]
            elif column == 'DISTANCE_GROUP_MEAN':
                dictrequest[column] = stdXreq[0][1]
            elif column == 'ARR_DELAY':
                pass
            elif column == 'RAND_ORIGIN':
                dictrequest[column] = originmiss
            elif column == 'RAND_DEST':
                dictrequest[column] = destmiss 
            elif column.startswith('DEST_'):
                dictrequest[column] = 1 if column.endswith(DEST) else 0
            elif column.startswith('ORIGIN_'):
                dictrequest[column] = 1 if column.endswith(ORIGIN) else 0
    
    
        datarequest = pd.DataFrame.from_dict(dictrequest, orient = 'index').T
        pred = np.dot(datarequest.values, np.concatenate((coefs, [meanORIGIN, meanDEST])))
        print(pred[0])
        print((datarequest.values).shape[1], len(np.concatenate((coefs, [meanORIGIN, meanDEST]))))
        return round(pred[0],2)
    
    def predicttable(self, airports,DATE, HOUR):
        table = []
        for carrier in sorted(self.carrierdict.keys()): 
            carriername = self.carrierdict[carrier]
            delay = self.predictflight(airports[0],airports[1],DATE, HOUR, carrier)
            available = self.existingoffer(carrier, airports)
            table.append([carriername, delay, available])
        return table
        
    def airportsavail(self):
        return self. airportdict
    
    def distance(self, dep, arr):
        
        radius = 6371.01 / 1.609344 #Statute Miles
        x1 = math.radians(dep[0])
        y1 = math.radians(dep[1])

        x2 = math.radians(arr[0])
        y2 = math.radians(arr[1])
    
        d = radius * math.acos(math.sin(x1)*math.sin(x2)+math.cos(x1)*math.cos(x2)*math.cos(abs(y1-y2)))
        return d 
    
    def airportsname(self, code):
        return self. airportdict[code]
    
    def existingoffer(self, carrier, airports):
        return True if carrier in self.possibletripdict.get(airports, 'False') else False

if __name__ == "__main__":
    predictioneng = Predictioneng()
    print(predictioneng.existingoffer('AA', ('ABE', 'ABI')))
import pickle


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
        self.distancegroupdict = load_obj('distancegroupdict')
        self.airportdict = load_obj('airportdict')
        self.carrierdict = load_obj('carrierdict')
        self.possibletripdict = load_obj('possibletripdict')
        
    
    def predict(self, carrier, airports):
        pass
    
    def airportsavail(self):
        return self. airportdict
    
    def distance(self, airports):
        pass
    
    def airportsname(self, code):
        return self. airportdict[code]

if __name__ == "__main__":
    predictioneng = Predictioneng()
    print(predictioneng.airportsname('ORD'))
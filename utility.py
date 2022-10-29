import csv
import json



class Data:
    def loadProxies(self,directory):
        proxies = []
        with open(directory,'r') as e:
            e = e.readlines()
            for i in e:
                i = i.strip().split(':')
                proxies.append({'http':'http://{}:{}@{}:{}'.format(i[2],i[3],i[0],i[1]),'https':'https://{}:{}@{}:{}'.format(i[2],i[3],i[0],i[1])})

        if proxies == []:
            proxies.append(None)
        return proxies

    def csvToJson(self,directory):
        count = -1
        headers = []

        json_file = {}
        with open(directory,'r') as e:
            csvreader = csv.reader(e)
            
            for i in csvreader:
                count += 1
                if count == 0:
                    headers = i
                    continue
                
                count_2 = -1
                json_file[str(count)] = {}

                for k in i:
                    count_2 += 1
                    
                    
                    json_file[str(count)][headers[count_2]] = k

        return json_file

    def loadJson(self,directory):
        with open(directory) as e:
            return json.load(e)
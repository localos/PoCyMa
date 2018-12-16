import ipaddress
import json
import os

    
def __flowInd_Metric(flowInd,max):
    if(flowInd == '0'): return str(0)
    if(flowInd == max): return str(1)
    else:
        return str(int(flowInd)/int(max))    

def __Duration_Metric(durationTimes, time):
    global __division
    
    temp = durationTimes
    high = max(temp)
    
    if(check_String_Array_Const(temp)): 
        return str(1.0)
    else:
        return __division(time, high) 
            
def __IP4_Metric(ip):
    moreReservedNetworks = ["100.64.0.0"]

    for a in range(0,len(moreReservedNetworks)):
        if(ipaddress.IPv4Address(ip) in ipaddress.IPv4Network(moreReservedNetworks[a])):
            return str(1)

    if(ipaddress.ip_address(ip).is_private or 
       ipaddress.ip_address(ip).is_reserved or 
       ipaddress.ip_address(ip).is_multicast): return str(1)
    else: return str(0);

def __Port_Metric(port):
    if(port == '0'): return str(0)
    if(port == '65535'): return str(1)
    else:
        return str(int(port)/int(65535))   

def __l4Proto_Metric(l4Proto):
    if(l4Proto == '0'): return str(0)
    if(l4Proto == '255'): return str(1)
    else:
        return str(int(l4Proto)/int(255))     

def __dstPortClass_Metric(portname):
    global calculation

    with open(os.path.abspath('templateAttributes.json')) as json_data:
        data = json.load(json_data)
        dstPortClass = data['dstPortClass'];
    
        if portname not in dstPortClass:
            dstPortClass.append(portname)
            dstPortClass.sort(key=None, reverse=False)
            data['dstPortClass'] = dstPortClass  
        
    json_data.close()
    
    writeJSON(data,os.path.abspath('templateAttributes.json'))

    return calculation(data,portname,'dstPortClass')

def __pkt_byte_Asm_Metric(value):
    if(float(value)<=1.0 and float(value)>=-1.0):
        return str(((float(value))+1)/2)
    else:
        if(float(value)<-1.0):
            return str(float(0.0))
        return str(float(1.0))

def __tcpStat_Metric(vhex):
    return __division(int((vhex), 16), int('0x80',16))
        
def __min_max_TTL_Metric(value):
    if(value == '0'): return str(0)
    if(value == '255'): return str(1)
    else:
        return str(int(value)/int(255))     

def __tcpSeqAckFaultCnt_tcpPSeqAckCnt_Metric(numerator,denominator):
    try:
        if((float(numerator)/float(denominator))<=1.0):
            solution = (float(numerator)/float(denominator))
            return str(solution)
        else:
            return str(1)
    except ZeroDivisionError:
        return str(0)

def __tcpAggrFlags_Metric(vhex):
    return __division(int((vhex), 16), int('0x80',16))  

def __tcpAggrAnomaly_Metric(vhex):
    return __division(int((vhex), 16), int('0x8000',16))  

def __tcpAggrOptions_Metric(vhex):
    return __division(int((vhex), 16), int('0x80000000',16)) 

def __tcpStates_Metric(value):
    if(int(value, 16)>=128): return str(1);
    if(int(value, 16)==0): return str(0);
    return str((int(value, 16))/128) #31

'''Area for generic methods'''
def __division(numerator, denominator):
    if((float(numerator)/float(denominator))<=1.0):
        solution = (float(numerator)/float(denominator))
        return str(solution)
    else:
        return str(1.0)
    
def calculation(jsonArray,attr,jsclass):
    index = jsonArray[jsclass].index(attr)
    return str(index/len(jsonArray[jsclass]))

def writeJSON(data,projPath):
    with open(projPath, 'w') as f:
        f.write(json.dumps(data))
    f.close() 
        
def check_String_Array_Const(array):
    cnt = 0
    bool = False
    temp = ''
    for elem in array:
        if(cnt == 0): 
            temp = elem
            cnt = cnt+1
        if(cnt>0):            
            if(elem!=temp):
                bool = False
                break;
            else:
                bool = True
    return bool
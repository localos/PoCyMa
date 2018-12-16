        while(flag==False):
            'WebService'
            if(flag == False and str(parsed_json["tcpAggrAnomaly"])!= '0x0000' and float(parsed_json["pktAsm"]) >= 0 and float(parsed_json["bytAsm"]) < -0.49 and binaryTCPStates[-2]=="1" and binaryTCPStates[-1]=="0"): #byteAssymetrie ab -0.75 auch mit betrachtbar
                lastLabel.append(1)
                flag = True
                synNumber.append(("","","","",""))   
                break;
            'DOS anhand IDS-ALERT'                      
            if(flag == False and (parse_alert(parsed_json["snort_alerts"],'class')=='Detection of a Denial of Service Attack')): 
                lastLabel.append(2)                   
                flag = True
                break;
            'Erkennung DOS'       
            if(flag == False and str(parsed_json["tcpAggrFlags"])!= '0x00' and float(parsed_json["Duration"])!= 0.0 and len(binaryTCPFlag)>=4 and 
               str(parsed_json["bytAsm"]) != "-1" and str(parsed_json["tcpAggrAnomaly"])!= '0x0000'): #Kein Systemausfall, deswegen Symmetrie ungleich -1 and str(parsed_json["bytAsm"]) != "1"
                if(binaryTCPFlag[-2]=='1'):
                    synNumber.append((parsed_json['flowInd'],parsed_json['SrcIP4'],parsed_json['DstIP4'],parsed_json['SrcPort'],parsed_json['DstPort']))
                    lastLabel.append(0) #vorlaufig 0 danach 2  
                    flag = True
                    break
                else:
                    synNumber.append(("","","","","")) 
                    lastLabel.append(0) #keine DOS-EIgnung
                    flag = True
                    break
                    
            if flag == False: 
                lastLabel.append(0) 
                synNumber.append(("","","","","")) 
                break
        flag = False




def tcp_Rate(flowStat,ipv4Src,ipv4Dest,tresholdLine,synNumber,numberFilteredFlows,intervall,lastLabel,synRate,tcpPAckCntASM,forTemp):
    connectionsInIntervall = []
    allHosts = []
    connectionRising = []
    ipCallSyn = []
    ipCallSynInt = []
    templateipCallSyn = []
    
    'DOS-Ansatz'
    '''Bestimme TCP-Verhaeltnise'''
    flowVerhaeltnis = (intervall*numberFilteredFlows)
    rest = (flowVerhaeltnis) % 2
    reverseIntervall = (1/(intervall))
      
    for a in range(0,int(reverseIntervall)):
        connectionsInIntervall.append([])
         
    if(rest > 0): flowVerhaeltnis = flowVerhaeltnis - rest
            
    for a in range(0, int(reverseIntervall)):
        for b in range(0, int(flowVerhaeltnis)+1):
            if(a == 0):
                iterateNumber = int((b+1+(reverseIntervall*(a))))
            else:
                iterateNumber = int((flowVerhaeltnis*a+((b+1))))
      
            try:
                (fInd,sIP,dIP,sPort,dPort) = synNumber[iterateNumber]
                        
                if(str(fInd)!= ""):
                    if((sIP,dIP) not in allHosts):
                        allHosts.append((sIP,dIP))
                        connectionRising.append(0)

            except IndexError:
                pass    
                
    for a in range(0, int(reverseIntervall)):
                
        'Bereich fuer Erhoeungsrate der TCP-Verbindungen in allen Flows ueber alle Intervallen uebergreifend'
        for b in range(0, int(flowVerhaeltnis)+1):

            'Fuer die durchgehende Iteration'
            if(a == 0):
                iterateNumber = int((b+1+(reverseIntervall*(a))))
            else:
                iterateNumber = int((flowVerhaeltnis*a+((b+1))))
     
            try:
                (fInd,sIP,dIP,sPort,dPort) = synNumber[iterateNumber]
                        
                if(str(fInd)!= ""):
                    connectionRising[allHosts.index((sIP,dIP))] = connectionRising[allHosts.index((sIP,dIP))]+1

            except IndexError:
                        pass

        for b in range(0,len(connectionRising)):                      #flowCount,numberFilteredFlows fuer alle Flows
            'Berechnen der SynRaten'
            ipCallSyn.append(((connectionRising[b]/numberFilteredFlows),a)) #flowVerhaeltnis fuer Flows innerhalb des Intervalls
            connectionsInIntervall[a].append(connectionRising[b]);
                   
    for a in range(len(connectionsInIntervall)-1,1,-1):
        temp = connectionsInIntervall
        for b in range(0,len(connectionsInIntervall[a])):
            connectionsInIntervall[a][b] = connectionsInIntervall[a][b]-connectionsInIntervall[a-1][b]   

    for a in range(0,len(connectionsInIntervall)):
        for b in range(0,len(connectionsInIntervall[a])):
            ipCallSynInt.append(connectionsInIntervall[a][b]/numberFilteredFlows)

    'Gebe ipCallSynInt eine Intervallzuordnung'
    for a in range(0,len(ipCallSyn)):
        (prozent,intervall) = ipCallSyn[a]
        prozent2 = ipCallSynInt[a]
        ipCallSynInt[a] = (prozent2,intervall)

    tresholdExceeded = createSynRate(len(allHosts))
       
    'Schwellenlinienpruefung' 
    for a in range(0, len(ipCallSynInt)):
        (prozent,intervall) = ipCallSyn[a] # Rising oder ipCallSyn fuer intervallartig..
        if(prozent>=tresholdLine):
            if a==0: tresholdExceeded[a] = 2
            else: 
                if a%len((allHosts)) == 0: tresholdExceeded[a%len((allHosts))] = 2
                else: tresholdExceeded[a%len((allHosts))] = 2
                
    for b in range(0,len(ipCallSyn)):
        (rate, iv) = ipCallSyn[b]
                
        if iv == intervall:
            templateipCallSyn.append(str(rate))
                
    'Adressen holen mit Index-TresholdExceeded und saemtliche Pakete mit Src- und Dst-IP-Adressen markieren mit 2'        
    for a in range(0,len(tresholdExceeded)):
        (ipSrc,ipDst) = allHosts[a]
                  
        for b in range (0,len(ipv4Src)): 
            if(tresholdExceeded[a]==2):
                if(ipv4Src[b]==ipSrc and ipv4Dest[b]==ipDst and str(lastLabel[b]) != "1"):
                    lastLabel[b] = 2
                    
            if(ipv4Src[b]==ipSrc and ipv4Dest[b]==ipDst and str(lastLabel[b]) == "2"):
                synRate[b] = templateipCallSyn[a]
                      
            if(a==len(tresholdExceeded)-1):  
                if(flowStat[b]=="0x00000001" and flowStat[b-1]=="0x00000000"):
                    '-1 fuer dir a und b fuer dir b'
                    asmA = int(tcpPAckCntASM[b-1])
                    asmB = int(tcpPAckCntASM[b])
                            
                    'Hier koennen auch DDOS sein Bedingung: =>0'
                    if(asmA==asmB):
                        tcpPAckCntASM[b-1] = "0"
                        tcpPAckCntASM[b] = "0"

                    else:
                                
                        if(lastLabel[b-1]==2 or lastLabel[b]==2):
                            asyHin = -1*((asmA-asmB)/(asmA+asmB))
                            asyZurueck = -1*((asmB-asmA)/(asmB+asmA))
                            forTemp[b-1] = asyHin
                            forTemp[b] = asyZurueck
                            tcpPAckCntASM[b-1] = asyHin
                            tcpPAckCntASM[b] = asyZurueck   
'Hilsmethode zum Erstellen einer Synrate'
def createSynRate(intervall):
    rate = []
    for i in range(0,int(intervall)):
        rate.append(0)
    return rate
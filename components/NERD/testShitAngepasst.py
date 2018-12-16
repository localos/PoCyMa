def tcp_Rate(flowStat,ipv4Src,ipv4Dest,tresholdLine,synNumber,numberFilteredFlows,intervall,lastLabel,synRate,tcpPAckCntASM,forTemp):
	
	connectionsInIntervall = []
	allHosts = []
	connectionRising = []
	ipCallSyn = []
	templateipCallSyn = []
	
	flowVerhaeltnis = (intervall*flowCount)
	rest = (flowVerhaeltnis) % 2
	if(rest > 0): flowVerhaeltnis = flowVerhaeltnis - rest
	
	anzahlIntervalle = (1/(intervall))
	
	
	for a in range(0,int(anzahlIntervalle)):
		connectionsInIntervall.append([])
		
		for b in range(0, int(flowVerhaeltnis+1)):
			if(a==0):
				iterateNumber = int((b+1+(anzahlIntervalle*(a)))) 
			
			else:
				iterateNumber = int((flowVerhaeltnis*a+((b+1))))
				
			try:
				(fInd,sIP,dIP,sPort,dPort) = synNumber[iterateNumber]
				
				if(str(fInd)!= ""):
					if((sIP,dIP) not in allHosts):
						allHosts.append((sIP,dIP))
						connectionRising.append(0)
					connectionRising[allHosts.index((sIP,dIP))] = connectionRising[allHosts.index((sIP,dIP))]+1

			except IndexError:
				pass   
		
		for b in range(0,len(connectionRising)):                      
			'Berechnen der SynRaten'
			ipCallSyn.append(((connectionRising[b]/numberFilteredFlows),a)) 
	
	tresholdExceeded = [0 for i in range(0,len(allHosts))]
	
	for a in range(0, len(ipCallSyn)):
		(prozent,intervall) = ipCallSyn[a]
		if(prozent>=tresholdLine):
			if a==0: tresholdExceeded[a] = 2
			else: 
				if a%len((allHosts)) == 0: tresholdExceeded[a%len((allHosts))] = 2
				else: tresholdExceeded[a%len((allHosts))] = 2
				
	for b in range(0,len(ipCallSyn)):
		(rate, iv) = ipCallSyn[b]
                
		if iv == intervall:
			templateipCallSyn.append(str(rate))
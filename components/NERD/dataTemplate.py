import json
import sys
import os
import inspect
import numpy as np
from editConfigParser import *

def load_json_file(path):
	"Erzeugt DataTemplate"
	print("DataTemplateTest")
	neuralNetworkData = ""
	with open(path,encoding="utf-8") as file:
		neuralNetworkData = createTemplate(file)
		file.close()
	
	neuralNetworkData = prepareNeuralNetworkData(neuralNetworkData)
	return neuralNetworkData
	
def split_json(file):
	temp = ""
	
	for line in file:
		temp += line
		try:
			yield json.loads(temp)
			temp = ""
		except ValueError:
			pass
			
def parse_alert(alert, mode):
	if(str(alert)!="[]"):
		if(mode=="class"):
			return alert[0]["classification"]
		if(mode=="prio"):
			return alert[0]["priority"]
	else:
		return ""

def prepareNeuralNetworkData(template):
	'Convert stringvalue to floatvalue'
	print("Daten für NN vorbereiten")
	printProgressBar(0,len(template),prefix="Progress",suffix="Complete",length= 50)
	for c in range(0, len(template)):
		printProgressBar(c+1,len(template),prefix="Progress",suffix="Complete",length= 50)
		for r in range(0, len(template[c])):
			value = template[c,r]
			template[c,r] = float(value)
                 
	return template

#def labeling():
def tcp_Rate(flowStat,ipv4Src,ipv4Dest,tresholdLine,synNumber,numberFlows,intervall,lastLabel,synRate,tcpPAckCntASM):
	
	connectionsInIntervall = []
	allHosts = []
	connectionRising = []
	ipCallSyn = []
	templateipCallSyn = []
	
	flowVerhaeltnis = (intervall*numberFlows)
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
			ipCallSyn.append(((connectionRising[b]/numberFlows),a)) 
	
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
							tcpPAckCntASM[b-1] = asyHin
							tcpPAckCntASM[b] = asyZurueck  		

# Progressbar
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
	"""
	Call in a loop to create terminal progress bar
	@params:
		iteration   - Required  : current iteration (Int)
		total       - Required  : total iterations (Int)
		prefix      - Optional  : prefix string (Str)
		suffix      - Optional  : suffix string (Str)
		decimals    - Optional  : positive number of decimals in percent complete (Int)
		length      - Optional  : character length of bar (Int)
		fill        - Optional  : bar fill character (Str)
	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
	# Print New Line on Complete
	if iteration == total: 
		print()							
		
def createTemplate(file):
	
#	np.set_printoptions(treshold=np.inf)
#	np.set_printoptions(suppress=True)
	
	#benötigte Parameter
	numberFilteredFlows = 0
	attributeNumber = int(readValue(("NET","NumberOfInputs")))+2 #+2 wegen Label und SynRate - to Do : +1 wenn SynRate ausgelagert ist
	intervall = 0.2
	tresholdLine = 0.18
	flowCount = 0
	
	#Dicts anlegen
	dictModuleRef = {}
	dictArgs = {}
	dictLists = {}
	
	#Metriken aus Konfigdatei auslesen
	for item in getOptions("METRICS"):
		
		#Wenn Metric benutzt werden soll
		if readValue(("METRICS",item)) == "yes": 
	#		print(item)
			#Pfad auf metrics/ ändern	
			path = list(sys.path)
			sys.path.insert(0, "metrics/")
			#Dynamisches importieren
			imp = __import__(item)
			#Pfad zurücksetzen
			sys.path[:] = path 
			#Referenz einspeichern
			dictModuleRef[item] = imp
	#		print(dictModuleRef.get(item))
			#benötigte Parameter auslesen
			args = inspect.signature(dictModuleRef.get(item).evaluate).parameters
			#Parameter umwandeln und iterieren
			dictArgs[item] = tuple(list(args))
			for arg in list(args):
				#Erzeugen der Listen falls nicht vorhanden
				if not arg in dictLists:
					dictLists[arg] = []
					
	#Extra Listen für Labeling (toDo : bei Auslagern mit auslagern)
	dictLists["label"] = []
	dictLists["synNumber"] = []
	dictLists["synRate"] = []
	dictLists["flowStat"] = []
	dictLists["SrcIP4"] = []
	dictLists["DstIP4"] = []
	dictLists["tcpPAckCntASM"] = []
	
	#print(dictModuleRef)
	#print(dictArgs)
	#print(dictLists)
	

	for parsed_json in split_json(file):
	        
		flowCount = flowCount+1
		#'Counter fuer gefilterte Flows (keine Betrachtung der IP-Pakete an den Multicast beispielsweise'
		#if(str(parsed_json["tcpAggrFlags"])!= '0x00' and float(parsed_json["Duration"])!= 0.0 and str(parsed_json["tcpAggrAnomaly"])!= '0x0000'):
		#	numberFilteredFlows = numberFilteredFlows+1
        
		#Auslesen der benötigten Werte
		for key in list(dictLists.keys()):
			
			if key not in ("label","synNumber","synRate","flowStat","SrcIP4","DstIP4","tcpPAckCntASM"):
			
				if key == "forTemp":
					dictLists.get(key).append("-1")
				else:
					dictLists.get(key).append(str(parsed_json[key]))
	
		#Vorlabeln und SynRate Vorbereitung (toDo : wenns geht auslagern ...)
		dictLists.get("synRate").append(0)
		
			
		dictLists.get("flowStat").append(str(parsed_json["flowStat"]))
		dictLists.get("SrcIP4").append(str(parsed_json['SrcIP4']))
		dictLists.get("DstIP4").append(str(parsed_json['DstIP4']))
		if(str(parsed_json["tcpAggrFlags"])!= '0x00' and float(parsed_json["Duration"])!= 0.0 and
			str(parsed_json["tcpAggrAnomaly"])!= '0x0000'):
			dictLists.get("tcpPAckCntASM").append(str(parsed_json['tcpPAckCnt']))
		else:
			dictLists.get("tcpPAckCntASM").append("0")
			
		flag = False
		binaryTCPFlag = bin(int(str(parsed_json["tcpAggrFlags"]), 16))
		binaryTCPStates = bin(int(str(parsed_json["tcpStates"]), 16))
		
		while(flag==False):
			'WebService'
			if(flag == False and str(parsed_json["tcpAggrAnomaly"])!= '0x0000' and float(parsed_json["pktAsm"]) >= 0 and float(parsed_json["bytAsm"]) < -0.49 and binaryTCPStates[-2]=="1" and binaryTCPStates[-1]=="0"): #byteAssymetrie ab -0.75 auch mit betrachtbar
				dictLists.get("label").append(1)
				flag = True
				dictLists.get("synNumber").append(("","","","",""))   
				break;
			'DOS anhand IDS-ALERT'                      
			if(flag == False and (parse_alert(parsed_json["snort_alerts"],'class')=='Detection of a Denial of Service Attack')): 
				dictLists.get("label")	.append(2)                   
				flag = True
				break;
			'Erkennung DOS'       
			if(flag == False and str(parsed_json["tcpAggrFlags"])!= '0x00' and float(parsed_json["Duration"])!= 0.0 and len(binaryTCPFlag)>=4 and 
				str(parsed_json["bytAsm"]) != "-1" and str(parsed_json["tcpAggrAnomaly"])!= '0x0000'): #Kein Systemausfall, deswegen Symmetrie ungleich -1 and str(parsed_json["bytAsm"]) != "1"
				if(binaryTCPFlag[-2]=='1'):
					dictLists.get("synNumber").append((parsed_json['flowInd'],parsed_json['SrcIP4'],parsed_json['DstIP4'],parsed_json['SrcPort'],parsed_json['DstPort']))
					dictLists.get("label").append(0) #vorlaufig 0 danach 2  
					flag = True
					break
				else:
					dictLists.get("synNumber").append(("","","","","")) 
					dictLists.get("label").append(0) #keine DOS-EIgnung
					flag = True
					break

			if flag == False: 
				dictLists.get("label").append(0) 
				dictLists.get("synNumber").append(("","","","","")) 
				break
		flag = False		
	
	#labeln mit TCP Rate, Ausfüllen der SynRates
	#tcp_Rate(flowStat,ipv4Src,ipv4Dest,tresholdLine,synNumber,numberFilteredFlows,intervall,lastLabel,synRate,tcpPAckCntASM)
	tcp_Rate(dictLists.get("flowStat"),dictLists.get("SrcIP4"),dictLists.get("DstIP4"),tresholdLine,dictLists.get("synNumber"),flowCount,intervall,dictLists.get("label"),dictLists.get("synRate"),dictLists.get("tcpPAckCntASM"))
	
	template = np.zeros(shape=(flowCount,attributeNumber))	
	
	print("Füllen des Templates")
	printProgressBar(0,len(template),prefix="Progress",suffix="Complete",length= 50)
	
	for i in range(0,len(template)):
		printProgressBar(i+1,len(template),prefix="Progress",suffix="Complete",length= 50)
		for index, item in enumerate(list(dictModuleRef.keys())):
			#print(i, index, item)
			if item == "flow_ind_metric":											
				template[i,index] = dictModuleRef.get("flow_ind_metric").evaluate((dictLists.get("flowInd")[i],len(dictLists.get("flowInd"))))
				#flowInd = flowind[i]
				#max = len(flowind)
			elif item == "duration_metric":
				template[i,index] = dictModuleRef.get("duration_metric").evaluate((dictLists.get("Duration"),dictLists.get("Duration")[i]))
				#time = Duration[i]
			elif item == "perc_num_sntpkt_metric":
				template[i,index] = dictModuleRef.get("perc_num_sntpkt_metric").evaluate((dictLists.get("numPktsSnt"),i))
			else:
				#Auslesen der einzelnen Args
				args = dictArgs.get(item)
				lst = []
				#Werte für Args auslesen
				for arg in args:
					lst.append(dictLists.get(arg)[i])
				t = tuple(lst)
				#Tupel entpacken und an Evaluate übergeben
				template[i,index] = dictModuleRef.get(item).evaluate(*t)
		
		#Manuelles Hinzufügen von Label und SynRate
		template[i,-2] = dictLists.get("synRate")[i] #-2 für vorletzten Eintrag
		template[i,-1] = dictLists.get("label")[i]	#-1 für letzten Eintrag
		
	#print(template[481])
	#print(flowCount)
	#print(numberFilteredFlows)
	
	#print(template[1])
	
	return template
	

			
	
	
if __name__ == '__main__':
	load_json_file("resource/normal_1_combined.json")
	
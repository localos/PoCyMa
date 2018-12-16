import configparser

def createStartConfig():

	config = configparser.ConfigParser()
	config['NET'] = {'NumberOfOutputs': '3','NumberOfInputs': '21','NumberOfHiddenLayers': '1','RecentlyChanged': 'no'}

	config["METRICS"] = {"flow_ind_metric" : "yes",
						"duration_metric" : "yes",
						"ip4_metric" : "yes",
						"src_port_metric" : "yes",
						"dst_port_metric" : "yes",
						"l4_proto_metric" : "yes",
						"dst_port_class_metric" : "yes",
						"for_temp_metric" : "yes",
						"pkt_asm_metric" : "yes",
						"byt_asm_metric" : "yes",
						"tcp_stat_metric" : "yes",
						"min_ttl_metric" : "yes",
						"max_ttl_metric" : "yes",
						"perc_num_sntpkt_metric" : "yes",
						"tcppseq_faultcnt_metric" : "yes",
						"tcppack_faultcnt_metric" : "yes",
						"tcppseq_tcpavewinsz_metric" : "yes",
						"tcpaggrflags_metric" : "yes",
						"tcpaggranomaly_metric" : "yes",
						"tcpaggroptions_metric" : "yes",
						"tcpstates_metric" : "yes"}
	
	config["KUERZEL"] = {"Normaler Netzverkehr" : "normal",
						"WebService-Ausfall" : "webservice",
						"DOS-Angriff" : "dos"}
	
	config["HANDLUNGSEMPFEHLUNGEN"] = {"Normal" : "Normaler Netzverkehr","Normal1" :"keine Aktion notwendig",
										"WebService" : "WebService-Ausfall","WebService1" : "Service Neustart","WebService2" : "IP Blacklisten",
										"DOS" : "DOS-Angriff", "DOS1" : "Port Sperren", "DOS2" : "IP Blacklisten"}
					
	config["BESTPRACTICES"] = {"Normal" : "Normaler Netzverkehr",
							"Normal1" : "Sicherheits- und Systemarchitektur kontinuierlich verbessern",
							"Normal2" :"Regelmaeßige Benchmarks durchfuehren lassen",
							"Normal3" :"Keine direkten Handlungsmaßnahmen erforderlich",
							"WebService" : "WebService-Ausfall",
							"WebService1" : "Zugriffsrechte prüfen lassen",
							"WebService2" : "Falls noch nicht vorhanden demilitarisierte Zone einrichten",
							"WebService3" : "Regelmäßige Backups der Webserver erstellen",
							"DOS" : "DOS-Angriff",
							"DOS1" : "DOS-Abwehrprogramme patchen lassen",
							"DOS2" : "DOS-Abwehrprovider kontaktieren",
							"DOS3" : "Sicherheits-Architektur optimieren"}
							
	with open('config.ini', 'w') as configfile:
		config.write(configfile)

def readValue(value):

	config = configparser.ConfigParser()
	config.read("config.ini","utf-8-sig")
	
	return config[value[0]][value[1]]

def getOptions(section):

		config = configparser.ConfigParser()
		config.read("config.ini","utf-8-sig")
		
		return config.options(section)

def addValue(value):	
	
	config = configparser.ConfigParser()
	config.read("config.ini","utf-8-sig")
	
	config.set(value[0],value[1],value[2])
	
	with open("config.ini","w") as configfile:
		config.write(configfile)

def getAllSzenarioNames():
	optionsHand = getOptions("HANDLUNGSEMPFEHLUNGEN")
	szenarios = [elem for elem in optionsHand if not any(char.isdigit() for char in elem)]
	szenarioNames = []
	for szenario in szenarios:
		szenarioNames.append(readValue(("HANDLUNGSEMPFEHLUNGEN",szenario)))		
	return szenarioNames
		
def getAllHandlungen():

		allHandlungen = getOptions("HANDLUNGSEMPFEHLUNGEN")
		allValues = []
		for handlung in allHandlungen:
			allValues.append(readValue(("HANDLUNGSEMPFEHLUNGEN",handlung)))
		
		return allHandlungen,allValues
		
def getAllPractices():

		allPractices = getOptions("BESTPRACTICES")
		allValues = []
		for practice in allPractices:
			allValues.append(readValue(("BESTPRACTICES",practice)))
		
		return allPractices,allValues
		
def getAllMetrics():

		allMetrics = getOptions("METRICS")
		allValues = []
		for metric in allMetrics:
			allValues.append(readValue(("METRICS",metric)))
		
		return allMetrics,allValues

def removeOption(value):
	config = configparser.ConfigParser()
	config.read("config.ini","utf-8-sig")
	
	config.remove_option(value[0],value[1])
	
	with open("config.ini","w") as configfile:
		config.write(configfile)

def getInt(value):
	config = configparser.ConfigParser()
	config.read("config.ini","utf-8-sig")
	
	return config.getint(value[0],value[1])

	
		

#createStartConfig()

#readValue(("NET","NumberOfOutputs"))
#readValue(("METRICS","testmetric"))
#addValue(("METRICS","testmetric2","yes"))
#print(getOptions("BESTPRACTICES"))
#name = getOptions("METRICS")
#print(readValue(("METRICS",name[0])))
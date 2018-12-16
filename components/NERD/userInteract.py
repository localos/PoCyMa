import numpy as np
from editConfigParser import *


def rate_pred(inp,prediction):
	
	#Auslesen der Config Datei
	anzahlOutputs = int(readValue(("NET","NumberOfOutputs")))
	#adaptedOutputs = int(readValue(("NET","NumberOfOutputs")))
	optionsHand = getOptions("HANDLUNGSEMPFEHLUNGEN")
	szenarios = [elem for elem in optionsHand if not any(char.isdigit() for char in elem)]
	
	#Initialisieren der Variablen
	net_input = inp
	net_pred = prediction
	used_meth = []
	user_rating = []
	
	#Alle Inputs durchlaufen
	for index, item in enumerate(net_input):
	
		#Ausgeben der Predictions
		print("Prediction %3d hat folgende Lösung vorhergesagt: "% (index))
		
		for i in range(0,anzahlOutputs):
			print(readValue(("HANDLUNGSEMPFEHLUNGEN",szenarios[i]))+" %5s" % ("{:.2%}".format(net_pred[index][i])))
			
		#Einlesen der gewaehlten Loesung
		var = input("Geben sie bitte Ihre gewählte Lösung an: ")
		
		
		while not var.isdigit() or int(var) not in range(0,anzahlOutputs) :
			var = input("Geben sie bitte Ihre gewählte Lösung an: ")
			
		print("Sie haben Lösung %3s gewählt" % (var))
		
		#Part für Hizufügen neuer Lösungen ausgelagert in console mit eigenem Befehl
		#nur hier drin für Vollständigkeit und Sicherung
		'''
		while not var.isdigit() :
			var = input("Geben sie bitte Ihre gewählte Lösung an: ")
		
		if int(var) in range(0,adaptedOutputs):
			print("Sie haben Lösung %3s gewählt" % (var))
			
		else:
			print("Sie wollen eine neue Lösung angeben")
			name = input("Geben Sie die Bezeichnung Ihrer Lösung (zB. DoS) ohne Zahlen an: ")
			while any(char.isdigit() for char in name):
				name = input("Geben Sie die Bezeichnung Ihrer Lösung (zB. DoS) ohne Zahlen an: ")
			print("Sie haben Lösung " +name+ " angelegt")
			addValue(("HANDLUNGSEMPFEHLUNGEN",name,name))
			addValue(("BESTPRACTICES",name,name))
			
			handlungen = input("Geben Sie Handlungsempfehlungen an (meherere bitte mit \",\" trennen)")
			handlungenList = handlungen.split(",")
			for index, item in enumerate(handlungenList):
				addValue(("HANDLUNGSEMPFEHLUNGEN",name+str(index+1),item))
				
			best_practices = input("Geben Sie Best-Practices an (meherere bitte mit \",\" trennen)")
			best_practicesList = best_practices.split(",")
			for index, item in enumerate(best_practicesList):
				addValue(("BESTPRACTICES",name+str(index+1),item))
			addValue(("NET","numberofoutputs",str(anzahlOutputs+1)))
			adaptedOutputs += 1
			print("Werte hinzugefügt")
			
		#while not var.isdigit() or int(var) not in range(0,3):
		#	var = input("Geben sie bitte Ihre gewählte Lösung an: ")
		#print("Sie haben Lösung %3s gewählt" % (var))
		'''
		
		#Speichern der gewaehlten Loesung
		used_meth.append(var)
		
		#Einlesen der Bewertung
		var = input("Geben sie bitte Ihre Bewertung zwischen 1 und 5 ein: ")
		while not var.isdigit() or int(var) not in range(1,6):
			var = input("Geben sie bitte Ihre Bewertung zwischen 1 und 5 ein: ")
		print("Sie haben wie folgt bewertet: %3s" % (var))

		#Speichern der Bewertung
		user_rating.append(var)
	
	#bool = anzahlOutputs == adaptedOutputs
	
	#Rückgabe aller Werte	
	#return net_input,net_pred,used_meth,user_rating,bool
	return net_input,net_pred,used_meth,user_rating




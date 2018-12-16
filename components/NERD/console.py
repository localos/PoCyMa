import sys,os.path
import os
import time
import numpy as np
from optparse import OptionParser
import keras
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Activation
from keras.layers.core import Dense
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from train import train
from saveAndLoad import *
from predicts import *
from userInteract import *
from generate import *
from pdfPrint import *
from editConfigParser import *

def train_and_save(vlevel, retrain):
		
	if retrain:
		
		if readValue(("NET","recentlychanged")) == "no":
			createStartConfig()
		else:
			addValue(("NET","recentlychanged","no"))
		
		if os.path.exists("resource/trainsetOrig.npz"):
			os.remove("resource/trainsetOrig.npz")
		if os.path.exists("resource/trainset.npz"):
			os.remove("resource/trainset.npz")
		if os.path.exists("resource/weights"):
			os.remove("resource/weights")
		if os.path.exists("resource/model"):
			os.remove("resource/model")
		if os.path.exists("resource/pred.npz"):
			os.remove("resource/pred.npz")
		
		#Trainset generieren falls nicht vorhanden
		if not os.path.exists("resource/trainsetOrig.npz"):
			gen_orig_set()
			gen_train_set_from_orig()
		else :
			gen_train_set_from_orig()
		#Trainset laden 
		ts, tl = load_whole_ts("resource/trainsetOrig.npz")
		
		#Model generieren
		model = load_complete_model()
		
		#Model trainieren
		model = train(model,ts,tl,vlevel)
		
		#Werte speichern
		save_w("resource/weights",model)
		save_m("resource/model",model)
	
	else:
	
		if readValue(("NET","recentlychanged")) == "yes":
			print("Konfiguration wurde kürzlich geändert")
			print("Zuerst Netz zurücksetzen (-r oder --retrain)")
			sys.exit(2)
		
		#Prüfen ob angepasstes Trainset vorhanden
		if os.path.exists("resource/trainset.npz"):
		
			print("Trainieren mit angepasstem Trainset")
			time.sleep(1)
			#Trainset laden 
			ts, tl = load_ts("resource/trainset.npz")
				
			#Model generieren
			model = load_complete_model()
		
			#Model trainieren
			model = train(model,ts,tl,vlevel)
			
			
			#Variante für Bool
			'''
			if bool:
				print("Trainieren mit angepasstem Trainset")
				time.sleep(1)
				#Trainset laden 
				ts, tl = load_ts("resource/trainset.npz")
				
				#Model generieren
				model = load_complete_model(bool)
		
				#Model trainieren
				model = train(model,ts,tl,vlevel)
			
			else:
				print("Trainieren mit angepasstem und original Set")
				print("Aufgrund von neuer Anzahl an Outputwerten")
				time.sleep(1)
				#Trainset Laden 1
				tsA, tlA = load_ts("resource/trainset.npz")
				#Trainset Laden 2
				tsO, tlO = load_whole_ts("resource/trainsetOrig.npz")
				
				#Model generieren 
				model = load_complete_model(bool)
		
				#Model trainieren 1
				model = train(model,tsO,tlO,vlevel)
				#Model trainieren 2
				model = train(model,tsA,tlA,vlevel)
			'''
	
			#Model und Gewichtungen speichern
			save_w("resource/weights",model)
			save_m("resource/model",model)
			
			print("Ende des Trainings")
		
		else:
			# Angepasstes Set nicht vorhanden -> Trainieren mit Originalset
			if os.path.exists("resource/trainsetOrig.npz"):
				gen_train_set_from_orig()
				print("Trainieren mit Originalem Trainset, da angepasstes nicht verfügbar")
				time.sleep(1)
				#Trainset laden 
				ts, tl = load_whole_ts("resource/trainsetOrig.npz")
				
				#Model generieren
				model = load_complete_model()
				
				#Model trainieren
				model = train(model,ts,tl,vlevel)
	
				#Model und Gewichtungen speichern
				save_w("resource/weights",model)
				save_m("resource/model",model)
				print("Ende des Trainings")
				
			else:
				print("Originales Trainset nicht verfügbar")
				print("Bitte zuerst -r oder --retrain ausführen")
				sys.exit(0)
	
def predict(path):
	if readValue(("NET","recentlychanged")) == "yes":
		print("Konfiguration wurde kürzlich geändert")
		print("Zuerst Netz zurücksetzen (-r oder --retrain)")
		sys.exit(2)

			
	#Model mit aktuellen Werten laden
	model = load_complete_model()
	
	#File mit zu vorhersagenden Daten laden
	file = load_pf(path)
	print(file["arr_0"])
	
	#Predicten und return Werte speichern
	predict_set,predictions,predictions_c = predict_data(model,file["arr_0"])
	print(predict_set,predictions,predictions_c)
	
	#Prediction Data speichern bzw. an Datei anhängen
	save_p(predict_set,predictions,predictions_c)
	
	#pdf ausgeben
	write_pdf(predictions)

	

def rate():
	
	#File mit predictions laden
	pred_set,preds,preds_c = load_p()
	
	#user feedback Funktion ausführen
	#net_input,net_pred,used_meth,user_rating,bool = rate_pred(pred_set,preds)
	net_input,net_pred,used_meth,user_rating = rate_pred(pred_set,preds)

	#Bewertete Predictions speichern
	save_rp(net_input,preds_c,used_meth,user_rating)
	
	#Netz mit neuen Werten trainieren
	print("Trainiere Netz mit neuen Daten")
	#train_and_save(1,False,bool)
	train_and_save(1,False)
	
def main():
	#Nutzerkommandos
	usage = "usage: %prog [options] arg"
	parser = OptionParser(usage)
	parser.add_option("-t","--train",action="store_true",dest="train",help="Startet das Training des NN")
	parser.add_option("-r","--retrain",action="store_true",dest="retrain",help="Setzt das NN zurück und trainiert es erneut - löscht das alte Trainingsset")
	parser.add_option("-p","--predict",action="store_true",dest="prediction",help="´Lässt NN die übergebenen Werte vorhersagen")
	parser.add_option("-R","--rate",action="store_true",dest="rate",help="Bewerten von zuvor getätigten Vorhersagen")
	parser.add_option("-i","--inputfile",dest="path",type= "string",help="JSON Datei aus der gelesen werden soll")
	parser.add_option("-v","--verbose",dest="verbose",type= "int",help="Verbosity. 0 per Default")
	parser.add_option("-m","--metrics",action="store_true",dest="metrics",help="Zeigt alle verfügbaren Metriken und ob diese genutzt werden")
	parser.add_option("-s","--szenarios",action="store_true",dest="szenarios",help="Zeigt alle eingetragenen Szenarien")
	parser.add_option("-c","--change",action="store_true",dest="change",help="Zum invertieren der Metriknutzung bzw. ändern von Handlungsempfehlungen und Best Practices")
	parser.add_option("-n","--name",dest="name",type="string",help="Der Name der Metrik oder Handlungsempfehlung/Best Practice deren Nutzung geändert werden soll.")
	parser.add_option("-e","--edit",action="store_true",dest="edit",help="Zum Anlegen bzw. Löschen von Metriken und Szenarios")
	#parser.add_option()
	(options,args) = parser.parse_args()
	
	#Prüfen ob Kommandos vorhanden sind	
	if len(sys.argv[1:]) == 0:
		print("Keine Argumente angegeben")
		print(usage)
		print("Tippe -h oder --help für Hilfemenue")
		sys.exit(2)
	
	#Training
	if options.train:
		#Verbosity prüfen
		if options.verbose == None:
			train_and_save(0,False)
		else:
			train_and_save(options.verbose,False)
			
	#Prediction
	if options.prediction:
		if options.path == None:
			print("Keine Datei mit zu vorhersehenden Werten angegeben")
			print("Nutze -i PFAD oder --inputfile=PFAD um die zu ladende Datei anzugeben")
			sys.exit(2)
		else:
			predict(options.path)
			
	#Bewertung		
	if options.rate:
		if os.path.exists("resource/pred.npz"):
			rate()
		else:
			print("Keine gespeicherten Vorhersagen zum bewerten")
			print("Diese Option wird nach einem weiteren Durchlauf von -p oder --predict verfügbar sein")
	
	#Retrain
	if options.retrain:
		if options.verbose == None:
			train_and_save(0,True)
		else:
			train_and_save(options.verbose,True)
	
	#Metriken
	if options.metrics:
		if options.change:
			#print(options.name)
			if options.name == "" or options.name == None:
				print("Kein Metrikname angegeben")
				sys.exit(2)
			else:
				metrics = getOptions("METRICS")
				if options.name in metrics:
					
					if options.edit:
						print("Metrik wird gelöscht")
						removeOption(("METRICS",options.name))
						addValue(("NET","numberofinputs",str(getInt(("NET","numberofinputs"))-1)))
						addValue(("NET","recentlychanged","yes"))
					
					else:
						if(readValue(("METRICS",options.name)) == "yes"):
							addValue(("METRICS",options.name,"no"))
							addValue(("NET","numberofinputs",str(getInt(("NET","numberofinputs"))-1)))
							addValue(("NET","recentlychanged","yes"))
						else:
							addValue(("METRICS",options.name,"yes"))
							addValue(("NET","numberofinputs",str(getInt(("NET","numberofinputs"))+1)))
							addValue(("NET","recentlychanged","yes"))
	
				else:
					print("Metrik nicht vorhanden")
					if options.edit:
						print("Metrik wird hinzugefügt")
						addValue(("METRICS",options.name,"yes"))
						addValue(("NET","numberofinputs",str(getInt(("NET","numberofinputs"))+1)))
						addValue(("NET","recentlychanged","yes"))
						
					else:
						print("Metrik soll nicht hinzugefügt werden")
						sys.exit(2)
		
		#Ausgabe aller Metriken und ob sie benutzt werden
		metrics, use = getAllMetrics()
		for m,u in zip(metrics,use):
			print("Using " +str(m)+ " : " +str(u))
	
	#Szenarios	
	if options.szenarios:
				
		if options.change:
			
			if options.name == "" or options.name == None:
				print("Kein Metrikname angegeben")
				sys.exit(2)
				
			else:
				#Auslesen benötigter Werte aus Config
				szenarioNames = getAllSzenarioNames()
				if options.name in szenarioNames:
					if options.edit:
						#to Do: wenn Labeling ausgelagert ist, das hier mit anfügen
						print("Hier findet das Löschen von Best Practices und Handlungsempfehlungen statt")
						print("Die Löschimplementierung funktioniert, jedoch ist der Labelvorgang noch nicht ausgelagert")
						print("Somit ist diese Funktion momentan nicht verfügbar")
						sys.exit(2)
						'''
						print("Handlungsempfehlungen und Best Practices werden gelöscht")
						kuerzel = readValue(("KUERZEL",options.name))
			
						optionsHand = [elem for elem in getOptions("HANDLUNGSEMPFEHLUNGEN") if kuerzel in elem]
						print(optionsHand)
						optionsBest = [elem for elem in getOptions("BESTPRACTICES") if kuerzel in elem]
						
						removeOption(("KUERZEL",options.name))
						for h in optionsHand:
							removeOption(("HANDLUNGSEMPFEHLUNGEN",h))
						for b in optionsBest:
							removeOption(("BESTPRACTICES",b))
						
						addValue(("NET","numberofoutputs",str(getInt(("NET","numberofoutputs"))-1)))
						addValue(("NET","recentlychanged","yes"))
						'''
					
					else:
						
						print("Sie wollen Handlungsempfehlungen und Best Practices der eingegebenen Lösung anpassen")
						kuerzel = readValue(("KUERZEL",options.name))
						handlungen = input("Geben Sie Handlungsempfehlungen an (meherere bitte mit \",\" trennen)\n")
						handlungenList = handlungen.split(",")
						for index, item in enumerate(handlungenList):
							addValue(("HANDLUNGSEMPFEHLUNGEN",kuerzel+str(len([elem for elem in getOptions("HANDLUNGSEMPFEHLUNGEN") if kuerzel in elem])+index),item))
							
						best_practices = input("Geben Sie Best-Practices an (meherere bitte mit \",\" trennen)\n")
						best_practicesList = best_practices.split(",")
						for index, item in enumerate(best_practicesList):
							addValue(("BESTPRACTICES",kuerzel+str(len([elem for elem in getOptions("BESTPRACTICES") if kuerzel in elem])+index),item))
		
						print("Daten hinzugefügt")
							
				else:
					print("Ein Szenario ist unter diesem Namen noch nicht eingetragen")
					print("Wollen Sie das Szenario inklusive Handlungsempfehlungen / Best Practices anlegen?")
					entscheidung = input("ja/nein eingeben\n")
					
					if entscheidung != "ja":
						print("Szenario wird nicht angelegt")
						sys.exit(2)
					
					name = options.name
					
					while any(char.isdigit() for char in name):
						name = input("Geben Sie bitte eine Szenariobezeichnung ohne Zahl ein")
					print("Sie haben Szenario " +name+ " angelegt")
					addValue(("KUERZEL",name,name))
					addValue(("HANDLUNGSEMPFEHLUNGEN",name,name))
					addValue(("BESTPRACTICES",name,name))
					
					handlungen = input("Geben Sie Handlungsempfehlungen an (meherere bitte mit \",\" trennen)\n")
					handlungenList = handlungen.split(",")
					for index, item in enumerate(handlungenList):
						addValue(("HANDLUNGSEMPFEHLUNGEN",name+str(index+1),item))
						
					best_practices = input("Geben Sie Best-Practices an (meherere bitte mit \",\" trennen)\n")
					best_practicesList = best_practices.split(",")
					for index, item in enumerate(best_practicesList):
						addValue(("BESTPRACTICES",name+str(index+1),item))
						
					addValue(("NET","numberofoutputs",str(getInt(("NET","numberofoutputs"))+1)))
					addValue(("NET","recentlychanged","yes"))
					print("Werte hinzugefügt")
					time.sleep(1)
					
				'''	
				else:
					print("Metrik nicht vorhanden")
					if options.edit:
						print("Metrik wird hinzugefügt")
						addValue(("METRICS",options.name,"yes"))
						addValue(("NET","numberofinputs",str(getInt(("NET","numberofinputs"))+1)))
						addValue(("NET","recentlychanged","yes"))
						
					else:
						print("Metrik soll nicht hinzugefügt werden")
						sys.exit(2)
				'''
		#Ausgabe aller Handlungsempfehlungen und Best Practices
		
		optionsHand = getOptions("HANDLUNGSEMPFEHLUNGEN")
		optionsBest = getOptions("BESTPRACTICES")
		szenarios = [elem for elem in optionsHand if not any(char.isdigit() for char in elem)]
		
		handlungen = []
		best_practices = []
		
		#test = [elem for elem in optionsHand if szenarios[i] in elem]
		
		
		for i in range(0,len(szenarios)):
				
			string = ""
			list = []
			
			for k in [elem for elem in optionsHand if szenarios[i] in elem]:

				string += readValue(("HANDLUNGSEMPFEHLUNGEN",k))+"\n"
				
			list.append(string)
			handlungen.append(list)		
	
		for i in range(0,len(szenarios)):
		
			string = ""
			list = []
		
			for k in [elem for elem in optionsBest if szenarios[i] in elem]:
				
				string += readValue(("BESTPRACTICES",k))+"\n"
			list.append(string)
			best_practices.append(list)
		
		print("Handlungsempfehlungen: \n")
		for szenario in handlungen:
			print("Szenario " + szenario[0])
	
			for anweisungen in szenario[1:]:
				
				print(anweisungen)	
		
		print("Best Practices	: \n")
		for szenario in best_practices:
			print("Szenario " + szenario[0])
			
			for anweisungen in szenario[1:]:
				
				print(anweisungen)
				

if __name__ == "__main__":
	main()
from time import gmtime,strftime
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Paragraph, Table
from editConfigParser import *

def write_pdf(predict_list):
	
	anzahlOutputs = int(readValue(("NET","NumberOfOutputs")))
	optionsHand = getOptions("HANDLUNGSEMPFEHLUNGEN")
	optionsBest = getOptions("BESTPRACTICES")
	szenarios = [elem for elem in optionsHand if not any(char.isdigit() for char in elem)]

	date = str("pdfs/"+strftime("%a%d%b%Y%H:%M:%S", gmtime())+".pdf").replace(":","-")
	c = canvas.Canvas(date,bottomup = 0, verbosity = 1)
	c.setPageSize((596.27,(25*anzahlOutputs)*(1+len(predict_list))))
	c.setTitle("Entscheidungsunterstützung")
	c.drawString(180,20,"Erkannte Wahrscheinlichkeiten")
	c.drawString(10,40,"Eine Analyse der übermittelten Daten ergab mit den folgenden Wahrscheinlichkeiten ein Vorliegen")
	c.drawString(10,60,"der entsprechenden Situationen. Handlungsempfehlungen und Best-Practice-Lösungen finden sich")
	c.drawString(10,80,"auf den nachfolgenden Seiten")
	
	for i in range(0,len(predict_list)):
		c.drawString(10,100+i*(20*(anzahlOutputs+1)),"Prediction "+str(i+1)+": ")
		
		for k in range(0,anzahlOutputs):
		
			c.drawString(10,100+i*(20*(anzahlOutputs+1))+(k+1)*20,readValue(("HANDLUNGSEMPFEHLUNGEN",szenarios[k]))+" {:.2%}".format(predict_list[i][k]))
		'''
			if(k == 1):
				c.drawString(10,100+i*80+k*20,"Normaler Netzverkehr "+"{:.2%}".format(predict_list[i][0]))
			elif(k == 2):
				c.drawString(10,100+i*80+k*20,"WebService-Ausfall "+"{:.2%}".format(predict_list[i][1]))
			else:
				c.drawString(10,100+i*80+k*20,"DOS-Angriff "+"{:.2%}".format(predict_list[i][2]))
		'''
	c.showPage()
	
	c.drawString(180,20,"Handlungsempfehlungen")	
	
	handlungen = []
	#indexHand = 1

	for i in range(0,len(szenarios)):
		
		string = ""
		#list = [readValue(("HANDLUNGSEMPFEHLUNGEN",szenarios[i]))]
		list = []
		#for k in range(1,sum(szenarios[i] in s for s in optionsHand)):	)
		for k in [elem for elem in optionsHand if szenarios[i] in elem][::-1]:
			#string += readValue(("HANDLUNGSEMPFEHLUNGEN",optionsHand[i+indexHand]))+"\n"
			#indexHand += 1
			string += readValue(("HANDLUNGSEMPFEHLUNGEN",k))+"\n"
		list.append(string)
		handlungen.append(list)
		
	#print(handlungen2)
	
	#handlungen =[["WebService-Ausfall","Service Neustart\nIP Blacklisten"],
	#			["DOS-Angriff","Port Sperren\nIP Blacklisten"],
	#			["Normaler Netzverkehr", "keine Aktion notwendig"]]
	
	table = Table(handlungen[::-1], colWidths=200)
	table.setStyle([("FONTSIZE",(0,0),(-1,-1),12),("TEXTFONT",(0,0),(-1,-1),"Times-Bold")])
	table.wrapOn(c, 596.27, 81)
	table.drawOn(c, 10, 60)
	c.showPage()
	
	c.drawString(180,20,"Best Practices")
	
	best_practices = []
	#indexBest = 1
	
	for i in range(0,len(szenarios)):
		
		string = ""
		#list = [readValue(("BESTPRACTICES",szenarios[i]))]
		list = []
		#for k in range(1,sum(szenarios[i] in s for s in optionsBest)):	
		for k in [elem for elem in optionsBest if szenarios[i] in elem][::-1]:	
			#string += readValue(("BESTPRACTICES",optionsBest[i+indexBest]))+"\n"
			#indexBest += 1
			string += readValue(("BESTPRACTICES",k))+"\n"
		list.append(string)
		best_practices.append(list)
	
	#best_practices =[["WebService-Ausfall","Zugriffsrechte prüfen lassen\nFalls noch nicht vorhanden demilitarisierte Zone einrichten\nRegelmäßige Backups der Webserver erstellen"],
	#				["DOS-Angriff","DOS-Abwehrprogramme patchen lassen\nDOS-Abwehrprovider kontaktieren\nSicherheits-Architektur optimieren"],
	#				["Normaler Netzverkehr","Sicherheits- und Systemarchitektur kontinuierlich verbessern\nRegelmäßige Benchmarks durchführen lassen\nKeine direkten Handlungsmaßnahmen erforderlich"]]
	
	table = Table(best_practices[::-1], colWidths=200)
	table.setStyle([("FONTSIZE",(0,0),(-1,-1),12),("TEXTFONT",(0,0),(-1,-1),"Times-Bold")])
	table.wrapOn(c, 596.27, 81)
	table.drawOn(c, 10, 60)
	c.showPage()

	c.save()	
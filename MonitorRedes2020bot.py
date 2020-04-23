# -*- coding:utf-8 -*-
import telebot
import os
import subprocess
import commands
import smtplib
import utilities
import requests
import random
import json
from datetime import date
from datetime import datetime
import sched
import time
from scheduler import Scheduler

#CAMPOS ELIMINADOS POR SEGURIDAD
host = ""
TOKEN = ""
ChatGrupo_id = 
USER = ""

bot = telebot.TeleBot(TOKEN)

def monitor():
	umbral = 80.00
	usado = utilities.getArrayValues("HOST-RESOURCES-MIB","hrStorageUsed",host)
	almacentotal= utilities.getArrayValues("HOST-RESOURCES-MIB","hrStorageSize",host)
	nombreobjeto = utilities.getArrayValues("HOST-RESOURCES-MIB","hrStorageDescr",host)
	#print"_________________________________________________________________"
	i=0
	mensaje = ""
	mensaje_malware = ""
	for i in range (0,len(nombreobjeto)):
		if int(almacentotal[i]) == 0:
			resultado = 0.00
			mensaje += "► 	Se esta usando un "+ str(resultado)+" % de " + nombreobjeto[i] + "\n\n"
		else:
			resultado = round((float(usado[i])/float(almacentotal[i]))*100,2)
			mensaje += "► 	Se esta usando un "+ str(resultado)+" % de " + nombreobjeto[i] + "\n\n"
			if (resultado > 88.00):
				bot.send_message(ChatGrupo_id,"WARNING: "+ nombreobjeto[i] + " se encuentra utilizando un " + str(resultado) + "% de su capacidad total"+ "\n\n"+
				"si supera el 95%, se enviará un email al servicio de soporte técnico notificando el problema.")
			if(resultado > 95.00):
				title = "WARNING: " + nombreobjeto[i] + " puede colapsar"
				contenido= str(datetime.now()) + ": el recurso " + nombreobjeto[i] +" del agente se encuentra usando un " + str(resultado) + "% de su capacidad.\n\n Atentamente:\n MonitorRedes2020bot"
				bot.send_message(ChatGrupo_id,"WARNING: "+ nombreobjeto[i] + " se encuentra utilizando un " + str(resultado) + "% de su capacidad total\n\nInformando al servicio de soporte.")
				utilities.send_mail(str(title), contenido)

	lista_procesos = utilities.getArrayValues("HOST-RESOURCES-MIB","hrSWRunName",host)
	f= open("maliciusProcessesDB.txt","r")
	lista_malware = f.read()
	#print lista_malware
	lista_malware_array = lista_malware.split("\n")
	f.close()
	j=0
	for i in range (0,len(lista_procesos)):
		for j in range(0,len(lista_malware_array)):
			if (str(lista_malware_array[j]) == str(lista_procesos[i])):
				mensaje_malware +=(str(lista_malware_array[j])+"\n")
	title = "WARNING: se han detectado posibles procesos maliciosos"
	contenido= str(datetime.now()) + ": se han detectado posibles procesos maliciosos: \n\n" + mensaje_malware+" \n Por favor, no ignore este mensaje y evalue la situacion.\n\n Atentamente:\n MonitorRedes2020bot"
	utilities.send_mail(str(title), contenido)
	bot.send_message(ChatGrupo_id,"WARNING: se han detectado posibles procesos maliciosos.\n\nInformando al servicio de soporte.")
				#print str(lista_malware_array[j])

scheduler = Scheduler()
scheduler.add(6000, 0, monitor)  # Agregar una tarea.
while True:
    scheduler.run()

bot.polling()

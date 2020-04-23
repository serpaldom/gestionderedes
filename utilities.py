# -*- coding:utf-8 -*-
import telebot
import os
import subprocess
import commands
import smtplib
import requests
import random
import json
from datetime import date
from datetime import datetime
import sched
import time
from scheduler import Scheduler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

#CAMPOS ELIMINADOS POR SEGURIDAD
TOKEN = ""
ChatGrupo_id = 
USER = ""

bot = telebot.TeleBot(TOKEN)

def get_OID(MIB,Nombre):
	database = str(MIB) + ".json"
	data = json.loads(open(database).read())
	for i in data:
	    if i['NAME'] == Nombre:
	        #print str(datetime.now())+" solicitud de OID: " +(i['OID'])+ "\n"
	        break
	return " "+str(i['OID'])

def get_NAME(MIB,ID):
	database = str(MIB) + ".json"
	data = json.loads(open(database).read())
	for i in data:
	    if i['OID'] == ID:
	       #print str(datetime.now)+ " solicitud de NOMBRE: " +(i['NOMBRE'])+ "\n"
	       break
	return str(i['NAME'])
def comprobar_conexion(host):
	res = commands.getstatusoutput('ping -c 1 '+ host)
	return res[1]

def comandos_disponibles():
	f=open("commands.txt","r")
	valor = f.read()
	lista = valor.split("\n")
	f.close()
	str1 = ''.join((str(e)+"\n") for e in lista)

	return str1

def send_mail(title, content):
		# create message object instance
	msg = MIMEMultipart()
	 
	 
	message = content
	 
	# setup the parameters of the message
	#los siguientes campos han sido eliminados por seguridad.
	password = ""
	msg['From'] = ""
	msg['To'] = ""
	msg['Subject'] = title
	 
	# add in the message body
	msg.attach(MIMEText(message, 'plain'))
	 
	#create server
	server = smtplib.SMTP('smtp.gmail.com: 587')
	 
	server.starttls()
	 
	# Login Credentials for sending the mail
	server.login(msg['From'], password)
	 
	 
	# send the message via the server.
	server.sendmail(msg['From'], msg['To'], msg.as_string())
	 
	server.quit()
 
	print "successfully sent email to %s:" % (msg['To'])

def getValues(MIB,NAME,host):
	
	#print str(datetime.now())+": Monitorizando: "+ NAME +"\n"
	query= 'snmpwalk -v1 -Ov -Oq -cpublic ' + host+ str(get_OID(MIB,NAME))
	if NAME == "sysName":
		query = 'snmpwalk -v1 -Ov -Oq -cpublic ' +host +' iso.3.6.1.2.1.1.5.0'
	if NAME == "sysDescr":
		query = 'snmpwalk -v1 -Ov -Oq -cpublic ' +host+ ' iso.3.6.1.2.1.1.1.0'
	if NAME == "sysUpTime":
		query = 'snmpwalk -v1 -Ov -cpublic ' +host +' iso.3.6.1.2.1.1.3.0'

	res = commands.getstatusoutput(query)
	lista = res[1].split("\n")

	if NAME == "ifName":
		NAME = "ifAdminStatus"
		query= 'snmpwalk -v1 -Ov -Oq -cpublic ' + host+ str(get_OID(MIB,NAME))
		res = commands.getstatusoutput(query)
		lista2 = res[1].split("\n")
		i= 0
		for i in range(0, len(lista)):
			if (lista2[i] == "1"):
				lista2[i] = "\t\tUP"
			if(lista2[i]=="2"):
				lista2[i] = "\t\tDOWN"
			if(lista2[i]=="3"):			
				lista2[i] = "\t\tTESTING"
		for i in range (0,len(lista)):
			lista[i]=lista[i] + lista2[i]

	values = ''.join(("► "+str(e)+"\n") for e in lista)
	return values

def getTamValues(MIB,NAME,host):
	
	#print str(datetime.now())+": Monitorizando: "+ NAME +"\n"
	query= 'snmpwalk -v1 -Ov -Oq -cpublic ' + host+ str(get_OID(MIB,NAME))
	res = commands.getstatusoutput(query)
	lista = res[1].split("\n")

	if NAME == "ifName":
		NAME = "ifAdminStatus"
		query= 'snmpwalk -v1 -Ov -Oq -cpublic ' + host+ str(get_OID(MIB,NAME))
		res = commands.getstatusoutput(query)
		lista2 = res[1].split("\n")
		i= 0
		for i in range(0, len(lista)):
			if (lista2[i] == "1"):
				lista2[i] = "\t\tUP"
			if(lista2[i]=="2"):
				lista2[i] = "\t\tDOWN"
			if(lista2[i]=="3"):			
				lista2[i] = "\t\tTESTING"
		for i in range (0,len(lista)):
			lista[i]=lista[i] + lista2[i]
	
	return str(len(lista))

def getArrayValues(MIB,NAME,host):
	query= 'snmpwalk -v1 -Ov -Oq -cpublic ' + host+ " " +str(get_OID(MIB,NAME))
	res = commands.getstatusoutput(query)
	lista = res[1].split("\n")
	return lista

def recursos(host):

	umbral = 80.00
	usado = getArrayValues("HOST-RESOURCES-MIB","hrStorageUsed",host)

	almacentotal= getArrayValues("HOST-RESOURCES-MIB","hrStorageSize",host)
	
	nombreobjeto = getArrayValues("HOST-RESOURCES-MIB","hrStorageDescr",host)
	
	#print"_________________________________________________________________"
	i=0
	mensaje = ""
	for i in range (0,len(nombreobjeto)):
		if int(almacentotal[i]) == 0:
			resultado = 0.00
			mensaje += "► 	Se esta usando un "+ str(resultado)+" % de " + nombreobjeto[i] + "\n\n"
		else:
			resultado = round((float(usado[i])/float(almacentotal[i]))*100,2)
			mensaje += "► 	Se esta usando un "+ str(resultado)+" % de " + nombreobjeto[i] + "\n\n"
			if (resultado > 88.00):
				bot.send_message(ChatGrupo_id,"WARNING: "+ nombreobjeto[i] + " se encuentra utilizando un " + str(resultado) + "% de su capacidad total."+ "\n\n"+
				"Si supera el 95%, mi colega, @MonitorRedes2020, enviará un email al servicio de soporte técnico notificando el problema.")
				
	return mensaje

def malwareScan(host):

	lista_procesos = getArrayValues("HOST-RESOURCES-MIB","hrSWRunName",host)
	f= open("maliciusProcessesDB.txt","r")
	lista_malware = f.read()
	#print lista_malware
	lista_malware_array = lista_malware.split("\n")
	f.close()
	j=0
	mensaje_malware=""
	for i in range (0,len(lista_procesos)):
		for j in range(0,len(lista_malware_array)):
			if (str(lista_malware_array[j]) == str(lista_procesos[i])):
				mensaje_malware +=(str(lista_malware_array[j])+"\n")
	return mensaje_malware

def writting_log(message):
	print str(datetime.now())+": "+str(message.from_user) + " Ha enviado: '" +str(message.text)+"'\n"
	f= open("Log.txt","a")
	f.write(str(datetime.now())+": "+str(message.from_user) + " Ha enviado: '" +str(message.text)+"'\n")
	f.close()


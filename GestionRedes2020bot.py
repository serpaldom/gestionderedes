# -*- coding:utf-8 -*-
import telebot
from  telebot import types
import os
import subprocess
import commands
import smtplib
import requests
import random
import json
import utilities
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

print "____________________________BOT INICIADO ____________________________\n"
print str(datetime.now()) + ": "+ str(bot.get_me())
print "\n"
bot.send_message(ChatGrupo_id,"¡Hola a tod@s!\nMe tropezado y me he caido pero ya estoy aquí de nuevo :)\nPD: tranquil@s, no me he hecho daño")

default_messages = {
    'welcome':u'¡Bienvenid@ {name}! :D\n\n'
        u'Si has ingresado en este grupo es porque has sido autorizado por Sergio Palacios Dominguez.\n'
        u'En este grupo recibirás todo tipo de información de gestion de redes y monitorizacion '
        u'sobre cuestiones relacionadas con la seguridad de un agente SNMP.'
        u'Puedes hacerme consultas usando los comandos disponibles.\n\n\n'
        u'Para ver una lista y descripción de los comandos disponibles escribe   "/comandos" \n\n'
        u'Si deseas interactuar con el menu de comandos disponible escribe       "/menu" o pulsa en el primero ' 
        u'de los tres iconos que puedes ver en la parte inferior derecha de la pantalla \n\n'
        u'¡Espero que disfrutes de la experiencia!',

    'goodbye':u'¡Hasta la proxima {name}! ;(\n\n'
        u'Espero que lo volvamos a ver algún dia.'
}
@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def on_user_joins(message):
    name = message.new_chat_members[0].first_name
    if hasattr(message.new_chat_members[0], 'last_name') and message.new_chat_members[0].last_name is not None:
        name += u" {}".format(message.new_chat_members[0].last_name)

    if hasattr(message.new_chat_members[0], 'username') and message.new_chat_members[0].username is not None:
        name += u" (@{})".format(message.new_chat_members[0].username)

    bot.send_message(ChatGrupo_id, default_messages['welcome'].format(name=name))

@bot.message_handler(func=lambda m: True, content_types=['left_chat_member'])
def on_user_lefts(message):
    name = message.left_chat_member.first_name
    if hasattr(message.left_chat_member, 'last_name') and message.left_chat_member.last_name is not None:
        name += u" {}".format(message.left_chat_member.last_name)

    if hasattr(message.left_chat_member, 'username') and message.left_chat_member.username is not None:
        name += u" (@{})".format(message.left_chat_member.username)

    bot.send_message(ChatGrupo_id, default_messages['goodbye'].format(name=name))

@bot.message_handler(commands=['menu'])
def send_menu(message):
	#utilities.monitor("HOST-RESOURCES-MIB","hrStorageUsed")
	markup = types.ReplyKeyboardMarkup()
	markup.add('/saludar','/despedirse')
	markup.add('/ayuda','/help')
	markup.add('/ping','/recursos')
	markup.add('/programas','/running')
	markup.add('/interfaces','/MWscan')
	markup.add('/menu','/info')
	
	msg = bot.send_message(ChatGrupo_id, "Selecciona una accion:", reply_markup=markup)
	
@bot.message_handler(commands=['saludar'])
def send_interfaces(message):							
	utilities.writting_log(message)
	
	bot.reply_to(message,"¡HOLA!\n¿Cómo estás @" + str(message.from_user.username) + "? :)")

@bot.message_handler(commands=['despedirse'])
def send_interfaces(message):							
	utilities.writting_log(message)
	bot.reply_to(message,"¡Hasta la próxima @"+ str(message.from_user.username) + "!\nEspero que sea pronto... ;(")

@bot.message_handler(commands=['help','ayuda'])
def send_help(message):
	utilities.writting_log(message)
	bot.reply_to(message, "¿Necesitas ayuda? Ponte en contacto con \n sergiopalaciosdominguez97@gmail.com")

@bot.message_handler(commands=['info'])
def send_help(message):
	utilities.writting_log(message)
	bot.reply_to(message, "Has solicitado información sobre el agente monitorizado. Aquí la tienes: \n\n"
		 + "Nombre: \n"+utilities.getValues("HOST-RESOURCES-MIB","sysName",host)+"\nDescripción: \n" + utilities.getValues("HOST-RESOURCES-MIB","sysDescr",host) +
		 "\nÚltima fecha de reinicio: \n" + utilities.getValues("HOST-RESOURCES-MIB","sysUpTime",host))


@bot.message_handler(commands=['comandos','commands'])
def send_commands(message):
	utilities.writting_log(message)
	bot.reply_to(message, utilities.comandos_disponibles())

@bot.message_handler(commands=['interfaces'])
def send_interfaces(message):							
	utilities.writting_log(message)
	bot.reply_to(message,"INTERFACES: \n\n"+ utilities.getValues("IF-MIB","ifName",host))

@bot.message_handler(commands=['programas'])
def send_programs(message):
	utilities.writting_log(message)						
	bot.reply_to(message,"Actualmente se encuentran "+ utilities.getTamValues("HOST-RESOURCES-MIB","hrSWInstalledName",host)+" programas instalados:\n\n"+ utilities.getValues("HOST-RESOURCES-MIB","hrSWInstalledName",host))

@bot.message_handler(commands=['running'])
def send_running(message):
	utilities.writting_log(message)				
	bot.reply_to(message,"Actualmente se encuentran "+ utilities.getTamValues("HOST-RESOURCES-MIB","hrSWRunName",host)+" procesos en ejecución:\n\n"+utilities.getValues("HOST-RESOURCES-MIB","hrSWRunName",host))
	
@bot.message_handler(commands=['ping'])
def send_ping(message):
	utilities.writting_log(message)
	bot.reply_to(message,"Comprobando conexion: \n\n"+ utilities.comprobar_conexion(host))

@bot.message_handler(commands=['recursos'])
def send_recursos(message):
	utilities.writting_log(message)
	bot.reply_to(message,"Aquí tienes los recursos utilizados actualmente por el agente: \n\n"+ utilities.recursos(host))

@bot.message_handler(commands=['MWscan'])
def send_recursos(message):
	utilities.writting_log(message)
	bot.send_message(ChatGrupo_id,"Realizando escaner de malware en el agente... \n\nPor favor, espere unos segundos.")
	time.sleep(5.00)
	if (utilities.malwareScan(host) == ""):
		bot.reply_to(message,"No se ha detectado malware en el equipo :)")
	else:
		bot.reply_to(message,"Se ha detectado posibles procesos relacionados con malware en el equipo:\n"+utilities.malwareScan(host)+"\n"+ 
			"NOTA: si un proceso aparece más de una vez en la lista, es posible que se esté ejecutando varias veces de manera simultánea."+
			"\nDebe ponerse cuanto antes en contacto con el servicio de soporte para evaluar la situación.")


bot.polling()

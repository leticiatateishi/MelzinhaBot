# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

import telebot
import random
import time
import threading
from datetime import datetime, date, timedelta
from telebot import types

inscritos = []

bot = telebot.TeleBot("TOKEN")

@bot.message_handler(commands=['mel'])
def mandar_foto(message):
	endereco = 'melzinha/' + str(random.randint(1, 64)) + '.jpg'
	foto = open(endereco, 'rb')
	bot.send_photo(message.chat.id, foto)


@bot.message_handler(commands=['inscrever'])
def inscrever(message):
	if message.chat.id in inscritos:
		msg = 'Você já está inscrito e deve receber uma foto da Mel todo dia às 9h'
		bot.send_message(message.chat.id, msg)
		return

	inscritos.append(message.chat.id)
	msg = 'Inscrição feita. Você deve receber uma foto da Mel todo dia!! Parabéns!!!'
	bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['cancelar_inscricao'])
def cancelar(message):
	if message.chat.id in inscritos:
		inscritos.remove(message.chat.id)
		msg = 'Inscrição cancelada. Mas a Mel ainda te ama.'
		bot.send_message(message.chat.id, msg)


def processar_inscricoes():
	for inscrito in inscritos:
		endereco = 'melzinha/' + str(random.randint(1, 64)) + '.jpg'
		foto = open(endereco, 'rb')
		bot.send_photo(inscrito, foto)


def inicia_cronometro():
	global sub_timer
	horario = datetime.now()
	proximo = horario.replace(hour = 13, minute = 26)


	delta = proximo.timestamp() - horario.timestamp()
	for inscrito in inscritos:
		msg = 'delta = ' + delta + 'segundos'
		bot.send_message(inscrito, msg)
	sub_timer = threading.Timer(delta, processar_inscricoes)
	sub_timer.start()


def main():
	inicia_cronometro()
	bot.polling()

if __name__ == "__main__":
	main()
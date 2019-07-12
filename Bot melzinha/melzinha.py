# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

import telebot
import random
import time
from datetime import datetime, date
from telebot import types

inscritos = []

bot = telebot.TeleBot("845551679:AAGL_ksuJ30URFrFS_amf3r0-hNmma0VWCk")

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


bot.polling()
# def main():
# 	while True:
# 		tempo = datetime.now()
# 		if (tempo.hour == 21):
# 			for pessoa in inscritos:
# 				endereco = 'melzinha/' + str(random.randint(1, 63)) + '.jpg'
# 				foto = open(endereco, 'rb')
# 				bot.send_photo(pessoa, foto)

# if __name__ == "__main__":
# 	main()
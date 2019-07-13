# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

import telebot
import random
import time
import threading
import glob
import json
from datetime import datetime, date, timedelta
from telebot import types


"""Caminho do arquivo de configuração do tipo JSON."""
caminho_configuracao = 'config.json'


# Na thread inicial, configuramos e aguardamos as respostas do bot
if __name__ == "__main__":
	# Abrimos o arquivo de configuração como leitura
	with open(caminho_configuracao, mode='rt', encoding='utf-8') as arquivo:
		# Carregamos o JSON a partir do arquivo
		configuracao = json.load(arquivo)

	# Com o token, registramos o bot
	bot = telebot.TeleBot(configuracao['token'])


	def salvar_configuracao():
		"""Salva a configuração do bot no arquivo."""
		with open(caminho_configuracao, mode='wt', encoding='utf-8') as arquivo:
			json.dump(configuracao, arquivo, indent='\t')


	# Registramos os handlers

	@bot.message_handler(commands=['mel'])
	def mandar_foto(message):
		"""Envia uma foto aleatória ao receber o comando '/mel' no Telegram."""
		foto = open(pegar_arquivo_aleatorio(), 'rb')
		bot.send_photo(message.chat.id, foto)


	@bot.message_handler(commands=['inscrever'])
	def inscrever(message):
		"""Confere se o chat que enviou o comando '/inscrever' está inscrito e o inscreve se necessário."""
		# Conferimos se já é inscrito
		if message.chat.id in configuracao['inscritas']:
			msg = 'Essa conversa já está inscrita e deve receber uma linda foto da Mel todo dia <3'
			bot.send_message(message.chat.id, msg)
			return

		# Se não é, inscrevemos o ID e salvamos o JSON
		configuracao['inscritas'].append(message.chat.id)
		salvar_configuracao()
		msg = 'Inscrição feita. Essa conversa deve receber uma foto da Mel todo dia!! Parabéns!!!'
		bot.send_message(message.chat.id, msg)


	@bot.message_handler(commands=['cancelar_inscricao'])
	def cancelar(message):
		"""Confere se o chat que enviou o comando '/cancelar_inscricao' está inscrito e o desinscreve se necessário."""
		# Conferimos se o chat não está inscrito
		if message.chat.id not in configuracao['inscritas']:
			msg = 'Você precisa se inscrever primeiro!! Veja mais a Melzinha!'
			bot.send_message(message.chat.id, msg)
			return

		# Se usuário foi inscrito, removemos e salvamos o JSON
		configuracao['inscritas'].remove(message.chat.id)
		salvar_configuracao()
		msg = 'Inscrição cancelada. Mas a Mel ainda te ama.'
		bot.send_message(message.chat.id, msg)


def pegar_arquivo_aleatorio():
	"""Retorna um caminho aleatório dentro da pasta configurada de fotos."""
	# Pegamos apenas os arquivos da pasta configurada
	enderecos = glob.glob(configuracao['caminho_fotos'] + '*.jpg', recursive=True)
	# Escolhemos um caminho aleatório
	return random.choice(enderecos)


def processar_inscricoes():
	"""Envia uma foto aleatória da pasta configurada de fotos a cada chat inscrito."""
	# Para cada chat...
	print('Enviando mensagem às', len(configuracao['inscritas']), 'conversas inscritas.')
	for inscrito in configuracao['inscritas']:
		# ... o enviamos uma foto aleatória
		foto = open(pegar_arquivo_aleatorio(), 'rb')
		bot.send_photo(inscrito, foto)

	# Reconfiguramos o cronômetro
	inicia_cronometro()


def inicia_cronometro():
	"""Inicia um cronômetro para executar a função que envia uma foto aleatória para cada chat inscrito."""
	global sub_timer

	# Calculamos o período de execução
	delta = timedelta(days = 1)

	# Agendamos para executar a função de enviar uma foto a cada inscrito
	sub_timer = threading.Timer(delta.total_seconds(), processar_inscricoes)
	sub_timer.start()


def main():
	"""Inicia o cronômetro para executar a função de mandar fotos aos inscrítos e responde às mensagens."""
	inicia_cronometro()
	bot.polling()


# Na thread inicial, executamos 'main()'
if __name__ == "__main__":
	main()

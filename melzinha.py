# Letícia Mayumi A. Tateishi

# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

from telegram import Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

import json
import time
import glob
import random
import logging
import threading

from datetime import time


"""Caminho do arquivo de configuração do tipo JSON."""
caminho_configuracao = 'config.json'

def salvar_configuracao():
	"""Salva """
	# Abrimos o arquivo de configuração com escrita
	with open(caminho_configuracao, mode='wt', encoding='utf-8') as arquivo:
		# Salvamos o arquivo de configuração JSON
		json.dump(configuracao, arquivo, indent='\t')


def pegar_arquivo_aleatorio():
	"""Retorna um caminho aleatório dentro da pasta configurada de fotos."""
	# Pegamos apenas os arquivos da pasta configurada
	enderecos = glob.glob(configuracao['caminho_fotos'] + '*.jpg', recursive=True)
	# Escolhemos um caminho aleatório
	return random.choice(enderecos)


def help(update, context):
	"""Envia uma mensagem quando usuário utiliza /help."""
	# Enviamos mensagem de ajuda
	update.message.reply_text(
		"""A melzinha pode te enviar uma foto diariamente se você se inscrever.

		Pode utilizar /inscrever para isso e
		/cancelar_inscricao para infelizmente parar de receber as fotos.

		Se quiser, ainda tem /mel para receber uma foto aleatória da Mel."""
	)


def mel(update, context):
	"""Envia uma foto aleatória ao receber o comando '/mel' no Telegram."""
	# Conferimos se estamos num chat válido (possui chat id)
	if update.effective_chat is not None:
		# Abrimos uma foto aleatória
		foto = open(pegar_arquivo_aleatorio(), 'rb')
		# Enviamos a foto
		context.bot.send_photo(update.effective_chat.id, foto)


def inscrever(update, context):
	"""Processamos pedido de inscrição do usuário (comando /inscrever no Telegram)"""
	# Conferimos se temos chat id
	if update.effective_chat is None:
		return

	# Pegamos o chat id do chat
	chat_id = update.effective_chat.id

	"""Confere se o chat que enviou o comando '/inscrever' está inscrito e o inscreve se necessário."""
	# Conferimos se já é inscrito
	if chat_id in configuracao['inscritas']:
		update.message.reply_text('Essa conversa já está inscrita e deve receber uma linda foto da Mel todo dia <3')
		return

	# Se não é, inscrevemos o ID e salvamos o JSON
	configuracao['inscritas'].append(chat_id)
	salvar_configuracao()
	update.message.reply_text('Inscrição feita. Essa conversa deve receber uma foto da Mel todo dia!! Parabéns!!!')


def cancelar_inscricao(update, context):
	"""Processamos pedido de cancelamento de inscrição do usuário (comando /cancelar_inscricao no Telegram)"""
	# Conferimos se temos chat id
	if update.effective_chat is None:
		return

	# Pegamos o chat id do chat
	chat_id = update.effective_chat.id

	# Conferimos se o chat não está inscrito
	if chat_id not in configuracao['inscritas']:
		update.message.reply_text('Você precisa se inscrever primeiro!! Veja mais a Melzinha!')
		return

	# Se usuário foi inscrito, removemos e salvamos o JSON
	configuracao['inscritas'].remove(chat_id)
	salvar_configuracao()
	update.message.reply_text('Inscrição cancelada. Mas a Mel ainda te ama.')


def processar_inscricoes(context):
	"""Envia uma foto aleatória da pasta configurada de fotos a cada chat inscrito."""
	# Para cada chat...
	print('Enviando mensagem às', len(configuracao['inscritas']), 'conversas inscritas.')
	for inscrito in configuracao['inscritas']:
		# ... o enviamos uma foto aleatória
		foto = open(pegar_arquivo_aleatorio(), 'rb')
		context.bot.send_photo(inscrito, foto)


# Na thread inicial, configuramos e aguardamos as respostas do bot
if __name__ == "__main__":
	# Ativamos logging
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

	# Abrimos o arquivo de configuração como leitura
	with open(caminho_configuracao, mode='rt', encoding='utf-8') as arquivo:
		# Carregamos o JSON a partir do arquivo
		configuracao = json.load(arquivo)

	# Iniciamos updater
	updater = Updater(configuracao['token'], use_context=True)

	# Definimos horário e mostramos imagem diariamente
	horario = time(12, 0, 0)
	job_daily = updater.job_queue.run_daily(processar_inscricoes, horario)

	# Adicionamos handler para comandos
	dispatcher = updater.dispatcher
	dispatcher.add_handler(CommandHandler("start", help))
	dispatcher.add_handler(CommandHandler("help", help))
	dispatcher.add_handler(CommandHandler("mel", mel))
	dispatcher.add_handler(CommandHandler("inscrever", inscrever))
	dispatcher.add_handler(CommandHandler("cancelar_inscricao", cancelar_inscricao))

	# Iniciamos o bot
	updater.start_polling()

	# Idle até Ctrl+C
	updater.idle()

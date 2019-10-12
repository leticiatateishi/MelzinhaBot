# Letícia Mayumi A. Tateishi

# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

from telegram import Bot
import logging
import json
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
import random
import time
import threading
import glob
import json
from datetime import time

"""Caminho do arquivo de configuração do tipo JSON."""
caminho_configuracao = 'config.json'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def salvar_configuracao():
	with open(caminho_configuracao, mode='wt', encoding='utf-8') as arquivo:
		json.dump(configuracao, arquivo, indent='\t')

def pegar_arquivo_aleatorio():
	"""Retorna um caminho aleatório dentro da pasta configurada de fotos."""
	# Pegamos apenas os arquivos da pasta configurada
	enderecos = glob.glob(configuracao['caminho_fotos'] + '*.jpg', recursive=True)
	# Escolhemos um caminho aleatório
	return random.choice(enderecos)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
	"""Send a message when the command /start is issued."""
	update.message.reply_text('Hi!')
	print(update)


def help(update, context):
	"""Send a message when the command /help is issued."""
	update.message.reply_text('HAlp!')

def mel(update, context):
	"""Envia uma foto aleatória ao receber o comando '/mel' no Telegram."""
	if (update.effective_chat != None):
		foto = open(pegar_arquivo_aleatorio(), 'rb')
		bot.send_photo(update.effective_chat.id, foto)

def inscrever(update, context):
	if (update.effective_chat != None):
		chat_id = update.effective_chat.id
	else:
		return

	"""Confere se o chat que enviou o comando '/inscrever' está inscrito e o inscreve se necessário."""
	# Conferimos se já é inscrito
	if chat_id in configuracao['inscritas']:
		msg = 'Essa conversa já está inscrita e deve receber uma linda foto da Mel todo dia <3'
		update.message.reply_text(msg)
		return

	# Se não é, inscrevemos o ID e salvamos o JSON
	configuracao['inscritas'].append(chat_id)
	salvar_configuracao()
	msg = 'Inscrição feita. Essa conversa deve receber uma foto da Mel todo dia!! Parabéns!!!'
	update.message.reply_text(msg)


def cancelar_inscricao(update, context):
	if (update.effective_chat != None):
		chat_id = update.effective_chat.id
	else:
		return

	"""Confere se o chat que enviou o comando '/cancelar_inscricao' está inscrito e o desinscreve se necessário."""
	# Conferimos se o chat não está inscrito
	if chat_id not in configuracao['inscritas']:
		msg = 'Você precisa se inscrever primeiro!! Veja mais a Melzinha!'
		update.message.reply_text(msg)
		return

	# Se usuário foi inscrito, removemos e salvamos o JSON
	configuracao['inscritas'].remove(chat_id)
	salvar_configuracao()
	msg = 'Inscrição cancelada. Mas a Mel ainda te ama.'
	update.message.reply_text(msg)

def processar_inscricoes(context):
	"""Envia uma foto aleatória da pasta configurada de fotos a cada chat inscrito."""
	# Para cada chat...
	print('Enviando mensagem às', len(configuracao['inscritas']), 'conversas inscritas.')
	for inscrito in configuracao['inscritas']:
		# ... o enviamos uma foto aleatória
		foto = open(pegar_arquivo_aleatorio(), 'rb')
		bot.send_photo(inscrito, foto)

# Na thread inicial, configuramos e aguardamos as respostas do bot
if __name__ == "__main__":
	# Abrimos o arquivo de configuração como leitura
	with open(caminho_configuracao, mode='rt', encoding='utf-8') as arquivo:
		# Carregamos o JSON a partir do arquivo
		configuracao = json.load(arquivo)

	token = configuracao['token']
	updater = Updater(token, use_context=True)
	bot = Bot(token=token)
	dispatcher = updater.dispatcher
	jobqueue = updater.job_queue

	horario = time(12, 0, 0)
	job_daily = jobqueue.run_daily(processar_inscricoes, horario)

	dispatcher.add_handler(CommandHandler("start", start))
	dispatcher.add_handler(CommandHandler("help", help))
	dispatcher.add_handler(CommandHandler("mel", mel))
	dispatcher.add_handler(CommandHandler("inscrever", inscrever))
	dispatcher.add_handler(CommandHandler("cancelar_inscricao", cancelar_inscricao))

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()

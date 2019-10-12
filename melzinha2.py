# Letícia Mayumi A. Tateishi

# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

import logging
import json
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters


"""Caminho do arquivo de configuração do tipo JSON."""
caminho_configuracao = 'config.json'


# Na thread inicial, configuramos e aguardamos as respostas do bot
if __name__ == "__main__":
	# Abrimos o arquivo de configuração como leitura
	with open(caminho_configuracao, mode='rt', encoding='utf-8') as arquivo:
		# Carregamos o JSON a partir do arquivo
		configuracao = json.load(arquivo)

	# Com o token, registramos o bot
	bot = telegram.Bot(token='token')

	def salvar_configuracao():
		"""Salva a configuração do bot no arquivo."""
		with open(caminho_configuracao, mode='wt', encoding='utf-8') as arquivo:
			json.dump(configuracao, arquivo, indent='\t')



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token='token', use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sou a Mel")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()

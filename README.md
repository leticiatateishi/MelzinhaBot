# MelzinhaBot

Esse é o bot que te acaricia como se fosse a linda Melzinha. Com ele, você pode receber imagens fofas da melhor e maior cachorra do mundo! Até diariamente!

Amamos ela e você amará também! Disponível em [@MelzinhaBot](https://t.me/MelzinhaBot) no [Telegram](https://telegram.org/).


## Configurando o bot

Para executar o bot, é necessário possuir um [_token_](https://core.telegram.org/bots#generating-an-authorization-token) de Telegram e escrever no arquivo `config.json`, que é ignorado pelo GitHub para segurança. Seu exemplo pode ser econtrado abaixo:
```
{
    "caminho_fotos": "melzinha/",
    "token": "INSIRA TOKEN AQUI",
    "inscritas": []
}

```

Apenas imagens JPEG poderão ser utilizadas, com a extensão `.jpg`.

Além da configuração, precisamos ter instalado a API utilizada [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) através do comando:
```
$ pip3 install --user python-telegram-bot
```

E executar:
```
$ python3 melzinha.py
```


## Resumo de funcionamento

O bot utiliza o arquivo de configuração em formato JSON como banco de dados de conversas inscritas. Além disso, reagenda o envio de imagens após execução com período de 1 dia, ou seja, irá enviar sempre uma foto às inscritas no mesmo horário de início de execução do bot.

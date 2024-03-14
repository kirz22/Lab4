import telebot
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Конфигурация биткойн-узла
rpc_user = 'kzcashrpc'
rpc_password = 'rJSOnO4Ik7U4tULJektex3Fz'
rpc_host = 'localhost'
rpc_port = 8276
telegram_token = '6997050555:AAEmrN_-hc747dxe4jKWIJS6i9fCh578PZE'

# Подключение к кошельку KZCash
def connect_to_wallet():
    return AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

bot = telebot.TeleBot(telegram_token)

# Генерация нового адреса
@bot.message_handler(commands=['getnewaddress'])
def get_new_address(message):
    wallet = connect_to_wallet()
    new_address = wallet.getnewaddress()
    bot.reply_to(message, f'Новый адрес: {new_address}')

# Получение баланса
@bot.message_handler(commands=['getbalance'])
def get_balance(message):
    wallet = connect_to_wallet()
    balance = wallet.getbalance()
    bot.reply_to(message, f'Баланс: {balance:.15f}')

# Получение баланса отдельного адреса
@bot.message_handler(commands=['getaddressbalance'])
def get_address_balance(message):
    wallet = connect_to_wallet()
    address = message.text.split()[1] if len(message.text.split()) > 1 else None
    if address:
        balance = wallet.getreceivedbyaddress(address)
        bot.reply_to(message, f'Баланс адреса {address}: {balance:.15f}')
    else:
        bot.reply_to(message, 'Пожалуйста, укажите адрес после команды.')

# Обработка неправильных команд
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Неправильная команда. Пожалуйста, попробуйте еще раз.')

# Запуск бота Telegram
if __name__ == '__main__':
    bot.polling()

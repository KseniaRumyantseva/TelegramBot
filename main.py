import config
import telebot
import requests
import functions
from telebot import types

token = config.my_token
api_news = config.api_news
bot = telebot.TeleBot(token)

news = []

def convertList(news):
    str = ''
    for i in news:
        str += i+"\n"
    return str

def categoriesList(categories):
    cs = ''
    for category in categories:
        cs += category + "\n"
    return cs


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Список команд, котрые вы можете использовать:\n"
                          "/news - посмотреть новости по категориям из подписок\n"
                          "/subscribe - подписаться на категорию\n"
                            "/unsubscribe - отписаться от категории\n"
                            "/mycategories - посмотреть список моих категорий\n")


@bot.message_handler(commands=['start'])
def get_start(message):
    user_id = message.from_user.id
    if functions.check_user(user_id) is not None:
        bot.send_message(message.chat.id, "Чтобы посмотреть список команд введите /help")
    else:
        functions.add_user(user_id)
        bot.send_message(message.chat.id, "Чтобы посмотреть список команд введите /help")

@bot.message_handler(commands=['subscribe'])
def send_categories(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    business = types.KeyboardButton('business')
    entertainment = types.KeyboardButton('entertainment')
    general = types.KeyboardButton('general')
    health = types.KeyboardButton('health')
    science = types.KeyboardButton('science')
    sports = types.KeyboardButton('sports')
    technology = types.KeyboardButton('technology')
    markup.add(business, entertainment, general, health, science, sports, technology)
    bot.send_message(message.chat.id, "На какую категорию хотите подписаться?", reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def message_input_step(message):
        text = message.text
        bot.send_message(message.chat.id, functions.add_subscribe(message.text, message.from_user.id))
    bot.register_next_step_handler(message, message_input_step)

@bot.message_handler(commands=['unsubscribe'])
def send_categories(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    business = types.KeyboardButton('business')
    entertainment = types.KeyboardButton('entertainment')
    general = types.KeyboardButton('general')
    health = types.KeyboardButton('health')
    science = types.KeyboardButton('science')
    sports = types.KeyboardButton('sports')
    technology = types.KeyboardButton('technology')
    markup.add(business, entertainment, general, health, science, sports, technology)
    bot.send_message(message.chat.id, "От какой категории хотите отписаться?", reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def message_input_step(message):
        text = message.text
        bot.send_message(message.chat.id, functions.delete_subscribe(message.text, message.from_user.id))
    bot.register_next_step_handler(message, message_input_step)

@bot.message_handler(commands=['mycategories'])
def show_mycategories(message):
    bot.send_message(message.chat.id, functions.show_mycategories(message.from_user.id))


@bot.message_handler(commands=['news'])
def send_news(message):
    categories = functions.user_categories(message.from_user.id)
    if categories != []:
        for category in categories:
            news = []
            a = requests.get(f'https://newsapi.org/v2/top-headlines?apiKey={api_news}&category={category}&pageSize=1&language=ru')
            for i in a.json()['articles']:
                news.append([i['title'], i['publishedAt'], i['url']])
            for line in news:
                bot.send_message(message.chat.id, convertList(line))
    else:
        bot.send_message(message.chat.id, "У вас нет подписок! " \
               "Воспользуйтесь командой /subscribe, чтобы подписаться на категории")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, 'Возможно, вам нужна команда /help')

bot.infinity_polling()



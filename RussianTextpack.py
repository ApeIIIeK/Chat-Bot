import telebot
from telebot import types
import sqlite3
from telebot.types import LabeledPrice
prices = [LabeledPrice(label='Lore of the heroes', amount=5750), LabeledPrice('Gift wrapping', 500)]
provider_token = "1744374395:TEST:5feeb7ae1d47732e8cfc"
bot = telebot.TeleBot("6424637647:AAEXDGYGwpAY59tJIh4zNF5M2VM6umky-Z4")
conn = sqlite3.connect('bd.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(userID: int, User_Name: str, User_Surname: str):
	cursor.execute('INSERT INTO id_users (userID, User_Name, User_Surname) VALUES (?, ?, ?)', (userID, User_Name, User_Surname))
	conn.commit()
     
def db_table_val2(userID: int, Username: str, Usersurname: str):
	cursor.execute('INSERT INTO Donate (userID, Username, Usersurname) VALUES (?, ?, ?)', (userID, Username, Usersurname))
	conn.commit()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    About = types.KeyboardButton('О боте ❓')
    Items = types.KeyboardButton('Предметы 🛠️')
    Database = types.KeyboardButton('Добавить меня в БД 📊')
    LoreHeroes = types.KeyboardButton('Лор героев 💸')
    markup.row(About, Items,Database, LoreHeroes)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} !", reply_markup=markup)
    bot.register_next_step_handler(message, markup_click)
    
@bot.message_handler(content_types=['text'])
def markup_click(message):
    if message.text == 'О боте ❓':
         bot.send_message(message.chat.id, "Данный бот, поможет вам быстрее найти сборку на любого героя в доте на любом устройсте на котором установлен Телеграм. Главное прописывать имя героя правильно иначе ничего не получиться. "
                          "\n\nА так же может рассказать вам интересные истории о героях за символическую плату" )
    elif message.text == 'Предметы 🛠️':
         bot.send_message(message.chat.id, "Напишите название героя, для которого нужна сборка")
         bot.register_next_step_handler(message, a_replace)
    elif message.text == 'Добавить меня в БД 📊':
         bot.send_message(message.chat.id, "В ответ на сообщение напишите <<Привет>>, Спасибо!")
         bot.register_next_step_handler(message, db_place)
    elif message.text == 'Лор героев 💸':
         bot.send_message(message.chat.id, "Это функция бота платная, стоимость услуги - 70р. Чтобы приобрести ее выполните команду /buy")
         bot.register_next_step_handler(message, buy_place)
@bot.message_handler(content_types=['text'])
def a_replace(message):
     Heroes = message.text 
     a = "dota2protracker.com/hero/"
     a+=Heroes.replace(" ", "%20")
     bot.send_message(message.chat.id, a )

@bot.message_handler(content_types=['text'])
def db_place(message):
	if message.text.lower() == 'привет':
		bot.send_message(message.chat.id, 'Привет! Ваше имя добавлено в базу данных!')
		
		us_id = message.from_user.id
		us_name = message.from_user.first_name
		us_sname = message.from_user.last_name
				
		db_table_val(userID=us_id, User_Name=us_name, User_Surname=us_sname)

PRICE = types.LabeledPrice(label="Подписка на 1 месяц", amount=70*100)  # в копейках (руб)

@bot.message_handler(commands=['buy'])
def buy_place(message):
    bot.send_message(message.chat.id,
                     "Реальные карты у меня не будут работать, деньги с вашего счета списываться не будут."
                     " Используйте этот номер тестовой карты для оплаты: `4242 4242 4242 4242`"
                     "\n\nЭто ваш демо-счет:", parse_mode='Markdown')
    bot.send_invoice(
                     message.chat.id,  #chat_id
                     'Рабочая', #Название
                     ' Хотите узнать за кого вы играете, его историю? Может с кем он близок, а с кем он Враг? Или просто узнать свое персонажа поближе, тогда покупайте данную функцию сегодня!', #description
                     'Счастливый пятничний купон', #Счет
                     provider_token, #Токен 
                     'rub', #Валюта
                     prices, #Цены
                     photo_url='https://cq.ru/storage/uploads/posts/83811/dota-geroi-fan-art-personazhi.jpg',
                     photo_height=512,  # !=0/Нет или изображение не будет отображаться
                     photo_width=512,
                     photo_size=512,
                     is_flexible=False,  #true, если вам нужно настроить стоимость доставки
                     start_parameter='Lore_heroes-example')

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Крипы пытались украсть CVV вашей карты, но мы успешно защитили ваши учетные данные")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
           
     bot.send_message(message.chat.id,
                     'Уах! Спасибо за оплату!'
                     'Оставайтесь на связи.\n\nИспользуйте /buy ещё раз, чтобы купить подписку для друга'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')
                   

bot.polling(none_stop=True)
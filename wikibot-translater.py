import telebot, wikipedia, re, translators
from time import sleep

# while True:
#     a = input("lol")
#     b = a[::-1]
#     if a == b:
#         print(a[:-1])
#     else:
#         print(a)

bot = telebot.TeleBot('5062500880:AAHSUEB9DKFB4kfr-aFm2WMaJBFQEZ3si8Y')

english = 'eng english английский англ ан en англійська'
ukraine = 'uk ukr ukraine украинский ук українська укр'
russian = 'ru rus russian русский рус ру російська'

searches = open('save.txt', 'r')
searches_message = set()
for line in searches:
    searches_message.add(line.strip())
searches.close()

def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext=ny.content[:1000]
        wikimas=wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not('==' in x):
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'Нету информации по вашему запросу или вы ввели некоректным языком по заданой команде'

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Как использовать бота? Нажмите на\n/help для детальной информации')

@bot.message_handler(commands=["help"])
def helper(m):
    bot.send_message(m.chat.id, 'Как правильно пользоваться ботом?\n\ntext = слово будь якою мовою\n\nsearch [text] - для надання інформації англійською мовою\nпоиск [text] - російською\nпошук [text] - українською\n\ncomment [text] -коментарий автору')
    bot.send_message(m.chat.id, 'напишите перевод, переклад, translate чтобы включить переводчик\n\nЧтобы поддержать создателя бота коментарий должен содержать словo "respect"')

@bot.message_handler(content_types=["text"])
def handle_text(message):
    print(message.text)
    if message.text.lower()[:6] == 'search':
        if not str(message.text) in searches_message:
            searches = open('save.txt', 'a')
            searches.write(str(f'firstname:{message.from_user.first_name} lastname:{message.from_user.last_name} username:{message.from_user.username} id:{message.from_user.id} запрос поиска:[|{message.text[6:]}|]'))
            searches.close()
        wikipedia.set_lang("en")
        bot.send_message(message.chat.id, getwiki(message.text))
    if message.text.lower()[:5] == 'поиск':
        if not str(message.text) in searches_message:
            searches = open('save.txt', 'a')
            searches.write(str(f'firstname:{message.from_user.first_name} lastname:{message.from_user.last_name} username:{message.from_user.username} id:{message.from_user.id} запрос поиска:[|{message.text[5:]}|]'))
            searches.close()
        wikipedia.set_lang("ru")
        bot.send_message(message.chat.id, getwiki(message.text[5:]))
    if message.text.lower()[:5] == 'пошук':
        if not str(message.text) in searches_message:
            searches = open('save.txt', 'a')
            searches.write(str(f'firstname:{message.from_user.first_name} lastname:{message.from_user.last_name} username:{message.from_user.username} id:{message.from_user.id} запрос поиска:[|{message.text[5:]}|]'))
            searches.close()
        wikipedia.set_lang("uk")
        bot.send_message(message.chat.id, getwiki(message.text))
    if message.text.lower()[:7] == 'comment':
        if "respect".lower() in message.text:
            bot.send_message(message.from_user.id, 'Спасибо что пользуетесь моим ботом пишите мне в личку по другим вопросам @shakal11052002')
        bot.send_message(-540623459, f'{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username}\nComment:\n{message.text[7:]}')

    if message.text.lower()[:7] == 'перевод' or message.text.lower()[:8] == "переклад" or message.text.lower()[:9] == "translate":
        word_uk = '`' + str("украинский")+ '`'
        word_en = '`' + str("английский") + '`'
        word_ru = '`' + str("русский") + '`'
        bot.send_message(message.chat.id, 'Языки:\n'+'`'+ str("украинский")+'`'+" | "+word_en+" | "+word_ru, parse_mode='Markdown')
        bot.send_message(message.chat.id, f'напишите язык на который перевести и текст который перевести.\n\nНапример:\n\nукраинский I love you\nили\nанглийский я люблю тебя')
    if message.text.lower()[:10] == 'английский':
        messages = translators.google(message.text[11:], from_language='auto', to_language='en')
        sleep(1)
        bot.send_message(message.chat.id, f"{messages}")
    elif message.text.lower()[:10] == 'украинский':
        messages = translators.google(message.text[11:], from_language='auto', to_language='uk')
        sleep(1)
        bot.send_message(message.chat.id, f"{messages}")
    elif message.text.lower()[:7] == 'русский':
        messages = translators.google(message.text[9:], from_language='auto', to_language='ru')
        sleep(1)
        bot.send_message(message.chat.id, f"{messages}")

bot.polling(none_stop=True, interval=0)

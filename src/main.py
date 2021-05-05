import telebot
import xlrd
import os
from random import (randint, random)
import sqlite3
from sqlalchemy import create_engine
import pandas as pd
from random import randint

db = create_engine('sqlite:////Users/rahme/Desktop/linguahelper-move_old_code/linguahelper/inputs/orders.db',
                   echo=False)

sql_chats = """CREATE TABLE if not exists chats
               (chat_id int PRIMARY KEY, date_registration datetime)
            """
sql_words = """CREATE TABLE if not exists Words
                        (chat_id int,
                        from_language text,
                        to_language text,
                        from_word text,
                        to_word text,
                        FOREIGN KEY(chat_id) REFERENCES chats(chat_id));
                                             """
sql_games = """CREATE TABLE if not exists Games
                        (chat_id int,
                        from_language text,
                        to_languge text,
                        from_word text,
                        to_word text PRIMARY KEY,
                        FOREIGN KEY(chat_id) REFERENCES chats(chat_id));
                                                 """
sql_commands = [sql_chats, sql_words, sql_words, sql_games]


def checklang(user_id):
    mysheet = []
    conn = db.connect()
    result = conn.execute(
        f"SELECT from_language,to_language, from_word ,to_word  FROM words where chat_id={user_id} ")
    for i in result:
        mysheet.append([i[0], i[1], i[2], i[3]])
    n = len(mysheet)
    lan = set()
    for i in range(n):
        lan.add(str(mysheet[i][0]) + " ---- " + str(mysheet[i][1]))
    for i in range(n):
        lan.add(str(mysheet[i][1]) + " ---- " + str(mysheet[i][0]))
    return lan



def randtwo(ls, sr, chatid):
    mysheet = []
    conn = db.connect()
    result = conn.execute(f"SELECT from_language,to_language, from_word ,to_word  FROM words where chat_id={chatid}")
    for i in result:
        mysheet.append([i[0], i[1], i[2], i[3]])
    n = len(mysheet)
    rm = randint(0, n - 1)
    if (ls == mysheet[rm][0] and sr == mysheet[rm][1]):
        return mysheet[rm][0] + ' ----- ' + mysheet[rm][1] + '\n' + mysheet[rm][2] + ' ----- ' + mysheet[rm][3]
    if (ls == mysheet[rm][1] and sr == mysheet[rm][0]):
        return mysheet[rm][1] + ' ----- ' + mysheet[rm][0] + '\n' + mysheet[rm][3] + ' ----- ' + mysheet[rm][2]
    else:
        return 'exit'



TOKEN = "1001230120:AAHB5gaj02BOsMTENcNDBGJFgKOzNYm4L70"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salam")
    chat_id = message.chat.id
    conn = sqlite3.connect(r'../inputs/orders.db')
    curr = conn.cursor()
    curr.execute(f"select chat_id from chats where chat_id={chat_id}")
    result = curr.fetchone()
    if result == None:
        print('inserted')
        curr.execute(f"insert into chats values({chat_id},DateTime('now'))")
    curr.close()
    conn.commit()
    conn.close()


@bot.message_handler(content_types=['document'])
def document(message):
    try:
        conn_documents = db.connect()
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        local_path = file_id + ".xlsx"
        downloaded_file = bot.download_file(file_path)
        with open(local_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        df = pd.read_excel(local_path, header=None, index_col=None)
        df = df.rename(columns={0: 'from_language', 1: 'to_language', 2: 'from_word', 3: 'to_word'})
        chat_id = message.chat.id
        df['chat_id'] = chat_id
        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols]
        df.to_sql('Words', conn_documents, if_exists='append', index=False)
        os.remove(local_path)
    finally:
        conn_documents.close()


@bot.message_handler(commands=['test'])
def englishfrench(message):
    user_id = message.chat.id

    def rand():
        mysheet = []
        conn = db.connect()
        result = conn.execute(
            f"SELECT from_language,to_language, from_word ,to_word  FROM words where chat_id={user_id} ORDER BY RANDOM() LIMIT 1")
        for i in result:
            mysheet.append(i[0] + ' ----- ' + i[1] + '\n' + i[2] + ' ----- ' + i[3])
            return mysheet

    bot.send_message(user_id, rand())


@bot.message_handler(commands=['englishfrench'])
def frenchenglish(message):
    ''' function randomly selects and displays words from an Exsel file,
    only translating words from English to French.
    '''
    bot.send_message(message.chat.id, randtwo('English', 'French'))


@bot.message_handler(commands=["listoflanguages"])
def handle_start(message):
    '''list of language combinations'''
    user_markup = telebot.types.ReplyKeyboardMarkup()
    for i in checklang(message.chat.id):
        user_markup.row(i)
    bot.send_message(message.chat.id, 'Selected language!!!', reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def main(message):
    '''choice of language combinations'''
    checklan = str(message.text)
    conn = db.connect()
    lans = checklan.split(' ---- ')
    bot.send_message(message.chat.id, randtwo(lans[0], lans[1], message.chat.id))


if __name__ == '__main__':
    try:
        conn = db.connect()
        for command in sql_commands:
            conn.execute(command)
        bot.polling(none_stop=True)
    finally:
        conn.close()

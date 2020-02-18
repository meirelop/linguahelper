import telebot
import xlrd
from random import (randint, random)
def rand():
    rb = xlrd.open_workbook('/Users/admin/Projects/linguahelper/Saved translations.xlsx')
    sheet = rb.sheet_by_index(0)
    rownum = randint(0, sheet.nrows)
    return sheet.cell_value(rownum, 0)+' ----- '+sheet.cell_value(rownum, 1) + '\n' +sheet.cell_value(rownum, 2)+ ' ----- ' + sheet.cell_value(rownum, 3)
    """Эта функция  выбирает случайного слова с Exsel файла."""
Token = "  "
bot = telebot.TeleBot(Token)

def randtwo(ls, sr):
    rb = xlrd.open_workbook('/Users/admin/Projects/linguahelper/Saved translations.xlsx')
    sheet = rb.sheet_by_index(0)
    rownum = randint(0, sheet.nrows)
    while (True):
     if(ls==sheet.cell_value(rownum, 0) and sr==sheet.cell_value(rownum, 1)):
        break
     else:
        rownum = randint(0, sheet.nrows)
    return sheet.cell_value(rownum, 0) + ' ----- ' + sheet.cell_value(rownum, 1) + '\n' +sheet.cell_value(rownum, 2)+ ' ----- ' + sheet.cell_value(rownum, 3)



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, rand())


@bot.message_handler(commands=['frenchenglish'])  #  french - english
def englishfrench(message):
    bot.send_message(message.chat.id, randtwo('French','English'))
    ''' Это функция показываеть слова с Exsel файла рандомно только перевод с французкого на английский .'''

@bot.message_handler(commands=['englishfrench']) # english -frensh
def frenchenglish(message):
    bot.send_message(message.chat.id, randtwo('English','French'))
    ''' Это функция показываеть слова с Exsel файла рандомно только перевод с Английского на Французкий .'''
bot.polling()


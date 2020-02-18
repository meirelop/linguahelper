import telebot
import xlrd
from random import (randint, random)


"""This function selects a random word from an exsel file."""
def rand():
      rb = xlrd.open_workbook('/Users/admin/Projects/linguahelper/Saved translations.xlsx')
      sheet = rb.sheet_by_index(0)
      rownum = randint(0, sheet.nrows)
      return sheet.cell_value(rownum, 0)+' ----- '+sheet.cell_value(rownum, 1) + '\n' +sheet.cell_value(rownum, 2)+ ' ----- ' + sheet.cell_value(rownum, 3)


TOKEN = "  "
bot = telebot.TeleBot(TOKEN)


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

'''This function randomly selects and displays words from an Exsel file,only translate words from French to English.'''
@bot.message_handler(commands=['frenchenglish'])
def englishfrench(message):
    bot.send_message(message.chat.id, randtwo('French','English'))


'''This function randomly selects and displays words from an Exsel file,only translating words from English to French.'''
@bot.message_handler(commands=['englishfrench'])
def frenchenglish(message):
    bot.send_message(message.chat.id, randtwo('English','French'))


bot.polling()


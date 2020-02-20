import telebot
import xlrd
from random import (randint, random)


def rand():
    '''
    Get randomly one translation from given file
       Returns
       -------
       str
           Random translated phrase/sentence
    '''
    rb = xlrd.open_workbook('../inputs/Savedtranslations.xlsx')
    sheet = rb.sheet_by_index(0)
    rownum = randint(0, sheet.nrows)
    return sheet.cell_value(rownum, 0)+' ----- '+sheet.cell_value(rownum, 1) + '\n' +sheet.cell_value(rownum, 2)+ ' ----- ' + sheet.cell_value(rownum, 3)


TOKEN = " "
bot = telebot.TeleBot(TOKEN)


def randtwo(ls, sr):
    '''
    Get randomly one translation from given file
       Parameters
       ----------
       ls: str
           Language to translate from
       sr: str
           Language to translate to

       Returns
       -------
       str
           Random translated phrase/sentence
    '''
    rb = xlrd.open_workbook('../inputs/Savedtranslations.xlsx')
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


@bot.message_handler(commands=['frenchenglish'])
def englishfrench(message):
    ''' function randomly selects and displays words from an Exsel file,only
    translate words from French to English.
    '''
    bot.send_message(message.chat.id, randtwo('French','English'))


@bot.message_handler(commands=['englishfrench'])
def frenchenglish(message):
    ''' function randomly selects and displays words from an Exsel file,
    only translating words from English to French.
    '''
    bot.send_message(message.chat.id, randtwo('English','French'))

#bot.delete_webhook()


if __name__ == '__main__':
     bot.polling(none_stop=True)


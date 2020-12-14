import telebot
import xlrd

from random import randint

rb = xlrd.open_workbook('../inputs/Savedtranslations.xlsx')
sheet = rb.sheet_by_index(0)
mysheet = []
for i in range(sheet.nrows):
    mysheet.append([sheet.cell_value(i, 0), sheet.cell_value(i, 1), sheet.cell_value(i, 2), sheet.cell_value(i, 3)])
n = len(mysheet)

def checklan():
    lan = set()
    for i in range(n):
       lan.add(str(mysheet[i][0]) + " ---- " + str(mysheet[i][1]))
    return lan

def randtwo(ls, sr):
    rm = randint(0, n)
    print(rm)
    while (True):
        if(ls == mysheet[rm][0] and sr == mysheet[rm][1]):
            break
        else:
            rm = randint(0, n)
    return mysheet[rm][0] + ' ----- ' + mysheet[rm][1] + '\n' + mysheet[rm][2] + ' ----- ' + mysheet[rm][3]


TOKEN = "1001230120:AAHB5gaj02BOsMTENcNDBGJFgKOzNYm4L70"
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=["start"])
def handle_start(message):
    user_markup =telebot.types.ReplyKeyboardMarkup()
    for i in checklan():
        user_markup.row(f'{i}')
    bot.send_message(message.chat.id,'Tandanyz!!!',reply_markup=user_markup)
@bot.message_handler(content_types=['text'])
def main(message):
    checklan = str(message.text)
    lans = checklan.split(' ---- ')
    bot.send_message(message.chat.id, randtwo(lans[0], lans[1]))

if __name__ == '__main__':
     bot.polling(none_stop=True)
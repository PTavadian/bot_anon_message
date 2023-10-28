from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


def get_kb_list_group(lst, text=''):
    '''Возвращает клавиатуру из списка групп'''
    lst.sort()

    b2 = KeyboardButton('/cancel') 
    b3 = KeyboardButton('/help') 

    kb_message_4 = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder=text)
    kb_message_4.row(b3, b2)
    for i, n in enumerate(lst):
        if i == 0:
            kb_message_4.add(KeyboardButton(n))
        else:
            kb_message_4.insert(KeyboardButton(n))

    return kb_message_4



def check_kb(text=''):
    ''''''
    b1 = KeyboardButton('/cancel')
    b2 = KeyboardButton('отправить') 

    kb_message = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder=text)
    kb_message.row(b1, b2)

    return kb_message



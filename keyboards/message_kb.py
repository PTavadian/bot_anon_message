from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

global b2, b3

b1 = KeyboardButton('/delete') 
b2 = KeyboardButton('/cancel') 
b3 = KeyboardButton('/help') 

kb_message = ReplyKeyboardMarkup(resize_keyboard=True) 
kb_message.row(b3, b2)

kb_message_2 = ReplyKeyboardMarkup(resize_keyboard=True) 
kb_message_2.row(b1, b2)



def get_kb(text):
    '''Возвращает клавиатуру с текстом в поле ввода'''
    b1 = KeyboardButton('/check') 

    kb_message_3 = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder=text)
    kb_message_3.row(b3, b1)

    return kb_message_3



def get_kb_list_group(lst, text):
    '''Возвращает клавиатуру из списка групп'''
    lst.sort()

    kb_message_4 = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder=text)
    kb_message_4.row(b3, b2)
    for i, n in enumerate(lst):
        if i == 0:
            kb_message_4.add(KeyboardButton(n))
        else:
            kb_message_4.insert(KeyboardButton(n))

    return kb_message_4










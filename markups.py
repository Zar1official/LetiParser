from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import json
# Выбор формы обучения
main_menu  = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Очная')).add(KeyboardButton('Очно-заочная')).add(KeyboardButton('Заочная'))

# Очная, менюшка с выбором специальности
och_menu = InlineKeyboardMarkup(resize_keyboard=True)
with open('specialities/leti_och.json', 'r') as f:
    data=json.loads(f.read())
counter=0
for k,v in data.items():
    och_menu.row(InlineKeyboardButton(text=k, callback_data=f"o_menu_{counter}"))
    counter+=1
och_menu.add(InlineKeyboardButton('<<', callback_data="o_back_1"))


# Очная выбор финансирования
och_finances=[]
counter=0
for k,v in data.items():
    och_finances.append(InlineKeyboardMarkup().row(InlineKeyboardButton("Бюджет", callback_data=f'o_f_b{counter}'),
                                                   InlineKeyboardButton("Контракт", callback_data=f'o_f_k{counter}')).add(
                                                   InlineKeyboardButton('<<', callback_data="o_back_2")))
    counter+=1

# Очно-заочная, менюшка с выбором специальности
och_zaoch_menu = InlineKeyboardMarkup(resize_keyboard=True)
with open('specialities/leti_och_zaoch.json', 'r') as f:
    data=json.loads(f.read())
counter=0
for k,v in data.items():
    och_zaoch_menu.row(InlineKeyboardButton(text=k, callback_data=f"o_zao_menu_{counter}"))
    counter+=1
och_zaoch_menu.add(InlineKeyboardButton('<<', callback_data="o_zao_back_1"))

# Очно-заочная, выбор формы финансирования
och_zaoch_finances=[]
counter=0
for k,v in data.items():
    och_zaoch_finances.append(InlineKeyboardMarkup().row(InlineKeyboardButton("Бюджет", callback_data=f'o_zao_f_b_{counter}'),
                                                   InlineKeyboardButton("Контракт", callback_data=f'o_zao_f_k_{counter}')).add(
                                                   InlineKeyboardButton('<<', callback_data="o_zao_back_2")))
    counter+=1

# Заочная, менюшка с выбором специальности
zaoch_menu = InlineKeyboardMarkup(resize_keyboard=True)
with open('specialities/leti_zaoch.json', 'r') as f:
    data=json.loads(f.read())
counter=0
for k,v in data.items():
    zaoch_menu.row(InlineKeyboardButton(text=k, callback_data=f"zao_menu_{counter}"))
    counter+=1
zaoch_menu.add(InlineKeyboardButton('<<', callback_data="zao_back_1"))

# Заочная, выбор формы финансирования
zaoch_finances=[]
counter=0
for k,v in data.items():
    zaoch_finances.append(InlineKeyboardMarkup().add(
                                                   InlineKeyboardButton("Контракт", callback_data=f'zao_f_k_{counter}')).add(
                                                   InlineKeyboardButton('<<', callback_data="zao_back_2")))
    counter+=1
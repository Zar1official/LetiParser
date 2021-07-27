from setup import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram import types, executor
import markups as kb
import re
import json
import parse
from states import States


@dp.message_handler(commands=['start'], state=None)
async def start_message(message: types.Message):
    await message.answer("Задайте снилс в такой форме: ААА-ААА-ААА ББ, где А и Б - цифры")
    await States.setSnils.set()

@dp.message_handler(state = States.setSnils)
async def set_snils_message(message: types.Message, state: FSMContext):
    snils=message.text
    await state.update_data(snils= snils)
    await message.answer("Снилс успешно установлен, выберите форму обучения", reply_markup=kb.main_menu)
    await States.next()

@dp.message_handler(commands=['change'], state=States.botInWork)
async def change_snils_message(message: types.Message, state:FSMContext):
    await message.answer("Задайте снилс в такой форме ААА-ААА-ААА ББ, где А и Б - цифры")
    await States.setSnils.set()

@dp.message_handler(state = States.botInWork)
async def o_message(message: types.Message, state: FSMContext):
    reply  = "Выберите направление подготовки"
    if message.text == "Очная":
        await message.answer(reply,
                               reply_markup=kb.och_menu)
    elif message.text=="Очно-заочная":
        await message.answer(reply,
                               reply_markup=kb.och_zaoch_menu)
    elif message.text=="Заочная":
        await message.answer(reply,
                               reply_markup=kb.zaoch_menu)
    else:
        await message.answer("Неизвестная команда")



'''ОЧНАЯ'''

@dp.callback_query_handler(lambda c: c.data.startswith('o_menu_'), state = States.botInWork)
async def callback_och(callback_query: types.CallbackQuery, state: FSMContext):
    n = int(re.sub("[^0-9]", "", callback_query.data))
    await bot.edit_message_text(message_id=callback_query.message.message_id, text="Выберите источник финансирования",
                                chat_id=callback_query.message.chat.id, reply_markup=kb.och_finances[n])
    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data.startswith("o_f_"), state = States.botInWork)
async def callback_och_fin(callback_query: types.CallbackQuery, state: FSMContext):
    SpecialityIndex = int(re.sub("[^0-9]", "", callback_query.data))
    state_data = await state.get_data()
    snils = state_data['snils']

    with open('specialities/leti_och.json', 'r') as f:
        data=json.loads(f.read())

    if callback_query.data.__contains__('o_f_b'):
        place = parse.get_place(user_snils=snils, data=data,
                                n=SpecialityIndex, type="Бюджет")
    else:
        place= parse.get_place(user_snils=snils, data=data,
                               n=SpecialityIndex, type= "Контракт")

    if place == None:
        await bot.send_message(callback_query.from_user.id,
                               'Вас нет в списке по заданным критериям')
    else:
        await bot.send_message(callback_query.from_user.id,
                               f'Ваше место - {place}')

    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data.endswith("back_1"), state=States.botInWork)
async def back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(message_id=callback_query.message.message_id, chat_id=callback_query.message.chat.id)
    await bot.send_message(callback_query.from_user.id, "Выберите форму обучения",
                           reply_markup=kb.main_menu)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data=="o_back_2", state=States.botInWork)
async def o_f_back(callback_query: types.CallbackQuery, state:FSMContext):
    await bot.delete_message(message_id=callback_query.message.message_id,
                             chat_id=callback_query.message.chat.id)
    await bot.send_message(callback_query.from_user.id, "Выберите направление подготовки",
                           reply_markup=kb.och_menu)
    await callback_query.answer()


'''ОЧНО-ЗАОЧНАЯ'''

@dp.callback_query_handler(lambda c: c.data.startswith('o_zao_menu'), state=States.botInWork)
async def callback_och_zao(callback_query: types.CallbackQuery, state: FSMContext):
    n = int(re.sub("[^0-9]", "", callback_query.data))
    await bot.edit_message_text(message_id=callback_query.message.message_id, text="Выберите источник финансирования",
                                chat_id=callback_query.message.chat.id, reply_markup=kb.och_zaoch_finances[n])
    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data.startswith("o_zao_f_"), state=States.botInWork)
async def callback_och_zao_fin(callback_query: types.CallbackQuery, state:FSMContext):
    SpecialityIndex = int(re.sub("[^0-9]", "", callback_query.data))
    state_data= await state.get_data()
    snils= state_data['snils']

    with open('specialities/leti_och_zaoch.json', 'r') as f:
        data=json.loads(f.read())

    if callback_query.data.__contains__('o_zao_f_b_'):
        place = parse.get_place(user_snils=snils, data=data,
                                n=SpecialityIndex, type="Бюджет")
    else:
        place= parse.get_place(user_snils=snils, data=data,
                               n=SpecialityIndex, type= "Контракт")

    if place == None:
        await bot.send_message(callback_query.from_user.id,
                               'Вас нет в списке по заданным критериям')
    else:
        await bot.send_message(callback_query.from_user.id,
                               f'Ваше место - {place}')

    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data=="o_zao_back_2", state=States.botInWork)
async def o_zao_f_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(message_id=callback_query.message.message_id,
                             chat_id=callback_query.message.chat.id)
    await bot.send_message(callback_query.from_user.id, "Выберите направление подготовки",
                           reply_markup=kb.och_menu)

    await callback_query.answer()


'''ЗАОЧНАЯ'''

@dp.callback_query_handler(lambda c: c.data.startswith('zao_menu'), state=States.botInWork)
async def callback_zao(callback_query: types.CallbackQuery, state: FSMContext):
    n = int(re.sub("[^0-9]", "", callback_query.data))
    await bot.edit_message_text(message_id=callback_query.message.message_id, text="Выберите источник финансирования",
                                chat_id=callback_query.message.chat.id, reply_markup=kb.zaoch_finances[n])
    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data.startswith("zao_f_"), state= States.botInWork)
async def callback_zao_fin(callback_query: types.CallbackQuery, state: FSMContext):
    SpecialityIndex = int(re.sub("[^0-9]", "", callback_query.data))
    state_data = await state.get_data()
    snils = state_data['snils']

    with open('specialities/leti_zaoch.json', 'r') as f:
        data=json.loads(f.read())

    place= parse.get_place(user_snils=snils, data=data,
                            n=SpecialityIndex, type= "Контракт")

    if place == None:
        await bot.send_message(callback_query.from_user.id,
                               'Вас нет в списке по заданным критериям')
    else:
        await bot.send_message(callback_query.from_user.id,
                               f'Ваше место - {place}')

    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data=="zao_back_2", state= States.botInWork)
async def zao_f_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(message_id=callback_query.message.message_id,
                             chat_id=callback_query.message.chat.id)
    await bot.send_message(callback_query.from_user.id, "Выберите направление подготовки",
                           reply_markup=kb.och_menu)

    await callback_query.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)







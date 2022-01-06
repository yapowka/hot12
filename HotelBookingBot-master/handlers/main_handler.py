from aiogram import types

from bot import dp
from states import MainForm, main_menu
from keyboards import main_menu_keyboard


@dp.message_handler(state='*', commands='start')
async def cmd_start(message: types.Message):
    await message.answer('Hello, welcome to the our Hotel bot!')
    await MainForm.menu.set()
    await message.answer('Choose further action',
                         reply_markup=main_menu_keyboard)


@dp.message_handler(lambda message: message.text == 'Main menu', state=main_menu,
                    content_types=types.ContentTypes.TEXT)
async def process_menu(message: types.Message):
    await MainForm.menu.set()
    await message.answer('Choose a room or check out our lounge area',
                         reply_markup=main_menu_keyboard)


@dp.message_handler(state='*', commands='help')
async def cmd_help(message: types.Message):
    await message.answer('To return to the main menu press: /start\n'
                         'Date format: "DD.MM.YYYY" without quotes\n'
                         'In the "feedback" section you can write a feedback  \n'
                         'For all remaining questions, call the number: +998937777777')

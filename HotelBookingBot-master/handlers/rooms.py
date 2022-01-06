import re
import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from database import queries
from bot import dp, bot
from states import MainForm, RoomsForm, main_menu
from keyboards import keyboard_with_back_button, back_button, \
    type_of_rooms_keyboard, type_of_rooms_buttons, \
    book_room_keyboard, \
    accept_data_keyboard, accept_data_button, change_data_button, \
    back_to_main_menu_keyboard, \
    back_to_choosing_room_button, \
    book_room_button, \
    change_parameters_button


def is_date(date):
    return re.match(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$', date)


def is_phone_humber(number):
    return re.match(r'^\+?\d+$', number)


@dp.message_handler(lambda message: message.text in book_room_button + change_data_button + change_parameters_button,
                    state=[MainForm.menu, RoomsForm.accepting_data1, RoomsForm.choosing_specific_room,
                           RoomsForm.choosing_type_of_room],
                    content_types=types.ContentTypes.TEXT)
async def choose_arrival_date(message: types.Message):
    await RoomsForm.getting_arrival_date.set()
    await message.answer(
        'Enter your check-in date in the following format: "YYYY-MM-DD" without quotes,example: "2022-01-03"',
        reply_markup=types.ReplyKeyboardRemove())


def is_valid_date(date):
    return datetime.date.today() <= datetime.datetime.strptime(date, '%Y-%m-%d').date()


@dp.message_handler(lambda message: is_date(message.text),
                    state=RoomsForm.getting_arrival_date,
                    content_types=types.ContentTypes.TEXT)
async def choose_date_of_departure(message: types.Message, state: FSMContext):
    if not is_valid_date(message.text):
        await message.reply('Incorrect date, entered date is less than current')
        return

    await RoomsForm.getting_departure_date.set()
    await state.update_data(arrival_date=message.text)
    await message.answer('Enter your departure date in the following format: "YYYY-MM-DD" without quotes, example: "2022-01-03"')


@dp.message_handler(lambda message: not is_date(message.text),
                    state=[RoomsForm.getting_arrival_date, RoomsForm.getting_departure_date])
async def choose_date_invalid(message: types.Message):
    await message.reply('Incorrect date format entered')


def is_valid_staying_date(arrival_date, departure_date):
    return datetime.datetime.strptime(arrival_date, '%Y-%m-%d').date() < \
           datetime.datetime.strptime(departure_date, '%Y-%m-%d').date()


@dp.message_handler(lambda message: is_date(message.text),
                    state=RoomsForm.getting_departure_date,
                    content_types=types.ContentTypes.TEXT)
async def choose_count_of_humans(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if not is_valid_staying_date(user_data['arrival_date'], message.text):
        await message.reply('Incorrect date, check-in date is more than check-out date')
        return

    await RoomsForm.counting_humans.set()
    await state.update_data(departure_date=message.text)
    await message.answer('Enter the number of people')


@dp.message_handler(lambda message: message.text.isdigit(),
                    state=RoomsForm.counting_humans,
                    content_types=types.ContentTypes.TEXT)
async def accept_data(message: types.Message, state: FSMContext):
    await RoomsForm.accepting_data1.set()
    await state.update_data(humans_count=message.text)

    user_data = await state.get_data()
    await message.answer(f'Entered data\n'
                         f'arrival date: {user_data["arrival_date"]}\n'
                         f'departure date: {user_data["departure_date"]}\n'
                         f'number of persons: {user_data["humans_count"]}\n'
                         f'confirm the entered data or change them',
                         reply_markup=accept_data_keyboard)


@dp.message_handler(lambda message: message.text in back_button + accept_data_button + back_to_choosing_room_button,
                    state=[RoomsForm.accepting_data1, RoomsForm.choosing_specific_room,
                           RoomsForm.booking_specific_room],
                    content_types=types.ContentTypes.TEXT)
async def choose_type_of_room(message: types.Message):
    await RoomsForm.choosing_type_of_room.set()
    await message.answer('Select room type', reply_markup=type_of_rooms_keyboard)


@dp.message_handler(lambda message: message.text in type_of_rooms_buttons,
                    state=RoomsForm.choosing_type_of_room,
                    content_types=types.ContentTypes.TEXT)
async def choose_specific_room(message: types.Message, state: FSMContext):
    await RoomsForm.choosing_specific_room.set()

    await state.update_data(room_type=message.text)

    user_data = await state.get_data()
    room_type = user_data['room_type']
    count = user_data['humans_count']
    arrival_date = user_data['arrival_date']
    departure_date = user_data['departure_date']

    rooms = queries.unload_vacant_rooms(room_type, count, arrival_date, departure_date)

    rooms_numbers = [room[0] for room in rooms]
    await state.update_data(rooms_numbers=rooms_numbers)

    if not rooms:
        await message.answer('Sorry, there are no matching rooms', reply_markup=keyboard_with_back_button)
    else:
        answer = ''
        for room in rooms:
            answer += f'{room[0]}, price: {room[1]}, number of beds: {room[2]}\n'
        await message.answer(answer)
        await message.answer('Select room number', reply_markup=keyboard_with_back_button)


def room_number_filter(number, numbers):
    return number in numbers


@dp.message_handler(lambda message: message.text.isdigit(),
                    state=RoomsForm.choosing_specific_room,
                    content_types=types.ContentTypes.TEXT)
async def book_room(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if not room_number_filter(int(message.text), user_data['rooms_numbers']):
        await message.reply('wrong room number, try again')
        return

    await RoomsForm.booking_specific_room.set()
    await state.update_data(booked_room=message.text)

    user_data = await state.get_data()
    room_number = user_data['booked_room']
    description = queries.unload_description(room_number)

    room_type = user_data['room_type']

    rooms = {'President': 'prezident', 'Lux': 'lux', 'Standart': 'standart'}
    img = open(f'images/rooms/{rooms[room_type]}/photo.jpg', 'rb')

    await message.answer(description)
    await bot.send_photo(message.chat.id, img)
    await message.answer('You can book a room or go back to the list of rooms',
                         reply_markup=book_room_keyboard)


@dp.message_handler(lambda message: message.text in book_room_button + change_data_button,
                    state=[RoomsForm.booking_specific_room, RoomsForm.accepting_data2],
                    content_types=types.ContentTypes.TEXT)
async def get_name(message: types.Message):
    await RoomsForm.getting_name.set()
    await message.answer('Enter your name',
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=RoomsForm.getting_name,
                    content_types=types.ContentTypes.TEXT)
async def get_phone_number(message: types.Message, state: FSMContext):
    await RoomsForm.getting_phone_number.set()
    await state.update_data(name=message.text)
    await message.answer(
        'Enter the mobile number by which the operator can contact you and confirm the booking')


@dp.message_handler(lambda message: not is_phone_humber(message.text),
                    state=RoomsForm.getting_phone_number,
                    content_types=types.ContentTypes.TEXT)
async def get_phone_number_invalid(message: types.Message):
    await message.reply('incorrect phone number format')


@dp.message_handler(lambda message: is_phone_humber(message.text),
                    state=RoomsForm.getting_phone_number,
                    content_types=types.ContentTypes.TEXT)
async def accept_data(message: types.Message, state: FSMContext):
    await RoomsForm.accepting_data2.set()
    await state.update_data(phone_number=message.text)

    user_data = await state.get_data()
    await message.answer(f'entered data\n'
                         f'name: {user_data["name"]}\n'
                         f'telephone number: {user_data["phone_number"]}\n'
                         f'confirm the entered data or change them',
                         reply_markup=accept_data_keyboard)


@dp.message_handler(lambda message: message.text in accept_data_button,
                    state=RoomsForm.accepting_data2,
                    content_types=types.ContentTypes.TEXT)
async def back_to_main_menu(message: types.Message, state: FSMContext):
    await main_menu[0].set()

    user_data = await state.get_data()
    room_number = user_data['booked_room']
    arrival_date = user_data['arrival_date']
    departure_date = user_data['departure_date']
    name = user_data['name']
    phone = user_data['phone_number']
    count = user_data['humans_count']

    queries.upload_reserve(room_number, arrival_date, departure_date, name, phone, count)

    await message.answer('The number is reserved, now our agent will contact you\n'
                         'While you can go to the main menu',
                         reply_markup=back_to_main_menu_keyboard)

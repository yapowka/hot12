from aiogram import types


def add_buttons_to_keyboard(keyboard, buttons):
    for button in buttons:
        keyboard.add(button)


# ОБЩИЕ КНОПКИ
back_to_main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_to_main_menu_button = ['Main menu']
add_buttons_to_keyboard(back_to_main_menu_keyboard, back_to_main_menu_button)

keyboard_with_back_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_button = ['Back']
add_buttons_to_keyboard(keyboard_with_back_button, back_button)

change_parameters_button = ['Change check-in parameters']

# КЛАВИАТУРЫ ГЛАВНОГО МЕНЮ
main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
book_room_button = ['Book a room']
services_button = ['Check out the recreation area']
feedback_button = ['Feedback']
menu_buttons = book_room_button + services_button + feedback_button
add_buttons_to_keyboard(main_menu_keyboard, menu_buttons)

# КЛАВИАТУРЫ БРОНИРОВАНИЯ НОМЕРА
type_of_rooms_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
type_of_rooms_buttons = ['President', 'Lux', 'Standart']
add_buttons_to_keyboard(type_of_rooms_keyboard, type_of_rooms_buttons + change_parameters_button)

book_room_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_to_choosing_room_button = ['Back to room selection']
book_room_buttons = book_room_button + back_to_choosing_room_button
add_buttons_to_keyboard(book_room_keyboard, book_room_buttons)

accept_data_button = ['Confirm data']
change_data_button = ['Change the data']
accept_data_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
add_buttons_to_keyboard(accept_data_keyboard, accept_data_button + change_data_button)

# КНОПКИ ДЛЯ ФИДБЕКА
button1 = types.KeyboardButton('1')
button2 = types.KeyboardButton('2')
button3 = types.KeyboardButton('3')
button4 = types.KeyboardButton('4')
button5 = types.KeyboardButton('5')

estimations_keyboard = types.ReplyKeyboardMarkup().row(
    button1, button2, button3, button4, button5
).add('Main menu')

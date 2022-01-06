from aiogram import types

from bot import dp, bot
from states import MainForm, ServicesForm
from keyboards import back_to_main_menu_keyboard, keyboard_with_back_button, services_button, back_button

services = [('Gym',
             """Here are various models of sports equipment: all cardio (elliptical, stepper, treadmills, exercise bikes). There are all the necessary simulators for all muscle groups, as well as free weights (pancakes, dumbbells, barbells). \n \nWorking hours: from 7.00 to 23.00 daily.""",
             'images/services/gym.jpg'),
            ('Swimming pool',
             """Over the millennia that people have been using saunas and water treatments, they have begun to play a very significant role in their lives. Sauna and swimming pool are places where you can relieve fatigue, relax and gain new strength. Pleasant warmth, an opportunity conducive to complete relaxation, an amazing sensation of cleanliness and excellent well-being can only be provided by a sauna. Swimming in our small but comfortable pool will help you feel pleasant freshness and lightness. Pool: length - 20m, width - 4m, depth - 170 cm. \n\nOpening hours: from 7.00 to 23.00 daily.""",
             'images/services/swim_pool.jpg'),
            ('Billiards',
             """If you want to spend a pleasant evening and relax in the company of your friends, we invite you to the entertainment center of the AMAKS Safar hotel. At your service there is a billiard area on the ground floor. An exciting and sophisticated game appreciated by millions of people around the world will help you relax and enjoy a pleasant evening in the company of your friends. \n\nWorking mode: around the clock""",
             'images/services/pool.jpg'),
            ('Bar',
             """The warm atmosphere of the Piano Bar is an ideal place for holding a business meeting over a cup of aromatic coffee or to end a working day with a glass of exquisite cognac. Soft comfortable sofas will help you relax and fully experience the atmosphere of coziness and ease. The bar's menu also includes many types of tea, coffee, hot chocolate, soft and alcoholic drinks. Every evening, in the muted light of magic lanterns, live piano music performed by a virtuoso pianist sounds for you! \n\nThe bar is open for you every day and around the clock.""",
             'images/services/bar.jpg'),
            ('A restaurant',
             """The restaurant has 100 seats, a separate hall for 25 people is provided for VIP guests. The menu includes such dishes as beef steak with sauce, lamb on the bone, Norwegian salmon fillets, northern trout, tiger prawns and Fedor Ivanovich Chaliapin's favorite dishes. The Capella restaurant is a great place for a romantic dinner, banquets, weddings and business meetings with partners. \n\nHours: from 7.00 to 23.00, daily""",
             'images/services/restaurant.jpg')]


@dp.message_handler(lambda message: message.text in services_button + back_button,
                    state=[MainForm.menu, ServicesForm.checking_service],
                    content_types=types.ContentTypes.TEXT)
async def choose_service(message: types.Message):
    await ServicesForm.menu.set()

    services_titles = [f'{i}. {value[0]}\n' for i, value in enumerate(services, 1)]
    titles = ''.join(services_titles)
    await message.answer(f'Enter the ordinal number of the entertainment you want to learn more about, for example "1"\n'
                         f'{titles}', reply_markup=back_to_main_menu_keyboard)


def filter_service_number(message: types.Message):
    if message.text.isdigit():
        if 1 <= int(message.text) <= len(services):
            return True
    return False


@dp.message_handler(lambda message: not filter_service_number(message), state=ServicesForm.menu)
async def choose_service_invalid(message: types.Message):
    await message.reply('you entered a number that does not exist, try again')


@dp.message_handler(filter_service_number, state=ServicesForm.menu)
async def show_service(message: types.Message):
    await ServicesForm.checking_service.set()

    service_number = message.text
    service = services[int(service_number) - 1]

    await message.answer(service[1])
    await bot.send_photo(message.chat.id, open(service[2], 'rb'))
    await message.answer('please read the opening hours carefully, thank you!',
                         reply_markup=keyboard_with_back_button)

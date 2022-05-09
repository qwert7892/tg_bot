import random

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database import Db
from sigh import get_text
import config

TOKEN = config.TOCKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Db('database.db')


class Profile(StatesGroup):
    name = State()
    description = State()
    age = State()
    sign = State()
    city = State()
    photo = State()
    sex = State()


a_lot_symbols = ['Вы слишком много написали',
                 'Слишком много информации',
                 'Слишком много, напишите поменьше'
                 ]

underage = ['Слишком низкий возраст',
            'Возраст ниже приемлегого',
            'Возраст не проходит нижний порого',
            'К использованию бота допускаются только лица старше этого возраста'
           ]

unright_signs = ['Такого знака зодиака не существует',
                 'Неверный знак зодиака',
                 'Введите правильный знак зодиака',
                 'Знак зодиака введён некорректно'
                ]

look = ['Фото готово к использованию',
        'Фото загружено',
        'Бот получил ваше фото',
        'Бот добавил ваше фото в анкету'
       ]

# начало
@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    btn_start = KeyboardButton('Зайти в волшебный мир')
    bot_start = ReplyKeyboardMarkup(one_time_keyboard=True)
    bot_start.add(btn_start)
    await message.answer(
        'добро пожаловать', reply_markup=bot_start)
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.username, message.from_user.id, message.from_user.full_name, message.chat.id)


# для того чтоб меню вылазило
@dp.message_handler(
    lambda message: message.text == 'Зайти в волшебный мир' or message.text == '/bot_start',
    state='*')
async def bot_start(message: types.Message):
    btn_search = KeyboardButton('Смотреть анкеты')
    btn_create_profile = KeyboardButton('Создать анкету')
    btn_edit_profile = KeyboardButton('Посмотреть свой профиль')
    btn_remove_profile = KeyboardButton('Удалить анкету')
    menu = ReplyKeyboardMarkup()
    menu.add(btn_search, btn_create_profile, btn_edit_profile, btn_remove_profile)
    await message.answer('welcome', reply_markup=menu)


# создаем анкету
@dp.message_handler(lambda message: message.text == 'Создать анкету', state='*')
async def make_profile(message: types.Message):
    btn_exit = KeyboardButton('Выйти')
    menu_exit_btn = ReplyKeyboardMarkup()
    menu_exit_btn.add(btn_exit)
    if not db.profile_exists(message.from_user.id):
        if message.from_user.username is not None:
            await message.answer("Введите ваше имя", reply_markup=menu_exit_btn)
            await Profile.name.set()
    elif db.profile_exists(message.from_user.id):
        await message.answer('У тебя уже есть анкета')


@dp.message_handler(lambda message: message.text == 'Посмотреть свой профиль')
async def show_profile(message: types.Message):
    if not db.profile_exists(message.from_user.id):
        await message.answer('У тебя нет анкеты, заполни её а потом приходи сюда!')
    else:
        self_profile_name = (db.get_info(str(message.from_user.id)))[0][8]
        self_profile_age = (db.get_info(str(message.from_user.id)))[0][6]
        self_profile_desc = (db.get_info(str(message.from_user.id)))[0][2]
        self_profile_sign = (db.get_info(str(message.from_user.id)))[0][7]
        self_photo_profile = open(f'photo_user/{str(message.from_user.id)}.jpg', 'rb')
        text = f'пали, {self_profile_name}, {self_profile_age}, {self_profile_sign}\n\n {self_profile_desc}'
        await message.answer_photo(self_photo_profile, caption=text)


# обработаем имя
@dp.message_handler(state=Profile.name)
async def insert_name(message: types.Message, state: FSMContext):
    if str(message.text) == 'Выйти':
        await state.finish()
        await bot_start(message)
        return
    else:
        await state.update_data(profile_name=message.text.lower())
        await message.reply(f'{message.text.title()} вечер в хату')
        await message.answer("Теперь расскажи о себе")
        await Profile.next()
        return


# инфо о челе
@dp.message_handler(state=Profile.description)
async def insert_info(message: types.Message, state: FSMContext):
    if str(message.text) == 'Выйти':
        await state.finish()
        await bot_start(message)
        return
    elif len(message.text) < 100:
        await state.update_data(profile_description=message.text)
        await message.answer("Укажи свой возраст")
        await Profile.next()
    else:
        await message.answer(random.choice(a_lot_symbols))
        return


# возраст с проверкой на малолеток
@dp.message_handler(state=Profile.age)
async def insert_age(message: types.Message, state: FSMContext):
    if str(message.text) == 'Выйти':
        await state.finish()
        await bot_start(message)
        return
    if int(message.text) < 13:
        await message.answer(random.choice(underage))
        return
    elif int(message.text) >= 14:
        await state.update_data(profile_age=message.text)
        await message.answer('Введите свой знак зодиака')
        await Profile.next()


@dp.message_handler(state=Profile.sign)
async def insert_sign(message: types.Message, state: FSMContext):
    dictionary = {
        'овен': 'oven',
        'весы': 'vesy',
        'козерог': 'kozerog',
        'рыбы': 'ryby',
        'дева': 'deva',
        'близнецы': 'bliznecy',
        'стрелец': 'strelec',
        'скорпион': 'skorpion',
        'водолей': 'vodolej',
        'лев': 'lev',
        'рак': 'rak',
        'телец': 'telec'
    }
    if str(message.text) == 'Выйти':
        await state.finish()
        await bot_start(message)
        return
    if str(message.text).lower() not in dictionary:
        await message.reply(random.choice(unright_signs))
    else:
        await state.update_data(profile_sign=message.text)
        await message.answer('Введите город')
        await Profile.next()


@dp.message_handler(state=Profile.city)
async def insert_city(message: types.Message, state: FSMContext):
    if str(message.text) == 'Выйти':
        await state.finish()
        await bot_start(message)
        return
    if len(message.text) > 50:
        await message.answer(random.choice(a_lot_symbols))
        return
    else:
        await state.update_data(profile_city=message.text.lower())
        await message.answer('Теперь пришли свое фото')

        await Profile.next()


@dp.message_handler(state=Profile.photo, content_types=['photo'])
async def insert_photo(message: types.Message, state: FSMContext):
    if str(message.text) == 'Выйти':
        await state.finish()
        await bot_start(message)

    man_btn = KeyboardButton("М")
    woman_btn = KeyboardButton('Ж')
    t_btn = KeyboardButton('Трансформер')
    l_btn = KeyboardButton('Ламинат')
    sex_keybord = ReplyKeyboardMarkup(one_time_keyboard=True)
    sex_keybord.add(man_btn, woman_btn, t_btn, l_btn)

    await message.photo[-1].download('photo_user/' + str(message.from_user.id) + '.jpg')
    await message.answer(random.choice(look))
    await message.answer('укажи свой пол', reply_markup=sex_keybord)
    await Profile.next()


@dp.message_handler(state=Profile.sex)
async def insert_sex(message: types.Message, state: FSMContext):
    if str(message.text) == 'Выйти':
        await state.finish()
        await bot_start(message)
    if message.text == 'М' or message.text == 'Ж' or message.text == 'Ламинат' or message.text == 'Трансформер':
        await state.update_data(profile_sex=message.text)
        await message.answer('Анкета успешно создана!')
        user_data = await state.get_data()
        db.create_profile(message.from_user.id, message.from_user.username, str(user_data['profile_name']),
                          str(user_data['profile_description']), user_data['profile_age'], user_data['profile_sign'],
                          str(user_data['profile_city']), 'photo/' + str(message.from_user.id) + '.jpg',
                          str(user_data['profile_sex']))
        await state.finish()
        await bot_start(message)


class SP(StatesGroup):
    city_search = State()
    searching = State()


@dp.message_handler(lambda message: message.text == 'Смотреть анкеты')
async def search_profile(message: types.Message):
    try:
        if not db.profile_exists(message.from_user.id):
            await message.answer('У тебя нет анкеты, заполни её а потом приходи сюда!')
        else:
            await message.answer('Выбери город для поиска человечка :)')
            await SP.city_search.set()
    except Exception as e:
        await state.finish()
        print(e)
        return


@dp.message_handler(state=SP.city_search)
async def seach_profile_step2(message: types.Message, state: FSMContext):
    await state.update_data(search_profile_city=message.text.lower())
    user_data = await state.get_data()
    db.set_city_search(str(user_data['search_profile_city']), str(message.from_user.id))
    profile_id = db.search_profile(user_data['search_profile_city'])
    need_profile = str(random.choice(profile_id))[1:-2]
    while need_profile == str(message.from_user.id):
        need_profile = str(random.choice(profile_id))[1:-2]
    profile_need = db.get_info(need_profile)
    # await message.answer(db.get_info(need_profile))
    await state.update_data(last_profile_id=profile_id)

    profile_name = profile_need[0][8]
    profile_age = profile_need[0][6]
    profile_desc = profile_need[0][2]
    profile_sign = profile_need[0][7]
    self_profile_sign = (db.get_info(str(message.from_user.id)))[0][7]
    profile_match = get_text(profile_sign, self_profile_sign)

    # кнопки для оценки
    button_like = KeyboardButton('👍')

    button_dislike = KeyboardButton('👎')

    mark_menu = ReplyKeyboardMarkup()

    mark_menu.add(button_dislike, button_like)

    photo_profile = open(f'photo_user/{str(need_profile)}.jpg', 'rb')

    text_reply = f'смотри, {profile_name}, {profile_age} ' \
                 f'\n\n {profile_desc} \n\n {profile_match}'

    await message.answer(text_reply)
    await message.answer_photo(photo_profile, reply_markup=mark_menu)
    await SP.next()


@dp.message_handler(state=SP.searching)
async def seach_profile_step3(message: types.Message, state: FSMContext):
    if str(message.text) == '👍':
        user_data = await state.get_data()
        profile_id = db.search_profile(user_data['search_profile_city'])
        await state.update_data(last_profile_id=profile_id)
        if not db.add_like_exists(str(message.from_user.id), str(user_data['last_profile_id'])):
            db.add_like(str(message.from_user.id), str(user_data['last_profile_id']))
        person = str(random.choice(profile_id))[1:-2]

        need_profile = str(random.choice(profile_id))[1:-2]
        while need_profile == str(message.from_user.id):
            need_profile = str(random.choice(profile_id))[1:-2]
        profile_need = db.get_info(need_profile)
        profile_name = profile_need[0][8]
        profile_age = profile_need[0][6]
        profile_desc = profile_need[0][2]
        profile_sign = profile_need[0][7]
        self_profile_sign = (db.get_info(str(message.from_user.id)))[0][7]
        profile_match = get_text(profile_sign, self_profile_sign)
        photo_profile = open(f'photo_user/{str(need_profile)}.jpg', 'rb')
        text_reply = f'смотри, {profile_name}, {profile_age} ' \
                     f'\n\n {profile_desc}\n\n {profile_match}'
        await message.answer(text_reply)
        await message.answer_photo(photo_profile)

        self_profile_name = (db.get_info(str(message.from_user.id)))[0][8]
        self_profile_age = (db.get_info(str(message.from_user.id)))[0][6]
        self_profile_desc = (db.get_info(str(message.from_user.id)))[0][2]
        self_profile_sign = (db.get_info(str(message.from_user.id)))[0][7]
        self_photo_profile = open(f'photo_user/{str(message.from_user.id)}.jpg', 'rb')

        await state.update_data(last_profile_id=profile_id)
        texts = f'смотри, {self_profile_name}, {self_profile_age} \n {self_profile_desc}'
        await bot.send_message(chat_id=(int(need_profile)),
                               text=f'пали, {self_profile_name}, {self_profile_age} {self_profile_sign}' \
                                    f'\n\n {self_profile_desc}' \
                                    f'\n\n {profile_match} @{str(message.from_user.username)}')
        await state.finish()
    if str(message.text) == '👎':
        user_data = await state.get_data()
        profile_id = db.search_profile(user_data['search_profile_city'])
        need_profile = str(random.choice(profile_id))[1:-2]
        while need_profile == str(message.from_user.id):
            need_profile = str(random.choice(profile_id))[1:-2]
        profile_need = db.get_info(need_profile)
        profile_name = profile_need[0][7]
        profile_age = profile_need[0][6]
        profile_desc = profile_need[0][2]
        profile_sign = profile_need[0][7]
        self_profile_sign = (db.get_info(str(message.from_user.id)))[0][7]
        profile_match = get_text(profile_sign, self_profile_sign)
        photo_profile = open(f'photo_user/{str(need_profile)}.jpg', 'rb')
        text_reply = f'смотри, {profile_name}, {profile_age} ' \
                     f'\n\n {profile_desc}\n\n {profile_match}'
        await message.answer(text_reply)
        await message.answer_photo(photo_profile)


@dp.message_handler(lambda message: message.text == 'Удалить анкету')
async def delete_profile(message: types.Message):
    db.delete(message.from_user.id)
    await message.answer('Анкета успешно удалена!')
    await bot_start(message)


executor.start_polling(dp, skip_updates=True)

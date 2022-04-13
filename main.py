from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database import Db
import config

TOKEN = config.TOCKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Db('database.db')


class Profile(StatesGroup):
    name = State()
    description = State()
    age = State()
    city = State()
    photo = State()
    sex = State()


# начало
@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    btn_start = KeyboardButton('Зайти в волшебный мир')
    bot_start = ReplyKeyboardMarkup(one_time_keyboard=True)
    bot_start.add(btn_start)
    await message.answer(
        'добро пожаловать', reply_markup=bot_start)
    if not db.user_exists(message.from_user.id):
         db.add_user(message.from_user.username, message.from_user.id, message.from_user.full_name)


# для того чтоб меню вылазило
@dp.message_handler(
    lambda message: message.text == 'Зайти в волшебный мир' or message.text == '/bot_start',
    state='*')
async def bot_start(message: types.Message):
    btn_search = KeyboardButton('Смотреть анкеты')
    btn_create_profile = KeyboardButton('Создать анкету')
    btn_edit_profile = KeyboardButton('Редактировать анкету')
    btn_remove_profile = KeyboardButton('Удалить анкету')
    menu = ReplyKeyboardMarkup()
    menu.add(btn_search, btn_create_profile, btn_edit_profile, btn_remove_profile)
    await message.answer('welcume', reply_markup=menu)


# создаем анкету
@dp.message_handler(lambda message: message.text == 'Создать анкету', state='*')
async def make_profile(message: types.Message):
    btn_exit = KeyboardButton('Выйти нахуй')
    menu_exit_btn = ReplyKeyboardMarkup()
    menu_exit_btn.add(btn_exit)
    if message.from_user.username is not None:
        await message.answer("Введите ваше имя", reply_markup=menu_exit_btn)
        await Profile.name.set()


# обработаем имя
@dp.message_handler(state=Profile.name)
async def insert_name(message: types.Message, state: FSMContext):
    if str(message.text) == 'Выйти нахуй':
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
    if str(message.text) == 'Выйти нахуй':
        await state.finish()
        await bot_start(message)
        return
    elif len(message.text) < 100:
        await state.update_data(profile_description=message.text)
        await message.answer("Укажи свой возраст")
        await Profile.next()
    else:
        await message.answer('Ты нахуя столько настрочил, еблан')
        return


# возраст с проверкой на малолеток
@dp.message_handler(state=Profile.age)
async def insert_age(message: types.Message, state: FSMContext):
    if str(message.text) == 'Выйти нахуй':
        await state.finish()
        await bot_start(message)
        return
    if int(message.text) < 13:
        await message.answer('пиздюкам не рады')
        return
    elif int(message.text) >= 14:
        await state.update_data(profile_age=message.text)
        await message.answer('Введите город')
        await Profile.next()


@dp.message_handler(state=Profile.city)
async def insert_city(message: types.Message, state: FSMContext):
    if str(message.text) == 'Выйти нахуй':
        await state.finish()
        await bot_start(message)
        return
    if len(message.text) > 50:
        await message.answer('Ты нахуя столько настрочил, еблан')
        return
    else:
        await state.update_data(profile_city=message.text.lower())
        await message.answer('Теперь пришли свое фото')

        await Profile.next()


@dp.message_handler(state=Profile.photo, content_types=['photo'])
async def insert_photo(message: types.Message, state: FSMContext):
    if str(message.text) == 'Выйти нахуй':
        await state.finish()
        await bot_start(message)

    man_btn = KeyboardButton("М")
    woman_btn = KeyboardButton('Ж')
    t_btn = KeyboardButton('Трансформер')
    l_btn = KeyboardButton('Ламинат')
    sex_keybord = ReplyKeyboardMarkup(one_time_keyboard=True)
    sex_keybord.add(man_btn, woman_btn, t_btn, l_btn)

    await message.photo[-1].download('photo_user/' + str(message.from_user.id) + '.jpg')
    await message.answer('Пипец ты соска')
    await message.answer('укажи свой пол', reply_markup=sex_keybord)
    await Profile.next()


@dp.message_handler(state=Profile.sex)
async def insert_sex(message: types.Message, state: FSMContext):
    if str(message.text) == 'Выйти нахуй':
        await state.finish()
        await bot_start(message)
    if message.text == 'М' or message.text == 'Ж' or message.text == 'Ламинат' or message.text == 'Трансформер':
        await state.update_data(profile_sex=message.text)
        await message.answer('Анкета успешно создана!')
        user_data = await state.get_data()
        db.create_profile(message.from_user.id, message.from_user.username, str(user_data['profile_name']),
                          str(user_data['profile_description']), user_data['profile_age'],
                          str(user_data['profile_city']), 'photo/' + str(message.from_user.id) + '.jpg',
                          str(user_data['profile_sex']))
        await state.finish()
        await bot_start(message)


executor.start_polling(dp, skip_updates=True)

# -*- coding: utf-8 -*-
# Author: vezype

# ------------- Импорты -------------
import asyncio

import sqlite3

import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# ------------- Конфигурация -------------
TOKEN = '5257584597:AAG0KcRHRUWLS8yw2H-J5wBwjb0z_026O1s'
DATABASE_PATH = 'database.sqlite3'
logging.basicConfig(level=logging.INFO)


# ------------- Класс базы данных -------------
class Database:
    def __init__(self, path: str):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def create_profile(self, user_id: int, nick: str, team_name: str, avatar: str or None) -> bool:
        try:
            request = 'INSERT INTO profiles VALUES(?, ?, ?, ?)'
            data = (user_id, nick, team_name, avatar)
            self.cur.execute(request, data)
            self.con.commit()
            logging.info(f'Пользователь {user_id} успешно создал профиль!')
            return True
        except Exception as error_msg:
            logging.info(f'При создании профиля произошла ошибка: "{error_msg}".')
            return False

    def profile_exist(self, user_id: int) -> bool:
        try:
            request = 'SELECT * FROM profiles WHERE user_id = ?'
            data = (user_id,)
            response = self.cur.execute(request, data).fetchone()
            if response:
                return True
            else:
                return False
        except Exception as error_msg:
            logging.info(f'При проверке существования профиля произошла ошибка: "{error_msg}".')
            return False

    def get_profile(self, user_id: int) -> tuple or None:
        try:
            request = 'SELECT * FROM profiles WHERE user_id = ?'
            data = (user_id,)
            response = self.cur.execute(request, data).fetchone()
            if response:
                return response
            else:
                return False
        except Exception as error_msg:
            logging.info(f'При получении профиля произошла ошибка: "{error_msg}".')
            return False

    def create_game(self, code: str) -> bool:
        try:
            request = 'INSERT INTO games(code) VALUES(?)'
            data = (code,)
            self.cur.execute(request, data)
            self.con.commit()
            logging.info(f'Игра с кодом подключения "{code}" успешно создана!')
            return True
        except Exception as error_msg:
            logging.info(f'При создании игры произошла ошибка: "{error_msg}".')
            return False

    def game_exist(self, code: str) -> bool:
        try:
            request = 'SELECT * FROM games WHERE code = ?'
            data = (code,)
            response = self.cur.execute(request, data).fetchone()
            if response:
                return True
            else:
                return False
        except Exception as error_msg:
            logging.info(f'При проверке существования игры произошла ошибка: "{error_msg}".')
            return False

    def delete_game(self, code: str) -> bool:
        try:
            request = 'DELETE from games WHERE code = ?'
            data = (code,)
            self.cur.execute(request, data)
            self.con.commit()
            logging.info(f'Игра с кодом "{code}" успешно удалена!')
            return True
        except Exception as error_msg:
            logging.info(f'При удалении игры с кодом "{code}" произошла ошибка: "{error_msg}".')
            return False

    def set_avatar(self, user_id: int, avatar: str) -> bool:
        try:
            request = 'UPDATE profiles SET avatar = ? WHERE user_id = ?'
            data = (avatar, user_id)
            self.cur.execute(request, data)
            self.con.commit()
            logging.info(f'Аватар у пользователя {user_id} успешно установлен!')
            return True
        except Exception as error_msg:
            logging.info(f'При установке аватара у пользователя {user_id} произошла ошибка: "{error_msg}".')
            return False

    def set_nick(self, user_id: int, nick: str) -> bool:
        try:
            request = 'UPDATE profiles SET nick = ? WHERE user_id = ?'
            data = (nick, user_id)
            self.cur.execute(request, data)
            self.con.commit()
            logging.info(f'Никнейм у пользователя {user_id} успешно установлен!')
            return True
        except Exception as error_msg:
            logging.info(f'При установке никнейма у пользователя {user_id} произошла ошибка: "{error_msg}".')
            return False

    def delete_avatar(self, user_id: int) -> bool:
        try:
            request = 'UPDATE profiles SET avatar = ? WHERE user_id = ?'
            data = (None, user_id)
            self.cur.execute(request, data)
            self.con.commit()
            logging.info(f'Аватар у пользователя {user_id} успешно удалена!')
            return True
        except Exception as error_msg:
            logging.info(f'При удалении аватара у пользователя "{user_id}" произошла ошибка: "{error_msg}".')
            return False

    def get_avatar(self, user_id: int) -> str or None:
        try:
            request = 'SELECT * FROM profiles WHERE user_id = ?'
            data = (user_id,)
            response = self.cur.execute(request, data).fetchone()[-1]
            return response
        except Exception as error_msg:
            logging.info(f'При получении аватара произошла ошибка: "{error_msg}".')
            return None

    def get_nick(self, user_id: int) -> str or None:
        try:
            request = 'SELECT * FROM profiles WHERE user_id = ?'
            data = (user_id,)
            response = self.cur.execute(request, data).fetchone()[1]
            return response
        except Exception as error_msg:
            logging.info(f'При получении никнейма произошла ошибка: "{error_msg}".')
            return None

    def set_team_name(self, user_id: int, team_name: str) -> bool:
        try:
            request = 'UPDATE profiles SET team_name = ? WHERE user_id = ?'
            data = (team_name, user_id)
            self.cur.execute(request, data)
            self.con.commit()
            logging.info(f'Название команды у пользователя {user_id} успешно установлено!')
            return True
        except Exception as error_msg:
            logging.info(f'При установке названия команды у пользователя {user_id} произошла ошибка: "{error_msg}".')
            return False

    def get_team_name(self, user_id: int) -> str or None:
        try:
            request = 'SELECT * FROM profiles WHERE user_id = ?'
            data = (user_id,)
            response = self.cur.execute(request, data).fetchone()[2]
            return response
        except Exception as error_msg:
            logging.info(f'При получении названия команды произошла ошибка: "{error_msg}".')
            return None


# ------------- Инициализация классов -------------
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database(DATABASE_PATH)


# ------------- Подготовка бота к запуску -------------
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='- запустить бота.'),
        BotCommand(command='/menu', description='- вызвать меню.'),
        BotCommand(command='/cancel', description='- отменить текущее действие.'),
        BotCommand(command='/game', description='- вызвать игровое меню.'),
        BotCommand(command='/profile', description='- вызвать меню редактирования профиля.')
    ]
    await bot.set_my_commands(commands)


# ------------- Inline-клавиатуры -------------
buttons_for_menu = [
    types.InlineKeyboardButton('🎮 Игровое меню', callback_data='game_menu'),
    types.InlineKeyboardButton('🧑‍💻 Мой профиль', callback_data='my_profile')
]
keyboard_for_menu = types.InlineKeyboardMarkup(row_width=1)
keyboard_for_menu.add(*buttons_for_menu)

buttons_for_profile = [
    types.InlineKeyboardButton('🧑‍💻 Ник', callback_data='nick'),
    types.InlineKeyboardButton('👨‍👩‍👦 Название команды', callback_data='team_name'),
    types.InlineKeyboardButton('🖼 Аватар', callback_data='avatar')
]
keyboard_for_profile = types.InlineKeyboardMarkup(row_width=1)
keyboard_for_profile.add(*buttons_for_profile)

buttons_for_game_menu = [
    types.InlineKeyboardButton('✏ Ввести код', callback_data='input_code'),
    types.InlineKeyboardButton('🤖 Присоединиться', callback_data='game_connection')
]
keyboard_for_game_menu = types.InlineKeyboardMarkup(row_width=1)
keyboard_for_game_menu.add(*buttons_for_game_menu)


# ------------- Состояния -------------
class States(StatesGroup):
    game_state = State()
    input_code_state = State()
    change_nick_state = State()
    change_team_name_state = State()
    change_avatar_state = State()


# ------------- Хэндлеры на все команды -------------
@dp.message_handler(commands='start')
async def start(message: types.Message):
    try:
        user = message.from_user
        user_id = user.id
        full_name = user.full_name
        text = f'Здравствуйте, {full_name} 👋\n\n'

        await message.answer(text)

        profile_exist = db.profile_exist(user_id)
        if profile_exist:
            profile = db.get_profile(user_id)
            nick = profile[1]
            team_name = profile[2]
            avatar = profile[3]

            text = f'💬 У Вас есть профиль..\n\n' \
                   f'🧑‍💻 Ник: {nick}\n' \
                   f'👨‍👩‍👦 Название команды: {team_name}\n' \
                   f'🖼 Аватар: {"есть" if avatar else "отсутствует"}\n\n' \
                   f'/menu - вызвать меню для подключения к игре или редактирования профиля.\n' \
                   f'/game - вызвать меню для подключения к игре.'

            if avatar:
                await message.answer_photo(avatar, text)
            else:
                await message.answer(text)

            return

        db.create_profile(user_id, f'nick{user_id}', f'team{user_id}', None)
        nick = f'nick{user_id}'
        team_name = f'team{user_id}'
        avatar = None

        text = f'💬 У Вас не было профиля, бот создал его. Чуть позже Вы сможете его изменить.\n\n' \
               f'🧑‍💻 Ник: {nick}\n' \
               f'👨‍👩‍👦 Название команды: {team_name}\n' \
               f'🖼 Аватар: {"есть" if avatar else "отсутствует"}\n\n' \
               f'/menu - вызвать меню для подключения к игре и редактирования профиля.\n' \
               f'/game - вызвать меню для подключения к игре.'

        await message.answer(text)
    except Exception as error_msg:
        logging.info(f'В хэндлере start произошла ошибка: "{error_msg}".')


@dp.message_handler(commands='menu')
async def menu(message: types.Message):
    try:
        user = message.from_user
        user_id = user.id
        first_name = user.first_name

        if not db.profile_exist(user_id):
            await message.answer('⚠ Сначала Вам надо создать профиль: /start')
            return

        text = f'{first_name}, ниже представлены две кнопки. Выберите действие.\n\n' \
               f'📝 Мой профиль - раздел для редактирования профиля.'

        await message.answer(text, reply_markup=keyboard_for_menu)
    except Exception as error_msg:
        logging.info(f'В хэндлере menu произошла ошибка: "{error_msg}".')


@dp.callback_query_handler(text='my_profile')
async def my_profile_query(call: types.CallbackQuery):
    try:
        user = call.from_user
        user_id = user.id

        profile = db.get_profile(user_id)
        nick = profile[1]
        team_name = profile[2]
        avatar = profile[3]

        text = f'💬 Ваш профиль..\n\n' \
               f'🧑‍💻 Ник: {nick}\n' \
               f'👨‍👩‍👦 Название команды: {team_name}\n' \
               f'🖼 Аватар: {"есть" if avatar else "отсутствует"}\n\n' \
               f'/game - вызвать игровое меню.'

        await call.message.edit_text(text, reply_markup=keyboard_for_profile)
        await call.answer()
    except Exception as error_msg:
        logging.info(f'В хэндлере my_profile_query произошла ошибка: "{error_msg}".')


@dp.callback_query_handler(text='nick')
async def change_nick_query(call: types.CallbackQuery):
    try:
        user = call.from_user
        user_id = user.id
        first_name = user.first_name

        await States.change_nick_state.set()

        text = f'{first_name}, введите новый никнейм..\n\n' \
               f'/cancel - отменить текущее действие.'

        await call.answer(text, show_alert=True)

        @dp.message_handler(state=States.change_nick_state, content_types='text')
        async def get_nick(message: types.Message, state: FSMContext):
            nick = message.text

            if nick == '/cancel':
                await message.answer('Текущее действие отменено.')
                await state.finish()
                return

            db.set_nick(user_id, nick)

            profile = db.get_profile(user_id)
            nick = profile[1]
            team_name = profile[2]
            avatar = profile[3]

            text = f'💬 Ваш профиль..\n\n' \
                   f'🧑‍💻 Ник: {nick}\n' \
                   f'👨‍👩‍👦 Название команды: {team_name}\n' \
                   f'🖼 Аватар: {"есть" if avatar else "отсутствует"}\n\n' \
                   f'/game - вызвать меню для подключения к игре.'

            await call.message.edit_text(text, reply_markup=keyboard_for_profile)
            await state.finish()
    except Exception as error_msg:
        logging.info(f'В хэндлере change_nick_query произошла ошибка: "{error_msg}".')


@dp.callback_query_handler(text='team_name')
async def change_team_name_query(call: types.CallbackQuery):
    try:
        user = call.from_user
        user_id = user.id
        first_name = user.first_name

        await States.change_team_name_state.set()

        text = f'{first_name}, введите новое название команды..\n\n' \
               f'/cancel - отменить текущее действие.'

        await call.answer(text, show_alert=True)

        @dp.message_handler(state=States.change_team_name_state, content_types='text')
        async def get_team_name(message: types.Message, state: FSMContext):
            team_name = message.text

            if team_name == '/cancel':
                await message.answer('Текущее действие отменено.')
                await state.finish()
                return

            db.set_team_name(user_id, team_name)

            profile = db.get_profile(user_id)
            nick = profile[1]
            team_name = profile[2]
            avatar = profile[3]

            text = f'💬 Ваш профиль..\n\n' \
                   f'🧑‍💻 Ник: {nick}\n' \
                   f'👨‍👩‍👦 Название команды: {team_name}\n' \
                   f'🖼 Аватар: {"есть" if avatar else "отсутствует"}\n\n' \
                   f'/game - вызвать меню для подключения к игре.'

            await call.message.edit_text(text, reply_markup=keyboard_for_profile)
            await state.finish()
    except Exception as error_msg:
        logging.info(f'В хэндлере change_team_name_query произошла ошибка: "{error_msg}".')


@dp.callback_query_handler(text='avatar')
async def change_avatar_query(call: types.CallbackQuery):
    try:
        user = call.from_user
        user_id = user.id
        first_name = user.first_name

        await States.change_avatar_state.set()

        text = f'{first_name}, пришлите фотографию..\n\n' \
               f'/cancel - отменить текущее действие.\n' \
               f'/delete - удалить аватар.'

        await call.answer(text, show_alert=True)

        @dp.message_handler(state=States.change_avatar_state, content_types=['text', 'photo'])
        async def get_avatar(message: types.Message, state: FSMContext):
            text = message.text
            photo = message.photo

            if text == '/cancel':
                await message.answer('Текущее действие отменено.')
                await state.finish()
                return

            elif text == '/delete':
                db.delete_avatar(user_id)

            if photo:
                db.set_avatar(user_id, photo[-1].file_id)

            profile = db.get_profile(user_id)
            nick = profile[1]
            team_name = profile[2]
            avatar = profile[3]

            text = f'💬 Ваш профиль..\n\n' \
                   f'🧑‍💻 Ник: {nick}\n' \
                   f'👨‍👩‍👦 Название команды: {team_name}\n' \
                   f'🖼 Аватар: {"есть" if avatar else "отсутствует"}\n\n' \
                   f'/game - вызвать меню для подключения к игре.'

            await call.message.edit_text(text, reply_markup=keyboard_for_profile)
            await state.finish()
    except Exception as error_msg:
        logging.info(f'В хэндлере change_avatar_query произошла ошибка: "{error_msg}".')


@dp.callback_query_handler(text='game_menu')
async def game_menu_query(call: types.CallbackQuery):
    try:
        user = call.from_user
        user_id = user.id

        if not db.profile_exist(user_id):
            await call.message.answer('⚠ Сначала Вам надо создать профиль: /start')
            return

        profile = db.get_profile(user_id)
        nick = profile[1]
        team_name = profile[2]
        avatar = profile[3]

        text = f'✍ Прежде, чем присоединиться к игре Вам надо ввести код!'

        await call.message.edit_text(text, reply_markup=keyboard_for_game_menu)
        await call.answer()
    except Exception as error_msg:
        logging.info(f'В хэндлере game_menu_query произошла ошибка: "{error_msg}".')


@dp.callback_query_handler(text='input_code')
async def input_code_query(call: types.CallbackQuery):
    try:
        user = call.from_user
        user_id = user.id
        first_name = user.first_name

        await States.input_code_state.set()

        text = f'{first_name}, введите код для подключения к игре..\n\n' \
               f'/cancel - отменить текущее действие.'

        await call.answer(text, show_alert=True)

        @dp.message_handler(state=States.input_code_state, content_types='text')
        async def get_input_code(message: types.Message, state: FSMContext):
            code = message.text

            if code == '/cancel':
                await message.answer('Текущее действие отменено.')
                await state.finish()
                return

            if db.game_exist(code):
                await message.answer('Игра найдена 🔎 Нажмите на кнопку "Присоединиться"..')
                await States.game_state.set()

            else:
                await message.answer(f'Игра с кодом "{code}" не найдена 🔎 Попробуйте снова..')
    except Exception as error_msg:
        logging.info(f'В хэндлере input_code_query произошла ошибка: "{error_msg}".')


@dp.callback_query_handler(text='game_connection', state=States.game_state)
async def game_connection_query(call: types.CallbackQuery):
    try:
        user = call.from_user
        user_id = user.id
        first_name = user.first_name

        # Здесь надо начать игру!
        text = f'{first_name}, отлично! Дождитесь старта.'

        await call.answer(text, show_alert=True)

    except Exception as error_msg:
        logging.info(f'В хэндлере game_connection_query произошла ошибка: "{error_msg}".')


# ------------- Запуск бота -------------
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(set_commands(bot))
    executor.start_polling(dp, skip_updates=True)

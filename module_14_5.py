# Задача "Регистрация покупателей":
# Подготовка:
# Для решения этой задачи вам понадобится код из предыдущей задачи. Дополните его, следуя пунктам задачи ниже.
#
# Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:
# initiate_db дополните созданием таблицы Users, если она ещё не создана при помощи SQL запроса. Эта таблица должна содержать следующие поля:
# id - целое число, первичный ключ
# username - текст (не пустой)
# email - текст (не пустой)
# age - целое число (не пустой)
# balance - целое число (не пустой)
# add_user(username, email, age), которая принимает: имя пользователя, почту и возраст. Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными. Баланс у новых пользователей всегда равен 1000. Для добавления записей в таблице используйте SQL запрос.
# is_included(username) принимает имя пользователя и возвращает True, если такой пользователь есть в таблице Users, в противном случае False. Для получения записей используйте SQL запрос.
#
# Изменения в Telegram-бот:
# Кнопки главного меню дополните кнопкой "Регистрация".
# Напишите новый класс состояний RegistrationState с следующими объектами класса State: username, email, age, balance(по умолчанию 1000).
# Создайте цепочку изменений состояний RegistrationState.
# Фукнции цепочки состояний RegistrationState:
# sing_up(message):
# Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
# Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
# После ожидать ввода имени в атрибут RegistrationState.username при помощи метода set.
# set_username(message, state):
# Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
# Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии username на message.text. Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
# Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует, введите другое имя" и запрашивать новое состояние для RegistrationState.username.
# set_email(message, state):
# Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
# Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
# Далее выводить сообщение "Введите свой возраст:":
# После ожидать ввода возраста в атрибут RegistrationState.age.
# set_age(message, state):
# Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
# Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
# Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users при помощи ранее написанной crud-функции add_user.
# В конце завершать приём состояний при помощи метода finish().
# Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.



from aiogram import Bot, executor, types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from crud_functions1 import*
import sqlite3
import asyncio

api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage= MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard = True)
button = KeyboardButton(text = "Рассчитать")
button2 = KeyboardButton(text = "Информация")
button3 = KeyboardButton(text = "Купить")
button4 = KeyboardButton(text='Регистрация')
kb.row(button, button2)
kb.row(button3, button4)

kb1= InlineKeyboardMarkup()
kb2= InlineKeyboardMarkup()
i_1button = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data='calories')
i_2button = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
i_3button = InlineKeyboardButton(text='Гранат', callback_data='product_buying')
i_4button = InlineKeyboardButton(text='Грейпфрут', callback_data='product_buying')
i_5button = InlineKeyboardButton(text='Манго', callback_data='product_buying')
i_6button = InlineKeyboardButton(text='Лимон', callback_data='product_buying')

kb1.add(i_1button)
kb1.add(i_2button)
kb2.add(i_3button)
kb2.add(i_4button)
kb2.add(i_5button)
kb2.add(i_6button)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer('Приветствую!', reply_markup=kb)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in get_all_products():
        number = i[0]
        title = i[1]
        description = i[2]
        price = i[3]
        with open(f'{str(number) + ".jpg"}', 'rb') as img:
            await message.answer_photo(img, caption=f'Название: {title} | Описание: {description} | Цена: {price}')

    await message.answer(text='Выберите продукт для покупки: ', reply_markup=kb2)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(text='Вы успешно приобрели продукт!')
    await call.answer()

    products = [
        'Название: lemon | Сплошной витамин С | Цена: 100',
        'Название: mango | Профилактика раковых новообразований| Цена: 200',
        'Название: grapefrute | Микроэлементы для сердца| Цена: 300',
        'Название: granat| Рубиновый сочный цвет и масса железа!| Цена: 400'
    ]

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Хочешь узнать свою суточную норму калорий по науке?'
                         '\n Нажми на кнопку Рассчитать')
@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=kb1)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Расчет для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161'
                              '\nРасчет для мужчин : 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) + 5')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите Ваш возраст цифрой:")
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите Ваш рост в см:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес в кг:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def rec_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    rec_calor_woman = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    rec_calor_man = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f'Ваша норма калорий: {rec_calor_woman} ккал в сутки (для женщин)')
    await message.answer(f'Ваша норма калорий: {rec_calor_man} ккал в сутки (для мужчин)')
    await state.finish()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000

@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'], )
    await message.answer("Регистрация прошла успешно!")
    await state.finish()



@dp.message_handler()
async def all_message(message):
    await message.answer(f"Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
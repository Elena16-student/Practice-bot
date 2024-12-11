from aiogram import Bot, executor, types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio

api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage= MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard = True)
button = KeyboardButton(text = "Рассчитать")
button2 = KeyboardButton(text = "Информация")
button3 = KeyboardButton(text = "Купить")
kb.row(button, button2)
kb.row(button3)

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

    images = ['lemon.jpg', 'mango.jpg', 'grapefrute.jpg', 'granat.jpg']
    products = [
        'Название: lemon | Сплошной витамин С | Цена: 100',
        'Название: mango | Профилактика раковых новообразований| Цена: 200',
        'Название: grapefrute | Микроэлементы для сердца| Цена: 300',
        'Название: granat| Рубиновый сочный цвет и масса железа!| Цена: 400'
    ]
    for i in range(len(images)):
        with open(images[i], 'rb') as img:
            await message.answer_photo(img, caption=products[i])
    await message.answer('Выберите продукт:', reply_markup = kb2)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()
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

@dp.message_handler()
async def all_message(message):
    await message.answer(f"Введите команду /start, чтобы начать общение.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

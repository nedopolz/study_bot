MESSAGE_FOR_NOT_AUTHORIZED_USERS = """Чтобы использовать этого бота введите код приглашения, либо пройдите по реферальной ссылке"""
HELP_FOR_AUTHORIZED_USERS = """Пойск осуществляется через инлайн мод.
Введите в строке: @my_balamce_bot """

REFERALS_LINK = """Привет, вот твоя реферальная ссылка https://telegram.me/{}?start={}"""  # bot_name and code
YOUR_BONUSES = """На твоем счету {} бонусов"""

WELCOME = """Добро пожаловать, {}!"""
ERORR_LINK = """Привет {}! Твоя ссылка не работает, попробуй ввести код вручную"""  # user name
HI_USER = """Привет, {}!"""  # user name
CODE_IS_NOT_NUMBER = """Код должее быть числом"""
BAD_CODE = """Не верный код"""
ON_STURTUP_READY = """Бот готов к работе"""

# inline search messages
INLINE_NOT_FOUND_ITEM = """К сожалению ничего не нашлось"""
INLINE_NOT_FOUND_ITEM_REPLY = """Попробуйте пойск по описанию"""

# product addition messages
ASK_FOR_PRODUCT_NAME = """Введите название продукта"""
ASK_FOR_PRODUCT_DESCRIPTION = """Введите описание {}"""  # product name
ASK_FOR_PRODUCT_PRICE = """Введите цену в рублях числом """
ASK_FOR_PRODUCT_PHOTO = """Отправьте фотографию в сжатом виде"""
YOU_CANT_USE_THIS_COMMAND = """У вас нет прав на эту команду"""
INCORRECT_PRICE = """Цена должна быть числом"""
TO_BIG_DESCRIPTION = """Описание не должно превышать 2000 символов"""
PRODUCT_SUMMARY_CAPTION = """Название товара {}.\nОписание товара {}.\nЦена {}\n"""  # name, description, price
PRODUCT_CONFORMATION = """нажмите ОК чтобы подтвердить"""
PRODUCT_UNDO = """отменено"""
PRODUCT_WRITTEN_IN_DB = """Подтверждено и внесено в базу данных"""
UNKNOWN_ERORR="""произошла какая-то ошибка"""

# purchase messages
ASK_FOR_AMOUNT = """Введите количество {}"""  # product name
ASK_FOR_BONUSES_SPEND = """У вас есть {} бонусов. Хотите их потратить?"""  # bonuses
ASK_FOR_DELIVERY_ADRESS = """Введите адрес доставки"""
INVALID_AMOUNT = """Количество должно быть числом"""
SUCCESFUL_BONUS_SPEND = """Успешно. Итого к оплате {}
Введите адрес доставки"""  # final price
PURCHASE_SUMMARY_CAPTION = """Подтвердите правильность заказа:
{} в количестве {} с общей ценой: {}р
заказ будет доставлен по адресу: {}"""  # name, amount, final price, adress
PAYMENT_BEFORE_LINK = """Оплатите не менее {} по номеру телефона или по адресу"""  # final price
PAYMENT_BEFORE_ID = """И обязательно укажите ID платежа:"""
PURCHASE_UNDO = """Покупка отменена"""
ERORR_NO_FOUND = """Транзакция не найдена."""
ERORR_LESS_THEN_NEED = """Оплаченная сума меньше необходимой.
Пополните счет еще на {}"""
SUCCESFUL_PURCHASE = """Успешно оплачено"""
YOUR_MONEY_SAVE = """Вы перевели на {} больше необходимой ссумы.
Избыток отправлен на ваш бонусный счет"""

#keyboards
ACTIVATION_KEYBOARD  = """начать работу"""
CONFIRMATION_KEYBOARD_YES = """Да"""
CONFIRMATION_KEYBOARD_NO = """Нет"""
PAID_KEYBOARD_BUY = """Посмотреть {}""" #name
PURCHASE_INIT = """Купить"""
PAID_KEYBOARD_PAY = """оплатил"""
PAID_KEYBOARD_UNDO = """отмена"""

BUY_MESSAGE = """Нажмите на кнопк ниже чтобы купить {}. Цена: {}₽""" #name, price
ADMIN_NOTIFY = """все идет по плану"""
USER_STATE_RESET = """Бот был перезапущен, нажмите Start."""

#set_bot_commands are not in this config
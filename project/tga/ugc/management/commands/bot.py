from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from telegram import Bot, Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, Filters, MessageHandler, CommandHandler, Updater, CallbackQueryHandler
from telegram.utils.request import Request
from ugc.models import Profile


#текст с описанием команд
cmds = '/permit   Как оформить пропуск на территорию аэропорта?\n/instruction   Где и когда пройти обучение по охране труда?\n/transport   Информация о маршрутах корпоративного транспорта.\n/parking   Информация о парковочных местах.\n/DMS   Информация о получении карточки добровольного медицинского страхования.\n/coach   Узнать ФИО своего наставника и как с ним связаться.\n/services   Узнать телефоны срочных служб.\n/plans   Напоминание о важных событиях.\n/university   Местоположение корпоративного университета.\n/korpus4   Местоположение четвертого корпуса.'

#функция если не принял команду
def misunderstand(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    try:
        p = Profile.objects.get( external_id=chat_id,)
    except ObjectDoesNotExist:
        update.message.reply_text(text='Вы не имеете доступа к боту.\nВаш ID {} не внесен в базу.'.format(chat_id),)
        return
    reply_text = "К сожалению, я понимаю только эти команды:\n{}".format(cmds)
    update.message.reply_text(text=reply_text,)

#функция для /start
def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    try:
        p = Profile.objects.get( external_id=chat_id,)
    except ObjectDoesNotExist:
        update.message.reply_text(text='Вы не имеете доступа к боту.\nВаш ID {} не внесен в базу.'.format(chat_id),)
        return
    reply_text = "Привет, сотрудник, я hr-бот компании Шереметьево.\nЗдесь ты можешь узнать информацию через мои команды:\n{}".format(cmds)
    update.message.reply_text(text=reply_text,)

#функция для /permit
def permit(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        p = Profile.objects.get( external_id=chat_id,)
    except ObjectDoesNotExist:
        update.message.reply_text(text='Вы не имеете доступа к боту.\nВаш ID {} не внесен в базу.'.format(chat_id),)
        return
    reply_text = "Шаг 1. Заполнить Заявку на пропуск и заявку СКУД\nШаг 2. Подписать данные заявки у непосредственного руководителя\nШаг 3. С подписанными заявлениями, оригиналом паспорта, а также с 3 копии всех документов необходимо прийти в здание КИВЦ, эт.2, каб. 17.\nШаг 4. Отслеживать статус заявки на пропуск, по готовности прийти в КИВЦ за готовым пропуском."
    update.message.reply_text(text=reply_text,)

#функция для /instruction
def instruction(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        p = Profile.objects.get( external_id=chat_id,)
    except ObjectDoesNotExist:
        update.message.reply_text(text='Вы не имеете доступа к боту.\nВаш ID {} не внесен в базу.'.format(chat_id),)
        return
    reply_text = "Семинар по охране труда проводится каждый вторник и четверг в 9:15 в здании «Трансаэро», каб. 319. Семинар проводит ведущий специалист по охране труда – Чучвара Александр Игоревич, контактный номер: 8 (926) 244-6359. С собой необходимо иметь паспорт или пропуск."
    update.message.reply_text(text=reply_text,)




#'callback_data' - это то, что будет присылать TG при нажатии на каждую кнопку.
#поэтому каждый идентификатор должен быть уникальным
CALLBACK_BUTTON1_TO = 'callback_button1_to'
CALLBACK_BUTTON2_FROM = 'callback_button2_from'
CALLBACK_BUTTON3_LOBNYA1 = 'callback_button3_lobnya1'
CALLBACK_BUTTON4_KRAPOLYANA1 = 'callback_button4_krapolyana1'
CALLBACK_BUTTON5_SKHODNENSKAYA1 = 'callback_button5_skhodnenskaya1'
CALLBACK_BUTTON6_ZELENOGRAD1 = 'callback_button6_zelenograd1'
CALLBACK_BUTTON7_KHLEBNIKOVO1 = 'callback_button7_khlebnikovo1'
CALLBACK_BUTTON8_BACK1 = 'callback_button8_back1'
CALLBACK_BUTTON9_LOBNYA2 = 'callback_button9_lobnya2'
CALLBACK_BUTTON10_KRAPOLYANA2 = 'callback_button10_krapolyana2'
CALLBACK_BUTTON11_SKHODNENSKAYA2 = 'callback_button11_skhodnenskaya2'
CALLBACK_BUTTON12_ZELENOGRAD2 = 'callback_button12_zelenograd2'
CALLBACK_BUTTON13_KHLEBNIKOVO2 = 'callback_button13_khlebnikovo2'
CALLBACK_BUTTON14_BACK2 = 'callback_button14_back2'


TITLES = {
   CALLBACK_BUTTON1_TO : 'В Аэропорт',
   CALLBACK_BUTTON2_FROM : 'Из Аэропорта',
   CALLBACK_BUTTON3_LOBNYA1 : 'Из Лобни',
   CALLBACK_BUTTON4_KRAPOLYANA1 : 'С Красной Поляны',
   CALLBACK_BUTTON5_SKHODNENSKAYA1 : 'От м. Сходненская',
   CALLBACK_BUTTON6_ZELENOGRAD1 : 'Из Зеленограда',
   CALLBACK_BUTTON7_KHLEBNIKOVO1 : 'Из Хлебниково',
   CALLBACK_BUTTON8_BACK1 : '« Назад',
   CALLBACK_BUTTON9_LOBNYA2 : 'В Лобню',
   CALLBACK_BUTTON10_KRAPOLYANA2 : 'На Красную Поляну',
   CALLBACK_BUTTON11_SKHODNENSKAYA2 : 'К м. Сходненская',
   CALLBACK_BUTTON12_ZELENOGRAD2 : 'В Зеленоград',
   CALLBACK_BUTTON13_KHLEBNIKOVO2 :'В Хлебниково',
   CALLBACK_BUTTON14_BACK2 : '« Назад',
}

def get_inline_keyboard1():
   #получить клавиатуру для сообщения
   #она будет видна под каждым сообщением, где ее прикрепили (мы будем крепить ее к текстовому ответу на запрос информации о транспорте)
   #каждый список внутри 'keyboard' - это один горизонтальный ряд кнопок, каждый элемент списка - кнопка в этом ряду
   keyboard = [
		[InlineKeyboardButton(TITLES[CALLBACK_BUTTON1_TO], callback_data = CALLBACK_BUTTON1_TO),],
		[InlineKeyboardButton(TITLES[CALLBACK_BUTTON2_FROM], callback_data = CALLBACK_BUTTON2_FROM),],
	      ]
   return InlineKeyboardMarkup(keyboard)

def get_inline_keyboard2():
   keyboard = [
		[
			InlineKeyboardButton(TITLES[CALLBACK_BUTTON3_LOBNYA1], callback_data = CALLBACK_BUTTON3_LOBNYA1),
			InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_KRAPOLYANA1], callback_data = CALLBACK_BUTTON4_KRAPOLYANA1),
		],
		[
			InlineKeyboardButton(TITLES[CALLBACK_BUTTON5_SKHODNENSKAYA1], callback_data = CALLBACK_BUTTON5_SKHODNENSKAYA1),
			InlineKeyboardButton(TITLES[CALLBACK_BUTTON6_ZELENOGRAD1], callback_data = CALLBACK_BUTTON6_ZELENOGRAD1),
		],
		[
			InlineKeyboardButton(TITLES[CALLBACK_BUTTON7_KHLEBNIKOVO1], callback_data = CALLBACK_BUTTON7_KHLEBNIKOVO1),
			InlineKeyboardButton(TITLES[CALLBACK_BUTTON8_BACK1], callback_data = CALLBACK_BUTTON8_BACK1),
		],
	      ]
   return InlineKeyboardMarkup(keyboard)

def get_inline_keyboard3():
   keyboard = [
		[
                        InlineKeyboardButton(TITLES[CALLBACK_BUTTON9_LOBNYA2], callback_data = CALLBACK_BUTTON9_LOBNYA2),
                        InlineKeyboardButton(TITLES[CALLBACK_BUTTON10_KRAPOLYANA2], callback_data = CALLBACK_BUTTON10_KRAPOLYANA2),
                ],
                [
                        InlineKeyboardButton(TITLES[CALLBACK_BUTTON11_SKHODNENSKAYA2], callback_data = CALLBACK_BUTTON11_SKHODNENSKAYA2),
                        InlineKeyboardButton(TITLES[CALLBACK_BUTTON12_ZELENOGRAD2], callback_data = CALLBACK_BUTTON12_ZELENOGRAD2),
                ],
                [
                        InlineKeyboardButton(TITLES[CALLBACK_BUTTON13_KHLEBNIKOVO2], callback_data = CALLBACK_BUTTON13_KHLEBNIKOVO2),
                        InlineKeyboardButton(TITLES[CALLBACK_BUTTON14_BACK2], callback_data = CALLBACK_BUTTON14_BACK2),
                ],
	      ]
   return InlineKeyboardMarkup(keyboard)



#функция для /transport
def transport(update:Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        p = Profile.objects.get( external_id=chat_id,)
    except ObjectDoesNotExist:
        update.message.reply_text(text='Вы не имеете доступа к боту.\nВаш ID {} не внесен в базу.'.format(chat_id),)
        return
    reply_text = "Для того, чтобы пользоваться корпоративным транспортом, необходимо приобрести месячный абонемент и всегда иметь с собой пропуск.\nУзнайте расписание."
    context.bot.send_message(chat_id=chat_id, text=reply_text, reply_markup=get_inline_keyboard1(),)

#обработчик всех кнопок со всех клавиатур
def keyboard_callback_handler(update:Update, context: CallbackContext):
   query = update.callback_query
   data = query.data
   chat_id = update.effective_message.chat_id

   if data == CALLBACK_BUTTON1_TO:
      query.edit_message_text(text="Для того, чтобы пользоваться корпоративным транспортом, необходимо приобрести месячный абонемент и всегда иметь с собой пропуск.\nУзнайте расписание", reply_markup=get_inline_keyboard2(),)
   elif data == CALLBACK_BUTTON2_FROM:
      query.edit_message_text(text="Для того, чтобы пользоваться корпоративным транспортом, необходимо приобрести месячный абонемент и всегда иметь с собой пропуск.\nУзнайте расписание.", reply_markup=get_inline_keyboard3(),)
   elif data == CALLBACK_BUTTON3_LOBNYA1:
      query.edit_message_text(text='Для того, чтобы пользоваться корпоративным транспортом, необходимо приобрести месячный абонемент и всегда иметь с собой пропуск.\nСо станции Лобня\n\nМаршрут №3: Станция Лобня - Кафе "Севастополь"\n07-15\n\nМаршрут №5: Станция Лобня - Терминал D\n06-30 (*), 18-50\n\nМаршрут №6: Станция Лобня - Терминал E\n08-25 (по будням)\n\n(*) По выходным дням время отправления в 6:45', reply_markup=get_inline_keyboard2(),)
   elif data == CALLBACK_BUTTON4_KRAPOLYANA1:
      query.edit_message_text(text='Для того, чтобы пользоваться корпоративным транспортом, необходимо приобрести месячный абонемент и всегда иметь с собой пропуск.\nС Красной Поляны\n\nМаршрут №1: Красная Поляна - Кафе "Севастополь"\n07-05\n\nМаршрут №2: Красная Поляна - Терминал E\n07-40**\n\nМаршрут №4: Красная Поляна - Терминал E\n06-30 (*), 18-50\n\n(*) По выходным дням время отправления в 6:45\n(**) По выходным дням время отправления в 8.00\n(***) только по выходным дням (на ст. Лобня в 8:15)', reply_markup=get_inline_keyboard2(),)
   elif data == CALLBACK_BUTTON5_SKHODNENSKAYA1:
      query.edit_message_text(text='Для того, чтобы пользоваться корпоративным транспортом, необходимо приобрести месячный абонемент и всегда иметь с собой пропуск.\nОт метро Сходненская\n\nМаршрут №10: метро Сходненская - Терминал E\n07:50', reply_markup=get_inline_keyboard2(),)
   elif data == CALLBACK_BUTTON6_ZELENOGRAD1:
      query.edit_message_text(text='Для того, чтобы пользоваться корпоративным транспортом, необходимо приобрести месячный абонемент и всегда иметь с собой пропуск.\nИз Зеленограда\n\nМаршрут №7: Зеленоград - Терминал E\n06:25, 18:10\n\nМаршрут №8: Зеленоград - Терминал E\n07:25', reply_markup=get_inline_keyboard2(),)
   elif data == CALLBACK_BUTTON7_KHLEBNIKOVO1:
      query.edit_message_text(text='Для того, чтобы пользоваться корпоративным транспортом, необходимо приобрести месячный абонемент и всегда иметь с собой пропуск.\nОт Хлебниково\n\nМаршрут №11: Хлебниково - Терминал E\n07:00, 08:30, 19:00', reply_markup=get_inline_keyboard2(),)
   elif data == CALLBACK_BUTTON8_BACK1:
     query.edit_message_text(text="Для того, чтобы пользоваться корпоративным транспортом, необходимо приобрести месячный абонемент и всегда иметь с собой пропуск.\nУзнайте расписание.", reply_markup=get_inline_keyboard1(),)
   elif data == CALLBACK_BUTTON9_LOBNYA2:
      query.edit_message_text(text="Для того, чтобы пользоваться корпоративным транспортом, необходимо приобрести месячный абонемент и всегда иметь с собой пропуск.\nВ Лобню\n\nМаршрут №5: Терминал E - станция Лобня\n08:20, 17:05 (*) кроме выходных, 20:15.\n\n(*) По пятницам - отправление автобуса в 14 часов 35 минут", reply_markup=get_inline_keyboard3(),)
   elif data == CALLBACK_BUTTON10_KRAPOLYANA2:
      query.edit_message_text(text='Для того, чтобы пользоваться корпоративным транспортом, необходимо приобрести месячный абонемент и всегда иметь с собой пропуск.\nНа Красную Поляну\n\nМаршрут №1: Администрация - Красная Поляна\n18:15 (****) кроме выходных\n\nМаршрут №2: 7 корпус- Красная Поляна\n18-05 (**) кроме выходных\n\nМаршрут №3: 7 корпус - Красная Поляна (ул. Текстильная)\n17:05 (*) кроме выходных\n\nМаршрут №4: Терминал E - Красная Поляна\n08-20, 17-50 (***), 20-15\n\nМаршрут №6: Терминал E - ст. Лобня - Красная Поляна\n18:15 (****)\n\nМаршрут №8: Терминал E - Депо - Красная Поляна\n09-10\n\n(*) По пятницам - отправление автобуса в 14 часов 35 минут\n(**) По пятницам - отправление автобуса в 15 часов 50 минут\n(***) По пятницам - отправление автобуса в 15 часов 35 минут\n(****) По пятницам - отправление автобуса в 15 часов 45 минут',reply_markup=get_inline_keyboard3(),)
   elif data == CALLBACK_BUTTON11_SKHODNENSKAYA2:
      query.edit_message_text(text='Для того, чтобы пользоваться корпоративным транспортом, необходимо приобрести месячный абонемент и всегда иметь с собой пропуск.\nК метро Сходненская\n\nМаршрут №10: Шереметьево 1 – м.Сходненская\n18:15* ( кроме выходных)\n(*) По пятницам - отправление автобуса в 15 часов 45 минут', reply_markup=get_inline_keyboard3(),)
   elif data == CALLBACK_BUTTON12_ZELENOGRAD2:
      query.edit_message_text(text='Для того, чтобы пользоваться корпоративным транспортом, необходимо приобрести месячный абонемент и всегда иметь с собой пропуск.\nВ Зеленоград\n\nМаршрут №7: Терминал E - Зеленоград\n08:30; 17:05 (*), кроме выходных\n\nМаршрут №7: Шереметьево-1 - Зеленоград\n20:15\n\nМаршрут №8: Корпус №7 - Зеленоград\n18:15 (**)\n\n(*) По пятницам - отправление автобуса в 14 часов 35 минут\n(**) По пятницам - отправление автобуса в 15 часов 45 минут', reply_markup=get_inline_keyboard3(),)
   elif data == CALLBACK_BUTTON13_KHLEBNIKOVO2:
      query.edit_message_text(text='Для того, чтобы пользоваться корпоративным транспортом, необходимо приобрести месячный абонемент и всегда иметь с собой пропуск.\nВ Хлебниково\n\nМаршрут №11: Терминал E - Хлебниково\n08:10; 09:10; 17:05 (*) кроме выходных, 18:15 (**) кроме выходных, 20:15', reply_markup = get_inline_keyboard3(),)
   elif data == CALLBACK_BUTTON14_BACK2:
      query.edit_message_text(text='Для того, чтобы пользоваться корпоративным транспортом, необходимо приобрести месячный абонемент и всегда иметь с собой пропуск.\nУзнайте расписание.', reply_markup=get_inline_keyboard1(),)






#функция для /parking
def parking(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        p = Profile.objects.get( external_id=chat_id,)
    except ObjectDoesNotExist:
        update.message.reply_text(text='Вы не имеете доступа к боту.\nВаш ID {} не внесен в базу.'.format(chat_id),)
        return
    #сделать красивые картинки о парковке и отправить их пользователю

#функция для /DMS
def dms(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        p = Profile.objects.get( external_id=chat_id,)
    except ObjectDoesNotExist:
        update.message.reply_text(text='Вы не имеете доступа к боту.\nВаш ID {} не внесен в базу.'.format(chat_id),)
        return
    reply_text = "Для получения полиса ДМС необходимо обратиться в Поликлинику аэропорта, к. 316. Выдача производится - с понедельника по четверг с 8 до 16 часов; - в пятницу с 8 до 14 часов."
    update.message.reply_text(text=reply_text,)

#функция для /coach
def coach(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        p = Profile.objects.get( external_id=chat_id,)
    except ObjectDoesNotExist:
        update.message.reply_text(text='Вы не имеете доступа к боту.\nВаш ID {} не внесен в базу.'.format(chat_id),)
        return
    reply_text ="Ваш наставник\n{}".format(p.coach_information)
    update.message.reply_text(text=reply_text,)

#функция для /services
def services(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        p = Profile.objects.get( external_id=chat_id,)
    except ObjectDoesNotExist:
        update.message.reply_text(text='Вы не имеете доступа к боту.\nВаш ID {} не внесен в базу.'.format(chat_id),)
        return
    reply_text ="Сменный начальник аэропорта: +7 (495) 578 45 41; +7 (925) 500 65 21\nСменный начальник транспортной безопасности: +7 (495) 578 74 52; +7 (925) 500 41 25\nДежурный ЛУ МВД в аэропорту: +7 (795) 578 27 21; +7 (495) 578 14 25\nДежурный ФСБ в аэропорту: +7 (495) 578 23 14"
    update.message.reply_text(text=reply_text,)

#функция для /plans
def plans(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        p = Profile.objects.get( external_id=chat_id,)
    except ObjectDoesNotExist:
        update.message.reply_text(text='Вы не имеете доступа к боту.\nВаш ID {} не внесен в базу.'.format(chat_id),)
        return
    #текущие напоминая выводятся как текст (оформлены как модель джанго)

#функция для /university
def university(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        p = Profile.objects.get( external_id=chat_id,)
    except ObjectDoesNotExist:
        update.message.reply_text(text='Вы не имеете доступа к боту.\nВаш ID {} не внесен в базу.'.format(chat_id),)
        return
    #выслать пользователю картинки подсказки

#функция для /korpus4
def korpus4(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        p = Profile.objects.get( external_id=chat_id,)
    except ObjectDoesNotExist:
        update.message.reply_text(text='Вы не имеете доступа к боту.\nВаш ID {} не внесен в базу.'.format(chat_id),)
        return
    #выслать пользователю картинки подсказки


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        # 1 - правильно подключение
        request = Request(connect_timeout = 0.5, read_timeout = 1.0)
        bot = Bot(request=request, token=settings.TOKEN)
        print(bot.get_me())
        # 2 - обработчики
        updater = Updater(bot=bot,use_context=True,)

        command_handler_start = CommandHandler('start', start)
        updater.dispatcher.add_handler(command_handler_start)

        command_handler_permit = CommandHandler('permit', permit)
        updater.dispatcher.add_handler(command_handler_permit)

        command_handler_instruction = CommandHandler('instruction', instruction)
        updater.dispatcher.add_handler(command_handler_instruction)

        command_handler_transport = CommandHandler('transport', transport)
        updater.dispatcher.add_handler(command_handler_transport)

        command_handler_parking = CommandHandler('parking', parking)
        updater.dispatcher.add_handler(command_handler_parking)

        command_handler_dms = CommandHandler('dms', dms)
        updater.dispatcher.add_handler(command_handler_dms)

        command_handler_coach = CommandHandler('coach', coach)
        updater.dispatcher.add_handler(command_handler_coach)

        command_handler_services = CommandHandler('services', services)
        updater.dispatcher.add_handler(command_handler_services)

        command_handler_plans = CommandHandler('plans', plans)
        updater.dispatcher.add_handler(command_handler_plans)

        command_handler_university = CommandHandler('university', university)
        updater.dispatcher.add_handler(command_handler_university)

        command_handler_korpus4 = CommandHandler('korpus4', korpus4)
        updater.dispatcher.add_handler(command_handler_korpus4)

        buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler)
        updater.dispatcher.add_handler(buttons_handler)

        message_handler = MessageHandler(Filters.all, misunderstand)
        updater.dispatcher.add_handler(message_handler)

        # 3 - начать обработку входящих сообщений
        updater.start_polling()
	# 4 - не прерывать скрипт до обработки всех сообщений
        updater.idle()

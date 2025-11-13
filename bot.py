import telebot
from telebot import types

TOKEN = "8463880587:AAFprilgxyz0lPcze6phYJ0TSff83mPqeXI"
CHANNEL_USERNAME = "@tgpremiumsubscription"
CHANNEL_ID = -1002036065687
ADMIN_USERNAME = "@aslbek4777"

bot = telebot.TeleBot(TOKEN)

CLASSES = {
    "5-sinf": {"bsb": "https://sor-soch.com/bsb.php?klass=5", "chsb": "https://sor-soch.com/chsb.php?klass=5"},
    "6-sinf": {"bsb": "https://sor-soch.com/bsb.php?klass=6", "chsb": "https://sor-soch.com/chsb.php?klass=6"},
    "7-sinf": {"bsb": "https://sor-soch.com/bsb.php?klass=7", "chsb": "https://sor-soch.com/chsb.php?klass=7"},
    "8-sinf": {"bsb": "https://sor-soch.com/bsb.php?klass=8", "chsb": "https://sor-soch.com/chsb.php?klass=8"},
    "9-sinf": {"bsb": "https://sor-soch.com/bsb.php?klass=9", "chsb": "https://sor-soch.com/chsb.php?klass=9"},
    "10-sinf": {"bsb": "https://sor-soch.com/bsb.php?klass=10", "chsb": "https://sor-soch.com/chsb.php?klass=10"},
    "11-sinf": {"bsb": "https://sor-soch.com/bsb.php?klass=11", "chsb": "https://sor-soch.com/chsb.php?klass=11"}
}

def check_subscription(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

def subscription_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("📢 Kanalga obuna bo'lish", url="https://t.me/tgpremiumsubscription"))
    keyboard.add(types.InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_subscription"))
    return keyboard

def main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("5-sinf", "6-sinf")
    keyboard.add("7-sinf", "8-sinf")
    keyboard.add("9-sinf", "10-sinf")
    keyboard.add("11-sinf")
    keyboard.add("👤 ADMINGA BOG'LANISH")
    return keyboard

def type_keyboard(class_name):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("📝 BSB javoblar", callback_data=f"bsb_{class_name}"),
        types.InlineKeyboardButton("📝 CHSB javoblar", callback_data=f"chsb_{class_name}")
    )
    keyboard.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if check_subscription(user_id):
        bot.send_message(message.chat.id, f"👋 Assalomu alaykum, {message.from_user.first_name}!\n\n📚 Sinfingizni tanlang:", reply_markup=main_menu_keyboard())
    else:
        bot.send_message(message.chat.id, "⚠️ Botdan foydalanish uchun kanalimizga obuna bo'ling!", reply_markup=subscription_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_sub_callback(call):
    user_id = call.from_user.id
    if check_subscription(user_id):
        bot.answer_callback_query(call.id, "✅ Obuna tasdiqlandi!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"👋 Xush kelibsiz, {call.from_user.first_name}!\n\n📚 Sinfingizni tanlang:", reply_markup=main_menu_keyboard())
    else:
        bot.answer_callback_query(call.id, "❌ Siz hali obuna bo'lmadingiz!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
def back_to_main(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "📚 Sinfingizni tanlang:", reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda message: message.text in CLASSES.keys())
def select_class(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        bot.send_message(message.chat.id, "⚠️ Botdan foydalanish uchun kanalimizga obuna bo'ling!", reply_markup=subscription_keyboard())
        return
    class_name = message.text
    bot.send_message(message.chat.id, f"📚 {class_name} uchun turni tanlang:", reply_markup=type_keyboard(class_name))

@bot.callback_query_handler(func=lambda call: call.data.startswith(('bsb_', 'chsb_')))
def send_link(call):
    data_parts = call.data.split('_')
    type_name = data_parts[0]
    class_name = data_parts[1]
    link = CLASSES[class_name][type_name]
    type_text = "BSB" if type_name == "bsb" else "CHSB"
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🔗 Ochish", url=link))
    keyboard.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
    bot.edit_message_text(f"📖 {class_name} - {type_text} javoblar\n\n👇 Quyidagi tugmani bosing:", call.message.chat.id, call.message.message_id, reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "👤 ADMINGA BOG'LANISH")
def contact_admin(message):
    user_id = message.from_user.id
    if not check_subscription(user_id):
        bot.send_message(message.chat.id, "⚠️ Botdan foydalanish uchun kanalimizga obuna bo'ling!", reply_markup=subscription_keyboard())
        return
    bot.send_message(message.chat.id, f"👤 Admin bilan bog'lanish:\n{ADMIN_USERNAME}", reply_markup=main_menu_keyboard())

print("✅ Bot ishga tushdi...")
bot.polling(none_stop=True)
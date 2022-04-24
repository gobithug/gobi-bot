# This is a sample Python script.

import datetime

import telegram
from pytz import timezone
from telegram.ext import *
from telegram import *
import random
import pymongo
import logging
from big_text import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

client = pymongo.MongoClient(
    "mongodb+srv://pugalkmc:pugalkmc@cluster0.ey2yh.mongodb.net/mydb?retryWrites=true&w=majority")

mydb = client.get_default_database()
#
TWO, THREE = range(2)
CHOOSE = range(1)

bot = Bot(token="5123712096:AAFoWsAeO_sJyrsl0upMa-LUCeHE-k8AWYE")


# ---------- functions ---------


def main_buttons(update, context):
    reply_keyboard = [['Do TaskðŸ’¸', '', 'Create TaskðŸ“œ'], ['Balanceâš–ï¸', 'Depositâž•'], ['Referral linkðŸ“Ž', 'Moreâ•']]

    bot.sendMessage(chat_id=update.message.chat_id, text="Main Menu",
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                                     resize_keyboard=True,
                                                     one_time_keyboard=True))


def start(update, context):
    sender = update.message.reply_text
    chat_id = update.message.chat_id
    username = update.message.chat.username
    text = update.message.text
    if str(username) == "None":
        sender("No username found for your account")
        sender("Please set username for your telegram\n"
               "1)Go telegram account settings\n"
               "2)Click username\n"
               "3)Set unique and simplified username")
    else:
        checking_exist = mydb["people"]
        bot.sendMessage(chat_id=chat_id, text="This KMC TRX earning bot"
                                              "\nYou can earn TRX by doing tasks"
                                              "\nAlso You can create task for other to do")

        main_buttons(update, context)
        for i in checking_exist.find({}):
            if username == i["username"]:
                break
        else:
            rand_num = random.randrange(11023648, 12023648)
            rand_text = random.choice('qwertyuiopasfghjklzxcvbnm')
            link = "https://telegram.me/earn_trx_ind_bot?start=" + str(rand_num) + rand_text
            checking_exist.insert_one({"_id": chat_id, "username": username, "referral": link,
                                       "ref_count": 0, "TRX_balance": 0.0, "ref_income": 0.0,
                                       'earned_total': 0.0, 'payout_avail': 0.0})
            bot.sendMessage(chat_id=1291659507, text="New user found @" + str(username))
            referal(text, username)


def referal(text, username):
    referal_link = text.replace("/start", '')
    if "earn_trx_ind_bot" in text:
        ref = mydb["people"]
        link = "https://telegram.me/earn_trx_ind_bot?start=" + str(referal_link)
        try:
            get = ref.find_one({"referral": link})
            get_invitee = get["_id"]
            get_count = get["ref_count"]
            ref.update_one({"_id": get_invitee}, {"$set": {"ref_count": get_count + 1}})
            bot.sendMessage(chat_id=get_invitee, text=f"You got new referral: @{username}")
        except:
            get = ref.find_one({"referral": "https://telegram.me/earn_trx_ind_bot?start=11299293i"})
            get_invitee = get["_id"]
            get_count = get["ref_count"]
            ref.update_one({"_id": get_invitee}, {"$set": {"ref_count": get_count + 1}})


def msg_hand(update, context):
    chat_id = update.message.chat_id
    username = update.message.chat.username
    sender = update.message.reply_text
    text = update.message.text
    if 'Do TaskðŸ’¸' == text:
        task_list(update, context)
    elif 'Balanceâš–ï¸' == text:
        people = mydb['people']
        get = people.find_one({'_id': chat_id})
        bot.sendMessage(chat_id=chat_id, text=f"Balance: {get['TRX_balance']} TRX\n\n"
                                              f"Total Earned: {get['earned_total']} TRX\n\n"
                                              f"Available for payout:\n"
                                              f"{get['payout_avail']} TRX",
                        reply_to_message_id=update.message.message_id)
    elif 'Depositâž•' == text:
        bot.sendMessage(chat_id=chat_id, text="Send TRX to this address(TRC-20):\n"
                                              "<code>TSPZcEraokyNAuFR4Shgyn5D4ycsWjJhrL</code>\n\n"
                                              "Then send TXID of your transaction\n\n"
                                              "NEWS: Soon auto deposit , withdrawal will be enabled",
                        parse_mode=telegram.ParseMode.HTML, reply_to_message_id=update.message.message_id)
    elif 'Referral linkðŸ“Ž' == text:
        get_link = mydb['people']
        get = get_link.find_one({"_id": chat_id})
        bot.sendMessage(chat_id=chat_id, text=f"Your referral count: {get['ref_count']}\n\n"
                                              f"You have earned {get['ref_income']} TRX by referrals\n\n"
                                              f"Referral link: \n{get['referral']}\n\n"
                                              f"You can withdraw your referral income or spend it on ads\n\n"
                                              f"You will earn 7% commission when your friends do task or create task\n\n",
                        reply_to_message_id=update.message.message_id)
    elif "Withdrawâž•" == text:
        pass
    if text == "Moreâ•":
        reply_keyboard = [["Withdrawâž•", "SupportðŸ‘¤"], ["AboutðŸ’¬", "RulesðŸ”–"], ["Backâ†©"]]
        sender("Use below buttons for quick access",
               reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True),
               reply_to_message_id=update.message.message_id)
    elif 'RulesðŸ”–' == text:
        bot.sendMessage(chat_id=chat_id, text=rules, reply_to_message_id=update.message.message_id)
    elif "AboutðŸ’¬" == text:
        bot.sendMessage(chat_id=chat_id, text=about, reply_to_message_id=update.message.message_id)
    elif "SupportðŸ‘¤" == text:
        bot.sendMessage(chat_id=chat_id, text="Support group link:\n"
                                              "https://t.me/+dFsICH3quPRhYjVl\n\n"
                                              "Join our support group to get more benefits\n\n"
                                              "Note: ADMIN WILL NEVER DM YOU FIRST!\n\n"
                                              "Admin support: @PugalKMC", reply_to_message_id=update.message.message_id)
    elif text == "Backâ†©" or text == "cancel":
        main_buttons(update, context)


def task_list(update, context):
    chat_id = update.message.chat_id
    tasks_list = mydb["tasks"]
    list1 = []
    total = 0
    for i in tasks_list.find({}):
        if chat_id not in i['done_by']:
            total += 1
            text = f"Task No: {total}\n" \
                   f"Title: {i['title']}\n" \
                   f"Do task : /{i['cmd_id']}\n" \
                   f"Payment: {i['trx_per']} TRX\n" \
                   f"Users : {i['done']}/{i['limit']}\n"

            list1.append(text)

    update.message.reply_text("Total task found:{0}\n\n{1}\n\n".format(total, '\n'.join(x for x in list1)))


# def com():
#     tasks_list = mydb["tasks"]
#     task = ["empty"]
#     for i in tasks_list.find({}):
#         task.append(i["cmd_id"])
#     return task


def do_task(update: Update, context: CallbackContext):
    message_id = update.message.message_id
    text = update.message.text
    text_id = text.replace("/", '')
    chat_id = update.message.chat_id
    context.user_data["task_id"] = text_id
    context.user_data["chat_id"] = chat_id
    context.user_data["message_id"] = message_id
    find_task = mydb["tasks"]
    get = find_task.find_one({"cmd_id": text_id})
    if chat_id in get['done_by']:
        update.message.reply_text("You have already done this task!")
        return
    elif f"permit_{chat_id}" in get['pending']:
        update.message.reply_text("You already submitted this task!\n\n"
                                  "Pending approval without rejection will get auto approved"
                                  " after 24 hours of submission")
        return
        # keyboard = [["Submit Task", "Skip Task"]]
    reply_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton("Do task", callback_data="do"),
        InlineKeyboardButton("Close", callback_data="close")]])
    # reply_markup = ReplyKeyboardMarkup(keyboard,  one_time_keyboard=True , resize_keyboard=True)
    update.message.reply_text(f"Title: {get['title']}\n\n"
                              f"Description: {get['des']}\n\n"
                              f"Link: {get['link']}", reply_markup=reply_markup, timeout=10,
                              reply_to_message_id=message_id)


def task_select(update: Update, context: CallbackContext):
    if update.callback_query['data'] == "do":
        keyboard = [["Confirm Submit", "cancel"]]
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.sendMessage(chat_id=context.user_data['chat_id'],
                        text=f"Now send your task proof and click submit\nThis proof will send to task owner for verification",
                        reply_markup=markup)
        return TWO
    else:
        # bot.sendMessage(chat_id=context.user_data['chat_id'], text="Task Skipped")
        bot.editMessageText(chat_id=context.user_data['chat_id'], text="Task Skipped",
                            message_id=update.callback_query.message.message_id)
        return ConversationHandler.END


def get_photo(update: Update, context: CallbackContext):
    context.user_data["photo"] = update.message.photo[-1]
    context.user_data["caption"] = update.message.caption
    update.message.reply_text("Got it!")
    return THREE
    # update.message.reply_photo(photo=photo)


def confirm_task(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if update.message.text == "Confirm Submit":
        try:
            photo = context.user_data['photo']
        except:
            update.message.reply_text("Your document is empty!\n"
                                      "Please send me your proof of work")
            return TWO
        tasks = mydb['tasks']
        get = tasks.find_one({"cmd_id": context.user_data['task_id']})
        get_list = list(get['pending'])
        permit_id = f"permit_{context.user_data['task_id']}{chat_id}"
        get_list.append(permit_id)
        if str(context.user_data['caption']) == "None":
            bot.send_photo(chat_id=get["chat_id"], photo=photo,
                           caption=f"Click to approve-> /{permit_id}")
        else:
            bot.send_photo(chat_id=get["chat_id"], photo=photo,
                           caption=f"{context.user_data['caption']}\n\nClick to approve-> /{permit_id}")
        tasks.update_one({"cmd_id": context.user_data['task_id']}, {'$set': {'pending': get_list}})
        update.message.reply_text("Got your response and sent to task owner for verification")
        main_buttons(update, context)
        return ConversationHandler.END
    else:
        main_buttons(update, context)
        return ConversationHandler.END


CREATE, TITLE, TRX_TOTAL, TRX_PER, LINK, CONFIRM = range(6)


def task_new(update, context):
    chat_id = update.message.chat_id
    people = mydb["people"]
    get = people.find_one({"_id": chat_id})
    if get["TRX_balance"] >= 1:
        markup = ReplyKeyboardMarkup([["cancel"]], one_time_keyboard=True, resize_keyboard=True)
        bot.sendMessage(chat_id=chat_id, text="Send task title to go next step:", reply_markup=markup,
                        reply_to_message_id=update.message.message_id)
        return CREATE
    else:
        bot.sendMessage(chat_id=chat_id, text="You must have atleat more than 1 TRX to create task\n"
                                              "To create task deposit TRX to the bot")
        return ConversationHandler.END


def get_title(update, context):
    chat_id = update.message.chat_id
    title = update.message.text
    context.user_data["title"] = title
    if title == "cancel":
        main_buttons(update, context)
        return ConversationHandler.END
    bot.sendMessage(chat_id=chat_id, text="Enter total task budget of TRX")
    return TITLE


def get_total(update, context):
    chat_id = update.message.chat_id
    trx_total = update.message.text
    balance = mydb["people"]
    get = balance.find_one({"_id": chat_id})
    try:
        if trx_total == "cancel":
            main_buttons(update, context)
            return ConversationHandler.END
        elif float(trx_total) >= 1:
            if get["TRX_balance"] >= float(trx_total):
                update.message.reply_text("Enter how many TRX per task for the user")
                context.user_data["trx_total"] = trx_total
                return TRX_TOTAL
            else:
                update.message.reply_text("Insufficient balance...\n"
                                          f"Your TRX balance {get['TRX_balance']}")
                return TITLE
        else:
            update.message.reply_text("TRX budget must be greater than 1")
            return TITLE
    except:
        update.message.reply_text("TRX amount must be in numbers!")
        return TITLE


def get_per(update, context):
    chat_id = update.message.chat_id
    trx_per = update.message.text
    try:
        if trx_per == "cancel":
            main_buttons(update, context)
            return ConversationHandler.END
        elif float(trx_per) <= float(context.user_data["trx_total"]):
            if float(trx_per) >= 0.3:
                update.message.reply_text("Send Task description")
                context.user_data["trx_per"] = trx_per
                return TRX_PER
            else:
                update.message.reply_text("Task amount can't be less than 0.3 TRX")
                return TRX_TOTAL
    except:
        update.message.reply_text("TRX amount must be in numbers!")
        return TRX_TOTAL



def description(update, context):
    chat_id = update.message.chat_id
    des = update.message.text
    # trx_total = context.user_data["trx_total"]
    # trx_per = context.user_data["trx_per"]
    # title = context.user_data["title"]
    if des == "cancel":
        main_buttons(update, context)
        return ConversationHandler.END
    else:
        context.user_data["des"] = des
        update.message.reply_text("Send the link you want to promote")
        return LINK


def get_link(update, context):
    chat_id = update.message.chat_id
    link = update.message.text
    if link == "cancel":
        main_buttons(update, context)
        return ConversationHandler.END
    else:
        context.user_data["link"] = link
        markup = ReplyKeyboardMarkup([["Confirm", "cancel"]], one_time_keyboard=True, resize_keyboard=True)
        bot.sendMessage(chat_id=chat_id, text="Check task details once again and confirm:", reply_markup=markup)
        return CONFIRM


def sub_approve(title, trx_total, trx_per, link, des, chat_id):
    create_id = f"approve_{random.randint(100000, 999999)}"
    tasks = mydb['pending']
    cmd_id = f"task_{random.randint(100000, 999999)}"
    ind_time = datetime.datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M')
    tasks.insert_one({"chat_id": chat_id, "create_id": create_id, "title": title, "trx_total": trx_total,
                      "trx_per": trx_per, "link": link, "des": des, "limit": int(trx_total // trx_per),
                      "time": ind_time, "done": 0, "cmd_id": cmd_id, 'done_by': [], 'pending': []})
    bot.sendMessage(chat_id=1291659507, text=f"Task approve id:/{create_id}\n"
                                             f"Total budget: {trx_total}\n"
                                             f"TRX/user: {trx_per}\n"
                                             f"Users limit: {trx_total // trx_per}\n"
                                             f"title: {title}\n\n"
                                             f"Description:\n"
                                             f"{des}\n\n"
                                             f"link: {link}")


def confirm_create(update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    if text == "Confirm":
        title = context.user_data["title"]
        trx_total = context.user_data["trx_total"]
        trx_per = context.user_data["trx_per"]
        link = context.user_data["link"]
        des = context.user_data["des"]
        sub_approve(title, float(trx_total), float(trx_per), link, des, int(chat_id))
        detect = mydb["people"]
        get = detect.find_one({"_id": chat_id})
        trx = get["TRX_balance"] - float(trx_total)
        detect.update_one({"_id": chat_id}, {"$set": {"TRX_balance": trx}})
        bot.sendMessage(chat_id=chat_id, text="Task submitted to owner")
        main_buttons(update, context)
        return ConversationHandler.END
    elif text == "cancel":
        main_buttons(update, context)
        return ConversationHandler.END
    else:
        return CONFIRM


def approve_list():
    cmd = mydb["pending"]
    cmds = ["nothing"]
    for i in cmd.find({}):
        cmds.append(i["create_id"])
    return cmds


def commands(update, context):
    text = update.message.text
    after = text.replace("/", '')
    tasks = mydb["tasks"]
    if "approve" in text:
        pending = mydb['pending']
        get = pending.find_one({"create_id": after})
        if str(get) != "None":
            tasks.insert_one(get)
            pending.delete_one({"create_id": after})
            update.message.reply_text("Task permitted successfully")
    elif "permit_task_" in text:
        reuse = text.replace("/permit_task_", '')
        get_task_id = int(reuse[0:6])
        get_chat_id = int(reuse[6:])
        people = mydb['people']
        tasks = mydb['tasks']
        task_get = tasks.find_one({'cmd_id': f'task_{get_task_id}'})
        if str(task_get) != "None":
            done_by_list = list(task_get['done_by'])
            approve_list = list(task_get['pending'])
            try:
                reward = float(task_get['trx_per'])
                approve_list.remove(after)
                done_by_list.append(int(get_chat_id))
                tasks.update_one({"cmd_id": f'task_{get_task_id}'}, {'$inc': {"done": 1}})
                tasks.update_one({"cmd_id": f'task_{get_task_id}'}, {"$set": {"done_by": done_by_list}})
                tasks.update_one({"cmd_id": f'task_{get_task_id}'}, {'$set': {'pending': approve_list}})
                update.message.reply_text("Task approved!")
                people.update_one({'_id': get_chat_id}, {'$inc': {"TRX_balance": float(reward),
                                                                  "payout_avail": float(reward),
                                                                  "earned_total": float(reward)}})
            except:
                update.message.reply_text("Task already approved!")

    elif "task_" in text:
        get = tasks.find_one({'cmd_id': after})
        if str(get) != "None":
            do_task(update, context)


def main():
    updater = Updater("5123712096:AAFoWsAeO_sJyrsl0upMa-LUCeHE-k8AWYE", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    task = ConversationHandler(entry_points=[CallbackQueryHandler(task_select)],
                               states={TWO: [MessageHandler(Filters.photo, get_photo)],
                                       THREE: [MessageHandler(Filters.text, confirm_task)]
                                       }, fallbacks=[MessageHandler(Filters.text, confirm_task)])

    add_task = ConversationHandler(entry_points=[MessageHandler(Filters.text("Create TaskðŸ“œ"), task_new)],
                                   states={CREATE: [MessageHandler(Filters.text, get_title)],
                                           TITLE: [MessageHandler(Filters.text, get_total)],
                                           TRX_TOTAL: [MessageHandler(Filters.text, get_per)],
                                           TRX_PER: [MessageHandler(Filters.text, description)],
                                           LINK: [MessageHandler(Filters.text, get_link)],
                                           CONFIRM: [MessageHandler(Filters.text, confirm_create)]
                                           }, fallbacks=[]
                                   )
    dp.add_handler(task)
    dp.add_handler(add_task)
    dp.add_handler(MessageHandler(Filters.command, commands))
    dp.add_handler(MessageHandler(Filters.text, msg_hand))
    updater.start_polling()
    updater.idle()


main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

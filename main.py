import logging
import random

from telegram import (
    Update,
    ParseMode,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)

# ========= 在这里填你的机器人 TOKEN =========
TELEGRAM_TOKEN = "8014717607:AAFB0Y13VUNJqcVhH876v8Z-6j_KMYwoMyI"
# ==========================================
    

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------- 游戏数据 ----------

QUIZ_QUESTIONS = [
    {
        "q": "地球上面积最大的海洋是？",
        "options": ["A. 太平洋", "B. 大西洋", "C. 印度洋", "D. 北冰洋"],
        "answer": "A",
    },
    {
        "q": "一天有多少小时？",
        "options": ["A. 10", "B. 18", "C. 24", "D. 30"],
        "answer": "C",
    },
    {
        "q": "以下哪个是中国传统节日？",
        "options": ["A. 圣诞节", "B. 清明节", "C. 万圣节", "D. 感恩节"],
        "answer": "B",
    },
]

FORTUNES = [
    "大吉：今天状态很好，适合尝试新计划！",
    "中吉：一切顺利进行，保持节奏。",
    "小吉：有小收获，别太心急。",
    "平安：平平淡淡最幸福。",
    "小凶：注意情绪，别急躁。",
    "凶：保持低调，稳住不败。",
]

SPIN_RESULTS = [
    "今日幸运数字：" + str(random.randint(1, 99)),
    "今日幸运颜色：蓝色",
    "今天会遇到一个好消息～",
    "适合联系一位老朋友！",
    "早点休息，充满能量！",
    "喝杯水，保持心情愉快。",
]

CARDS = [
    "普通卡：平静的一天～",
    "普通卡：顺风顺水。",
    "稀有卡：你将遇到意外惊喜！",
    "稀有卡：好机会正在靠近！",
    "传说卡：好运爆棚，诸事顺利！",
    "传说卡：你是今天的幸运王！",
]

IDIOMS = [
    "一心一意",
    "意气风发",
    "发家致富",
    "富丽堂皇",
    "皇天后土",
    "土生土长",
    "长生不老",
    "老当益壮",
    "壮志凌云",
    "云开见月",
]

CARD_EMOJIS = ["🍎", "🍌", "🍒"]

AUTO_REPLIES = {
    "你好": "你好呀～需要我陪你玩点什么吗？😀",
    "hi": "Hi～我在的，随时可以玩小游戏！",
    "在吗": "我在！需要什么服务？",
    "干嘛": "陪你玩小游戏呀～猜数字、抽卡、抽签、转盘等都可以。",
    "机器人": "我是娱乐工具助手🤖～随时为你服务！",
    "你是谁": "我是你的娱乐搭子【娱乐工具助手】 🤖",
}

# ---------- 菜单 ----------
def menu_keyboard():
    keyboard = [
        [KeyboardButton("猜数字"), KeyboardButton("抽卡")],
        [KeyboardButton("抽签"), KeyboardButton("转盘")],
        [KeyboardButton("问答"), KeyboardButton("翻牌记忆")],
        [KeyboardButton("成语接龙")],
        [KeyboardButton("菜单"), KeyboardButton("帮助")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ---------- 基本命令 ----------
def start(update: Update, context: CallbackContext):
    text = (
        "欢迎使用【娱乐工具助手】🎉\n\n"
        "我可以陪你玩这些娱乐功能：\n"
        "• 猜数字\n"
        "• 抽卡\n"
        "• 抽签\n"
        "• 幸运转盘\n"
        "• 益智问答\n"
        "• 翻牌记忆\n"
        "• 成语接龙\n\n"
        "👇 点击下方按钮开始玩吧！"
    )
    update.message.reply_text(text, reply_markup=menu_keyboard())

def menu(update: Update, context: CallbackContext):
    update.message.reply_text("👇 请选择一个功能：", reply_markup=menu_keyboard())

def help_command(update: Update, context: CallbackContext):
    text = (
        "【使用说明】\n\n"
        "猜数字：/guess\n"
        "抽卡：/draw\n"
        "抽签：/fortune\n"
        "转盘：/spin\n"
        "问答：/quiz\n"
        "翻牌记忆：/flip\n"
        "成语接龙：/idiom\n"
    )
    update.message.reply_text(text)

# ---------- 猜数字（已修复 NoneType） ----------
def guess(update: Update, context: CallbackContext):
    user_data = context.user_data

    if not context.args:  
        num = random.randint(1, 100)
        user_data["guess_number"] = num
        update.message.reply_text(
            "🎯 猜数字游戏开始！我想了一个 1~100 的数字。\n"
            "用 `/guess 50` 这样来猜。",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if "guess_number" not in user_data:
        update.message.reply_text("请先输入 /guess 来开始游戏。")
        return

    try:
        guess_num = int(context.args[0])
    except ValueError:
        update.message.reply_text("请输入正确格式：/guess 50")
        return

    target = user_data["guess_number"]

    if guess_num < target:
        update.message.reply_text("太小了，再试试～")
    elif guess_num > target:
        update.message.reply_text("太大了，再试试～")
    else:
        update.message.reply_text(f"🎉 恭喜你猜对了！答案就是 {target}！")
        del user_data["guess_number"]

# ---------- 抽卡 ----------
def draw(update: Update, context: CallbackContext):
    update.message.reply_text("🃏 抽卡结果：\n" + random.choice(CARDS))

# ---------- 抽签 ----------
def fortune(update: Update, context: CallbackContext):
    update.message.reply_text("🔮 今日签文：\n" + random.choice(FORTUNES))

# ---------- 转盘 ----------
def spin(update: Update, context: CallbackContext):
    update.message.reply_text("🎡 幸运转盘结果：\n" + random.choice(SPIN_RESULTS))

# ---------- 问答 ----------
def quiz(update: Update, context: CallbackContext):
    q = random.choice(QUIZ_QUESTIONS)
    context.user_data["quiz"] = q

    text = f"🧠 问题：{q['q']}\n\n"
    for op in q["options"]:
        text += op + "\n"
    text += "\n请使用 `/answer A` 这种格式回答。"

    update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

def answer(update: Update, context: CallbackContext):
    if "quiz" not in context.user_data:
        update.message.reply_text("请先发送 /quiz 来出题。")
        return

    if not context.args:
        update.message.reply_text("请使用格式：/answer A")
        return

    q = context.user_data["quiz"]
    user_ans = context.args[0].upper()

    if user_ans == q["answer"].upper():
        update.message.reply_text("✅ 回答正确！👍")
    else:
        update.message.reply_text(f"❌ 回答错误，正确答案是：{q['answer']}")

    del context.user_data["quiz"]

# ---------- 成语接龙 ----------
def idiom(update: Update, context: CallbackContext):
    chain = random.sample(IDIOMS, min(5, len(IDIOMS)))
    update.message.reply_text("🀄 成语接龙：\n" + " ➜ ".join(chain))

# ---------- 翻牌记忆（已修复 NoneType） ----------
def new_flip_game(context: CallbackContext):
    cards = CARD_EMOJIS * 2
    random.shuffle(cards)
    context.user_data["flip_cards"] = cards
    context.user_data["flip_open"] = [False] * 6
    context.user_data["flip_step"] = []

def flip(update: Update, context: CallbackContext):
    user_data = context.user_data

    if "flip_cards" not in user_data:
        new_flip_game(context)
        update.message.reply_text(
            "🧩 翻牌记忆游戏开始！共有 6 张牌（3 对）。\n"
            "使用 `/flip 1` 翻牌。",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if not context.args:
        update.message.reply_text("请输入格式：/flip 1～6")
        return

    try:
        idx = int(context.args[0]) - 1
    except ValueError:
        update.message.reply_text("请输入数字编号，例如：/flip 2")
        return

    if idx < 0 or idx >= 6:
        update.message.reply_text("编号范围是 1～6")
        return

    cards = user_data["flip_cards"]
    opened = user_data["flip_open"]
    step = user_data["flip_step"]

    if opened[idx]:
        update.message.reply_text("这张牌已经翻开啦～")
        return

    step.append(idx)
    update.message.reply_text(f"你翻开的是：{cards[idx]}")

    if len(step) == 2:
        i, j = step

        if cards[i] == cards[j]:
            opened[i] = opened[j] = True
            update.message.reply_text("⭕ 配对成功！")
        else:
            update.message.reply_text("❌ 没配对成功～继续努力！")

        user_data["flip_step"] = []

        if all(opened):
            update.message.reply_text("🎉 所有牌都配对成功！游戏结束～")
            del user_data["flip_cards"]
            del user_data["flip_open"]
            del user_data["flip_step"]

# ---------- 群欢迎 ----------
def welcome(update: Update, context: CallbackContext):
    for member in update.message.new_chat_members:
        update.message.reply_text(
            f"欢迎 {member.full_name} 🎉\n"
            "我是娱乐工具助手～下面有按钮可以玩小游戏 👇",
            reply_markup=menu_keyboard(),
        )

# ---------- 自动回复 ----------
def auto_reply(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    for key, val in AUTO_REPLIES.items():
        if key in text:
            update.message.reply_text(val, reply_markup=menu_keyboard())
            return

# ---------- 按钮处理（最终修复：全部用中文识别） ----------
def handle_buttons(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    if "猜数字" in text:
        return guess(update, context)
    if "抽卡" in text:
        return draw(update, context)
    if "抽签" in text:
        return fortune(update, context)
    if "转盘" in text:
        return spin(update, context)
    if "问答" in text:
        return quiz(update, context)
    if "翻牌记忆" in text:
        return flip(update, context)
    if "成语接龙" in text:
        return idiom(update, context)
    if "菜单" in text:
        return menu(update, context)
    if "帮助" in text:
        return help_command(update, context)

# ---------- 主程序 ----------
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    # 命令
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("guess", guess))
    dp.add_handler(CommandHandler("draw", draw))
    dp.add_handler(CommandHandler("fortune", fortune))
    dp.add_handler(CommandHandler("spin", spin))
    dp.add_handler(CommandHandler("quiz", quiz))
    dp.add_handler(CommandHandler("answer", answer))
    dp.add_handler(CommandHandler("idiom", idiom))
    dp.add_handler(CommandHandler("flip", flip))

    # 按钮（核心）
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_buttons))

    # 自动回复
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, auto_reply))

    # 欢迎语
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

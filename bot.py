from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ---------- CONFIG ----------
BOT_TOKEN = "8376326046:AAG8hvCJVfMv3TbtIFuKWl9gMsU8kkhDL7E"

YOUTUBE_LINK = "https://youtube.com/@spd111-ff?si=Bk4OExSdHDcm3d1N"

LEVELUP_LINK = "https://gplinks.co/hGd1fUT"
GUILD_LINK = "https://gplinks.co/HJ33gX"

user_state = {}
# -----------------------------


# --------- MAIN MENU ----------
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 Level Up", callback_data="levelup")],
        [InlineKeyboardButton("🏰 Guild", callback_data="guild")],
        [InlineKeyboardButton("❌ Exit", callback_data="exit_main")]
    ]

    await update.message.reply_text(
        "👋 Welcome to SPeeD 111 Bot!\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# --------- BUTTON HANDLER ----------
async def button_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    data = query.data

    # ---- LEVEL UP ----
    if data == "levelup":
        user_state[uid] = "waiting_levelup"
        await query.message.reply_text(
            f"📢 *Subscribe To SPeeD 111*\n\n👉 {YOUTUBE_LINK}\n\n⚠️ Click the link first!",
            parse_mode="Markdown"
        )

    # ---- GUILD ----
    elif data == "guild":
        user_state[uid] = "waiting_guild"
        await query.message.reply_text(
            f"📢 *Subscribe To SPeeD 111*\n\n👉 {YOUTUBE_LINK}\n\n⚠️ Click the link first!",
            parse_mode="Markdown"
        )

    # ---- EXIT: Main Menu ----
    elif data == "exit_main":
        user_state.pop(uid, None)
        await show_menu(update, context)


# --------- AFTER CLICK MESSAGE ----------
async def after_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id

    # যদি কোনো স্টেট না থাকে → আবার মেইন মেনু দেখাবে
    if uid not in user_state:
        return await show_menu(update, context)

    state = user_state[uid]

    if state == "waiting_levelup":
        await update.message.reply_text(f"🔗 Your LevelUp Link:\n{LEVELUP_LINK}")
        user_state.pop(uid, None)

    elif state == "waiting_guild":
        await update.message.reply_text(f"🔗 Your Guild Link:\n{GUILD_LINK}")
        user_state.pop(uid, None)


# --------- RUN BOT ----------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # ▶️ Auto Menu when entering bot (/start)
    app.add_handler(CommandHandler("start", show_menu))

    # Text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, after_message))

    # Buttons
    app.add_handler(CallbackQueryHandler(button_actions))

    print("Bot is Running…")
    app.run_polling()


if __name__ == "__main__":
    main()
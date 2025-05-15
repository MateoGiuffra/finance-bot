from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackContext, ConversationHandler,
    MessageHandler, filters
)
from telegram import Update
from app.FinanceSheetManager import FinanceSheetManager
from app.OCR import get_the_ticket_total
from config.sheet_client import spreadsheet, worksheet
from tickets.app_config import TOKEN
import os


NAME, CATEGORIES, GET_CATEGORY, GET_IMAGE = range(4)

finance_manager = None


def set_ticket_total(image_path: str) -> str:
    try:
        total = get_the_ticket_total(image_path)
        print("Total found:", total)
        if total is None:
            raise ValueError("No total found in the image!!!!.")
        return total
    except Exception as e:
        print(f"Error processing image: {e}")
        raise RuntimeError("Error processing image") from e


async def start_command(update: Update, context: CallbackContext):
    if update.message is None:
        return
    await update.message.reply_text("Welcome! Please send your name to set the worksheet.")
    return NAME

async def receive_name(update: Update, context: CallbackContext):
    global finance_manager
    finance_manager = FinanceSheetManager(update.message.text.strip(), spreadsheet, worksheet, []) if finance_manager == None else finance_manager
    await update.message.reply_text("Now send your categories separated by commas.")
    return CATEGORIES

async def receive_categories(update: Update, context: CallbackContext):
    raw = update.message.text
    categories = [cat.strip() for cat in raw.split(",") if cat.strip()]
    if not categories:
        await update.message.reply_text("Invalid categories. Please try again.")
        return CATEGORIES
    global finance_manager
    finance_manager.set_columns(categories)
    print("Categories set:", finance_manager.columns)
    await update.message.reply_text("Excelent! Your categories have been set. Now you can use the bot to send tickets and get totals.")
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

# Other commands

async def help_command(update: Update, _: CallbackContext):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/send - Write a category and send a ticket image\n"
        "/getsheet - Get the sheet link\n"
        "todo:\n"
        "/totalcategory - Get total of a category\n"
        "/total - Get total of all categories\n"
    )

async def start_send(update: Update, context: CallbackContext):
    await update.message.reply_text("Please write the category for this ticket.")
    return GET_CATEGORY

async def get_category(update: Update, context: CallbackContext):
    context.user_data["category"] = update.message.text
    await update.message.reply_text("Now please send the ticket image.")
    return GET_IMAGE

async def get_image(update: Update, context: CallbackContext):
    if not update.message.photo:
        await update.message.reply_text("Please send a valid image.")
        return GET_IMAGE

    category = context.user_data["category"]
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)

    os.makedirs("tickets", exist_ok=True)
    path = f"tickets/{photo.file_id}.jpg"
    await file.download_to_drive(path)

    try:
        total = set_ticket_total(path)
        url = finance_manager.sum_or_create(total, category)
        await update.message.reply_text(
            f"✅ Ticket processed.\nCategory: {category}\nTotal: {total}\nSaved at: {url}"
        )
    except Exception as e:
        print(f"Error processing ticket: {e}")
        await update.message.reply_text(f"❌ Something went wrong, try again later.")

    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Ticket submission cancelled.")
    return ConversationHandler.END

async def get_url_command(update: Update, _: CallbackContext):
    await update.message.reply_text(f"You can find your sheet here: {finance_manager.get_url()}")

async def get_total_of_category_command(update: Update, _: CallbackContext):
    return finance_manager.get_total_of_category(update.message.text)

async def get_total_command(update: Update, _: CallbackContext):
    """
    Get the total of all categories of the current month.
    """
    return finance_manager.get_total_of_all_categories()

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Conversation para el comando /start
    start_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
            CATEGORIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_categories)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Conversation para el comando /send
    send_ticket_conv = ConversationHandler(
        entry_points=[CommandHandler("send", start_send)],
        states={
            GET_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_category)],
            GET_IMAGE: [MessageHandler(filters.PHOTO, get_image)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(start_conv_handler)
    application.add_handler(send_ticket_conv)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("totalcategory", get_total_of_category_command))
    application.add_handler(CommandHandler("total", get_total_command))
    application.add_handler(CommandHandler("getsheet", get_url_command))

    print("Bot started. Listening for messages...")
    application.run_polling()
    print("Bot stopped.")
# 
if __name__ == "__main__":
    main()

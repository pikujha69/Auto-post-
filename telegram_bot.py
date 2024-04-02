import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import requests

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot's API token
TOKEN = '6927052523:AAEQOBNb9GQ-ymbcp0iVyobgDsv1CqUUdjE'

# Your main channel chat_id
MAIN_CHANNEL_CHAT_ID = '-1002075070793'

# Dictionary of target channels and their corresponding chat_ids
TARGET_CHANNELS = {
    'Channel 1': '-1002041790711',
    'Channel 2': '-1002133702625'
}

# Function to start the bot
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Bot started! Fetching and posting messages every hour.')

    # Start the job to fetch and post messages every hour
    context.job_queue.run_repeating(fetch_and_post_messages, interval=3600, first=0)

# Function to fetch and post messages
def fetch_and_post_messages(context: CallbackContext) -> None:
    """Fetch messages from the main channel and repost to target channels."""
    try:
        # Fetching messages from the main channel
        response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getChatHistory?chat_id={MAIN_CHANNEL_CHAT_ID}&limit=5")
        messages = response.json()['result']['messages']
        
        # Posting messages to target channels
        for message in messages:
            for channel_name, channel_chat_id in TARGET_CHANNELS.items():
                context.bot.send_message(chat_id=channel_chat_id, text=message['text'])
    except Exception as e:
        logger.error(f"An error occurred: {e}")

# Function to handle errors
def error(update: Update, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Main function
def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add command handler for /start
    dp.add_handler(CommandHandler("start", start))

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()

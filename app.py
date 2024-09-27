from flask import Flask, request
import telebot
import random
import string
import uuid
import requests

# Your Telegram bot token
TOKEN = '7822965732:AAGuyrZAolVUHN88it8DSkbT9LBEM5_-hHg'

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

class InstagramPasswordReset:
    def __init__(self, username):
        self.target = username
        self.prepare_data()

    def prepare_data(self):
        # Checking if the input contains '@' to differentiate between email and username
        if "@" in self.target:
            self.data = {
                "_csrftoken": "".join(
                    random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=32)
                ),
                "user_email": self.target,
                "guid": str(uuid.uuid4()),
                "device_id": str(uuid.uuid4())
            }
        else:
            self.data = {
                "_csrftoken": "".join(
                    random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=32)
                ),
                "username": self.target,
                "guid": str(uuid.uuid4()),
                "device_id": str(uuid.uuid4())
            }

        self.send_password_reset()

    def send_password_reset(self):
        # Random string for user-agent
        random_device_info = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
        head = {
            "user-agent": f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; {random_device_info}/{random_device_info}; {random_device_info}; {random_device_info}; en_GB;)"
        }

        # Proxies to use for the request
        proxies = {
            "http": "http://hkkqxzia-rotate:h8kgwqbiwytr@p.webshare.io:80/",
            "https": "http://hkkqxzia-rotate:h8kgwqbiwytr@p.webshare.io:80/"
        }

        # Sending the password reset request through the proxy
        try:
            req = requests.post(
                "https://i.instagram.com/api/v1/accounts/send_password_reset/",
                headers=head,
                data=self.data,
                proxies=proxies  # Pass proxies here
            )

            # Checking the response and returning the result
            if "obfuscated_email" in req.text:
                response_data = req.json()
                return f"Please check {response_data['obfuscated_email']} for a link to reset your password."
            else:
                return "Failed to send password reset. Please check the username or try again later."
        except requests.RequestException as e:
            # Handle any request-related errors
            return f"Error sending password reset request: {str(e)}"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        json_str = request.get_data(as_text=True)
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return 'ok', 200
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

# Command handler for /reset command
@bot.message_handler(commands=['reset'])
def handle_reset(message):
    try:
        # Extract the username from the message
        username = message.text.split()[1]  # /reset username

        # Check if the username starts with '@' and ask the user to remove it
        if username[0] == "@":
            bot.reply_to(message, "Please enter the username without '@'.")
        else:
            # Create an instance of InstagramPasswordReset class
            reset_handler = InstagramPasswordReset(username)
            
            # Get the reset message and reply to the user
            reset_message = reset_handler.send_password_reset()
            bot.reply_to(message, reset_message)

    except IndexError:
        bot.reply_to(message, "Please provide a valid username. Example: /reset username")

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app.run()

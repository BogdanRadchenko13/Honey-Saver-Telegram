# pip install pyTelegramBotAPI yt-dlp

import threading
import telebot
from yt_dlp import YoutubeDL
import os
from flask import Flask

TOKEN = '8025791518:AAEw7CYa_UW-ueEOKyzOG4g8sX7b_5K79DQ'
bot = telebot.TeleBot(TOKEN)

ydl_opts = {
    'format': 'best',
    'outtmpl': 'downloaded_video.%(ext)s',
    'quiet': True,
    'no_warnings': True,
}

@bot.message_handler(commands=['start'])
def start_message(message):
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name
    bot.send_message(message.chat.id, f" Привет {first_name} {last_name}! \n \n Это Чат-Бот для скачивания видео с TikTok прямо в Telegram! Просто кинь ссылку на видео, и Бот - Загрузит.")

app = Flask('')

@app.route('/')
def home():
    return "✅ Бот работает!"

def run():
    app.run(host='0.0.0.0', port=8080)

# --- Запуск Flask в отдельном потоке ---
def keep_alive():
    t = threading.Thread(target=run)
    t.start()

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    
    # Проверяем, что это ссылка на TikTok
    if 'tiktok.com' not in url:
        bot.send_message(message.chat.id, " Пожалуйста, отправь ссылку именно с TikTok.")
        return
    
    msg = bot.send_message(message.chat.id, " Видео скачиваеться...")
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_filename = ydl.prepare_filename(info)
        
        with open(video_filename, 'rb') as video:
            bot.send_video(message.chat.id, video)
        
        os.remove(video_filename)
        bot.edit_message_text(" Видео успешно скачано и отправлено!", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f" Ошибка при скачивании видео: {str(e)}", message.chat.id, msg.message_id)

keep_alive()
bot.polling()
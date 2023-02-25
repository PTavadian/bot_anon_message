
class Text:

    reply = {'reply_1': {'en': 'Send nothing!', 'ru': 'Нечего отправлять!'},
            'reply_2': {'en': 'Where to send?', 'ru': 'Куда отправить?'},
            'reply_3': {'en': 'Anything else?', 'ru': 'Что-нибудь еще?'},
            'reply_4': {'en': 'This group does not use a bot. Click: /Help', 'ru': 'Эта группа не использует бота. Нажмите: /Help'},
            'reply_5': {'en': 'Sending error. Check the bot\'s permissions.', 'ru': 'Ошибка отправления. Проверьте права бота.'},
            'reply_6': {'en': 'Ok', 'ru': 'Как скажешь'},
            'reply_7': {'en': 'Bot activated', 'ru': 'Бот активирован'},
            'reply_8': {'en': 'Make the bot a group admin, then activate it with a team: /add', 'ru': 'Сделай бота администратором группы, затем активируй командой: /add'},
            'reply_9': {'en': 'Ready', 'ru': 'Готово'},
            'reply_10': {'en': '''The bot can send on its own behalf:
     - your message
     - photos and videos
     - audio files
     - a voice message
     - survey
     - documentation

To get started:
1. Add him to your group
2. Make it an administrator
3. Activate with command: /add

To remove a group from the list, use the command: /delete''',


                        'ru': '''Бот может отправлять от своего имени:
    - ваше сообщение
    - фотографии и видео
    - аудиофайлы
    - голосовое сообщение
    - опрос
    - документы

Для начала работы:
1. Добавте его в свою группу 
2. Сделайте администратором
3. Активируйте командой: /add

Для удаления группы из списка - воспользуйся командой /delete'''},
            'reply_11': {'en': 'Delete?', 'ru': 'Удалить?'},
            'reply_12': {'en': 'Which group to remove?', 'ru': 'Какую группу удалить?'},
            'reply_13': {'en': 'Choose a group', 'ru': 'Выбери группу'},
            'reply_14': {'en': 'Add files of the same type', 'ru': 'Добавляй файлы одного типа'}}



    def get_msg(self, msg=None, language=None):

        if language == 'ru':
            self.msg = self.reply[msg]['ru']
        else:
            self.msg = self.reply[msg]['en']

        return self.msg
            











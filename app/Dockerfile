FROM python:latest


WORKDIR /app


RUN pip install SQLAlchemy==2.0.20

RUN pip install aiogram==2.25.1

RUN pip install python-dotenv==1.0.0

RUN pip install redis==5.0.0


COPY . .

CMD [ "python", "bot_telegram.py" ]


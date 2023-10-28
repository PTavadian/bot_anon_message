from dotenv import load_dotenv
import os

load_dotenv()

ADMIN_ID = os.environ.get('ADMIN_ID').split(', ')
IS_DOCKER = True if os.environ.get('IS_DOCKER') == 'True' else False # тип запуска


import os

from startup.createapp import create_app_and_api
from dotenv import load_dotenv


load_dotenv()
app, api = create_app_and_api(os.getenv("FLASK_APP_ENV"))

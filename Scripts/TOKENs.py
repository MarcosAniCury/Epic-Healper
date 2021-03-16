from boto.s3.connection import S3Connection
import os
from dotenv import load_dotenv

s3 = S3Connection(os.environ['DISCORD_API_KEY'], os.environ['MONGO_URL_CONNECTION'])
load_dotenv()

def get_token():
    return os.environ['DISCORD_API_KEY'] if os.environ['DISCORD_API_KEY'] != ""  else os.getenv('DISCORD_API_KEY') 
     

def get_tokenCrud():
    return os.environ['MONGO_URL_CONNECTION'] if os.environ['MONGO_URL_CONNECTION'] != ""  else os.getenv('MONGO_URL_CONNECTION') 

def get_prefix():
    return "t "
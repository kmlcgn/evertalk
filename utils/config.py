BOT_TOKEN = "5" # Your Telegram bot token
STRING_SESSION = [] # Pyrogram string session. Seperate sessions with comma.
SESSION_USER_ID = [] # User ID of above string session. Add as int. Need to be a list
API_ID = "" # Your Telegram api id
API_HASH = "" # Your Telegram api hash
MONGO_DB = "" # Put your mongodb url
SUDO_ID = "" #475842612 IDs of users who want to give bot control, Seperate ids with a space
OPENAI_KEY = "" #Open AI API KEY

"""
Example to put STRING_SESSION and SESSION_USER_ID

Put your string session with secific name as tuple. You can seperate them using comma. Like below
STRING_SESSION = [("anyshortname","stringsession"),("anithername","othersession")]

Example :
SESSION_USER_ID = [124567,123444]
"""
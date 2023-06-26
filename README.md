# Auto Responder Bot
### Guide to use the bot

- Before use the bot you need to get telegram bot token, api id, api hash, string session for user account in pyrogram, mongodb url, open ai key for chatgpt. Then fill them in `utils/config.py` file. Enter your id as `SUDO_ID` as a string. If you have many ids you can sperate them with a space.
Add user id of user account as int which used to generate string session as `SESSION_USER_ID` in config.

- Commands like `help`, `filter`, `filters`, `delfilter`, `clearfilter` only recognize only ids that added to `SUDO_ID`.

- The bot genereate responded using ChatGPT for added filters and the useraccount which used to generate string session will send the reply message.

- You can always get messages in mongo db as all messages are stored in mongo db.

- What you have to do finally is hosting the bot. If you using github and heroku, you can simply upload the files to github. Then edit config. After that you can create app in heroku and connect github repo. Finally click on deploy. Then the bot should work.

#### How to add configs
First go to `utils/config.py`. Then you can add your own values
```
BOT_TOKEN - Your Telegram bot token
STRING_SESSION  - Pyrogram string session. For more info check below.
SESSION_USER_ID - User ID of above string sessions. Add as int into the list. For more info, check below.
API_ID - Your Telegram api id
API_HASH - Your Telegram api hash
MONGO_DB - Put your mongodb url
SUDO_ID - IDs of users who want to give bot control, Seperate ids with a space
OPENAI_KEY- Open AI API KEY for ChatGPT
```
_Note: `SESSION_USER_ID` should be an `integer` and the other all values should be `string`._

#### How to add string session
Adding string session is somewhat advanced due to using mutiply accounts.
```
Put your string session with secific name as tuple. You can seperate them using comma. Like below
STRING_SESSION = [("anyshortname","stringsession"),("anithername","othersession")]

Using your virtual number telegram accounts get their account ids and add as follow in config.
SESSION_USER_ID = [12345678,12344353]
```

#### When you need to give auto reply without filtering, You can rename `bot.py` to `backup_bot.py` and rename `bot_nofilter.py` to `bot.py`
from pyrogram import Client

API_ID = int(input("Enter APP ID here: "))
API_HASH = input("Enter API HASH here: ")

with Client("Sessiongen", API_ID, API_HASH, in_memory=True) as bot :
    session = bot.export_session_string()
    print(session)
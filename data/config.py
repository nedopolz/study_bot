import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
IMGBBKEY = str(os.getenv("IMGBBKEY"))
QIWI_TOKEN = str(os.getenv("QIWI_TOKEN"))
WALLET_QIWI = str(os.getenv("WALLET_QIWI"))
QIWI_PUBKEY = str(os.getenv("QIWI_PUBKEY"))
DATABASE = os.getenv("DATABASE")
ip = os.getenv("ip")

admins = [
    419519710, 362089194
]
referal_bonus = 10

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}

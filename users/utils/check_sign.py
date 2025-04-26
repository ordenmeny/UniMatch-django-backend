# utils.py
import hmac
import hashlib

def check_telegram_auth(data: dict, bot_token: str) -> bool:
    data = data.copy()

    email = data.pop('email')
    check_hash = data.pop('hash')
    sorted_data = sorted([f"{k}={v}" for k, v in data.items()])
    data_string = '\n'.join(sorted_data)
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    hmac_hash = hmac.new(secret_key, data_string.encode(), hashlib.sha256).hexdigest()
    return hmac_hash == check_hash

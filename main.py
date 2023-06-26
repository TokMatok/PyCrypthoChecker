import threading
import requests
from eth_keys import keys
from eth_utils import decode_hex
from bip_utils import Bip44, Bip44Coins
from bip_utils import EthAddr

# Функция для чтения приватных ключей из файла
def read_private_keys(filename):
    with open(filename, 'r') as file:
        private_keys = file.read().splitlines()
    return private_keys

# Функция для получения адреса из приватного ключа
def get_address(private_key_hex):
     private_key = keys.PrivateKey(decode_hex(private_key_hex))
     adress = private_key.public_key.to_checksum_address()
     return adress


# Функция для проверки баланса адреса
def check_balance(address):
    api_url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest"
    response = requests.get(api_url)
    if response.status_code == 200:
        balance = int(response.json()['result']) / 10**18  # Преобразование из Wei в ETH
        return balance

# Функция для обработки каждого приватного ключа и проверки баланса
def process_private_key(private_key):
    address = get_address(private_key)
    balance = check_balance(address)
    print(f"Адрес: {address}, Баланс: {balance} ETH")

# Основная функция
def main():
    filename = "private_keys.txt"  # Имя файла с приватными ключами
    private_keys = read_private_keys(filename)

    threads = []
    for private_key in private_keys:
        thread = threading.Thread(target=process_private_key, args=(private_key,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("Проверка баланса завершена")

if __name__ == "__main__":
    main()

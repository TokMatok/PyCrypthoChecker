import threading
import requests

from bip_utils import Bip44, Bip44Coins, Bip44Eth
from bip_utils import EthAddr
from eth_utils import remove_0x_prefix

# Функция для чтения приватных ключей из файла
def read_private_keys(filename):
    with open(filename, 'r') as file:
        private_keys = file.read().splitlines()
    return private_keys

# Функция для получения адреса из приватного ключа
def get_address(private_key):
    
    private_key = remove_0x_prefix(private_key) # Удаление префикса "0x" из приватного ключа, если присутствует
    bip44_eth = Bip44.FromPrivateKeyBytes(bytes.fromhex(private_key), Bip44Coins.ETH) # Создание экземпляра Bip44Eth с использованием приватного ключа
    # Получение адреса
    address_bytes = bip44_eth.PublicKey().ToBytes()
    address = EthAddr.EncodeKey(address_bytes)
    return address


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

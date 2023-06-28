import asyncio
import aiohttp
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
     address = private_key.public_key.to_checksum_address()
     return address

# Асинхронная функция для проверки баланса адреса
async def check_balance(session, address):
    api_url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest"
    async with session.get(api_url) as response:
        if response.status == 200:
            json_response = await response.json()
            balance = int(json_response['result']) / 10**18  # Преобразование из Wei в ETH
            return balance

# Асинхронная функция для обработки каждого приватного ключа и проверки баланса
async def process_private_key(session, private_key):
    address = get_address(private_key)
    balance = await check_balance(session, address)
    print(f"Адрес: {address}, Баланс: {balance} ETH")


async def main():
    filename = "private_keys.txt" 
    private_keys = read_private_keys(filename)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for private_key in private_keys:
            task = process_private_key(session, private_key)
            tasks.append(task)
            await asyncio.sleep(0.2) 
        await asyncio.gather(*tasks)

    print("Проверка баланса завершена")

if __name__ == "__main__":
    asyncio.run(main())

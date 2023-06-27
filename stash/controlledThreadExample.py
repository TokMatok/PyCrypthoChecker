from concurrent.futures import ThreadPoolExecutor

# Основная функция
def main():
    filename = "private_keys.txt"  # Имя файла с приватными ключами
    private_keys = read_private_keys(filename)

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_private_key, private_keys)

    print("Проверка баланса завершена")

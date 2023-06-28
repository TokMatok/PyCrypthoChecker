from concurrent.futures import ThreadPoolExecutor

def main():
    filename = "private_keys.txt" 
    private_keys = read_private_keys(filename)

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_private_key, private_keys)

    print("Проверка баланса завершена")

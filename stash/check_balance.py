def check_balance(address):
    try:
        api_url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={API_KEY}"
        response = requests.get(api_url)
        response.raise_for_status()
        balance = int(response.json()['result']) / 10**18  # Преобразование из Wei в ETH
        return balance
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при обращении к API: {e}")
    except ValueError:
        print("Ошибка при преобразовании баланса")
    return None

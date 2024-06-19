import requests
import json
from urllib.parse import parse_qs
from colorama import Fore, Style, init
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

init()

def convert_unix_to_regular(unix_timestamp):
    time = datetime.datetime.fromtimestamp(unix_timestamp)
    regular_time = time.strftime('%Y-%m-%d %H:%M:%S')
    return regular_time

def process_key(key_data):
    url = 'https://api.cyberfin.xyz/api/v1/game/initdata'
    headers = {
        'Content-Length': '306',
        'Sec-Ch-Ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
        'Accept': 'application/json',
        'Secret-Key': 'cyberfinance',
        'Content-Type': 'application/json',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Origin': 'https://g.cyberfin.xyz',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://g.cyberfin.xyz/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Priority': 'u=1, i',
    }
    payload = {"initData": key_data}
    response = requests.post(url, headers=headers, json=payload)

    try:
        json_response = response.json()
        access_token = json_response['message']['accessToken']
        print(f"{Fore.YELLOW}Access Token={access_token}{Style.RESET_ALL}")

        query_params = parse_qs(key_data)
        user_info = json.loads(query_params['user'][0])
        first_name = user_info.get('first_name', 'N/A')
        last_name = user_info.get('last_name', 'N/A')
        full_name = f"{first_name} {last_name}"
        print(f"{Fore.GREEN}================Full Name: {full_name}================{Style.RESET_ALL}")

        game_data_url = "https://api.cyberfin.xyz/api/v1/game/mining/gamedata"
        game_data_url_headers = {
            'Authorization': f'Bearer {access_token}'
        }
        game_response = requests.get(game_data_url, headers=game_data_url_headers)
        data = game_response.json()

        # Convert UNIX timestamps to regular datetime
        last_claim_time = convert_unix_to_regular(data['message']['miningData']['lastClaimTime'])
        crack_time = convert_unix_to_regular(data['message']['miningData']['crackTime'])

        print(f"{Fore.BLUE}Mining Data:")
        print(f"Last Claim Time: {last_claim_time}")
        print(f"Mining Rate: {data['message']['miningData']['miningRate']}")
        print(f"Crack Time: {crack_time}\n")

        print(f"{Fore.BLUE}User Data:")
        print(f"Balance: {data['message']['userData']['balance']}")
        print(f"Tokens: {data['message']['userData']['tokens']}\n")

        print(f"{Fore.BLUE}League Distribution:")
        for league in data['message']['leagueDistribution']:
            print(f"{league['league'].capitalize()}: More than {league['moreThan']}")
        print(Style.RESET_ALL)

        claim_url = 'https://api.cyberfin.xyz/api/v1/mining/claim'
        claim_headers = {
            'Authorization': f'Bearer {access_token}'
        }
        claim_response = requests.get(claim_url, headers=claim_headers)

        if claim_response.status_code == 200:
            print(f"{Fore.GREEN}Claim Result:")
            print(f"Status: Claim successful")
        elif claim_response.status_code == 400:
            print(f"{Fore.YELLOW}Claim Result:")
            print(f"Status: Already claimed")
        else:
            print(f"{Fore.RED}Claim Result:")
            print(f"Status: Unknown")

    except json.decoder.JSONDecodeError:
        print("Response is not in JSON format")

print(f"{Fore.RED}===============Hello sir deyan! Welcome back================{Style.RESET_ALL}")

with open('key.txt', 'r') as file:
    key_data_lines = file.readlines()

print(f"{Fore.YELLOW}================Sedang mengambil token... tunggu ya :)================{Style.RESET_ALL}")

with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(process_key, key_data.strip()) for key_data in key_data_lines]
    for future in as_completed(futures):
        future.result()  # wait for each thread to complete and catch any exceptions

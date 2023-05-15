import requests
import configparser


CONFIG_PATH = 'config.ini'  
CONFIG = configparser.RawConfigParser()
CONFIG.read(CONFIG_PATH)

API_KEY = str(CONFIG.get('steam', 'STEAM_API_KEY'))
ADDRESS = str(CONFIG.get('steam', 'SERVER_IP'))
PORT = str(CONFIG.get('steam', 'SERVER_PORT'))
APP_ID = 730  #csgo

def server_update():
    # Construct the URL to retrieve server information for the specified App ID
    url = f"https://api.steampowered.com/ISteamApps/GetServersAtAddress/v1/?addr={ADDRESS}:{PORT}&format=json&appid={APP_ID}&key={API_KEY}"

    # Make the API request and retrieve the server information
    response = requests.get(url)

    if response.status_code == 200:
        server_info = response.json()
    else:
        print(f"Error retrieving server information (status code {response.status_code})")
        return None

    # Construct the URL to retrieve server information for the specified server IP and port
    url = f"https://api.steampowered.com/IGameServersService/GetServerList/v1/?key={API_KEY}&filter=addr\{ADDRESS}:{PORT}"

    # Make the API request and retrieve the server information
    response = requests.get(url)

    if response.status_code == 200:
        server_info = response.json()["response"]["servers"][0]
        server_name = server_info['name']
        map_name = server_info['map']
        player_count = f"{server_info['players']}/{server_info['max_players']}"
        ip_address = server_info['addr']
        map = server_info['map']
        return {'server_name': server_name, 'map_name': map_name, 'player_count': player_count, 'ip_address': ip_address, 'map': map}
    else:
        print(f"Error retrieving server information (status code {response.status_code})")
        return None
    
def print_server_info():
    server_info = server_update()
    if server_info:
        print(f"Server name: {server_info['server_name']}")
        print(f"Map name: {server_info['map_name']}")
        print(f"Player count: {server_info['player_count']}")
        print(f"IP Address: {server_info['ip_address']}")
        print(f"Map: {server_info['map']}")
    else:
        print("Failed to retrieve server information.")

#print_server_info()
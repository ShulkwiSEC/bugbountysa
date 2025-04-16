import requests
import json
from core.programs import fetch_programs, save_programs
from core.utils import save_programs, save_scopes
from core.analysis import analyze_scope
from colorama import init, Fore, Style
from datetime import datetime
from core.config import Config
import sys

API_ENDPOINT = Config.API_ENDPOINT
HEADERS = Config.HEADERS
OUTPUT_DIR = Config.OUTPUT_DIR

def fetch_scopes(id):
    try:
        response = requests.get(API_ENDPOINT + f'/{id}', headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}[!] Timeout while fetching scope for ID {id}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[!] Error fetching scope for ID {id}: {str(e)}")
        return None
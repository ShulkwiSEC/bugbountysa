import requests
import json
from core.utils import save_programs, save_scopes
from core.analysis import analyze_scope
from colorama import init, Fore, Style
from datetime import datetime
from core.config import Config

API_ENDPOINT = Config.API_ENDPOINT
HEADERS = Config.HEADERS
OUTPUT_DIR = Config.OUTPUT_DIR

def fetch_programs():
    response = requests.get(API_ENDPOINT, headers=HEADERS)
    return dict(response.json())
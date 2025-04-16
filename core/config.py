from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
class Config:
    API_ENDPOINT = "https://api.bugbounty.sa/api/programs"
    HEADERS = {"Authorization": f"Bearer {os.getenv('ACCOUNT_TOKEN')}"}
    OUTPUT_DIR = "output"
import json
import os
from core.config import Config

API_ENDPOINT = Config.API_ENDPOINT
HEADERS = Config.HEADERS
OUTPUT_DIR = Config.OUTPUT_DIR

def ensure_dirs(program_name):
    """Create program directory structure if it doesn't exist"""
    program_dir = os.path.join(OUTPUT_DIR, program_name)
    scopes_dir = os.path.join(program_dir, "scopes")
    
    # Create directories if they don't exist
    os.makedirs(program_dir, exist_ok=True)
    os.makedirs(scopes_dir, exist_ok=True)
    return program_dir, scopes_dir

def save_programs(programs):
    # Ensure output dir exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "programs.json"), "w") as f:
        json.dump(programs, f, indent=4)

def save_scopes(name, scopes, id):
    _, scopes_dir = ensure_dirs(name)
    with open(os.path.join(scopes_dir, f"scope_{id}.json"), "w") as f:
        json.dump(scopes, f, indent=4)

def save_domains(name, domains, id):
    _, scopes_dir = ensure_dirs(name)
    with open(os.path.join(scopes_dir, "domains.txt"), "w") as f:
        f.write("\n".join(domains))
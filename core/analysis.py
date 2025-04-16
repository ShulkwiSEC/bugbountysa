import json
from datetime import datetime, timezone
from colorama import init, Fore, Style
from tabulate import tabulate
import os

# Initialize colorama
init(autoreset=True)

def color_status(is_active):
    return f"{Fore.GREEN}ACTIVE" if is_active else f"{Fore.RED}INACTIVE"

def color_type(type_):
    return f"{Fore.CYAN}{type_.upper()}" if type_ == "public" else f"{Fore.MAGENTA}{type_.upper()}"

def bounty_bar(from_val, to_val):
    bar = f"{Fore.YELLOW}[{'■' * (to_val // 500)}]"
    return f"{from_val}–{to_val} SAR {bar}"

def analyze_scope(scope):
    data = scope["data"]
    now = datetime.now(timezone.utc)
    start = datetime.fromisoformat(data["start_date"].replace("Z", "+00:00"))
    end = datetime.fromisoformat(data["end_date"].replace("Z", "+00:00"))
    duration_days = (end - start).days

    bounty_ranges = {
        "Critical": (data["critical_range_from"], data["critical_range_to"]),
        "High": (data["high_range_from"], data["high_range_to"]),
        "Medium": (data["medium_range_from"], data["medium_range_to"]),
        "Low": (data["low_range_from"], data["low_range_to"])
    }

    print(f"\n{Fore.CYAN}{Style.BRIGHT}┌───[ Program: {data['name']} ]" + "─" * 40)
    print(f"{Fore.BLUE}│ Status       : {color_status(data['is_active'])}")
    print(f"{Fore.BLUE}│ Type         : {color_type(data['type'])}")
    print(f"{Fore.BLUE}│ Platform     : {data.get('platform', {}).get('name', 'Unknown')}")
    print(f"{Fore.BLUE}│ Start Date   : {start.strftime('%Y-%m-%d')}")
    print(f"{Fore.BLUE}│ End Date     : {end.strftime('%Y-%m-%d')} ({(end - now).days} days remaining)")
    print(f"{Fore.BLUE}│ Duration     : {duration_days} days")
    print(f"{Fore.BLUE}│ Policy Size  : {len(data['policy'])} chars")
    print(f"{Fore.BLUE}│ Out of Scope : {len(data['out_of_scope'])} chars")
    print(f"{Fore.BLUE}│ Availbles Domains : {len(data['domains'])} domains")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}├───[ Bounty Ranges (SAR) ]")
    bounty_table = [
        [severity, f"{r[0]} – {r[1]}", bounty_bar(r[0], r[1])]
        for severity, r in bounty_ranges.items()
    ]
    print(tabulate(bounty_table, headers=["Severity", "Range", "Visual"], tablefmt="fancy_grid"))

    print(f"{Fore.CYAN}{Style.BRIGHT}└──────────────────────────────────────────────────────\n")
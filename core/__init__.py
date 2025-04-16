# web scraping and data analysis
# Bug Bounty SA Programs Scraper

import requests
import json
import argparse
import sys
import signal
from tqdm import tqdm
from core.programs import fetch_programs
from core.utils import save_programs, save_scopes, save_domains
from core.analysis import analyze_scope
from core.scope import fetch_scopes
from core.domains import extract_domains
from colorama import init, Fore, Style
from datetime import datetime
from core.config import Config

API_ENDPOINT = Config.API_ENDPOINT
HEADERS = Config.HEADERS
OUTPUT_DIR = Config.OUTPUT_DIR
interrupted = False

def signal_handler(signum, frame):
    global interrupted
    if interrupted:
        print(f"\n{Fore.RED}[!] Forced exit")
        sys.exit(1)
    interrupted = True
    print(f"\n{Fore.YELLOW}[!] Gracefully shutting down... (Ctrl+C again to force)")

def setup_argparse():
    parser = argparse.ArgumentParser(
        description='Bug Bounty SA Programs Scraper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --save                    # Fetch and save all data
  python main.py --domains                 # Only show domains
  python main.py --no-analysis            # Skip analysis output
  python main.py --program "Program Name"  # Process specific program
  python main.py --format json            # Output in JSON format
  python main.py --all-domains            # Export all domains in a single list
  python main.py --output-file domains.txt # Save output to a file
        """
    )
    
    # Data handling options
    parser.add_argument('--save', action='store_true', help='Save data to output directory')
    parser.add_argument('--output-dir', help='Specify output directory (default: output)')
    parser.add_argument('--output-file', help='Save output to a file instead of printing to console')
    parser.add_argument('--format', choices=['json', 'txt'], default='txt', help='Output format')
    
    # Display options
    parser.add_argument('--domains', action='store_true', help='Show domains only')
    parser.add_argument('--all-domains', action='store_true', help='Export all domains in a single list')
    parser.add_argument('--no-analysis', action='store_true', help='Skip analysis output')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--quiet', action='store_true', help='Suppress all non-error output')
    
    # Filtering options
    parser.add_argument('--program', help='Process specific program by name')
    parser.add_argument('--active-only', action='store_true', help='Only process active programs')
    
    return parser

def write_output(content, args):
    """Write output to file or print to console"""
    if args.output_file:
        with open(args.output_file, 'w') as f:
            if isinstance(content, str):
                f.write(content + '\n')
            elif args.format == 'json':
                json.dump(content, f, indent=4)
            else:
                for line in content:
                    f.write(line + '\n')
        if args.verbose and not args.quiet:
            print(f"{Fore.GREEN}[+] Output saved to {args.output_file}")
    else:
        if args.format == 'json':
            print(json.dumps(content, indent=4))
        elif isinstance(content, str):
            print(content)
        else:
            for line in content:
                print(line)

def print_domains(domains, format='txt', program_name=None):
    if format == 'json':
        if program_name:
            return {program_name: domains}
        return domains
    else:
        if program_name:
            return [f"# Domains for {program_name}:"] + domains
        return domains

def scarp(args=None):
    if args is None:
        parser = setup_argparse()
        args = parser.parse_args()
    
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    if args.output_dir:
        global OUTPUT_DIR
        OUTPUT_DIR = args.output_dir
    
    if args.verbose and not args.quiet:
        print(f"{Fore.CYAN}[*] Fetching programs...")
    
    try:
        programs = fetch_programs()
        if not programs or "data" not in programs:
            print(f"{Fore.RED}[!] Error: No program data received")
            return 1
        
        if args.save:
            save_programs(programs)
            if args.verbose and not args.quiet:
                print(f"{Fore.GREEN}[+] Saved programs data")
        
        processed_count = 0
        error_count = 0
        all_domains = set()
        program_domains = {}
        
        # Filter programs first
        filtered_programs = [
            p for p in programs["data"]
            if (not args.active_only or p.get('is_active', False)) and
               (not args.program or args.program.lower() == p['name'].lower())
        ]
        
        # Setup progress bar
        pbar = tqdm(
            filtered_programs,
            disable=args.quiet or (not args.verbose),
            desc="Processing programs",
            unit="program"
        )
        
        for program in pbar:
            if interrupted:
                break
                
            if args.verbose and not args.quiet:
                pbar.set_description(f"Processing {program['name']}")
                
            scope = fetch_scopes(program['id'])
            if scope is None:
                error_count += 1
                continue
                
            try:
                domains = extract_domains(scope)
                
                # Add domains to the all_domains set if needed
                if args.all_domains or args.domains:
                    all_domains.update(domains)
                    program_domains[program['name']] = domains
                
                if not args.no_analysis and not args.domains and not args.quiet:
                    analyze_scope(scope)
                    
                if args.domains and not args.all_domains and not args.quiet:
                    output = print_domains(domains, args.format, program['name'])
                    write_output(output, args)
                    
                if args.save:
                    save_domains(program['name'], domains, program['id'])
                    save_scopes(program['name'], scope, program['id'])
                    
                processed_count += 1
                
            except Exception as e:
                print(f"\n{Fore.RED}[!] Error processing {program['name']}: {str(e)}")
                error_count += 1
                continue
        
        # Handle all-domains output after processing is complete
        if not interrupted and args.all_domains:
            if args.format == 'json':
                write_output({"all_domains": sorted(list(all_domains))}, args)
            else:
                write_output(sorted(list(all_domains)), args)
        
        if args.verbose and not args.quiet:
            print(f"\n{Fore.GREEN}[+] Processing complete!")
            print(f"{Fore.CYAN}[*] Programs processed: {processed_count}")
            if error_count > 0:
                print(f"{Fore.YELLOW}[!] Errors encountered: {error_count}")
                
        return 0 if error_count == 0 and not interrupted else 1
        
    except Exception as e:
        print(f"\n{Fore.RED}[!] Fatal error: {str(e)}")
        return 1
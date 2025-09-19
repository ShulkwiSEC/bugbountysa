# bugbounty.sa CLI Tool

A command-line interface tool for managing and analyzing Bug Bounty SA programs. This tool helps security researchers track programs, analyze scopes, and extract domains from the Bug Bounty SA platform.

## Features

- 🔍 Fetch and analyze Bug Bounty SA programs
- 📊 Display detailed program analysis including bounty ranges
- 🌐 Extract and manage program domains
- 💾 Save program data locally for offline access
- 🎯 Filter programs by name or status
- 📜 Multiple output formats (JSON/TXT)

## Installation

### Using pip

```bash
pip install bugbountysa
```

### From Source

```bash
git clone https://github.com/ShulkwiSEC/bugbountysa.git
cd bugbountysa
pip install -e .
```

## Usage

### Basic Commands

```bash
# Show all programs with analysis
bugbountysa

# Extract domains only
bugbountysa --domains

# Save all data
bugbountysa --save

# Process specific program
bugbountysa --program "Program Name"

# Show only active programs
bugbountysa --active-only

# Export all domains to a file
bugbountysa --all-domains --output-file domains.txt

# JSON output
bugbountysa --format json
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--save` | Save data to output directory |
| `--output-dir DIR` | Specify output directory (default: output) |
| `--output-file FILE` | Save output to a file |
| `--format {json,txt}` | Output format |
| `--domains` | Show domains only |
| `--all-domains` | Export all domains in a single list |
| `--no-analysis` | Skip analysis output |
| `-v, --verbose` | Verbose output |
| `--quiet` | Suppress all non-error output |
| `--program NAME` | Process specific program by name |
| `--active-only` | Only process active programs |

## Output Structure

When using `--save`, the tool creates the following directory structure:

```
output/
├── programs.json
└── program_name/
    └── scopes/
        ├── scope_{id}.json
        └── domains.txt
```

## Example Output

### Program Analysis
```
┌───[ Program: Example Program ]────────────────────────────────────────
│ Status       : ACTIVE
│ Type         : PUBLIC
│ Platform     : Web
│ Start Date   : 2025-02-25
│ End Date     : 2025-05-12 (26 days remaining)
│ Duration     : 76 days
│ Policy Size  : 2286 chars
│ Out of Scope : 1766 chars

├───[ Bounty Ranges (SAR) ]
╒════════════╤═════════════╤════════════════════════════════╕
│ Severity   │ Range       │ Visual                         │
╞════════════╪═════════════╪════════════════════════════════╡
│ Critical   │ 5238 – 7000 │ 5238–7000 SAR [■■■■■■■■■■■■■■] │
│ High       │ 2729 – 5082 │ 2729–5082 SAR [■■■■■■■■■■]     │
│ Medium     │ 916 – 2635  │ 916–2635 SAR [■■■■■]           │
│ Low        │ 500 – 885   │ 500–885 SAR [■]                │
╘════════════╧═════════════╧════════════════════════════════╛
```

## Configuration

### Environment Variables
Copy `.env.example` to `.env` and set your configuration:
```bash
cp .env.example .env
```

Required environment variables:
- `ACCOUNT_TOKEN`: Your Bug Bounty SA API token

The tool uses the following configuration settings:
- `API_ENDPOINT`: The Bug Bounty SA API endpoint
- `HEADERS`: API authentication headers
- `OUTPUT_DIR`: Default output directory for saved data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- ShulkwiSEC
- Twitter: [@ShulkwiSEC](https://twitter.com/ShulkwiSEC)
- GitHub: [ShulkwiSEC](https://github.com/ShulkwiSEC)

## Acknowledgments

- Bug Bounty SA Platform for providing the API
- The bug bounty community in Saudi Arabia
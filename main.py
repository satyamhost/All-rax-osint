#!/usr/bin/env python3
"""
Termux OSINT Tool with Rich TUI
Author: TEAM RAX
Version: 2.0
"""

import os
import sys
import json
import requests
import socket
import time
import re
import webbrowser
from datetime import datetime
from urllib.parse import urlparse
from typing import Dict, List, Optional, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Rich imports for beautiful UI
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt, Confirm
from rich.columns import Columns
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich import box
from rich.align import Align
from rich.style import Style
import pyfiglet

# Initialize console
console = Console()

# ================= CONFIG =================
CONFIG = {
    "tool_name": "RAX OSINT TOOL",
    "version": "2.0",
    "author": "TEAM RAX",
    "contact": "@TEAM_RAX",
    "github": "https://github.com/teamrax",
    "website": "https://teamrax.io"
}

# ================= APIs =================
APIS = {
    "📱 Phone Number": {
        "api": "https://abbas-apis.vercel.app/api/phone?number=91{num}",
        "description": "Get phone number information",
        "icon": "📱",
        "category": "Personal"
    },
    "🆔 Aadhaar Card": {
        "api": "https://adhar-info.lakhan81712.workers.dev/?aadhar={aadhar}&key=ANUP",
        "description": "Aadhaar card verification",
        "icon": "🆔",
        "category": "Government"
    },
    "📮 PIN Code": {
        "api": "https://pin-code.lakhan81712.workers.dev/?pin={pin}",
        "description": "Indian PIN code lookup",
        "icon": "📮",
        "category": "Location"
    },
    "📸 Instagram": {
        "api": "https://ins-anup.lakhan81712.workers.dev/?username={user}",
        "description": "Instagram profile info",
        "icon": "📸",
        "category": "Social Media"
    },
    "🌐 IP Address": {
        "api": "https://abbas-apis.vercel.app/api/ip?ip={ip}",
        "description": "IP geolocation & details",
        "icon": "🌐",
        "category": "Network"
    },
    "🏦 IFSC Code": {
        "api": "https://abbas-apis.vercel.app/api/ifsc?ifsc={ifsc}",
        "description": "Bank IFSC code details",
        "icon": "🏦",
        "category": "Financial"
    },
    "🎮 Free Fire Ban": {
        "api": "https://abbas-apis.vercel.app/api/ff-ban?uid={uid}",
        "description": "Check Free Fire ban status",
        "icon": "🎮",
        "category": "Gaming"
    },
    "📧 Email": {
        "api": "https://abbas-apis.vercel.app/api/email?mail={mail}",
        "description": "Email verification & info",
        "icon": "📧",
        "category": "Communication"
    },
    "🎮 Free Fire Info": {
        "api": "https://abbas-apis.vercel.app/api/ff-info?uid={uid}",
        "description": "Free Fire player stats",
        "icon": "🎮",
        "category": "Gaming"
    },
    "💳 PAN Card": {
        "api": "https://abbas-apis.vercel.app/api/pan?pan={pan}",
        "description": "PAN card verification",
        "icon": "💳",
        "category": "Government"
    },
    "🇵🇰 Pakistan Number": {
        "api": "https://abbas-apis.vercel.app/api/pakistan?number={number}",
        "description": "Pakistan phone lookup",
        "icon": "🇵🇰",
        "category": "Personal"
    },
    "💻 GitHub": {
        "api": "https://abbas-apis.vercel.app/api/github?username={username}",
        "description": "GitHub profile info",
        "icon": "💻",
        "category": "Social Media"
    },
    "🎭 Name Masking": {
        "api": "https://abbas-apis.vercel.app/api/num-name?number={number}",
        "description": "Phone to name lookup",
        "icon": "🎭",
        "category": "Personal"
    },
    "🔓 Leaked Data": {
        "api": "https://source-code-api.vercel.app/?num={num}",
        "description": "Check leaked data",
        "icon": "🔓",
        "category": "Security"
    }
}

# ================= UTILITIES =================
class Color:
    """Color codes for terminal"""
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color_code):
    """Print colored text"""
    print(f"{color_code}{text}{Color.END}")

def print_banner():
    """Print animated banner"""
    clear_screen()
    
    # ASCII Art Banner
    banner_text = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ██████╗  █████╗ ██╗  ██╗    ██████╗ ███████╗██╗███╗   ██╗  ║
║  ██╔══██╗██╔══██╗╚██╗██╔╝    ██╔═══██╗██╔════╝██║████╗  ██║  ║
║  ██████╔╝███████║ ╚███╔╝     ██║   ██║███████╗██║██╔██╗ ██║  ║
║  ██╔══██╗██╔══██║ ██╔██╗     ██║   ██║╚════██║██║██║╚██╗██║  ║
║  ██║  ██║██║  ██║██╔╝ ██╗    ╚██████╔╝███████║██║██║ ╚████║  ║
║  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝     ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝  ║
║                                                              ║
║                    O S I N T   T O O L                       ║
║                    V E R S I O N   2 . 0                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    
    console.print(Panel.fit(
        banner_text,
        title=f"[bold cyan]{CONFIG['tool_name']}[/bold cyan]",
        subtitle=f"[yellow]by {CONFIG['author']}[/yellow]",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    # Stats panel
    stats_table = Table(show_header=False, box=box.ROUNDED, show_edge=False)
    stats_table.add_column("Stats", justify="center")
    stats_table.add_column("Value", justify="center")
    stats_table.add_row("🔍 Search Types", str(len(APIS)))
    stats_table.add_row("⚡ Version", CONFIG["version"])
    stats_table.add_row("👑 Author", CONFIG["author"])
    stats_table.add_row("📞 Contact", CONFIG["contact"])
    
    console.print(Columns([
        Panel(stats_table, title="[bold green]📊 TOOL STATS[/bold green]", border_style="green"),
        Panel(
            "[bold]✨ Features:[/bold]\n• 15+ OSINT APIs\n• Beautiful TUI\n• Fast Results\n• Secure\n• Free to Use",
            title="[bold magenta]🚀 FEATURES[/bold magenta]",
            border_style="magenta"
        )
    ]))
    
    console.print("\n")

def validate_input(input_type: str, value: str) -> bool:
    """Validate user input based on type"""
    patterns = {
        "phone": r'^[6-9]\d{9}$',
        "aadhaar": r'^\d{12}$',
        "pin": r'^\d{6}$',
        "pan": r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$',
        "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        "ip": r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
        "ifsc": r'^[A-Z]{4}0[A-Z0-9]{6}$'
    }
    
    if input_type in patterns:
        return bool(re.match(patterns[input_type], value))
    return True

def make_request(api_url: str, params: Dict) -> Dict:
    """Make API request with error handling"""
    try:
        response = requests.get(api_url.format(**params), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API Error: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}

def format_json(data: Dict) -> str:
    """Format JSON data for display"""
    try:
        return json.dumps(data, indent=2, ensure_ascii=False)
    except:
        return str(data)

def create_search_table() -> Table:
    """Create search options table"""
    table = Table(
        title="[bold cyan]🔍 Available Search Types[/bold cyan]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("No.", style="cyan", width=5)
    table.add_column("Icon", style="yellow", width=3)
    table.add_column("Type", style="green", width=20)
    table.add_column("Category", style="blue", width=15)
    table.add_column("Description", style="white")
    
    for idx, (search_type, info) in enumerate(APIS.items(), 1):
        table.add_row(
            str(idx),
            info["icon"],
            search_type,
            info["category"],
            info["description"]
        )
    
    return table

def display_results(data: Dict, search_type: str, query: str):
    """Display results in beautiful format"""
    console.clear()
    
    # Header
    console.print(Panel.fit(
        f"[bold green]✅ SEARCH COMPLETED[/bold green]\n"
        f"[cyan]Type:[/cyan] {search_type}\n"
        f"[cyan]Query:[/cyan] {query}\n"
        f"[cyan]Time:[/cyan] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        border_style="green",
        padding=(1, 2)
    ))
    
    if "error" in data:
        console.print(Panel(
            f"[bold red]❌ ERROR[/bold red]\n\n{data['error']}",
            border_style="red",
            padding=(1, 2)
        ))
        return
    
    # Create results table
    results_table = Table(
        title=f"[bold yellow]📊 {search_type.upper()} RESULTS[/bold yellow]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    results_table.add_column("Field", style="green", width=20)
    results_table.add_column("Value", style="white")
    
    # Add data to table
    if isinstance(data, dict):
        for key, value in data.items():
            if value and str(value).strip():
                results_table.add_row(key, str(value))
    else:
        results_table.add_row("Response", str(data))
    
    console.print(results_table)
    
    # JSON View
    console.print("\n")
    if Confirm.ask("[bold]📋 Show raw JSON data?[/bold]", default=False):
        console.print(Panel(
            Syntax(format_json(data), "json", theme="monokai", line_numbers=True),
            title="[bold]📄 JSON Response[/bold]",
            border_style="blue"
        ))

def search_flow():
    """Main search workflow"""
    while True:
        console.clear()
        print_banner()
        
        # Show search options
        console.print(create_search_table())
        console.print("\n")
        
        try:
            choice = Prompt.ask(
                "[bold cyan]Select search type (1-15) or 0 to exit[/bold cyan]",
                choices=[str(i) for i in range(0, len(APIS) + 1)],
                default="0"
            )
            
            if choice == "0":
                break
            
            search_types = list(APIS.keys())
            selected_type = search_types[int(choice) - 1]
            search_info = APIS[selected_type]
            
            # Get query
            console.print(f"\n[bold yellow]{search_info['icon']} {selected_type}[/bold yellow]")
            console.print(f"[dim]{search_info['description']}[/dim]\n")
            
            query = Prompt.ask("[bold]Enter search query[/bold]")
            
            # Validate input
            if not query.strip():
                console.print("[red]❌ Query cannot be empty[/red]")
                time.sleep(1)
                continue
            
            # Make API call with progress
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                transient=True,
            ) as progress:
                task = progress.add_task(
                    f"[cyan]Searching {selected_type}...",
                    total=100
                )
                
                # Simulate progress
                for i in range(10):
                    progress.update(task, advance=10)
                    time.sleep(0.1)
                
                # Actual API call
                params = {"num": query, "aadhar": query, "pin": query, 
                         "user": query, "ip": query, "ifsc": query,
                         "uid": query, "mail": query, "pan": query,
                         "number": query, "username": query}
                
                result = make_request(search_info["api"], params)
                progress.update(task, completed=100)
            
            # Display results
            display_results(result, selected_type, query)
            
            # Next action
            console.print("\n")
            actions = ["🔍 New Search", "📋 Save Results", "🏠 Main Menu", "🚪 Exit"]
            action_table = Table(show_header=False, box=None)
            for i, action in enumerate(actions, 1):
                action_table.add_row(f"[cyan]{i}.[/cyan] {action}")
            console.print(action_table)
            
            next_action = Prompt.ask(
                "[bold]Select action[/bold]",
                choices=["1", "2", "3", "4"],
                default="1"
            )
            
            if next_action == "2":
                save_results(result, selected_type, query)
            elif next_action == "3":
                continue
            elif next_action == "4":
                console.print("[bold green]👋 Thank you for using RAX OSINT Tool![/bold green]")
                time.sleep(2)
                sys.exit(0)
                
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠️ Operation cancelled by user[/yellow]")
            time.sleep(1)
        except Exception as e:
            console.print(f"[red]❌ Error: {str(e)}[/red]")
            time.sleep(2)

def save_results(data: Dict, search_type: str, query: str):
    """Save results to file"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rax_osint_{search_type}_{timestamp}.json"
        
        save_data = {
            "tool": CONFIG["tool_name"],
            "version": CONFIG["version"],
            "timestamp": datetime.now().isoformat(),
            "search_type": search_type,
            "query": query,
            "results": data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        console.print(f"[green]✅ Results saved to: [/green][cyan]{filename}[/cyan]")
        time.sleep(2)
    except Exception as e:
        console.print(f"[red]❌ Failed to save: {str(e)}[/red]")
        time.sleep(2)

def about_section():
    """Display about information"""
    console.clear()
    
    about_md = f"""
# RAX OSINT Tool v{CONFIG['version']}

## About
A powerful Open Source Intelligence (OSINT) tool with beautiful Terminal User Interface (TUI).
Built for security researchers, investigators, and privacy enthusiasts.

## Features
- **15+ Search Types**: Phone, Email, IP, Social Media, and more
- **Beautiful TUI**: Rich terminal interface with colors and animations
- **Fast & Efficient**: Quick API responses with progress indicators
- **Secure**: No data storage, all requests are anonymous
- **Free**: Completely free to use

## Author
**{CONFIG['author']}**  
📞 Contact: {CONFIG['contact']}  
🌐 GitHub: {CONFIG['github']}  
🌐 Website: {CONFIG['website']}

## Disclaimer
This tool is for **educational and authorized testing purposes only**.
Always ensure you have proper authorization before conducting any OSINT investigation.
The developers are not responsible for any misuse of this tool.
    """
    
    console.print(Panel(
        Markdown(about_md),
        title="[bold cyan]📖 ABOUT RAX OSINT TOOL[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    console.print("\n")
    Prompt.ask("[bold]Press Enter to continue...[/bold]")

def quick_search():
    """Quick search mode"""
    console.clear()
    
    console.print(Panel.fit(
        "[bold yellow]⚡ QUICK SEARCH MODE[/bold yellow]\n"
        "Enter search type and query separated by space\n"
        "Example: phone 9876543210\n"
        "Type 'back' to return to main menu",
        border_style="yellow"
    ))
    
    while True:
        try:
            console.print("\n")
            command = Prompt.ask("[bold cyan]Enter search command[/bold cyan]")
            
            if command.lower() == 'back':
                break
            
            parts = command.split(maxsplit=1)
            if len(parts) != 2:
                console.print("[red]❌ Format: type query[/red]")
                continue
            
            search_type, query = parts
            search_type = search_type.lower()
            
            # Find matching search type
            matched_type = None
            for stype, info in APIS.items():
                if search_type in stype.lower() or search_type in info["category"].lower():
                    matched_type = stype
                    break
            
            if not matched_type:
                console.print("[red]❌ Invalid search type[/red]")
                continue
            
            search_info = APIS[matched_type]
            
            # Make API call
            with console.status(f"[bold cyan]Searching {matched_type}...[/bold cyan]"):
                params = {"num": query, "aadhar": query, "pin": query, 
                         "user": query, "ip": query, "ifsc": query,
                         "uid": query, "mail": query, "pan": query,
                         "number": query, "username": query}
                
                result = make_request(search_info["api"], params)
            
            # Display quick results
            console.print(Panel(
                f"[bold green]{matched_type.upper()} SEARCH[/bold green]\n"
                f"[cyan]Query:[/cyan] {query}\n\n"
                f"[yellow]Results:[/yellow]\n{format_json(result)}",
                border_style="green"
            ))
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]❌ Error: {str(e)}[/red]")

def main_menu():
    """Main menu interface"""
    while True:
        console.clear()
        print_banner()
        
        # Create menu options
        menu_table = Table(
            title="[bold magenta]📋 MAIN MENU[/bold magenta]",
            box=box.ROUNDED,
            show_header=False,
            width=60
        )
        menu_table.add_column("Option", style="cyan", width=10)
        menu_table.add_column("Description", style="white")
        
        menu_options = [
            ("🔍", "Search", "Interactive search mode"),
            ("⚡", "Quick Search", "Fast command-line search"),
            ("📊", "View APIs", "Show all available APIs"),
            ("💾", "Recent", "View recent searches"),
            ("📖", "About", "About this tool"),
            ("🛠", "Settings", "Tool settings"),
            ("🚪", "Exit", "Exit the tool")
        ]
        
        for i, (icon, name, desc) in enumerate(menu_options, 1):
            menu_table.add_row(f"{i}. {icon}", f"[bold]{name}[/bold]\n[dim]{desc}[/dim]")
        
        console.print(Align.center(menu_table))
        console.print("\n")
        
        try:
            choice = Prompt.ask(
                "[bold cyan]Select option (1-7)[/bold cyan]",
                choices=[str(i) for i in range(1, 8)],
                default="1"
            )
            
            if choice == "1":
                search_flow()
            elif choice == "2":
                quick_search()
            elif choice == "3":
                console.clear()
                console.print(create_search_table())
                Prompt.ask("[bold]Press Enter to continue...[/bold]")
            elif choice == "4":
                console.print("[yellow]🔄 Feature coming soon...[/yellow]")
                time.sleep(2)
            elif choice == "5":
                about_section()
            elif choice == "6":
                console.print("[yellow]🔄 Feature coming soon...[/yellow]")
                time.sleep(2)
            elif choice == "7":
                console.print("[bold green]👋 Thank you for using RAX OSINT Tool![/bold green]")
                time.sleep(2)
                break
                
        except KeyboardInterrupt:
            if Confirm.ask("\n[yellow]⚠️ Are you sure you want to exit?[/yellow]"):
                console.print("[bold green]👋 Goodbye![/bold green]")
                time.sleep(1)
                break

# ================= MAIN =================
def check_dependencies():
    """Check and install required dependencies"""
    try:
        import rich
        import requests
        return True
    except ImportError as e:
        console.print(f"[red]❌ Missing dependency: {str(e)}[/red]")
        console.print("[yellow]Installing dependencies...[/yellow]")
        
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "requests", "pyfiglet"])
            console.print("[green]✅ Dependencies installed successfully![/green]")
            time.sleep(2)
            return True
        except:
            console.print("[red]❌ Failed to install dependencies[/red]")
            console.print("[yellow]Please install manually:[/yellow]")
            console.print("[white]pip install rich requests pyfiglet[/white]")
            return False

def main():
    """Main entry point"""
    try:
        # Check dependencies
        if not check_dependencies():
            sys.exit(1)
        
        # Welcome message
        console.clear()
        console.print("[bold cyan]🚀 Starting RAX OSINT Tool...[/bold cyan]")
        time.sleep(1)
        
        # Show main menu
        main_menu()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Tool interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Fatal error: {str(e)}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
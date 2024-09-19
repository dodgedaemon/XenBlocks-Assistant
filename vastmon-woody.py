import requests
import subprocess
import json
import os
from dotenv import load_dotenv
import platform
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Style, init
import uuid
import time

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv('API_KEY')
ADDR = os.getenv('ADDR')

# Define color constants
MATRIX_GREEN = Fore.GREEN
MATRIX_BRIGHT_GREEN = Fore.LIGHTGREEN_EX
MATRIX_DARK_GREEN = Fore.GREEN + Style.DIM
MATRIX_CYAN = Fore.CYAN
MATRIX_RED = Fore.RED
MATRIX_YELLOW = Fore.YELLOW

def display_splash_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

    splash_screen = f"""
{MATRIX_BRIGHT_GREEN}
   _  __           ____  __           __           ___              _      __              __ 
  | |/ /__  ____  / __ )/ /___  _____/ /_______   /   |  __________(_)____/ /_____ _____  / /_
  |   / _ \/ __ \/ __  / / __ \/ ___/ //_/ ___/  / /| | / ___/ ___/ / ___/ __/ __ `/ __ \/ __/
 /   /  __/ / / / /_/ / / /_/ / /__/ ,< (__  )  / ___ |(__  |__  ) (__  ) /_/ /_/ / / / / /_  
/_/|_\___/_/ /_/_____/_/\____/\___/_/|_/____/  /_/  |_/____/____/_/____/\__/\__,_/_/ /_/\__/  
                                                                                             

{MATRIX_DARK_GREEN}Welcome to the XenBlocks Mining Assistant - Woody Edition.

    - Create a .env file with Wallet Address and API variables.
    - Open-source with zero fee collection: https://github.com/TreeCityWes/XenBlocks-Assistant.
    - Woody: https://woodyminer.com/ | Wes: https://www.buymeacoffee.com/treecitywes

{Style.RESET_ALL}"""
    print(splash_screen)
    input(f"{MATRIX_CYAN}Press Enter to continue...{Style.RESET_ALL}")

def format_hashrate(hashrate):
    if hashrate < 100:
        return f"{MATRIX_RED}{hashrate:.2f} H/s{Style.RESET_ALL}"
    elif hashrate < 1000:
        return f"{MATRIX_YELLOW}{hashrate:.2f} H/s{Style.RESET_ALL}"
    else:
        return f"{MATRIX_BRIGHT_GREEN}{hashrate:.2f} H/s{Style.RESET_ALL}"

def format_uptime(seconds):
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"

def run_vastai_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if result.stdout:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"{MATRIX_RED}Error executing command: {e}{Style.RESET_ALL}")
    return None

def get_vast_instances():
    print(f"{MATRIX_CYAN}Fetching Vast.ai instances...{Style.RESET_ALL}")
    command = ["vastai", "show", "instances", "--raw"]
    result = run_vastai_command(command)
    if isinstance(result, list):
        print(f"{MATRIX_BRIGHT_GREEN}Successfully fetched {len(result)} Vast.ai instances.{Style.RESET_ALL}")
        return result
    else:
        print(f"{MATRIX_RED}Error fetching instances.{Style.RESET_ALL}")
        return []

def get_woodyminer_stats(miner_address):
    print(f"{MATRIX_CYAN}Fetching WoodyMiner stats...{Style.RESET_ALL}")
    url = f"https://woodyminer.com/api/stat/get/{miner_address}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        stats = response.json()
        print(f"{MATRIX_BRIGHT_GREEN}Successfully fetched WoodyMiner stats for {len(stats)} workers.{Style.RESET_ALL}")
        return stats
    except requests.RequestException as e:
        print(f"{MATRIX_RED}Error fetching WoodyMiner stats. Account does not exist: {str(e)}{Style.RESET_ALL}")
    except json.JSONDecodeError:
        print(f"{MATRIX_RED}Error decoding WoodyMiner response{Style.RESET_ALL}")
    except Exception as e:
        print(f"{MATRIX_RED}Unexpected error fetching WoodyMiner stats: {str(e)}{Style.RESET_ALL}")
    return []

def display_vast_stats(instances):
    table = PrettyTable()
    table.field_names = [
        "#", "Instance ID", "GPU Type", "Status", "GPUs", "Cost/hr", "GPU Usage", "CPU Usage",
        "RAM Usage", "Disk Usage", "IP"
    ]
    table.align = "l"

    def gpu_usage_value(instance):
        """Convert GPU usage to a float for sorting. Handle 'N/A' and None as 0."""
        usage = instance.get('gpu_util')
        if usage is None or usage == 'N/A':
            return 0.0
        return float(usage)

    # Sort instances: running first, then by GPU usage (highest to lowest)
    sorted_instances = sorted(instances, key=lambda x: (
        (x.get('actual_status') or '') != 'running',  # Sort by status (running first)
        -gpu_usage_value(x)  # Sort by GPU usage (high usage first)
    ))

    for idx, instance in enumerate(sorted_instances, 1):
        status = instance.get('actual_status', 'N/A')
        status_color = MATRIX_BRIGHT_GREEN if status == 'running' else MATRIX_RED
        
        gpu_usage = instance.get('gpu_util', 'N/A')
        gpu_usage = f"{float(gpu_usage):.2f}%" if gpu_usage not in ['N/A', None] else "N/A"
        gpu_usage_color = MATRIX_RED if gpu_usage != 'N/A' and float(gpu_usage[:-1]) < 20 else MATRIX_GREEN

        cpu_usage = instance.get('cpu_util', 'N/A')
        cpu_usage = f"{float(cpu_usage):.2f}%" if cpu_usage not in ['N/A', None] else "N/A"

        ram_usage = instance.get('mem_usage', 'N/A')
        ram_usage = f"{float(ram_usage):.3f}%" if ram_usage not in ['N/A', None] else "N/A"

        disk_usage = instance.get('disk_usage', 'N/A')
        disk_usage = f"{float(disk_usage):.2f}%" if disk_usage not in ['N/A', None] else "N/A"
        
        table.add_row([
            f"{MATRIX_CYAN}{idx}{Style.RESET_ALL}",
            f"{MATRIX_GREEN}{instance.get('id', 'N/A')}{Style.RESET_ALL}",
            f"{MATRIX_DARK_GREEN}{instance.get('gpu_name', 'N/A')}{Style.RESET_ALL}",
            f"{status_color}{status}{Style.RESET_ALL}",
            f"{MATRIX_DARK_GREEN}{instance.get('num_gpus', 'N/A')}{Style.RESET_ALL}",
            f"{MATRIX_YELLOW}${instance.get('dph_total', 0):.4f}{Style.RESET_ALL}",
            f"{gpu_usage_color}{gpu_usage}{Style.RESET_ALL}",
            f"{MATRIX_GREEN}{cpu_usage}{Style.RESET_ALL}",
            f"{MATRIX_GREEN}{ram_usage}{Style.RESET_ALL}",
            f"{MATRIX_GREEN}{disk_usage}{Style.RESET_ALL}",
            f"{MATRIX_CYAN}{instance.get('public_ipaddr', 'N/A')}{Style.RESET_ALL}"
        ])

    print(f"\n{MATRIX_BRIGHT_GREEN}Vast.ai Instances:{Style.RESET_ALL}")
    print(table)

def display_woodyminer_stats(stats, vast_instances):
    table = PrettyTable()
    table.field_names = [
        "#", "Machine ID", "GPU Type", "Hashrate", "Accepted Blocks",
        "Rejected Blocks", "Uptime", "Status"
    ]
    table.align = "l"

    # Create a mapping of machine IDs to Vast.ai instance statuses
    vast_statuses = {instance.get('machine_id'): instance.get('actual_status') for instance in vast_instances}

    # Sort stats: Online first, then by hashrate
    sorted_stats = sorted(stats, 
                          key=lambda x: (x.get('status') != 'Online', 
                                         -float(x.get('totalHashrate', 0))))

    for idx, stat in enumerate(sorted_stats, 1):
        machine_id = stat.get('machineId', 'N/A')
        vast_status = vast_statuses.get(machine_id, 'N/A')
        status = stat.get('status', 'N/A')
        
        if status == 'Online':
            status_color = MATRIX_BRIGHT_GREEN
            hashrate = format_hashrate(float(stat.get('totalHashrate', 0)))
            uptime = format_uptime(stat.get('uptime', 0))
        else:
            status_color = MATRIX_RED
            hashrate = 'N/A'
            uptime = 'N/A'
        
        row = [
            f"{MATRIX_CYAN}{idx}{Style.RESET_ALL}",
            f"{status_color}{machine_id}{Style.RESET_ALL}",
            f"{status_color}{stat['gpus'][0]['name'] if stat.get('gpus') else 'N/A'}{Style.RESET_ALL}",
            f"{status_color}{hashrate}{Style.RESET_ALL}",
            f"{status_color}{stat.get('acceptedBlocks', 0)}{Style.RESET_ALL}",
            f"{status_color}{stat.get('rejectedBlocks', 0)}{Style.RESET_ALL}",
            f"{status_color}{uptime}{Style.RESET_ALL}",
            f"{status_color}{status}{Style.RESET_ALL}"
        ]
        
        table.add_row(row)

    print(f"\n{MATRIX_BRIGHT_GREEN}WoodyMiner Stats:{Style.RESET_ALL}")
    print(table)

def search_top_offers(criterion='dph_total', max_bid=99.99, min_gpus=None, max_gpus=None):
    print(f"{MATRIX_CYAN}Searching for Vast.ai offers...{Style.RESET_ALL}")
    query_parts = ["verified=false", "rented=false", f"min_bid <= {max_bid}"]

    if min_gpus is not None:
        query_parts.append(f"num_gpus >= {min_gpus}")
    if max_gpus is not None:
        query_parts.append(f"num_gpus <= {max_gpus}")

    query = " ".join(query_parts)

    command = ["vastai", "search", "offers", query, "--type", "bid", "--raw"]
    offers_response = run_vastai_command(command)

    if isinstance(offers_response, list):
        offers = offers_response

        if criterion == 'num_gpus':
            sorted_offers = sorted(offers, key=lambda x: (-int(x.get('num_gpus', 0)), float(x.get('dph_total', float('inf')))))
        else:
            sorted_offers = sorted(offers, key=lambda x: float(x.get(criterion, float('inf'))))

        print(f"{MATRIX_BRIGHT_GREEN}Found {len(sorted_offers)} offers matching your criteria.{Style.RESET_ALL}")
        return sorted_offers[:20]
    else:
        print(f"{MATRIX_RED}Unexpected response format. Please ensure your command execution function is correct.{Style.RESET_ALL}")
        return []

def print_offers(offers):
    if not offers:
        print(f"{MATRIX_YELLOW}No offers to display.{Style.RESET_ALL}")
        return

    table = PrettyTable()
    table.field_names = ["Number", "ID", "GPU", "Quantity", "Price/hr", "Total TFLOPS", "TFLOPS/$", "Location"]
    table.align = "l"

    for idx, offer in enumerate(offers, 1):
        table.add_row([
            f"{MATRIX_CYAN}{idx}{Style.RESET_ALL}",
            f"{MATRIX_GREEN}{offer['id']}{Style.RESET_ALL}",
            f"{MATRIX_DARK_GREEN}{offer['gpu_name'].replace('_', ' ')}{Style.RESET_ALL}",
            f"{MATRIX_DARK_GREEN}{offer.get('num_gpus', 'N/A')}{Style.RESET_ALL}",
            f"{MATRIX_YELLOW}${offer['dph_total']:.3f}{Style.RESET_ALL}",
            f"{MATRIX_BRIGHT_GREEN}{offer['total_flops']:.2f}{Style.RESET_ALL}",
            f"{MATRIX_BRIGHT_GREEN}{offer.get('flops_per_dphtotal', 0):.2f}{Style.RESET_ALL}",
            f"{MATRIX_CYAN}{offer.get('geolocation', 'Unknown')}{Style.RESET_ALL}"
        ])

    print(table)

def create_instance(offer_id, price, gpu_name):
    on_start_script = (
        f"env >> /etc/environment; "
        f"sudo apt install screen -y; "
        f"screen -S woodyminer -X quit 2>/dev/null; "
        f"screen -dmS woodyminer bash -c \"wget -N https://github.com/woodysoil/XenblocksMiner/releases/download/v1.4.0/xenblocksMiner-1.4.0-linux.tar.gz && "
        f"tar -zxvf xenblocksMiner-1.4.0-linux.tar.gz --overwrite && "
        f"chmod +x xenblocksMiner && "
        f"./xenblocksMiner --minerAddr {ADDR} --totalDevFee 0\"; "
        f"screen -r woodyminer"
    )

    command = [
        "vastai", "create", "instance", str(offer_id),
        "--price", str(round(float(price), 4)),
        "--image", "nvidia/cuda:11.0.3-runtime-ubuntu20.04",
        "--onstart-cmd", on_start_script,
        "--disk", "16",
        "--raw"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if result.stdout:
            # Print GPU name and price instead of Miner ID
            print(f"{MATRIX_BRIGHT_GREEN}Instance created successfully with {gpu_name} at ${price}/hr{Style.RESET_ALL}")
            return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"{MATRIX_RED}Error executing command: {e}{Style.RESET_ALL}")
        return None

def parse_selection(input_str):
    selection = set()
    for part in input_str.split(","):
        part = part.strip()
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                selection.update(range(start, end + 1))
            except ValueError:
                print(f"{MATRIX_RED}Invalid range input: {part}{Style.RESET_ALL}")
        else:
            try:
                selection.add(int(part))
            except ValueError:
                print(f"{MATRIX_RED}Invalid input: {part}{Style.RESET_ALL}")
    return sorted(selection)

def terminate_instances(instances):
    # Sort instances before displaying, as done in display_vast_stats
    sorted_instances = sorted(instances, key=lambda x: (
        (x.get('actual_status') or '') != 'running',  # Sort by status (running first)
        -float(x.get('gpu_util', 0) or 0)  # Sort by GPU usage (high to low)
    ))
    
    display_vast_stats(sorted_instances)  # Display the sorted list
    
    while True:
        selection = input(f"\n{MATRIX_CYAN}Enter the number(s) of the instance(s) to terminate (comma-separated), or 'q' to quit: {Style.RESET_ALL}")
        if selection.lower() == 'q':
            return
        
        selected_indices = parse_selection(selection)
        
        # Adjust the indices since the displayed index starts from 1, but Python lists are 0-indexed
        if all(1 <= idx <= len(sorted_instances) for idx in selected_indices):
            selected_instances = [sorted_instances[idx - 1] for idx in selected_indices]
            break
        else:
            print(f"{MATRIX_RED}Invalid selection. Please enter valid instance numbers.{Style.RESET_ALL}")
    
    for instance in selected_instances:
        instance_id = instance['id']
        print(f"{MATRIX_YELLOW}Terminating instance {instance_id}...{Style.RESET_ALL}")
        
        command = ["vastai", "destroy", "instance", str(instance_id)]
        result = run_vastai_command(command)
        if result:
            print(f"{MATRIX_BRIGHT_GREEN}Successfully terminated instance {instance_id}.{Style.RESET_ALL}")
        else:
            print(f"{MATRIX_RED}Failed to terminate instance {instance_id}.{Style.RESET_ALL}")


def main():
    display_splash_screen()

    while True:
        print(f"\n{MATRIX_BRIGHT_GREEN}XenBlocks Mining Assistant - Main Menu:{Style.RESET_ALL}\n")
        print(f"{MATRIX_CYAN}1. View Mining Network Status{Style.RESET_ALL}")
        print(f"{MATRIX_CYAN}2. Buy Miners{Style.RESET_ALL}")
        print(f"{MATRIX_CYAN}3. Terminate Miners{Style.RESET_ALL}")
        print(f"{MATRIX_CYAN}4. Exit{Style.RESET_ALL}")

        choice = input(f"\n{MATRIX_BRIGHT_GREEN}Enter your choice: {Style.RESET_ALL}")

        if choice == "1":
            print(f"\n{MATRIX_BRIGHT_GREEN}Fetching mining stats...{Style.RESET_ALL}")
            start_time = time.time()
            vast_instances = get_vast_instances()
            woodyminer_stats = get_woodyminer_stats(ADDR)
            
            display_vast_stats(vast_instances)
            display_woodyminer_stats(woodyminer_stats, vast_instances)
            
            end_time = time.time()
            print(f"\n{MATRIX_BRIGHT_GREEN}Total time to fetch and display stats: {end_time - start_time:.2f} seconds{Style.RESET_ALL}")

        elif choice == "2":
            max_bid = input(f"{MATRIX_CYAN}Enter your maximum spend limit per hour (e.g., 0.07): {Style.RESET_ALL}")
            try:
                max_bid = float(max_bid)
            except ValueError:
                print(f"{MATRIX_RED}Invalid input for spend limit. Please enter a valid number.{Style.RESET_ALL}")
                continue

            min_gpus = input(f"{MATRIX_CYAN}Enter minimum number of GPUs (or press Enter for no minimum): {Style.RESET_ALL}")
            max_gpus = input(f"{MATRIX_CYAN}Enter maximum number of GPUs (or press Enter for no maximum): {Style.RESET_ALL}")

            min_gpus = int(min_gpus) if min_gpus.isdigit() else None
            max_gpus = int(max_gpus) if max_gpus.isdigit() else None

            while True:
                print(f"\n{MATRIX_BRIGHT_GREEN}Search for GPU offers:{Style.RESET_ALL}\n")
                print(f"{MATRIX_CYAN}0. Exit to previous menu{Style.RESET_ALL}")
                print(f"{MATRIX_CYAN}1. Lowest Price/hr{Style.RESET_ALL}")
                print(f"{MATRIX_CYAN}2. Highest Total TFLOPS{Style.RESET_ALL}")
                print(f"{MATRIX_CYAN}3. Highest TFLOPS/${Style.RESET_ALL}\n")

                offer_type = input(f"{MATRIX_CYAN}Enter your choice: {Style.RESET_ALL}").upper()

                if offer_type == '0':
                    break

                criterion = {'1': 'dph_total', '2': 'total_flops', '3': 'flops_per_dphtotal'}.get(offer_type, '')

                top_offers = search_top_offers(criterion=criterion, max_bid=max_bid, min_gpus=min_gpus, max_gpus=max_gpus)
                if not top_offers:
                    print(f"{MATRIX_YELLOW}No offers to display.{Style.RESET_ALL}")
                    continue
                else:
                    print_offers(top_offers)

                offer_selection = input(f"\n{MATRIX_CYAN}Enter the numbers of the offers to purchase, 'R' to refresh prices, or 'X' to exit to the previous menu: {Style.RESET_ALL}").upper()
                if offer_selection == 'X':
                    break
                elif offer_selection == 'R':
                    continue
                else:
                    selected_indices = parse_selection(offer_selection)
                    for index in selected_indices:
                        if 1 <= index <= len(top_offers):
                            selected_offer = top_offers[index - 1]
                            print(f"{MATRIX_BRIGHT_GREEN}Purchasing offer ID {selected_offer['id']} with {selected_offer['gpu_name']} at ${selected_offer['dph_total']:.3f}/hr...{Style.RESET_ALL}")
                            # Ensure gpu_name is passed to create_instance
                            create_instance(selected_offer['id'], selected_offer['dph_total'], selected_offer['gpu_name'])
                        else:
                            print(f"{MATRIX_RED}Invalid selection: {index}. Please try again.{Style.RESET_ALL}")

        elif choice == "3":
            print(f"\n{MATRIX_BRIGHT_GREEN}Fetching instances for termination...{Style.RESET_ALL}")
            vast_instances = get_vast_instances()
            if vast_instances:
                terminate_instances(vast_instances)
            else:
                print(f"{MATRIX_YELLOW}No instances available to terminate.{Style.RESET_ALL}")

        elif choice == "4":
            print(f"\n{MATRIX_BRIGHT_GREEN}Exiting XenBlocks Mining Assistant. Goodbye!{Style.RESET_ALL}")
            break

        else:
            print(f"\n{MATRIX_RED}Invalid choice. Please try again.{Style.RESET_ALL}")


if __name__ == "__main__":
    main()

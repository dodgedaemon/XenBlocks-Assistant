import requests
import subprocess
import json
import os
from dotenv import load_dotenv
import platform
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Style, init
from collections import defaultdict
import uuid
import time

 
init(autoreset=True)

 
load_dotenv()
API_KEY = os.getenv('API_KEY')
ADDR = os.getenv('ADDR')

 
MATRIX_GREEN = Fore.GREEN
MATRIX_BRIGHT_GREEN = Fore.LIGHTGREEN_EX
MATRIX_DARK_GREEN = Fore.GREEN + Style.DIM
MATRIX_CYAN = Fore.CYAN
MATRIX_RED = Fore.RED
MATRIX_YELLOW = Fore.YELLOW

CUSTOM_NAME_FILE = "custom_names.json"

def display_splash_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

    splash_screen = f"""
{MATRIX_BRIGHT_GREEN}


██╗░░██╗███████╗███╗░░██╗██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗░██████╗
╚██╗██╔╝██╔════╝████╗░██║██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝██╔════╝
░╚███╔╝░█████╗░░██╔██╗██║██████╦╝██║░░░░░██║░░██║██║░░╚═╝█████═╝░╚█████╗░
░██╔██╗░██╔══╝░░██║╚████║██╔══██╗██║░░░░░██║░░██║██║░░██╗██╔═██╗░░╚═══██╗
██╔╝╚██╗███████╗██║░╚███║██████╦╝███████╗╚█████╔╝╚█████╔╝██║░╚██╗██████╔╝
╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝╚═════╝░╚══════╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░

░█████╗░░██████╗░██████╗██╗░██████╗████████╗░█████╗░███╗░░██╗████████╗
██╔══██╗██╔════╝██╔════╝██║██╔════╝╚══██╔══╝██╔══██╗████╗░██║╚══██╔══╝
███████║╚█████╗░╚█████╗░██║╚█████╗░░░░██║░░░███████║██╔██╗██║░░░██║░░░
██╔══██║░╚═══██╗░╚═══██╗██║░╚═══██╗░░░██║░░░██╔══██║██║╚████║░░░██║░░░
██║░░██║██████╔╝██████╔╝██║██████╔╝░░░██║░░░██║░░██║██║░╚███║░░░██║░░░
╚═╝░░╚═╝╚═════╝░╚═════╝░╚═╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝░░░╚═╝░░░

{MATRIX_DARK_GREEN}Welcome to the XenBlocks Mining Assistant - Woody Edition.

    - Create a .env file with Wallet Address and API variables.
    - Install the Vast.ai SDK and sign in. 
    - Script is open-source with zero fee collection: https://github.com/TreeCityWes/XenBlocks-Assistant.
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
    print(f"\n{MATRIX_CYAN}Fetching Vast.ai instances...{Style.RESET_ALL}")
    command = ["vastai", "show", "instances", "--raw"]
    result = run_vastai_command(command)
    if isinstance(result, list):
        print(f"{MATRIX_BRIGHT_GREEN}✔  - Successfully fetched {len(result)} Vast.ai instances.{Style.RESET_ALL}")
        return result
    else:
        print(f"{MATRIX_RED}✘  -  Error fetching instances.{Style.RESET_ALL}")
        return []

def get_woodyminer_stats(miner_address):
    print(f"\n{MATRIX_CYAN}Fetching WoodyMiner stats...{Style.RESET_ALL}")
    url = f"https://woodyminer.com/api/stat/get/{miner_address}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        stats = response.json()
        print(f"{MATRIX_BRIGHT_GREEN}✔  - Successfully fetched WoodyMiner stats for {len(stats)} workers.{Style.RESET_ALL}")
        print(f"")
        return stats
    except requests.RequestException as e:
        print(f"{MATRIX_RED}✘  -  Error fetching WoodyMiner stats: {str(e)}{Style.RESET_ALL}")
    except json.JSONDecodeError:
        print(f"{MATRIX_RED}✘  -  Error decoding WoodyMiner response{Style.RESET_ALL}")
    return []

def get_vast_instances():
    print(f"\n{MATRIX_CYAN}Fetching Vast.ai instances...{Style.RESET_ALL}")
    command = ["vastai", "show", "instances", "--raw"]
    result = run_vastai_command(command)
    if isinstance(result, list):
        print(f"{MATRIX_BRIGHT_GREEN}✔  - Successfully fetched {len(result)} Vast.ai instances.{Style.RESET_ALL}")
        return result
    else:
        print(f"{MATRIX_RED}✘  -  Error fetching instances.{Style.RESET_ALL}")
        return []

def get_woodyminer_stats(miner_address):
    print(f"\n{MATRIX_CYAN}Fetching WoodyMiner stats...{Style.RESET_ALL}")
    url = f"https://woodyminer.com/api/stat/get/{miner_address}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        stats = response.json()
        print(f"{MATRIX_BRIGHT_GREEN}✔  - Successfully fetched WoodyMiner stats for {len(stats)} workers.{Style.RESET_ALL}")
        return stats
    except requests.RequestException as e:
        print(f"{MATRIX_RED}✘  -  Error fetching WoodyMiner stats: {str(e)}{Style.RESET_ALL}")
    except json.JSONDecodeError:
        print(f"{MATRIX_RED}✘  -  Error decoding WoodyMiner response{Style.RESET_ALL}")
    return []

def store_instance_mapping(offer_id, instance_id):
    """
    Store the offer ID (custom name) and instance ID in a JSON file for later lookup.
    """
    try:
        with open(CUSTOM_NAME_FILE, "r") as f:
            instance_mappings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        instance_mappings = {}

     
    instance_mappings[offer_id] = instance_id

     
    with open(CUSTOM_NAME_FILE, "w") as f:
        json.dump(instance_mappings, f, indent=4)

def get_instance_mapping():
    """
    Retrieve the stored instance mappings from the JSON file.
    """
    try:
        with open(CUSTOM_NAME_FILE, "r") as f:
            instance_mappings = json.load(f)
            return instance_mappings if isinstance(instance_mappings, dict) else {}
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def create_instance(offer_id, price, gpu_name):
    custom_name = str(offer_id)   

    on_start_script = (
        f"env >> /etc/environment; "
        f"sudo apt install screen -y; "
        f"screen -S woodyminer -X quit 2>/dev/null; "
        f"screen -dmS woodyminer bash -c \"wget -N https://github.com/woodysoil/XenblocksMiner/releases/download/v1.4.0/xenblocksMiner-1.4.0-linux.tar.gz && "
        f"tar -zxvf xenblocksMiner-1.4.0-linux.tar.gz --overwrite && "
        f"chmod +x xenblocksMiner && "
        f"./xenblocksMiner --minerAddr {ADDR} --totalDevFee 0 --customName {custom_name}\"; "
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
            print(f"{MATRIX_BRIGHT_GREEN}✔  - Instance created with {gpu_name} at ${price}/hr (Custom Name: {custom_name}){Style.RESET_ALL}")
            
            try:
                instance_data = json.loads(result.stdout)
                instance_id = str(instance_data.get('new_contract'))
                if instance_id:
                    store_instance_mapping(offer_id, instance_id)
                    print(f"{MATRIX_CYAN}ℹ  - Saved offer ID '{offer_id}' with Instance ID '{instance_id}'.{Style.RESET_ALL}")
                    print(f"")

                else:
                    print(f"{MATRIX_YELLOW}⚠ Could not extract instance ID from the response.{Style.RESET_ALL}")
            except json.JSONDecodeError:
                print(f"{MATRIX_YELLOW}⚠ Could not parse the response as JSON.{Style.RESET_ALL}")

            return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"{MATRIX_RED}✘  -  Error creating instance: {e}{Style.RESET_ALL}")
        return None

def merge_vast_and_woodyminer(vast_instances, woodyminer_stats):
    instance_mapping = get_instance_mapping()
    woodyminer_by_custom_name = {stat['customName']: stat for stat in woodyminer_stats if stat['customName']}

    table = PrettyTable()
    table.field_names = [
        "#", "Instance ID", "GPU Type", "Count", "Status", "Cost/hr", "Hashrate", "Hashrate/$", 
        "XNM", "X.BLK", "Accepted", "Rejected", "Efficiency", "GPU Usage", "GPU Temp", 
        "Power", "Uptime", "Difficulty", "Last Update", "Version", "Machine ID"
    ]
    table.align = "l"

    merged_data = []
    total_gpu_count = 0
    gpu_counts = defaultdict(int)   

    for instance in vast_instances:
        instance_id = str(instance.get('id', 'N/A'))
        gpu_name = instance.get('gpu_name', 'N/A')
        status = instance.get('actual_status', 'N/A')
        num_gpus = instance.get('num_gpus', 1)   

        if status == 'running':
            gpu_counts[gpu_name] += num_gpus   
            total_gpu_count += num_gpus   

        cost_per_hour = instance.get('dph_total', 0)
        
        offer_id = next((key for key, value in instance_mapping.items() if value == instance_id), None)
        woodyminer_stat = woodyminer_by_custom_name.get(offer_id, {})

        if status == 'running':
            cpu_usage = instance.get('cpu_util', 'N/A')
            cpu_usage = f"{int(float(cpu_usage))}%" if cpu_usage not in ['N/A', None] else "N/A"
            gpu_usage = instance.get('gpu_util', 'N/A')
            gpu_usage = f"{int(float(gpu_usage))}%" if gpu_usage not in ['N/A', None] else "N/A"
            gpu_temp = instance.get('gpu_temp', 'N/A')
            gpu_temp = f"{int(float(gpu_temp))}°C" if gpu_temp not in ['N/A', None] else "N/A"
            hashrate = float(woodyminer_stat.get('totalHashrate', 0))
            hashrate_per_dollar = hashrate / cost_per_hour if cost_per_hour > 0 else 0
            accepted_blocks = woodyminer_stat.get('acceptedBlocks', 0)
            rejected_blocks = woodyminer_stat.get('rejectedBlocks', 0)
            uptime = format_uptime(woodyminer_stat.get('uptime', 0))
            xnm = woodyminer_stat.get('normalBlocks', 0)
            xblk = woodyminer_stat.get('superBlocks', 0)
            difficulty = woodyminer_stat.get('difficulty', 'N/A')
            total_power = woodyminer_stat.get('totalPower', 'N/A')
            efficiency = f"{hashrate / total_power:.2f}" if isinstance(total_power, (int, float)) and total_power > 0 else 'N/A'
            last_update = woodyminer_stat.get('status', 'N/A').replace('Offline, ', '')
            version = woodyminer_stat.get('version', 'N/A')
            machine_id = woodyminer_stat.get('machineId', 'N/A')
        else:
            cpu_usage = gpu_usage = gpu_temp = "N/A"
            hashrate = hashrate_per_dollar = 0
            accepted_blocks = rejected_blocks = xnm = xblk = 0
            uptime = difficulty = total_power = efficiency = last_update = version = machine_id = "N/A"

        merged_data.append({
            'index': len(merged_data) + 1,
            'instance_id': instance_id,
            'gpu_name': gpu_name,
            'num_gpus': num_gpus,   
            'status': status,
            'cost_per_hour': cost_per_hour,
            'gpu_usage': gpu_usage,
            'gpu_temp': gpu_temp,
            'hashrate': hashrate,
            'accepted_blocks': accepted_blocks,
            'rejected_blocks': rejected_blocks,
            'uptime': uptime,
            'hashrate_per_dollar': hashrate_per_dollar,
            'xnm': xnm,
            'xblk': xblk,
            'difficulty': difficulty,
            'total_power': total_power,
            'efficiency': efficiency,
            'last_update': last_update,
            'version': version,
            'machine_id': machine_id
        })

     
    merged_data.sort(key=lambda x: (x['status'] != 'running', -x['hashrate_per_dollar']))

    total_cost = 0
    total_hashrate = 0
    total_accepted = 0
    total_rejected = 0
    total_xnm = 0
    total_xblk = 0
    total_power = 0

    for idx, data in enumerate(merged_data, 1):
        if data['status'] == 'running':
            total_cost += data['cost_per_hour']
            total_hashrate += data['hashrate']
            total_accepted += data['accepted_blocks']
            total_rejected += data['rejected_blocks']
            total_xnm += data['xnm']
            total_xblk += data['xblk']
            if isinstance(data['total_power'], (int, float)):
                total_power += data['total_power']

        if data['status'] == 'running':
            status_color = MATRIX_BRIGHT_GREEN
            hashrate_color = MATRIX_RED if data['hashrate'] < 100 else MATRIX_YELLOW if data['hashrate'] < 1000 else MATRIX_GREEN
            hashrate_dollar_color = MATRIX_RED if data['hashrate_per_dollar'] < 10000 else MATRIX_YELLOW if data['hashrate_per_dollar'] < 30000 else MATRIX_GREEN
            rejected_color = MATRIX_RED if data['rejected_blocks'] > 0 else MATRIX_GREEN
            gpu_usage_color = MATRIX_RED if data['gpu_usage'] == 'N/A' or int(data['gpu_usage'].replace('%', '')) < 10 else MATRIX_YELLOW if int(data['gpu_usage'].replace('%', '')) < 30 else MATRIX_GREEN
            gpu_temp_color = MATRIX_RED if data['gpu_temp'] == 'N/A' or int(data['gpu_temp'].replace('°C', '')) > 85 else MATRIX_YELLOW if int(data['gpu_temp'].replace('°C', '')) > 75 else MATRIX_GREEN
            efficiency_color = MATRIX_RED if data['efficiency'] == 'N/A' or float(data['efficiency']) < 0.01 else MATRIX_YELLOW if float(data['efficiency']) < 0.02 else MATRIX_GREEN
        else:
            status_color = hashrate_color = hashrate_dollar_color = rejected_color = gpu_usage_color = gpu_temp_color = efficiency_color = MATRIX_RED

        table.add_row([
            f"{MATRIX_GREEN}{idx}{Style.RESET_ALL}",
            f"{status_color}{data['instance_id']}{Style.RESET_ALL}",
            f"{status_color}{data['gpu_name']}{Style.RESET_ALL}",
            f"{status_color}{data['num_gpus']}{Style.RESET_ALL}",  
            f"{status_color}{data['status']}{Style.RESET_ALL}",
            f"{status_color}${data['cost_per_hour']:.4f}{Style.RESET_ALL}",
            f"{hashrate_color}{data['hashrate']:.2f} H/s{Style.RESET_ALL}" if data['status'] == 'running' else f"{status_color}N/A{Style.RESET_ALL}",
            f"{hashrate_dollar_color}{data['hashrate_per_dollar']:.2f}{Style.RESET_ALL}" if data['status'] == 'running' else f"{status_color}N/A{Style.RESET_ALL}",
            f"{status_color}{data['xnm']}{Style.RESET_ALL}",
            f"{status_color}{data['xblk']}{Style.RESET_ALL}",
            f"{status_color}{data['accepted_blocks']}{Style.RESET_ALL}",
            f"{rejected_color}{data['rejected_blocks']}{Style.RESET_ALL}" if data['status'] == 'running' else f"{status_color}0{Style.RESET_ALL}",
            f"{efficiency_color}{data['efficiency']}{Style.RESET_ALL}",
            f"{gpu_usage_color}{data['gpu_usage']}{Style.RESET_ALL}" if data['status'] == 'running' else f"{status_color}N/A{Style.RESET_ALL}",
            f"{gpu_temp_color}{data['gpu_temp']}{Style.RESET_ALL}" if data['status'] == 'running' else f"{status_color}N/A{Style.RESET_ALL}",
            f"{status_color}{data['total_power']}{Style.RESET_ALL}",
            f"{status_color}{data['uptime']}{Style.RESET_ALL}",
            f"{status_color}{data['difficulty']}{Style.RESET_ALL}",
            f"{status_color}{data['last_update']}{Style.RESET_ALL}",
            f"{status_color}{data['version']}{Style.RESET_ALL}",
            f"{status_color}{data['machine_id']}{Style.RESET_ALL}"
        ])

    total_hashrate_per_dollar = total_hashrate / total_cost if total_cost > 0 else 0
    total_efficiency = total_hashrate / total_power if total_power > 0 else 0

    table.add_row(['-' * len(field) for field in table.field_names])
    table.add_row([
        f"{MATRIX_GREEN}TOTAL{Style.RESET_ALL}",
        f"{MATRIX_GREEN}---{Style.RESET_ALL}",
        f"{MATRIX_GREEN}---{Style.RESET_ALL}",
        f"{MATRIX_GREEN}{total_gpu_count}{Style.RESET_ALL}",  
        f"{MATRIX_GREEN}---{Style.RESET_ALL}", 
        f"{MATRIX_GREEN}${total_cost:.4f}{Style.RESET_ALL}",
        f"{MATRIX_GREEN}{total_hashrate:.2f} H/s{Style.RESET_ALL}",
        f"{MATRIX_GREEN}{total_hashrate_per_dollar:.2f}{Style.RESET_ALL}",
        f"{MATRIX_GREEN}{total_xnm}{Style.RESET_ALL}",
        f"{MATRIX_GREEN}{total_xblk}{Style.RESET_ALL}",
        f"{MATRIX_GREEN}{total_accepted}{Style.RESET_ALL}",
        f"{MATRIX_GREEN}{total_rejected}{Style.RESET_ALL}",
        f"{MATRIX_GREEN}{total_efficiency:.4f}{Style.RESET_ALL}",
        f"{MATRIX_GREEN}---{Style.RESET_ALL}",
        f"{MATRIX_GREEN}---{Style.RESET_ALL}",
        f"{MATRIX_GREEN}{total_power}{Style.RESET_ALL}",
        f"{MATRIX_GREEN}---{Style.RESET_ALL}",
        f"{MATRIX_GREEN}---{Style.RESET_ALL}",
        f"{MATRIX_GREEN}---{Style.RESET_ALL}",
        f"{MATRIX_GREEN}---{Style.RESET_ALL}",
        f"{MATRIX_GREEN}---{Style.RESET_ALL}"
    ])


    print(f"\n{MATRIX_BRIGHT_GREEN}XenBlocks Vast Assistant + WoodyMiner.com Stats:{Style.RESET_ALL}")
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

def terminate_instances(vast_instances, woodyminer_stats):
    instance_mapping = get_instance_mapping()
    woodyminer_by_custom_name = {stat['customName']: stat for stat in woodyminer_stats if stat['customName']}

    merged_data = []
    for instance in vast_instances:
        instance_id = str(instance.get('id', 'N/A'))
        offer_id = next((key for key, value in instance_mapping.items() if value == instance_id), None)
        woodyminer_stat = woodyminer_by_custom_name.get(offer_id, {})
        
        hashrate = float(woodyminer_stat.get('totalHashrate', 0))
        cost_per_hour = instance.get('dph_total', 0)
        hashrate_per_dollar = hashrate / cost_per_hour if cost_per_hour > 0 else 0

        merged_data.append({
            'instance': instance,
            'hashrate_per_dollar': hashrate_per_dollar
        })

     
    sorted_data = sorted(merged_data, key=lambda x: (x['instance']['actual_status'] != 'running', -x['hashrate_per_dollar']))

     
    merge_vast_and_woodyminer([item['instance'] for item in sorted_data], woodyminer_stats)

    while True:
        selection = input(f"\n{MATRIX_CYAN}Enter the number(s) of the instance(s) to terminate (comma-separated), or 'q' to quit: {Style.RESET_ALL}").strip()
        if selection.lower() == 'q':
            return

        selected_indices = parse_selection(selection)

        if all(1 <= idx <= len(sorted_data) for idx in selected_indices):
            selected_instances = [sorted_data[idx - 1]['instance'] for idx in selected_indices]
            break
        else:
            print(f"{MATRIX_RED}Invalid selection. Please enter valid instance numbers.{Style.RESET_ALL}")

     
    for instance in selected_instances:
        instance_id = instance['id']
        print(f"{MATRIX_YELLOW}Terminating instance {instance_id}{Style.RESET_ALL}")
        
        command = ["vastai", "destroy", "instance", str(instance_id)]
        result = run_vastai_command(command)
        if result:
            print(f"{MATRIX_BRIGHT_GREEN}✔ - Successfully terminated {instance_id}{Style.RESET_ALL}")
            
             
            for offer_id, mapped_instance_id in instance_mapping.items():
                if mapped_instance_id == instance_id:
                    del instance_mapping[offer_id]
                    break
            
             
            with open(CUSTOM_NAME_FILE, "w") as f:
                json.dump(instance_mapping, f, indent=4)
            
            print(f"{MATRIX_CYAN}ℹ Updated instance mapping{Style.RESET_ALL}")
            print(f"")
        else:
            print(f"{MATRIX_RED}✘ - Failed to terminate {instance_id}{Style.RESET_ALL}")

    print(f"{MATRIX_BRIGHT_GREEN}Termination process completed.{Style.RESET_ALL}")

def main():
    display_splash_screen()

    while True:
        print(f"\n{MATRIX_BRIGHT_GREEN}═══════════════════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{MATRIX_BRIGHT_GREEN}           XenBlocks Mining Assistant - Main Menu           {Style.RESET_ALL}")
        print(f"{MATRIX_BRIGHT_GREEN}═══════════════════════════════════════════════════════════{Style.RESET_ALL}")
        print(f"{MATRIX_CYAN}[1]{Style.RESET_ALL} {MATRIX_BRIGHT_GREEN}View Vast.ai and WoodyMiner.com Miner Stats{Style.RESET_ALL}")
        print(f"{MATRIX_CYAN}[2]{Style.RESET_ALL} {MATRIX_BRIGHT_GREEN}Buy XenBlocks Miners on Vast.ai{Style.RESET_ALL}")
        print(f"{MATRIX_CYAN}[3]{Style.RESET_ALL} {MATRIX_BRIGHT_GREEN}Terminate Vast.ai Instances{Style.RESET_ALL}")
        print(f"{MATRIX_CYAN}[4]{Style.RESET_ALL} {MATRIX_BRIGHT_GREEN}Exit{Style.RESET_ALL}")
        print(f"{MATRIX_BRIGHT_GREEN}═══════════════════════════════════════════════════════════{Style.RESET_ALL}")

        choice = input(f"\n{MATRIX_CYAN}Enter your choice (1-4): {Style.RESET_ALL}")

        if choice == "1":
            print(f"\n{MATRIX_BRIGHT_GREEN}Fetching mining stats...{Style.RESET_ALL}")
            start_time = time.time()

            vast_instances = get_vast_instances()
            woodyminer_stats = get_woodyminer_stats(ADDR)

            merge_vast_and_woodyminer(vast_instances, woodyminer_stats)

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
                print(f"\n{MATRIX_BRIGHT_GREEN}═══════════════════════════════════{Style.RESET_ALL}")
                print(f"{MATRIX_BRIGHT_GREEN}      Search for GPU offers        {Style.RESET_ALL}")
                print(f"{MATRIX_BRIGHT_GREEN}═══════════════════════════════════{Style.RESET_ALL}")
                print(f"{MATRIX_CYAN}[0]{Style.RESET_ALL} {MATRIX_BRIGHT_GREEN}Exit to previous menu{Style.RESET_ALL}")
                print(f"{MATRIX_CYAN}[1]{Style.RESET_ALL} {MATRIX_BRIGHT_GREEN}Lowest Price/hr{Style.RESET_ALL}")
                print(f"{MATRIX_CYAN}[2]{Style.RESET_ALL} {MATRIX_BRIGHT_GREEN}Highest Total TFLOPS{Style.RESET_ALL}")
                print(f"{MATRIX_CYAN}[3]{Style.RESET_ALL} {MATRIX_BRIGHT_GREEN}Highest TFLOPS/${Style.RESET_ALL}")
                print(f"{MATRIX_BRIGHT_GREEN}═══════════════════════════════════{Style.RESET_ALL}")

                offer_type = input(f"\n{MATRIX_CYAN}Enter your choice (0-3): {Style.RESET_ALL}").upper()

                if offer_type == '0':
                    break

                criterion = {'1': 'dph_total', '2': 'total_flops', '3': 'flops_per_dphtotal'}.get(offer_type, '')

                top_offers = search_top_offers(criterion=criterion, max_bid=max_bid, min_gpus=min_gpus, max_gpus=max_gpus)
                if not top_offers:
                    print(f"{MATRIX_YELLOW}No offers to display.{Style.RESET_ALL}")
                    continue
                else:
                    print_offers(top_offers)

                offer_selection = input(f"\n{MATRIX_CYAN}Enter the numbers of the offers to purchase, 'R' to refresh prices, or 'X' to exit: {Style.RESET_ALL}").upper()
                print(f"")
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
                            create_instance(selected_offer['id'], selected_offer['dph_total'], selected_offer['gpu_name'])
                        else:
                            print(f"{MATRIX_RED}Invalid selection: {index}. Please try again.{Style.RESET_ALL}")

        elif choice == "3":
            print(f"\n{MATRIX_BRIGHT_GREEN}Fetching instances for termination...{Style.RESET_ALL}")
            vast_instances = get_vast_instances()
            woodyminer_stats = get_woodyminer_stats(ADDR)
            if vast_instances:
                terminate_instances(vast_instances, woodyminer_stats)
            else:
                print(f"{MATRIX_YELLOW}No instances available to terminate.{Style.RESET_ALL}")

        elif choice == "4":
            print(f"\n{MATRIX_BRIGHT_GREEN}Thank you for using XenBlocks Mining Assistant. Goodbye!{Style.RESET_ALL}")
            break

        else:
            print(f"\n{MATRIX_RED}Invalid choice. Please enter a number between 1 and 4.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

import ping3  
import concurrent.futures
import subprocess
from colorama import init, Fore, Style

def ip_range(start_ip, end_ip):
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start.copy()
    ip_range_list = []

    ip_range_list.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1, 0):
            if temp[i] == 256:
                temp[i] = 0
                temp[i-1] += 1
        temp = start.copy()
        ip_range_list.append(".".join(map(str, temp)))

    return ip_range_list

def check_ip(ip):
    responses = []
    for _ in range(3):  # Ping three times to confirm
        response = ping3.ping(ip, timeout=1)
        responses.append(response)
    # If at least one response is not None, consider the IP active
    if any(responses):
        return ip
    else:
        return None

def check_multiple_ips(ip_list):
    active_ips = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(check_ip, ip_list))
    for result in results:
        if result:
            active_ips.append(result)
    return active_ips

def display_ips_with_highlight(ip_list, search_term):
    found_ips = 0
    for ip in ip_list:
        if search_term in ip:
            print(f"{Fore.GREEN}{ip}{Style.RESET_ALL}")
            found_ips += 1
        else:
            print(ip)
    print(f"\n</> Number of found IPs: {found_ips}\n")

def search_ip(ip_list):
    while True:
        search_term = input("</> Enter the last octet to search (or type 'exit' to quit): ")
        if search_term.lower() == 'exit':
            break
        search_term = f".{search_term}"
        subprocess.call("cls", shell=True)
        display_ips_with_highlight(ip_list, search_term)

if __name__ == "__main__":
    init(autoreset=True)

    # Define the range of IP addresses
    start_ip = "10.10.23.1"
    end_ip = "10.10.23.254"

    ip_list = ip_range(start_ip, end_ip)

    active_ips = check_multiple_ips(ip_list)

    if active_ips:
        print("\n</> Active IPs:\n")
        for ip in active_ips:
            print(ip)
        print(f"\n</> Number of active IPs: {len(active_ips)}\n")
    else:
        print("</> No active IPs found.")
    
    # Start the IP search functionality
    search_ip(active_ips)


import requests
import time
import json
from cmd import Cmd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import threading
import concurrent.futures

# List of miner device IP addresses and hostnames
miner_devices = []

# Alert thresholds
alert_thresholds = {
    "hashRate": None,
    "fanSpeed": None,
    "bestShare": None,
}

# Function to fetch data from a miner device
def fetch_miner_data(ip):
    url = f"http://{ip}/api/system/info"
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
        data = response.json()
        data['ip'] = ip
        return data
    except requests.RequestException:
        return None

# Function to display miner data
def display_miner_data(miner_data_list):
    for miner_data in miner_data_list:
        if miner_data is None:
            continue
        if 'error' in miner_data:
            print(f"IP Address: {miner_data['ip']} - Error: {miner_data['error']}")
        else:
            for key, value in miner_data.items():
                print(f"{key}: {value}")
            print()

# Function to scan a range of IPs
def scan_ip_range(ip_range):
    devices = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future_to_ip = {executor.submit(fetch_miner_data, f"{ip_range}.{i}"): i for i in range(1, 255)}
        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                data = future.result()
                if data is not None:
                    devices.append(data)
            except Exception as exc:
                print(f"IP {ip_range}.{ip} generated an exception: {exc}")
    return devices

# Initialize data structures for real-time charting
metrics = {
    'power': deque(maxlen=20),
    'voltage': deque(maxlen=20),
    'hashRate': deque(maxlen=20),
    'temp': deque(maxlen=20),
    'sharesAccepted': deque(maxlen=20),
    'sharesRejected': deque(maxlen=20),
}

fig, axes = plt.subplots(5, 1, figsize=(10, 15))
plt.subplots_adjust(hspace=0.5)
ax1, ax2, ax3, ax4, ax5 = axes
current_ip = None
selected_metrics = []

def animate(i):
    if current_ip:
        miner_data = fetch_miner_data(current_ip)
        if 'error' not in miner_data:
            if 'power' in selected_metrics:
                metrics['power'].append(miner_data['power'])
                ax1.clear()
                ax1.plot(metrics['power'], label='Power (W)')
                ax1.legend(loc='upper left')
                ax1.set_title('Power Over Time')

            if 'voltage' in selected_metrics:
                metrics['voltage'].append(miner_data['voltage'])
                ax2.clear()
                ax2.plot(metrics['voltage'], label='Voltage (V)')
                ax2.legend(loc='upper left')
                ax2.set_title('Voltage Over Time')

            if 'hashRate' in selected_metrics:
                metrics['hashRate'].append(miner_data['hashRate'])
                ax3.clear()
                ax3.plot(metrics['hashRate'], label='Hash Rate (MH/s)')
                ax3.legend(loc='upper left')
                ax3.set_title('Hash Rate Over Time')
                if alert_thresholds["hashRate"] and miner_data['hashRate'] > alert_thresholds["hashRate"]:
                    print(f"Alert: Hash rate exceeded threshold! Current: {miner_data['hashRate']} MH/s")

            if 'temp' in selected_metrics:
                metrics['temp'].append(miner_data['temp'])
                ax4.clear()
                ax4.plot(metrics['temp'], label='Temperature (°C)')
                ax4.legend(loc='upper left')
                ax4.set_title('Temperature Over Time')

            if 'shares' in selected_metrics:
                metrics['sharesAccepted'].append(miner_data['sharesAccepted'])
                metrics['sharesRejected'].append(miner_data['sharesRejected'])
                ax5.clear()
                ax5.plot(metrics['sharesAccepted'], label='Shares Accepted')
                ax5.plot(metrics['sharesRejected'], label='Shares Rejected')
                ax5.legend(loc='upper left')
                ax5.set_title('Shares Over Time')

class MinerMonitor(Cmd):
    prompt = 'miner-monitor> '
    intro = """

                ⠀⠀⠀⠀⠀⣀⣤⣴⣶⣾⣿⣿⣿⣿⣷⣶⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀⠀⠀
            ⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀
            ⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⠟⠿⠿⡿⠀⢰⣿⠁⢈⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀
            ⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣤⣄⠀⠀⠀⠈⠉⠀⠸⠿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀
            ⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⢠⣶⣶⣤⡀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⡆
            ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠼⣿⣿⡿⠃⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣷
            ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢀⣀⣀⠀⠀⠀⠀⢴⣿⣿⣿⣿⣿⣿⣿⣿⣿
            ⢿⣿⣿⣿⣿⣿⣿⣿⢿⣿⠁⠀⠀⣼⣿⣿⣿⣦⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⡿
            ⠸⣿⣿⣿⣿⣿⣿⣏⠀⠀⠀⠀⠀⠛⠛⠿⠟⠋⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⠇
            ⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⣤⡄⠀⣀⣀⣀⣀⣠⣾⣿⣿⣿⣿⣿⣿⣿⡟⠀
            ⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣄⣰⣿⠁⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀
            ⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀
            ⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⢿⣿⣿⣿⣿⡿⠿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀
                    AxePy Bitcoin
    
    Welcome to the AexPy Monitor Shell for BitAxe!

    This tool allows you to monitor and manage your BitAxe mining devices.
    You can fetch data, add or remove devices, list all devices,
    and display real-time charts for power, voltage, hash rate, and temperature and more!
    You can also set realtime alerts to keep track of your Axefarms!  

    Call each miner by hostname to save time hunting for the IP! 

    Tips Welcome : bc1q5686360yzeuv06awhx9aufs2kfajwgmpt4dkw9
    Donate Some Hashrate :  Worker bc1qtesc50ye5euqtr67sdqke8xdwef6klasc5vx59.Donate
                            Pool : solo.ckpool.org
                            Port : 3333
                            Password : x

    Feature requests accepted!

    Type ? to list commands, or help <command> for details on a specific command.
"""

    def do_fetch(self, args):
        """Fetch and display data from all or a specific miner device.
        
        Usage: fetch [hostname]
        Example: fetch
                 fetch Tr3y
        """
        hostname = args.strip()
        if hostname:
            device = next((d for d in miner_devices if d['hostname'] == hostname), None)
            if device:
                miner_data_list = [fetch_miner_data(device['ip'])]
            else:
                print(f"Hostname {hostname} not found.")
                return
        else:
            miner_data_list = [fetch_miner_data(device['ip']) for device in miner_devices]
        display_miner_data(miner_data_list)

    def do_add(self, args):
        """Add a new miner device IP and hostname to the list.
        
        Usage: add <IP_ADDRESS> <HOSTNAME>
        Example: add 192.168.0.190 Miner2
        """
        parts = args.strip().split()
        if len(parts) == 2:
            ip, hostname = parts
            miner_devices.append({"ip": ip, "hostname": hostname})
            print(f"Added IP: {ip}, Hostname: {hostname}")
        else:
            print("Usage: add <IP_ADDRESS> <HOSTNAME>")

    def do_remove(self, args):
        """Remove a miner device IP from the list.
        
        Usage: remove <IP_ADDRESS>
        Example: remove 192.168.0.190
        """
        ip = args.strip()
        global miner_devices
        miner_devices = [device for device in miner_devices if device['ip'] != ip]
        print(f"Removed IP: {ip}")

    def do_list(self, args):
        """List all miner device IPs and hostnames.
        
        Usage: list
        """
        print("Miner Devices:")
        for device in miner_devices:
            print(f"  IP: {device['ip']}, Hostname: {device['hostname']}")

    def do_chart(self, args):
        """Display real-time charts for power, voltage, hash rate, temperature, and/or shares.
        
        Usage: chart
        """
        print("Select a miner from the list:")
        for idx, device in enumerate(miner_devices):
            print(f"{idx + 1}. IP: {device['ip']}, Hostname: {device['hostname']}")
        
        try:
            selection = int(input("Enter the number of the miner: ")) - 1
            if 0 <= selection < len(miner_devices):
                selected_device = miner_devices[selection]
                global current_ip, selected_metrics
                current_ip = selected_device['ip']
                
                metrics = input("Enter the metrics to display (power, voltage, hashRate, temp, shares, all): ").strip().split()
                if 'all' in metrics:
                    selected_metrics = ['power', 'voltage', 'hashRate', 'temp', 'shares']
                else:
                    selected_metrics = metrics

                chart_thread = threading.Thread(target=self.run_chart)
                chart_thread.start()
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def run_chart(self):
        ani = animation.FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
        plt.show()

    def do_set_alert(self, args):
        """Set alert thresholds for monitoring metrics.
        
        Usage: set_alert <metric> <value>
        Metrics: hashRate, fanSpeed, bestShare
        Example: set_alert hashRate 600
                 set_alert fanSpeed 5000
                 set_alert bestShare 1000M
        """
        parts = args.strip().split()
        if len(parts) == 2:
            metric, value = parts
            if metric in alert_thresholds:
                alert_thresholds[metric] = float(value) if metric != 'bestShare' else value
                print(f"Alert threshold set for {metric}: {value}")
            else:
                print("Invalid metric. Available metrics: hashRate, fanSpeed, bestShare")
        else:
            print("Usage: set_alert <metric> <value>")

    def do_autofind(self, args):
        """Automatically find and add miner devices in the network.
        
        Usage: autofind
        """
        print("Starting autofind for miners in the network...")
        ip_ranges = ['192.168.0', '10.10.0']
        for ip_range in ip_ranges:
            print(f"Scanning IP range {ip_range}.1-254...")
            devices = scan_ip_range(ip_range)
            for device in devices:
                existing_device = next((d for d in miner_devices if d['ip'] == device['ip']), None)
                if not existing_device:
                    miner_devices.append({"ip": device['ip'], "hostname": device['hostname']})
                    print(f"Found and added device: IP={device['ip']}, Hostname={device['hostname']}")
        print("Autofind complete.")

    def do_stats(self, args):
        """Display the full API output for a selected miner.
        
        Usage: stats
        """
        print("Select a miner from the list:")
        for idx, device in enumerate(miner_devices):
            print(f"{idx + 1}. IP: {device['ip']}, Hostname: {device['hostname']}")
        
        try:
            selection = int(input("Enter the number of the miner: ")) - 1
            if 0 <= selection < len(miner_devices):
                selected_device = miner_devices[selection]
                miner_data = fetch_miner_data(selected_device['ip'])
                if miner_data:
                    for key, value in miner_data.items():
                        print(f"{key}: {value}")
                else:
                    print("Failed to fetch data from the selected miner.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def do_quit(self, args):
        """Quit the Miner Monitor Shell.
        
        Usage: quit
        """
        print("Quitting Miner Monitor Shell.")
        return True

if __name__ == "__main__":
    MinerMonitor().cmdloop()



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

miner-monitor> help

Documented commands (type help <topic>):
========================================
add  autofind  chart  fetch  help  list  quit  remove  set_alert  stats

miner-monitor>  add
Add a new miner device IP and hostname to the list.
        
        Usage: add <IP_ADDRESS> <HOSTNAME>
        Example: add 192.168.0.190 Miner2
        
miner-monitor> autofind
Automatically find and add miner devices in the network.
        
        Usage: autofind
        
miner-monitor> chart
Display real-time charts for power, voltage, hash rate, temperature, and/or shares.
        
        Usage: chart
        
miner-monitor> list
List all miner device IPs and hostnames.
        
        Usage: list
        
Remove a miner device IP from the list.
        
        Usage: remove <IP_ADDRESS>
        Example: remove 192.168.0.190
        
miner-monitor> set_alert
Set alert thresholds for monitoring metrics.
        
        Usage: set_alert <metric> <value>
        Metrics: hashRate, fanSpeed, bestShare
        Example: set_alert hashRate 600
                 set_alert fanSpeed 5000
                 set_alert bestShare 1000M
        
miner-monitor> stats

Display the full API output for a selected miner.
        
        Usage: stats

# AxePy Monitor Shell for BitAxe

Welcome to the AxePy Monitor Shell for BitAxe!

This tool allows you to monitor and manage your BitAxe mining devices. You can fetch data, add or remove devices, list all devices, and display real-time charts for power, voltage, hash rate, temperature, and more! Additionally, you can set real-time alerts to keep track of your mining devices.

## Features

- Fetch and display data from all or specific miner devices
- Add or remove miner devices dynamically
- List all miner devices with their IPs and hostnames
- Display real-time charts for various metrics
- Set alert thresholds for monitoring key metrics
- Automatically find and add miner devices within specified IP ranges

Tips and Donations
Tips are welcome: bc1q5686360yzeuv06awhx9aufs2kfajwgmpt4dkw9

Donate some hashrate:

Worker: bc1qtesc50ye5euqtr67sdqke8xdwef6klasc5vx59.Donate
Pool: solo.ckpool.org
Port: 3333
Password: x






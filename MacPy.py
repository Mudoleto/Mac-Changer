#Bookstore imports
import subprocess
import optparse
import re
import sys
from termcolor import colored, cprint

def get_arguments():

    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest = "interface",
                      help = "Interface to change Mac Address")

    parser.add_option("-m", "--mac", dest = "new_mac", 
                      help = "New Mac Address")

    parser.add_option("-d", "--devices", dest = "devices",
                      help = "Number of network devices, '-d yes' ")

    parser.add_option("-l", "--list", dest = "list",
                      help = "MAC addresses in your local network, '-l yes' ")

    (options, arguments) = parser.parse_args()

    if not options.interface and not options.new_mac and not options.devices and not options.list:
        parser.error("[-] Please provide at least one argument, use --help for more information")
    return options

def change_mac(interface, new_mac):

    cprint("[+] Changi mac address to {} by {}".format(interface, new_mac), 'green')
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):

    ifconfig_result = subprocess.check_output(["ifconfig", options.interface]).decode("utf-8")
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        cprint("[-] Cannot read mac address",'red')


def network_devices():

    number_device = subprocess.check_output("ifconfig | awk -F': ' '/^[^ ]/ {print $1}' | wc -l", shell = True)
    number_device = number_device.strip()
    number_device = number_device.decode("utf-8")
    cprint("[+]Number of network devices:{}".format(number_device),'green')
    cprint("│",'blue')

    net_device = subprocess.check_output("ifconfig | awk -F': ' '/^[^ ]/ {print $1}' | sort", shell = True)
    net_device = net_device.strip()
    net_device = net_device.decode("utf-8")
    net_device = net_device.split('\n')

    for i in net_device:
        cprint("├──{}".format(i),'blue')
    cprint("│\n└── This are devices, select one and then use the program",'blue')

def MAC_localhost():
    local_macs = subprocess.check_output("sudo arp-scan -I enp0s3 --localnet | grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}' | egrep -v Interface | sort", shell =True)

    local_macs = local_macs.strip()
    local_macs = local_macs.decode("utf-8")
    local_macs = local_macs.split('\n')
    cprint("[+]These are the mac addresses in your local network:",'red')
    
    for i in local_macs:
        cprint("├──{}".format(i),'yellow')
    cprint("│\n└──These are the mac addresses in your local network",'yellow')


if __name__ == "__main__":
    options = get_arguments()

    if options.devices == 'yes':
        network_devices()
        sys.exit()
    
    elif options.list == 'yes':
        MAC_localhost()
        sys.exit()

    elif options.interface and options.new_mac:
        current_mac = get_current_mac(options.interface)
        current_mac = str(current_mac)
        cprint("[+] Current MAC = {}".format(current_mac),'yellow')

        change_mac(options.interface, options.new_mac)
        current_mac = get_current_mac(options.interface)

        if current_mac == options.new_mac:
            cprint("[+] The Mac address has been successfully changed to:{}".format(current_mac),'magenta')
        else:
            cprint("[-] Mac address could not be changed", 'red')
            sys.exit(1)

    else:
        cprint("[-] No appropriate action provided, use the --help command to view the help panel.", 'red')

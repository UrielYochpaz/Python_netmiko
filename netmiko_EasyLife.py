# Creator : Uriel Yochpaz

# Imports
import re
import time
import sys
import netmiko
import telnetlib

# Constants
USER = 'user'  # Change it to your Username
PASS = 'password'  # Change it to your Password
l_telnet = []


def connect_telnet(ip):
    
    """
    connect_telnet(ip) >>> bool
    This function run commands on network devices via TELNET protocol
    and creates report on devices that supports Telnet
    """
    
    # Try to connect with Telnet
    try:
        device = telnetlib.Telnet(ip)
    # The device doesnt support either SSH or Telnet   
    except:
        return False
    
    device.read_until("Username: ")
    device.write(USER + "\n")
    device.read_until("Password: ")
    device.write(PASS + "\n")

    # Telnet is sucks
    time.sleep(1.5)

    try:
        msg = device.read_until("Login invalid", timeout=1)
        if "Login invalid" in msg:
            print "Wrong credentials with Telnet"
            return False
    except:
        pass
    
    print "Connected with Telnet"
    device.write("config t" + "\n")
    device.read_until("#")
    device.write("ENTER COMMAND HERE" + "\n")
    device.read_until("#")
    device.write("ENTER COMMAND HERE" + "\n")
    device.read_until("#")
    device.write("ENTER COMMAND HERE" + "\n")
    device.read_until("#")
  
    print "Configuration committed successfully with Telnet at IP: {}\n".format(ip)

    # Report on Telnet devices (Unsecured)
    with open(r"Telnet_devices.txt", 'a') as log:
            log.write(ip+'\n')
    return True


def connect_ssh(ip):
    
    """
    check_ssh(ip) >>> bool
    This function run commands on network devices via SSH protocol
    """

    print "Trying to connect with SSH to {}...".format(ip)

    # Trying to connect with SSH
    try:
        device = netmiko.ConnectHandler(device_type='cisco_ios', ip = ip, username = USER, password = PASS)

    # Wrong Credential's Error
    except netmiko.NetMikoAuthenticationException:
        print "Wrong Credentials (Username or Password) for SSH!\n"
        sys.exit(0)

    # Here, sys.exit(0) means continue to next device

    # SSH is disable Error
    except netmiko.NetMikoTimeoutException:
        print "SSH is disabled on {}".format(ip)
        if connect_telnet(ip) is False:
            print "Failed to connect to {} with SSH and Telnet".format(ip)
            sys.exit(0)
        else:
            return True
    except:
        sys.exit(0)

    try:
        # Entering config mode
        device.config_mode()  # If you run only Show Commands you do not need this

    # Something wrong with netmiko module
    except:
        sys.exit(0)

    device.send_command("ENTER COMMAND HERE")
    device.send_command("ENTER COMMAND HERE")
    device.send_command("ENTER COMMAND HERE")

    # Exit config mode
    device.exit_config_mode()

    # Saves configuration
    device.send_command("wr")

    # Disconnect device
    device.disconnect()

    print "Done with {} !\n".format(ip)


def main():

    # You can change the following and run the script only on one device. Just delete lines 124-133
    # and put device ip in connect_ssh function()

    # Read all ip's
    with open(r"Devices ip's.txt", 'r') as f:
        data = f.read()

    # Ip regex pattern   
    pat = r'(?:\d{1,3}\.){3}\d{1,3}'

    # Get all ip's 
    l_ip = re.findall(pat, data)
    
    for ip in l_ip:
        try:
            connect_ssh(ip)
            
        # Something wrong with the device 
        except SystemExit:
            continue
        

if __name__ == '__main__':
    main()

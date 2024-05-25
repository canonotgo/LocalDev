from scapy.all import *
import requests
import json

def parse_ssdp(pcap_file):
    packets = rdpcap(pcap_file)

    for packet in packets:
        if UDP in packet and packet[UDP].dport == 1900:
            ssdp_data = bytes(packet[UDP].payload)
            ssdp_lines = ssdp_data.decode().split('\r\n')

            ssdp_info = {
                'Method': ssdp_lines[0].split(' ')[0],
                'URL': ssdp_lines[0].split(' ')[1],
                'Protocol': ssdp_lines[0].split(' ')[2],
                'Headers': {}
            }

            for line in ssdp_lines[1:]:
                if line:
                    key, value = line.split(': ', 1)
                    ssdp_info['Headers'][key] = value

            # Get ip and mac for src dev
            ssdp_info['src_ip'] = packet[IP].src
            ssdp_info['src_mac'] = packet[Ether].src.upper()
            print(ssdp_info)
            url = "http://127.0.0.1:5000/api/ssdp"
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(ssdp_info), headers=headers)
            if response.status_code == 200:
                print("\033[92mDone\033[0m")
            else:
                print("\033[91mError\033[0m")
            # break

# read pcap file
parse_ssdp('windows.pcapng')


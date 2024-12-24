from scapy.all import ARP, Ether, srp
import threading
import time
from flask import Flask, jsonify, request

app = Flask(__name__)

# Global dictionary to store ARP records
arp_records = {}

def arp_scan(target_ip):
    global arp_records
    # Create an ARP request packet
    arp_request = ARP(pdst=target_ip)
    # Create an Ethernet frame with broadcast destination
    broadcast_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Combine the ARP request with the Ethernet frame
    packet = broadcast_frame / arp_request

    # Send the packet and receive the response
    result = srp(packet, timeout=3, verbose=0)[0]

    # Temporary dictionary to store discovered clients
    current_records = {}

    for sent, received in result:
        # Append discovered IP and MAC address to the current records
        current_records[received.psrc] = received.hwsrc

    # Update the global ARP records
    arp_records = current_records
    print(arp_records)
    print("ARP scan completed. Records updated.")

def periodic_scan(target_ip, interval=120):
    while True:
        arp_scan(target_ip)
        time.sleep(interval)

@app.route('/check_ip', methods=['GET'])
def check_ip():
    ip_address = request.args.get('ip')
    if ip_address in arp_records:
        return jsonify({'ip': ip_address, 'mac': arp_records[ip_address], 'status': 'alive'})
    else:
        return jsonify({'ip': ip_address, 'status': 'not found'})

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <target_ip>")
        sys.exit(1)
    
    target_ip = sys.argv[1]

    # Start the periodic ARP scan in a separate thread
    scan_thread = threading.Thread(target=periodic_scan, args=(target_ip,))
    scan_thread.daemon = True
    scan_thread.start()

    # Start the Flask web server
    app.run(host='0.0.0.0', port=5001)

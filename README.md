# Project Title

The SSDP protocol in the packet is parsed and put data to Webpage

## How to use

Provide step-by-step instructions on how to  set up the project. This may include:

1. install requirements in your env
2. python WebApp.py && open http://127.0.0.1:5000/ on chrome(or other)
3. Use wireshark or tcpdump to collect data on the LAN and save it as pacpng
4. python ParseSSDPInPcap.py

## curl test

```
curl -X POST \
  http://localhost:5000/api/ssdp \
  -H 'Content-Type: application/json' \
  -d '{
    "Method": "M-SEARCH",
    "URL": "*",
    "Protocol": "HTTP/1.1",
    "Headers": {
      "HOST": "239.255.255.250:1900",
      "MAN": "\"ssdp:discover\"",
      "MX": "1",
      "ST": "urn:dial-multiscreen-org:service:dial:1",
      "USER-AGENT": "Google Chrome/124.0.6367.201 Windows"
    },
    "src_ip": "8.8.8.8",
    "src_mac": "AA:AA:AA:AA:AA:AA"
}'
```
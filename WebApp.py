from flask import Flask, request, render_template
from collections import defaultdict

app = Flask(__name__)

# for save data of SSDP
ssdp_data = defaultdict(lambda: {'count': 0, 'src_ip': '', 'src_mac': '', 'user_agent': ''})

@app.route('/')
def index():
    return render_template('index.html', ssdp_data=ssdp_data.values())

@app.route('/api/ssdp', methods=['POST'])
def receive_ssdp_data():
    data = request.get_json()
    print(data)
    key = f"{data['src_ip']}_{data['src_mac']}_{data['Headers']['USER-AGENT']}"

    if key in ssdp_data:
        ssdp_data[key]['count'] += 1
    else:
        ssdp_data[key] = {
            'count': 1,
            'src_ip': data['src_ip'],
            'src_mac': data['src_mac'],
            'user_agent': data['Headers']['USER-AGENT']
        }

    return "OK"

if __name__ == '__main__':
    app.run(debug=True)

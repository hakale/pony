from collections import OrderedDict
import requests
import json
import re
user = {
    'email': 'xxxx@xxx.com',
    'password': 'xxxxxx'
}
def login(userdata):
    return requests.post('https://app.arukas.io/api/login', data=userdata)
r = login(user)
print(r.cookies, r.status_code)
cont = requests.get('https://app.arukas.io/api/containers', cookies = r.cookies)
cont = json.loads(cont.text)
data = cont['data']
config = {
    "configs": [],
    "strategy": "com.shadowsocks.strategy.balancing",
    "index": -1,
    "global": 'false',
    "enabled": 'false',
    "shareOverLan": 'true',
    "isDefault": 'false',
    "localPort": 1080,
    "pacUrl": 'null',
    "useOnlinePac": 'false',
    "availabilityStatistics": 'false',
    "autoCheckUpdate": 'false',
    "isVerboseLogging": 'true',
    "logViewer": {
    "fontName": "Consolas",
    "fontSize": 8.25,
    "bgColor": "Black",
    "textColor": "White",
    "topMost": 'false',
    "wrapText": 'false',
    "toolbarShown": 'false',
    "width": 974,
    "height": 735,
    "top": 184,
    "left": 123,
    "maximized": 'false'
    },
    "useProxy": 'false',
    "proxyServer": 'null',
    "proxyPort": 0
}
for index, da in enumerate(data):
    if da['attributes']['is_running']:
        passwd = re.findall(r'(?<=-k\s).*?(?=\s)', da['attributes']['cmd']+' ')[0]
        meth = re.findall(r'(?<=-m\s).*?(?=\s)', da['attributes']['cmd']+' ')[0]
        ip = da['attributes']['port_mappings'][0][0]['host'].strip('seaof-').split('.')[0].replace('-','.')
        port = da['attributes']['port_mappings'][0][0]['service_port']
        dataC = {
          "server": ip,
          "server_port": port,
          "password": passwd,
          "method": meth,
          "remarks": "jpp" + str(index),
          "auth": 'false'
        }
        config["configs"].append(dataC)
with open('gui-config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)
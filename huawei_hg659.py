import requests
import hashlib
import base64
import re

#Enter WiFi MAC address for device running the script here
currentMACAddress = "E4:A7:A0:BB:A1:CA"
#Enter router interface login details here
username = "admin"
password = "admin@HG659"

#Router comms parameters
csrfParam = ""
csrfToken = ""
response = ""
SessionID_R3 = ""
hostList = []

def reboot_modem():
    global SessionID_R3
    global csrfParam
    global csrfToken
    global response
    get_advance_page()

    cookies = {
        'username': 'admin',
        'SessionID_R3': SessionID_R3,
        'activeMenuID': 'maintain_settings',
        'activeSubmenuID': 'device_mngt',
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'http://192.168.1.1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://192.168.1.1/html/advance.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    data = '{\"csrf\":{\"csrf_param\":\"' + csrfParam + '\",\"csrf_token\":\"' + csrfToken + '\"}}'

    try:
       response = requests.post('http://192.168.1.1/api/service/reboot.cgi', headers=headers, cookies=cookies, data=data, verify=False)
    except:
       None
    print("Rebooted modem.")


def create_router_session():
    global response

    #Retrieve SessionID for router
    cookies = {
        'username': 'admin',
        'SessionID_R3': 'utvoQg5xMQ1A5PtPVohRfi4576DxBR10SCiw03nCq4cICAGMdGhczBYNpSyTaQfe10r92o08hI6uTgKPRO0h8MlCt2iYQuyB4uYcT9ESnXE4SryfpuHTZkSEISxKuOc',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://192.168.1.1/html/wizard/wizard.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    response = requests.get('http://192.168.1.1/', headers=headers, cookies=cookies, verify=False)
    update_session_id()
    update_csrf_params()

def update_csrf_params():
    global response
    global csrfParam
    global csrfToken

    matchObj1 = re.search( r'csrf_param\" content=\"([^\"]*)', response.content.decode('utf-8'))
    matchObj2 = re.search( r'csrf_token\" content=\"([^\"]*)', response.content.decode('utf-8'))
    if matchObj1:
       csrfParam = matchObj1.group(1)
       #print("Set csrf_param to: " + csrfParam)
    else:
       None

    if matchObj2:
       csrfToken = matchObj2.group(1)
       #print("Set csrf_token to: " + csrfToken)
    else:
       None

def update_session_id():
    global response
    global SessionID_R3

    try:
        SessionID_R3 = response.headers['Set-Cookie'].split(';')[0].split('=')[1]
    except:
        None

#Logout of router
def router_logout():
    global SessionID_R3
    global response
    global csrfParam
    global csrfToken

    update_csrf_params()
    
    cookies = {
        'username': 'admin',
        'SessionID_R3': SessionID_R3,
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'http://192.168.1.1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://192.168.1.1/html/wizard/wizard.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    data = '{\"csrf\":{\"csrf_param\":\"' + csrfParam + '\",\"csrf_token\":\"' + csrfToken + '\"}}'

    response = requests.post('http://192.168.1.1/api/system/user_logout', headers=headers, cookies=cookies, data=data, verify=False)
   
#Login to router
def router_login():
    global response
    global csrfParam
    global csrfToken
    global SessionID_R3
    global username
    global password

    encryptedPassword = hashlib.sha256((username + base64.b64encode(hashlib.sha256(password.encode('utf-8')).hexdigest().encode('utf-8')).decode('utf-8') + csrfParam + csrfToken).encode('utf-8')).hexdigest()

    cookies = {
        'username': 'admin',
        'SessionID_R3': SessionID_R3,
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'http://192.168.1.1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://192.168.1.1/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    data = "{\"csrf\":{\"csrf_param\":\"" + csrfParam + "\",\"csrf_token\":\"" + csrfToken + "\"},\"data\":{\"UserName\":\"admin\",\"Password\":\"" + encryptedPassword + "\",\"isInstance\":true,\"isDestroyed\":false,\"isDestroying\":false,\"isObserverable\":true}}"
    response = requests.post('http://192.168.1.1/api/system/user_login', headers=headers, cookies=cookies, data=data, verify=False)
    update_session_id()
    return len(response.content.decode('utf-8'))

def get_advance_page():
    global response
    global SessionID_R3
    
    update_session_id()
    update_csrf_params()
    cookies = {
        'username': 'admin',
        'SessionID_R3': SessionID_R3,
    }

    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://192.168.1.1/html/wizard/wizard.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    response = requests.get('http://192.168.1.1/html/advance.html#landevices', headers=headers, cookies=cookies, verify=False)
    update_csrf_params()
    update_session_id()

def get_host_devices():
    global response
    global SessionID_R3
    global hostList
    
    cookies = {
        'username': 'admin',
        'SessionID_R3': SessionID_R3,
        'activeMenuID': 'homenetwork_settings',
        'activeSubmenuID': 'landevices',
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'Referer': 'http://192.168.1.1/html/advance.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }


    response = requests.get('http://192.168.1.1/api/system/HostInfo', headers=headers, cookies=cookies, verify=False)

    it = re.finditer(r'\"ID\":\"([^\"]*).+?(?=MACAddress)MACAddress\":\"([^\"]*)', response.content.decode('utf-8'))
    i = 0
    for m in it:
        hostList.append(tuple((m.group(1), m.group(2))))

def disconnect_host(ID, MACAddress):
    global response
    global csrfParam
    global csrfToken
    global SessionID_R3

    get_advance_page()
    update_csrf_params()
    cookies = {
        'username': 'admin',
        'SessionID_R3': SessionID_R3,
        'activeMenuID': 'homenetwork_settings',
        'activeSubmenuID': 'landevices',
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'http://192.168.1.1',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'http://192.168.1.1/html/advance.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    data = '{\"csrf\":{\"csrf_param\":\"' + csrfParam + '\",\"csrf_token\":\"' + csrfToken + '\"},\"action\":\"delete\",\"data\":{\"ID\":\"' + ID + '\",\"MACAddress\":"' + MACAddress + '"}}'

    response = requests.post('http://192.168.1.1/api/system/HostInfo', headers=headers, cookies=cookies, data=data, verify=False)
    update_csrf_params()
    update_session_id()
    
    if response == "":
        return 0
    else:
        return 1

def disconnect_all_hosts():
    global hostList
    global response

    create_router_session()
    
    if router_login() < 160:
        print("Failed to login")
        return
    
    get_host_devices()
    

    for host in hostList:
        if (host[1] != currentMACAddress and host[1] != "0C:56:5C:89:D1:26"):
            result = disconnect_host(host[0], host[1])
            if result == 1:
                print("Disconnected: " + host[1])
            elif result == 0:
                print("Failed to disconnect: " + host[1])

    router_logout()

def main():
    disconnect_all_hosts()
    reboot_modem()


if __name__ == '__main__':
    main()            

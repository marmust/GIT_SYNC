import requests
import socket
from scapy.all import sniff, TCP, Raw
from datetime import datetime

def ascii_checksum(string):
    """
    calculate the ASCII checksum of a given string
    
    parameters:
    string (str): the input string
    
    returns:
    int: the ASCII checksum of the input string
    """
    return sum(ord(char) for char in string)

def least_chars_for_ascii_checksum(target):
    """
    create a string whose ASCII checksum equals the given target number using the least number of characters
    
    parameters:
    target (int): the target ASCII checksum value
    
    returns:
    str: the string with the least number of characters to achieve the given ASCII checksum
    """
    if target <= 0:
        return ""
    
    # max ascii value
    max_ascii = 127

    result = ""
    
    # loop until target is 0
    while target > 0:
        if target >= max_ascii:
            result += chr(max_ascii)
            target -= max_ascii
        else:
            result += chr(target)
            target = 0

    return result

def make_password_recovery_code(id):
    """
    create a password recovery code

    parameters:
    id (str): the id of the user
    date (str): the date of the code
    time (str): the time of the code

    returns:
    str: the password recovery code
    """
    translate = {
        "0": "A",
        "1": "B",
        "2": "C",
        "3": "D",
        "4": "E",
        "5": "F",
        "6": "G",
        "7": "H",
        "8": "I",
        "9": "J",
    }
    
    # id is a string like so: "18008"
    # make it so letters is the digits inside id (string), 0=a 1=b, etc
    letters = "".join([translate[char] for char in id])
    result = datetime.now().strftime("%d%m") + letters + datetime.now().strftime("%H%M")
    
    return result

def send_generic_website_message(headers, data, params, json_data, sub_url, url=fr"http://glitter.org.il/", method=requests.post):
    """
    send a generic message to the website version

    parameters:
    headers (dict): the headers of the http message
    params (dict): the params of the http message
    json_data (dict): the json data of the http message
    sub_url (str): the sub url of the message
    url (str): the url of the message

    returns:
    requests.Response: the response of the server
    """
    response = method(url + sub_url, data=data, headers=headers, params=params, json=json_data)
    return response

def send_generic_app_message(message, ip="54.187.16.171", port=1336, open_socket=None):
    """
    send a generic message to the app version

    parameters:
    message (str): the message to send
    ip (str): the ip of the server (do not touch this)
    port (int): the port of the server (do not touch this)
    open_socket (socket): the socket to use

    returns:
    (socket, str): the socket and the response
    """
    if open_socket == None:
        open_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        open_socket.connect((ip, port))
    
    open_socket.send(message.encode())
    
    response = open_socket.recv(1024).decode()
    
    return open_socket, response

def parse_response_data(data, dirty_chars='#}{"', seperator=","):
    """
    parse the response data of the server into a more usable list

    parameters:
    data (str): the data part of the message to parse
    dirty_chars (str): the dirty chars to remove from the data
    seperator (str): the seperator to split the data by

    returns:
    list: the parsed data
    """
    # remove all dirty chars to get clean message
    for current_char in dirty_chars:
        data = data.replace(current_char, "")
        
    # split message by seperator
    data = data.split(seperator)
    
    return data

def request_user_checksum(username):
    """
    requests an app checksum of a user for login
    
    parameters:
    username (str): the username of the user
    
    returns:
    (socket, int): the socket and the checksum
    """
    
    message = f"""100#<gli&&er><"user_name":"{username}","password":"-----","enable_push_notifications":true>##"""
    message = message.replace("<", "{").replace(">", "}")
    
    open_socket, response = send_generic_app_message(message)
    checksum = response[70:]
    checksum = checksum.split("{")[0]
    checksum = int(checksum)
    
    return open_socket, checksum

def authenticate_user_app(username, password):
    """
    returns a suable socket with an already authenticated user
    
    parameters:
    username (str): the username of the user
    password (str): the password of the user
    
    returns:
    (socket, str): the socket and the response
    """
    login_message = f"""100#<gli&&er><"user_name":"{username}","password":"{password}","enable_push_notifications":true>##""".replace("<", "{").replace(">", "}")
    checksum_message = f"""110#<gli&&er>{ascii_checksum(username + password)}##""".replace("<", "{").replace(">", "}")
    
    open_socket, response = send_generic_app_message(login_message)
    response = send_generic_app_message(checksum_message, open_socket=open_socket)
    
    return open_socket, response

def authenticate_user_website(username, password):
    """
    returns a suable socket with an already authenticated user
    
    parameters:
    username (str): the username of the user
    password (str): the password of the user
    
    returns:
    (socket, str): user id, cookie, and all other important parameters
    """
    
    headers = {
        "Host": "glitter.org.il",
        "Connection": "keep-alive",
        "Content-Length": "20",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Sec-GPC": "1",
        "Origin": "http://glitter.org.il",
        "Referer": "http://glitter.org.il/login",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    data = f"""["{username}","{password}"]"""
    
    json_data = None
    
    response = send_generic_website_message(headers, data, None, json_data, "user/")
    
    return parse_response_data(response.text)

def delete_user_website(id, cookie):
    headers = {
        "Host": "glitter.org.il",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Sec-GPC": "1",
        "Origin": "http://glitter.org.il",
        "Referer": "http://glitter.org.il/home",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": f"sparkle={cookie}"
    }
    
    suburl = f"user/{id}"
    
    response = send_generic_website_message(headers, None, None, None, suburl, method=requests.delete)

    print(response.text)

def extract_glit_id_website(packet, print_result=False):
    """
    extract the glit_id from the given packet
    
    parameters:
    packet (scapy.packet.Packet): the packet to extract the glit_id from
    print_result (bool): whether to print the result
    
    returns:
    bool: whether the glit_id was found
    int: the glit_id
    """
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load.decode(errors="ignore")
        if "glit_id" in payload:
            start = payload.find('glit_id":') + len('glit_id":')
            end = payload.find(",", start)
            glit_id = payload[start:end]
            
            if print_result:
                print(f"glit_id found: {glit_id}")
                
            return True, glit_id
    return False, -1

def get_post_id_website():
    """
    get the post id from the website version (waits for user to interact with post to extract)
    
    returns:
    int: the post id
    """
    print("like the post to retrieve id...")
    glit_id = -1

    def prn_specific_func(packet):
        nonlocal glit_id
        found, glit_id = extract_glit_id_website(packet, print_result=True)
        if found:
            return True
    
    sniff(filter="tcp and host 44.224.228.136", prn=prn_specific_func, stop_filter=prn_specific_func)
    return glit_id

def get_user_id_website(screen_name):
    # authenticate on my account, bcs its just for getting user id
    log_in_result = authenticate_user_website("dtest1", "abcdefg")
    user_id = log_in_result[4][3:]
    user_cookie = log_in_result[-1][8:]
    
    headers = {
        "Host": "glitter.org.il",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Sec-GPC": "1",
        "Referer": "http://glitter.org.il/home",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": f"sparkle={user_cookie}",
        "If-None-Match": "W/\"260-cKjoMgXM4AKsCwZCjB044QQ1iQA\""
    }
    
    response = send_generic_website_message(headers, None, None, None, f"entities?searchType=SIMPLE&searchEntry={screen_name}", method=requests.get)
    first_id = response.text[response.text.find('"id":') + len('"id":'):][:5]
    
    # de authenticate my account
    delete_user_website(user_id, user_cookie)
    
    return first_id

def extract_post_id_app(packet, print_result=False):
    """
    extract the post id from the given packet
    
    parameters:
    packet (scapy.packet.Packet): the packet to extract the post id from
    print_result (bool): if the result should be printed
    
    returns:
    (bool, int): if the post id was found and the post id
    """
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load.decode(errors="ignore")
        if "glit_id" in payload:
            start = payload.find('"glit_id"')
            end = payload.find(",", start)
            glit_id = payload[start:end]
            
            if print_result:
                print(f"glit_id found: {glit_id}")
                
            return True, glit_id
    return False, -1

def get_post_id_app():
    """
    get the post id from the app version (waits for user to interact with post to extract)
    
    returns:
    int: the post id
    """
    print("like the post to retrieve id...")
    glit_id = 0
    
    def prn_specific_func(packet):
        nonlocal glit_id
        res = extract_post_id_app(packet, print_result=False)
        found = res[0]
        glit_id = int(res[1][10:])
        
        return found
    
    sniff(filter="tcp and host 54.187.16.171", prn=prn_specific_func, stop_filter=prn_specific_func)
    
    return glit_id

def like_post_app(post_id):
    """
    adds 1 like to post (thru my account)
    
    parameters:
    post_id (int): the post id to like
    """
    # open socket (username + password doesnt matter since its just for putting a like, so i used mine)
    open_socket, _ = authenticate_user_app("localtest1", "abcdefg")
    
    # send message
    message = f"""710#<gli&&er><"glit_id":{post_id},"user_id":46978,"user_screen_name":"asdasd","id":-1>##""".replace("<", "{").replace(">", "}")
    open_socket.send(message.encode())
    
    # close socket
    open_socket.close()

def like_post_website(post_id):
    """
    adds 1 like to post (thru my account)
    
    parameters:
    post_id (int): the post id to like
    """
    
    sub_url = "likes/"
    
    headers = {
        "Host": "glitter.org.il",
        "Connection": "keep-alive",
        "Content-Length": "76",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Sec-GPC": "1",
        "Accept-Language": "en-US,en;q=0.5",
        "Origin": "http://glitter.org.il",
        "Referer": "http://glitter.org.il/home",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": "sparkle=23062024.4999ebab9c0520dafd526f93bf135ee2.1813.23062024"
    }
    
    json_data = {
        "glit_id": int(post_id),
        "user_id": 18008,
        "user_screen_name": "asdasd asdasd",
        "id": -1
    }
    
    # like is sent from my account, but it works on any post
    send_generic_website_message(headers, None, None, json_data, sub_url)
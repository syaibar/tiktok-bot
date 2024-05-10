from io           import BytesIO
from re           import findall
from time         import sleep
from utils        import *
from base64       import b64decode
from random       import choices
from string       import ascii_letters, digits
from pytermx      import Center, Fade, Utils
from requests     import Session, post
from urllib.parse import unquote

strings = ascii_letters + digits

banner = """
 ______      __            
|___  /     / _|           
   / /  ___| |_ ___  _   _ 
  / /  / _ \  _/ _ \| | | |
./ /__|  __/ || (_) | |_| |
\_____/\___|_| \___/ \__, |
                      __/ |
                     |___/ 
\nMade by seka
"""

url = "zefoy.com"

zefoy_mode = {}
input_valing = ""
count = 0
choice = 0

video_url = ""
video_id = ""
new_input = ""

def decode(string: str):
    return b64decode(unquote(string[::-1])).decode()

def wait(time: int):
    print("")
    for spent in range(time):
        sleep(1)
        print_status(f"Remaining Time: {time - (spent + 1)}", new_line = False)
    print("")
    print_success("Sending Command")

def solve_captcha(session: Session):
    while True:
        res = session.get(f"https://{url}/").text
        input_match = findall(r'<input class="form-control form-control-lg text-center rounded-0 remove-spaces" type="text" name="(.*?)"', res)
        img_match = findall(r'<img src="(.*?)"', res)

        input_val = input_match[0]
        img_val = img_match[0]

        encoded_image = BytesIO(session.get(f"https://{url}" + img_val).content).read()

        open("captcha.png", "wb").write(encoded_image)

        captcha_res = post(
            "https://api.ocr.space/parse/image",
            files = {
                "task": open("captcha.png", "rb")
            },
            data = {
                "apikey": "K81102154388957",
            }
        ).json()["ParsedResults"][0]["ParsedText"]

        res = session.post(
            f"https://{url}/",
            data = {
                input_val: captcha_res
            }
        ).text

        if "captcha" in res:
            print_error(f"Captcha failed as: {captcha_res}")
            sleep(1.5)
            continue
        else:
            print_success(f"Captcha solved as: {captcha_res}")
            return res
        
def manage_mode(html_source: str):
    global count, input_valing

    all_endpoints = findall(r'<h5 class="card-title mb-3"> (.*?)</h5>\n<form action="(.*?)">', html_source)
    valid_endpoints = findall(r'<button class="btn btn-primary rounded-0 t-(.*?)-button">', html_source)

    if "chearts" in valid_endpoints:
        valid_endpoints[valid_endpoints.index("chearts")] = "comment hearts"

    input_valing = findall(r'remove-spaces" name="(.*)" placeholder', html_source)[0]

    zefoy_mode.clear()

    for key, value in all_endpoints:
        if str(key).lower() in valid_endpoints:
            count += 1
            zefoy_mode[count] = {
                "key"  : str(key).title(),
                "value": value
            }

def input_user():
    global choice

    for counter in zefoy_mode:
        print_status(f"[ {counter} ] - {zefoy_mode[counter]['key']}")

    choice = int(ask_question("Your choice> "))
    print("")

def send(session: Session, video_id: int, new_input: str):
    rand_token = "".join(choices(strings, k = 16))

    data  = f'------WebKitFormBoundary{rand_token}\r\nContent-Disposition: form-data; name="{new_input}"\r\n\r\n{video_id}\r\n------WebKitFormBoundary{rand_token}--\r\n'

    res = session.post(
        f"https://{url}/{zefoy_mode[choice]['value']}",
        data = data,
        headers = {
            "Accept"         : "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection"     : "keep-alive",
            "Content-Type"   : f"multipart/form-data; boundary=----WebKitFormBoundary{rand_token}",
            "Host"           : url,
            "Origin"         : f"https://{url}",
            "User-Agent"     : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
    ).text

    decoded_res = decode(res)

    sleep(1.5)

    if "sent" in decoded_res:
        print_success(f"{zefoy_mode[choice]['key']} sent\n")

def send_command(session: Session):
    global input_valing, video_id, new_input

    rand_token = "".join(choices(strings, k = 16))

    data  = f'------WebKitFormBoundary{rand_token}\r\nContent-Disposition: form-data; name="{input_valing}"\r\n\r\n{video_url}\r\n------WebKitFormBoundary{rand_token}--\r\n'

    res = session.post(
        f"https://{url}/{zefoy_mode[choice]['value']}",
        data = data,
        headers = {
            "Authority"      : f"{url}",
            "Accept"         : "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection"     : "keep-alive",
            "Content-Type"   : f"multipart/form-data; boundary=----WebKitFormBoundary{rand_token}",
            "Host"           : url,
            "Origin"         : f"https://{url}",
            "User-Agent"     : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
    ).text

    decoded_res = decode(res)

    try:
        new_input, video_id = findall(r'<input type="hidden" name="([a-f0-9]+)" value="(\d+)">', decoded_res)[0]
    except:
        if "Checking Timer" in decoded_res:
            timess = findall(r"ltm=(.*?);", decoded_res)[0]
            wait(int(timess))
            pass

    sleep(1.5)
    send(session, int(video_id), new_input)

def main():
    global video_url

    video_url = ask_question("Video Url> ")

    with Session() as session:
        session.headers = {
            "Accept"         : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection"     : "keep-alive",
            "Host"           : url,
            "User-Agent"     : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

        print_status("Solving Captcha")
        res = solve_captcha(session)

        print_status("Traiting Modes\n")
        manage_mode(res)

        print_status("Recovering Modes\n")
        input_user()

        while True:
            send_command(session)
            sleep(1)

if __name__ == "__main__":
    Utils.clear()
    Utils.set_title("Zefoy Automator")

    print(Fade.in_green(Center.center_x(banner), 255, 100))
    
    main()
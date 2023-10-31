import os
from os.path import abspath
import json
from pathlib import Path
from time import sleep
import requests
from bs4 import BeautifulSoup
from windows_toasts import Toast, WindowsToaster, ToastDisplayImage

# set up globals
toaster = WindowsToaster('Twitch Live Checker')
temp_dir = os.path.join(os.environ['TEMP'], 'pytwitch_thumb')
os.makedirs(temp_dir, exist_ok=True)
abs_temp_dir = abspath(temp_dir)

# twitch channel constant
MELBA_TOAST = 'https://www.twitch.tv/melbathetoast'

def unpack_response(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    script = soup.find('script', type='application/ld+json')
    if not script:
        return 'invalid', 'invalid', 'invalid', False #pretty dumb hack solution
    else:
        data = json.loads(script.contents[0])
        ch_name = data[0]['name']
        description = data[0]['description']
        thumbnail = data[0]['thumbnailUrl'][2]
        live_status = data[0]['publication']['isLiveBroadcast']
        return ch_name, description, thumbnail, live_status

def build_toast(ch_name, description, thumbnail, live_status, link):
    if live_status == True:
        # locally save thumbnail
        filelist = [ f for f in os.listdir(temp_dir) if f.endswith(".*") ]
        x = len(filelist)+1
        filename = os.path.join(temp_dir, f"{x}_{os.path.basename(thumbnail)}") #increments regardless of channel owner but realistically it doesnt matter
        thumb_response = requests.get(thumbnail)
        if thumb_response.status_code == 200:
            with open(filename, 'wb') as local_copy:
                local_copy.write(thumb_response.content)
                thumb_path = abspath(filename)

        # build toast
        newToast = Toast()
        newToast.text_fields = [f'{ch_name} now live ', f'{description}', "Click to watch"]
        newToast.AddImage(ToastDisplayImage.fromPath(thumb_path))
        newToast.launch_action = f'{link}'
        return newToast        

def clean_temp_folder(folder):
    clean_bool = False # Change to True to enable cleaning
    if clean_bool == True:
        folder = Path(folder)
        for file in folder.glob('*.*'):
            if os.path.exists(file):
                os.unlink(file)

if __name__ == '__main__':
    # twitch_link = input("Enter twitch channel link: ")
    while True:
        ch_name, description, thumbnail, live_status = unpack_response(MELBA_TOAST)
        if live_status == True:
            newToast = build_toast(ch_name, description, thumbnail, live_status, MELBA_TOAST)
            toaster.show_toast(newToast)
            toast_sent = True
            while toast_sent:
                sleep(60) # trying to not get ip banned
                ch_name, description, thumbnail, live_status = unpack_response(MELBA_TOAST)
                if live_status == False:
                    toast_sent = False
                    clean_temp_folder(abs_temp_dir)
                    break
                else:
                    print("live status unchanged")
                    continue
        else:
            toast_sent = False
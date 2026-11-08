from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1309
from gpiozero import Button
from time import sleep
from registry import load_gits, get_username, get_clone_path, add_git_repo
import requests
from PIL import ImageFont
import subprocess
from pathlib import Path

CLONE_COORDS = (0, 30)
PULL_COORDS = (50, 30)
selected_text = "CLONE"
selected_coord = CLONE_COORDS

git_username = get_username()
git_api_url = f"https://api.github.com/users/{git_username}/repos"

selected = 0
top = 0
is_cloning = False

def draw_menu(device, items, line_h=12):
    global selected
    global top
    font = ImageFont.load_default()
    visible = device.height // line_h
    top = min(top, selected)
    top = max(top, selected - visible + 1)

    with canvas(device) as draw:
        for i, item in enumerate(items[top:top + visible]):
            y = i * line_h
            if top + i == selected:
                draw.rectangle((0, y, device.width - 1, y + line_h - 1), outline="white")
                draw.text((3, y + 1), item["name"], fill="white", font=font)
            else:
                draw.text((3, y + 1), item["name"], fill="white", font=font)
            if top > 0:
                draw.text((device.width - 8, 0), "^", fill="white", font=font)
            if top + visible < len(items):
                draw.text((device.width - 8, device.height - 10), "v", fill="white", font=font)
    return top
        
def move(device, delta, list):
    global selected
    selected = max(0, min(len(list) - 1, selected + delta))
    draw_menu(device, list)

def change():
    global selected_coord
    global selected_text
    if(selected_text == "CLONE"):
        selected_text = "PULL"
        selected_coord = PULL_COORDS
    else:
        selected_text = "CLONE"
        selected_coord = CLONE_COORDS

def clone(device, repos):
    global selected
    SELECTED_REPO = repos[selected]
    global is_cloning
    is_cloning = True
    clone_path = get_clone_path()
    print(SELECTED_REPO["html_url"])
    print(clone_path)
    print(is_cloning)
    subprocess.run(["git", "clone", SELECTED_REPO["html_url"]], cwd=clone_path)
    full_path = Path(clone_path) / SELECTED_REPO["name"]
    add_git_repo(SELECTED_REPO["name"], str(full_path), SELECTED_REPO["html_url"])

def select(device, BUTTON_ARRAY):
    global selected_text
    global is_cloning
    exitButton = BUTTON_ARRAY[3]
    upButton = BUTTON_ARRAY[0]
    downButton = BUTTON_ARRAY[4]
    selectButton = BUTTON_ARRAY[1]
    if(selected_text == "PULL"):
        git_list = load_gits()
        while not exitButton.is_pressed:
            draw_menu(device, git_list)
    else:
        response = requests.get(git_api_url)
        print(git_api_url)
        print(response)
        repositories = []
        if response.status_code == 250 or response.status_code == 200:
            repositories = response.json()
            for repo in repositories:
                print(f"Name: {repo['name']} | URL: {repo['html_url']}")
        else:
            print("GETTING REPOS FAILED")
        upButton.when_pressed = lambda: move(device, -1, repositories)
        downButton.when_pressed = lambda: move(device, 1, repositories)
        selectButton.when_pressed = lambda: clone(device, repositories)
        while not exitButton.is_pressed and not is_cloning:
            print(is_cloning)
            draw_menu(device, repositories)
        if(is_cloning):
            with canvas(device) as draw:
                draw.text((20,20), "CLONE COMPLETED", fill="white")
            sleep(2)
            is_cloning = False

def run(device, BUTTON_ARRAY):
    rightButton = BUTTON_ARRAY[4]
    leftButton = BUTTON_ARRAY[0]
    selectButton = BUTTON_ARRAY[1]
    exitButton = BUTTON_ARRAY[3]
    while not exitButton.is_pressed:
        rightButton.when_pressed = change
        leftButton.when_pressed = change
        with canvas(device) as draw:
            draw.text((20,0), "GIT MANAGER")

            left, top, right, bottom = draw.textbbox(selected_coord, selected_text)
            padding = 4
            border_left = left - padding
            border_top = top - padding
            border_right = right + padding
            border_bottom = bottom + padding
            
            draw.rectangle(
                (border_left, border_top, border_right, border_bottom), 
                outline="white", 
                fill=None
            )
            
            draw.text(CLONE_COORDS, "CLONE", fill="white")
            draw.text(PULL_COORDS, "PULL", fill="white")

        if selectButton.is_pressed:
            select(device, BUTTON_ARRAY)

        selectButton.when_pressed = None
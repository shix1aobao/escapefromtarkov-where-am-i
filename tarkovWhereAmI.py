import threading
import tkinter as tk
from tkinter import filedialog
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from pynput import keyboard

global directory
global browser

def mainFun(map):
    # 地图地址
    url = 'https://tarkov-market.com/maps/' + map
    options = webdriver.ChromeOptions()
    service = Service(executable_path='/Users/baojiaxing/PycharmProjects/pythonProject/chromedriver')
    driver = webdriver.Chrome(options=options, service=service)
    driver.get(url)
    time.sleep(5)

    # 点击where am i
    clickable = driver.find_element(By.CSS_SELECTOR, ".no-wrap")
    ActionChains(driver) \
        .click(clickable) \
        .perform()
    return driver

def on_release(key):
    global directory
    if key == keyboard.Key.esc:
        print('esc')
        # browser.close()
        # 如果按下'esc'键，则停止监听
        return False
    if key == keyboard.Key.down:
        files = os.listdir(directory)
        files = [os.path.join(directory, file) for file in files]
        files = filter(os.path.isfile, files)  # 过滤出文件，排除子目录

        latest_file_path = max(files, key=os.path.getctime)
        latest_file_name = os.path.basename(latest_file_path)

        # 找到输入框
        clickable_accourn = browser.find_element(By.CSS_SELECTOR,
                                                 "input[data-v-2fb07b41]")
        ActionChains(browser) \
            .send_keys_to_element(clickable_accourn, latest_file_name) \
            .perform()

def start_keyboard_listener():
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()

def browse_file_path():
    global directory
    directory = filedialog.askdirectory() # 将此路径替换为你要查询的目录路径

def button_click():
    global browser
    selected_value = options_mapping[selected_option.get()]
    browser=mainFun(selected_value)

window = tk.Tk()
window.title("塔科夫新手识图")
window.geometry("400x300+100+100")

# 创建标签
label = tk.Label(window, text="欢迎使用！", font=("Arial", 20))
label.pack(pady=20)

# 创建下拉菜单1
options_mapping = {
    '中心': 'ground-zero',
    '森林': 'woods',
    '海关': 'customs',
    '海岸线':'shoreline'
}
selected_option = tk.StringVar()
selected_option.set('森林')  # 默认选中第一个选项

drop_down_menu = tk.OptionMenu(window, selected_option, *options_mapping.keys())
drop_down_menu.pack(pady=10)

button = tk.Button(window, text="选择文件", command=browse_file_path)
button.pack(pady=20)

button = tk.Button(window, text="点击我", command=button_click)
button.pack(pady=10)

# 在新线程中启动键盘监听器
keyboard_thread = threading.Thread(target=start_keyboard_listener)
keyboard_thread.daemon = True  # 设置为守护线程，以便在主线程结束时自动关闭
keyboard_thread.start()

# 运行窗口程序
window.mainloop()




import uuid
import pyautogui
import random
from time import sleep
import string
PAGE_NUM = 100
LINKS_PER_PAGE=5
WAIT=0.5
INTER=0.05

pages = [str(random.randint(0, 100000)) for x in range(PAGE_NUM)]
print("Move to athens screen")
sleep(10)


for page in pages:
    with pyautogui.hold('command'):
        pyautogui.press('k')
    sleep(WAIT)
    pyautogui.write(page, interval=INTER)
    sleep(WAIT)
    pyautogui.press('enter')
    sleep(WAIT)
    pyautogui.press('enter')
    links = random.choices(pages, k=LINKS_PER_PAGE)
    sleep(WAIT)
    for link in links:
        pyautogui.write('[[' + link, interval=INTER)
        sleep(WAIT)
        with pyautogui.hold('command'):
            pyautogui.press('right')
        sleep(WAIT)
        pyautogui.press('enter')
        sleep(WAIT)
pyautogui.write("finished", interval=INTER)

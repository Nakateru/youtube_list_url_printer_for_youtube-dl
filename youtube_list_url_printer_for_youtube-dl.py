from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re,time
videolist=[]
resolution='137'

if __name__=='__main__':
    print('youtube list url printer for youtube-dl')
    print('Author  :  Nakateru (2020.02.18)')
    url=input('Input Youtube list URL:')
    if url.startswith('https://www.youtube.com/playlist?list='):
        print('Loading')
    else:
        print('Error URL')
        exit()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(chrome_options=options)

    driver.get(url)
    wait = WebDriverWait(driver, 10)
    ele = wait.until(EC.element_to_be_clickable((By.ID,'contents')))
    # print(ele)

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            print("Loaded")
            break
        last_height = new_height

    content = ele.find_elements_by_id('content')
    for i in content:
        videourl=i.find_element_by_tag_name('a').get_attribute('href')
        videolist.append(re.split(r"&list=", videourl)[0])

    # print(videolist)
    print('Found ' + str(len(videolist))+' videos in this youtube list')
    driver.quit()

    num=input('Select number: [1]1080 [2]720 [3]480 [4]360:\n')

    if num=='1':
        resolution='137'
    elif num=='2':
        resolution='136'
    elif num=='3':
        resolution='135'
    elif num=='4':
        resolution='134'
    else:
        print('Error number!')
        exit()

    try:
        with open('youtube-dl start list.bat', 'a', encoding='UTF-8') as f:
            for i in videolist:
                f.write('youtube-dl -f ' + resolution + '+140 ' + i + '\n')
            f.write('pause')
        print('Saved list youtube-dl start list.bat')
    except Exception:
        print('Failed to save list.bat')
        exit()


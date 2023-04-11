import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import pandas as pd

url = 'https://fullahead-yugi.com/shopbrand/yugi-b11-09/page1/recommend/'
res = requests.get(url,timeout=3.0)
res.raise_for_status()
sleep(1)
soup = BeautifulSoup(res.content,'lxml')
a_tags = soup.select('div.indexItemBox.cf > div > a')

img_num = 0
d_list = []
for a_tag in a_tags:
    img_num += 1
    page_url = 'https://fullahead-yugi.com' + a_tag.get('href')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(
        executable_path='./chromedriver_mac_arm64/chromedriver',
        options=options)
    driver.get(page_url)
    sleep(3)
    p_tags = driver.find_elements(By.CSS_SELECTOR,'#product_description')
    if p_tags:
        description = p_tags[0].text
        print(description)
    else:
        print('not found')

    img_tags = driver.find_elements(By.CSS_SELECTOR,'#image_main > img')
    if img_tags:
        img = img_tags[0].get_attribute('src')
        img_res = requests.get(img,timeout=3.0)
        img_res.raise_for_status()
        sleep(1)
        with open('img.jpg','wb') as f:
            f.write(img_res.content)
        try:
            img = Image.open('img.jpg')
            # 明度の調整
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.2)

            # 画像描画
            width,height = img.size
            new_width = width*2
            new_height = height*2
            new_img = Image.new('RGBA',(new_width,new_height),(0,0,0,0))

            draw = ImageDraw.Draw(new_img)
            text = 'sample '
            fontsize = 36
            font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',fontsize)
            font_width,font_height = draw.textsize(text,font=font)
            for y in range(0,new_height,font_height):
                for x in range(0,new_width,font_width):
                    draw.text((x,y),text,font=font,fill=(255,255,255,128))

            new_img = new_img.rotate(45)
            img.show()

            # 画面の中心の切り抜き
            def crop_center(pil_img, crop_width, crop_height):
                img_width, img_height = pil_img.size
                return pil_img.crop(((img_width - crop_width) // 2,
                                    (img_height - crop_height) // 2,
                                    (img_width + crop_width) // 2,
                                    (img_height + crop_height) // 2))

            new_img_crop = crop_center(new_img,width,height)
            # 画像結合
            img.paste(new_img_crop,(0,0),new_img_crop)
            # 画像保存
            img.save(f'processed_image{img_num}.png')
        except OSError:
            print('OSError')
    else:
        print('not image')
    driver.quit()
    d_list.append({'image_url':f'processed_image{img_num}.png',
                  'description':description})
df = pd.DataFrame(d_list)
df.to_excel('processed.xlsx',index=False)
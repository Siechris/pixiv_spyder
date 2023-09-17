
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

from selenium.common.exceptions import NoSuchElementException

# 滾動畫面
from selenium.webdriver.common.keys import Keys

import os

import re
# ==============================================================

class pixiv_spyder:
    def __init__(self,painter_author,g_email,g_password):
        # driver = webdriver.Chrome() 就是創建了一個 Chrome 瀏覽器的 WebDriver 實例，
        # 並將其賦值給變量 driver，這樣我們就可以通過 driver 來控制瀏覽器的行為了。
        self.driver = webdriver.Chrome()
  
        self.url = "https://www.google.com"
        # google 帳號
        self.g_email= g_email
        # google 密碼
        self.g_password=g_password     
        # 輸入作者
        self.painter_author = painter_author
        # 圖片張數
        self.count = 0
        # 設定下載圖片的Referer请求头
        self.headers = {
            "Referer": "https://www.pixiv.net/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        }
    # 打開網頁
    def start(self):
        # 使用driver.get()方法等待URL載入
        self.driver.get(self.url)
        time.sleep(2) # 等待網頁載入
        
        # 找到搜索输入框的元素并输入关键字
        search_box = self.driver.find_element("name", "q")
        search_box.send_keys(self.painter_author+" pixiv")#輸入keyword
        search_box.send_keys(Keys.RETURN)  # 模拟按下 Enter 键
        
        time.sleep(1)
        
        try:
            # 找到搜索结果中的第一个链接元素并点击，此方法只能用在pixiv
            link_element = self.driver.find_element("xpath", "//a[contains(@href, 'https://www.pixiv.net/users/')]")
            link_element.click()
        except NoSuchElementException:
            print("未找 第一個連結 是pixiv")
            
        time.sleep(1) 
        
        # 找到登录链接元素并点击
        try:
            login_link_element = self.driver.find_element(By.XPATH, "//a[contains(@href, '/login.php') and contains(@class, 'sc-oh3a2p-3')]")
            login_link_element.click()
        except NoSuchElementException:
            print("未找 登入按鍵")
            
        # 执行一次向下滚动
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)  
        
        time.sleep(1)
        
        # 點擊 透過 Google 繼續 按鈕
        try:
            # 根据按钮文本定位按钮元素并点击
            button_element = self.driver.find_element(By.XPATH, "//button[contains(text(), '透過 Google 繼續')]")
            button_element.click()

        except NoSuchElementException:
            print("未找 透過 Google 繼續 到按钮")
        
  
        try:
            # 尋找電子郵件輸入欄位
            email_input = self.driver.find_element(By.NAME, "identifier")
            # 清空輸入欄位內容
            email_input.clear()
            # 填寫電子郵件地址
            email_input.send_keys(self.g_email)  # 將此處替換為您的電子郵件地址
        except NoSuchElementException:
            print("找不到電子郵件輸入欄位")
        
        # 等待一些時間，讓您可以看到輸入的效果
        time.sleep(1)
        
        try:
            # 尋找下一步按鈕
            next_button = self.driver.find_element(By.XPATH, "//span[text()='下一步']")
            # 點擊下一步按鈕
            next_button.click()
        except NoSuchElementException:
            print("找不到下一步按鈕")
        
        time.sleep(3)
        
        try:
            # 尋找密碼輸入框
            password_input = self.driver.find_element(By.NAME, "Passwd")
            # 輸入您的密碼，假設您的密碼存儲在變數中
            password = self.g_password
            password_input.send_keys(password)
        except NoSuchElementException:
            print("找不到密碼輸入框")
            
        time.sleep(1)
            
        try:
            # 尋找下一步按鈕
            next_button = self.driver.find_element(By.XPATH, "//span[text()='下一步']")
            # 點擊下一步按鈕
            next_button.click()
        except NoSuchElementException:
            print("找不到下一步按鈕")
            
        time.sleep(5)
        
        
        # 创建資料夾
        if not os.path.exists(self.painter_author):
            os.makedirs(self.painter_author)
            print(f"文件夹 '{self.painter_author}' 创建成功")
        else:
            print(f"文件夹 '{self.painter_author}' 已存在")
        
        
        # 取得當前網址
        current_url = self.driver.current_url
        print("当前网址:", current_url)
        
        # 頁數
        num_pages = 1
        
        while True:
            time.sleep(2)
            self.driver.get(current_url+"/artworks?p="+str(num_pages))
            num_pages+=1
            
            time.sleep(2)
            
            # 定位具有特定 class 的 <div> 元素
            div_element = self.driver.find_element(By.CLASS_NAME, "sc-1xvpjbu-0")
            
            # 检查 <div> 元素下是否有 <img> 元素
            img_elements = div_element.find_elements(By.TAG_NAME, "img")
            if img_elements:
                self.download_png()

            else:
                print("已到最後一頁")
                break
            
        # 關閉網頁
        self.driver.quit()

        

    # 下載圖片        
    def download_png(self):      
        # 执行一次向下滚动
        for i in range(4):
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
        
        # # 找到所有包含指定CSS类的img元素
        img_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'sc-9y4be5-0')]//img")
        
        # 提取每个img元素的src属性
        image_urls = [img.get_attribute("src") for img in img_elements]

        print(len(image_urls))

               
        # 提取并处理每个img元素的src属性，生成新的图片URL
        for img_src in image_urls:
            
            match_square = re.search(r"img-master/img/(.*?)_square1200\.jpg", img_src)
            match_custom = re.search(r"custom-thumb/img/(.*?)_custom1200\.jpg", img_src)

            if match_square:
                image_path = match_square.group(1).replace("_", "/")
                new_img_url = f"https://i.pximg.net/img-original/img/{image_path}.jpg"
                new_url = new_img_url.replace("/p0.jpg", "_p0.jpg")

            elif match_custom:
                image_path = match_custom.group(1).replace("_", "/")
                new_img_url = f"https://i.pximg.net/img-original/img/{image_path}.jpg"
                new_url = new_img_url.replace("/p0.jpg", "_p0.jpg")
            else:
                print("无法处理图片URL")
            new_url = new_img_url.replace("/p0.jpg", "_p0.jpg")
            
            print(new_url)
            
            
            # 隱藏圖片數
            hidden_images = 0
            # 分割出基础 URL 和图像编号
            base_url, image_ext = new_url.rsplit("_p", 1)
            image_extension = "." + image_ext.split(".")[-1]

            
            while True:

                new_url = f"{base_url}_p{hidden_images}{image_extension}"

                # 发起请求，下载图片
                response = requests.get(new_url, headers=self.headers)
                
                # 检查请求的状态码
                if response.status_code == 200:
                    # 获取图片的二进制数据
                    image_data = response.content
                
                    # 保存图片到本地文件
                    with open("./" + self.painter_author + "/" + self.painter_author + "_" + str(self.count) + ".png", "wb") as f:
                        self.count += 1
                        f.write(image_data)
                    print(self.painter_author + "_" + str(self.count) + ".png 图片下载成功")
                else:
                
                    # 尝试请求png格式的图片
                    new_png_url = new_url.replace(".jpg", ".png")
                    response_png = requests.get(new_png_url, headers=self.headers)
               
                    # 检查请求的状态码
                    if response_png.status_code == 200:
                        # 获取图片的二进制数据
                        image_data_png = response_png.content
                
                        # 保存图片到本地文件
                        with open("./" + self.painter_author + "/" + self.painter_author + "_" + str(self.count) + ".png", "wb") as f:
                            self.count += 1
                            f.write(image_data_png)
                        print(self.painter_author + "_" + str(self.count) + ".png 图片下载成功")
                    else:
                        print("图片下载失败或没有更多隐藏图片")
                        break
                # 隱藏圖片+1
                hidden_images += 1


                        
if __name__=="__main__":
    # google 帳號
    email= ""
    # google 密碼
    password=""   
    keyword=input("輸入作者關鍵字 : ")
    test = pixiv_spyder(keyword,email,password)
    test.start()
    # 佐々

 # pixiv圖片格式
# https://i.pximg.net/c/250x250_80_a2/img-master/img/2023/08/15/00/12/56/110835027_p0_square1200.jpg

# https://i.pximg.net/img-master/img/2023/08/15/00/12/56/110835027_p0_master1200.jpg

# https://i.pximg.net/img-original/img/2023/08/15/00/12/56/110835027_p0.jpg
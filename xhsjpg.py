from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, PrivateMessageEvent, Message, MessageSegment
from nonebot.typing import T_State
from nonebot.matcher import Matcher

import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# 创建响应私聊消息的处理器
jpg_handler = on_message(block=False)

@jpg_handler.handle()
async def xhs_jpg(bot: Bot, event: PrivateMessageEvent, state: T_State):
    message: Message = event.get_message()

    messageStr = str(message).strip()

    match = re.search(r'"jumpUrl":"(https?://[^\"]+)"', messageStr)

    if match:
        jump_url = match.group(1)  # 提取 jumpUrl

        # 去除 &amp;
        cleaned_url = jump_url.replace("&amp;", "&")

        await bot.send(event, cleaned_url)
        
        if "xiaohongshu" not in messageStr:
            return

        # 配置浏览器选项（例如，设置为无头模式）
        chrome_options = Options()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')  # 为了避免一些系统问题
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')  # 使用常见的用户代理
        chrome_options.add_argument('--disable-blink-features=AutomationControlled') 
        chrome_options.add_argument("--disable-webgl")  # 禁用 WebGL
        chrome_options.add_argument("--disable-gpu")    # 禁用 GPU 加速

        # 使用 WebDriver Manager 自动管理 ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # 打开网页
        url = cleaned_url  # 替换为目标链接
        driver.get(url)

        # 等待页面加载完成
        time.sleep(3)  # 可以根据实际情况调整等待时间，或者使用显式等待

        # 查找所有 class="note-slider-img" 的元素
        elements = driver.find_elements(By.CLASS_NAME, 'note-slider-img')

        seen_images = set()

        for element in elements:
            img_src = element.get_attribute('src')
            
            # 检查是否已存在且非空
            if img_src and img_src not in seen_images:
                await bot.send(event, MessageSegment.image(img_src))
                seen_images.add(img_src)
                
        # 关闭浏览器
        driver.quit()

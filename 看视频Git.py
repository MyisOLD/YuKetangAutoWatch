from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')

# 驱动位置
driver = webdriver.Chrome("chromedriver.exe",chrome_options=options)

#cookies待定,暂为微信扫码登录
driver.get(f"雨课堂URL")

WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "button.el-button"))
)
driver.find_element(By.CSS_SELECTOR, "button.el-button").click()
time.sleep(6)
print("登录成功")
WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.CLASS_NAME, "title"))
)
list = driver.find_elements(By.CSS_SELECTOR, 'i.icon--shipin')
old_handle = driver.current_window_handle
for x in list:
    # try:
    x.click()

    # 切换到最后一个窗口，即新标签页
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.el-tooltip")))
    time.sleep(5)
    try:
        text0 = driver.find_elements(By.CSS_SELECTOR, "span.text")
        title1 = text0[0].text
        text1 = text0[1].text
    except:
        text0 = driver.find_element(By.CSS_SELECTOR, "span.text")
        text1 = 'ss：ss'
        title1 = text0.text

    if text1.split("：")[1] == '100%':
        print(f"{title1}已完成，跳过")
        print("=====================")
        driver.close()
        driver.switch_to.window(old_handle)  # 切换到最后一个窗口
    else:
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "xt_video_player_current_time_display"))
        )
        time.sleep(1)
        k = driver.find_element(By.CSS_SELECTOR, 'xt-time.xt_video_player_current_time_display')
        v = k.find_elements(By.TAG_NAME, 'span')
        time.sleep(3)

        # 计算时间
        seconds_now = int(v[0].text.split(":")[0]) * 3600 + int(v[0].text.split(":")[1]) * 60 + int(
            v[0].text.split(":")[2])
        time.sleep(3)
        seconds_total = int(v[1].text.split(":")[0]) * 3600 + int(v[1].text.split(":")[1]) * 60 + int(
            v[1].text.split(":")[2])
        seconds_span=seconds_total-seconds_now

        # 调整为2倍速
        WebDriverWait(driver,100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'xt-speedbutton.xt_video_player_speed')))
        speed=driver.find_element(By.CSS_SELECTOR, 'xt-speedbutton.xt_video_player_speed')
        ActionChains(driver).move_to_element(speed).perform()
        speed2X=driver.find_element(By.XPATH,'//*[@id="video-box"]/div/xt-wrap/xt-controls/xt-inner/xt-speedbutton/xt-speedlist/ul/li[1]')
        ActionChains(driver).move_to_element(speed2X).move_by_offset(5,5).click().perform()

        # 点击播放,默认就是自动播放,但是有些时候不是
        try:
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.xt_video_bit_play_btn')))
            driver.find_element(By.CSS_SELECTOR, 'button.xt_video_bit_play_btn').click()
        except:
            pass
        print(f"{title1}开始观看，已开启2倍速！此视频预计耗时{round(seconds_span / 120,3)}分钟")
        time.sleep(seconds_span/2)
        print(f"{title1}现已完成")
        print("=====================")
        driver.close()
        driver.switch_to.window(old_handle)  # 切换到最后一个窗口
# except Exception as e:
#     print(f"异常信息：{e}")

driver.quit()

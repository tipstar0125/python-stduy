#%%

# 1. 会社名以外の項目を取得して画面にprint文で表示してみましょう。
# 2. for文を使って、１ページ内の３つ程度の項目（会社名、年収など）を取得できるように改造してみましょう
# 3. ２ページ目以降の情報も含めて取得できるようにしてみましょう
# 4. 任意のキーワードをコンソール（黒い画面）から指定して検索できるようにしてみましょう
# 5. 取得した結果をpandasモジュールを使ってCSVファイルに出力してみましょう
# 6. エラーが発生した場合に、処理を停止させるのではなく、スキップして処理を継続できるようにしてみましょう(try文)
# 7. 処理の経過が分かりやすいようにログファイルを出力してみましょう
# ログファイルとは：ツールがいつどのように動作したかを後から確認するために重要なテキストファイルです。
# ライブラリを用いることもできますが、テキストファイルを出力する処理で簡単に実現できるので、試してみましょう。
# (今何件目、エラー内容、等を表示)

import os
from selenium.webdriver import Chrome, ChromeOptions
# import chromedriver_binary # chromedriverをpipインストールして使用する場合
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from logging import getLogger,  FileHandler, Formatter, DEBUG


logger = getLogger(__name__)
fomatterSetting = Formatter('[%(asctime)s] %(name)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
handler = FileHandler('test.log')
# handler = StreamHandler()
# handler = NullHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
handler.setFormatter(fomatterSetting)
logger.addHandler(handler)
logger.propagate = False

# Chromeを起動する関数

def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # Seleniumをあらゆる環境で起動させるChromeオプション
    # options = ChromeOptions()
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-extensions')
    # options.add_argument('--proxy-server="direct://"')
    # options.add_argument('--proxy-bypass-list=*')
    # options.add_argument('--start-maximized')
    # options.add_argument('--headless') # ※ヘッドレスモードを使用する場合、コメントアウトを外す

    # ChromeのWebDriverオブジェクトを作成する。

    
    # DRIVER_PATH = './chromedriver'
    # driver = Chrome(executable_path=DRIVER_PATH, chrome_options=options) # 環境パスを通さない場合に使用
    # chromedriverに環境パスを通している場合は"executable_path"は省略
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)


def main():

    search_keyword = input('検索キーワードを入力してください：')
    logger.debug(search_keyword)
    search_url = "https://tenshoku.mynavi.jp/"
    
    # driverを起動
    IsHeadless = True
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", IsHeadless)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", IsHeadless)
    
    # Webサイトを開く
    # ヘッドレスモード使用時に、画面サイズが小さくクリックが適切に動作できないので、画面サイズを大きく指定
    driver.set_window_size('1200', '1000')
    driver.get(search_url)
    time.sleep(5)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
  
    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # global df
    name_list = []
    apeal_list = []
    copy_list = []
    employment_status_list = []
    incom_list = []

    cur_url = driver.current_url
    logger.info(cur_url)

    # 検索結果の一番上の会社名を取得
    # html = requests.get('https://tenshoku.mynavi.jp/list/kw%E9%AB%98%E5%8F%8E%E5%85%A5/?jobsearchType=14&searchType=18')
    # html.encoding = html.apparent_encoding
    # soup = BeautifulSoup(html.content, "html.parser")

    for i in range(5): # 5ページ繰り返し
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # names = soup.select('.cassetteRecruit__name')
        names = soup.select('section[class^="cassetteRecruit"]>h3[class$="__name"]')
        # name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        # copies = soup.select('.cassetteRecruit__copy')
        copies = soup.select('section[class^="cassetteRecruit"]>p[class$="__copy"]')
        # copy_list = driver.find_elements_by_class_name("cassetteRecruit__copy")
        # infoTables = soup.select('.cassetteRecruit__main, .cassetteRecruit__mainM')
        # infoTables = soup.select('div[class^="cassetteRecruit__main"]')
        infoTables = soup.select('div[class^="cassetteRecruit"]>div[class$="__detail"]>div[class*="__main"]')

        logger.debug(len(names))
        logger.debug(len(copies))
        logger.debug(len(infoTables))

        # print(len(name_list))
        for name, copy, infoTable in zip(names, copies, infoTables):
            name_list.append(name.text.split('|')[0].replace(' ', '').replace('　', ''))
            try:
                apeal_list.append(name.text.split('|')[1].replace(' ', '').replace('　', ''))
            except IndexError as e:
                logger.error("情報がありません")
                apeal_list.append('')
            copy_list.append(copy.text.split('\n')[1].replace(' ', '').replace('　', ''))
            employment_status_list.append(copy.text.split('\n')[2].replace(' ', '').replace('　', ''))

            for content, incom in zip(infoTable.select('.tableCondition__head'), infoTable.select('.tableCondition__body')):
                IsIncom = False
                if '初年度年収' in content.text:
                    incom_list.append(incom.text)
                    IsIncom = True
            if IsIncom == False:
                incom_list.append('')

        logger.debug(str(i+1) + "ページ目完了")

        # 次ページ移動
        try:      
            driver.find_element_by_class_name("iconFont--arrowLeft").click()
        except:
            logger.error("求人情報はこれ以上ありません")
            break
        time.sleep(5)


    df = pd.DataFrame({ 'name' : name_list,
                        'apeal': apeal_list,
                        'copy' : copy_list,
                        'employment_status': employment_status_list,
                        'incoms': incom_list,
                        })
    
    df.to_csv("mynavi_high_incom_list_" + search_keyword + ".csv", encoding='utf-8-sig')

    logger.debug("CSV出力完了")


if __name__ == "__main__":
    main()


#%%



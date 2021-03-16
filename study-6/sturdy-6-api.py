#%%

# 1. 以下の仕様を参考にして、任意のキーワードでAPIを検索した時の 商品名と価格の一覧を取得してみましょう
# https://webservice.rakuten.co.jp/api/ichibaitemsearch/

import requests
import json
import pandas as pd

rakuten_id = "1061452151101776425"
formatVersion = "2"
keyword = "みかん"
url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?applicationId={id}&formatVersion={formatVersion}&keyword={keyword}"
url = url.format(id=rakuten_id, formatVersion=formatVersion, keyword=keyword)

data = requests.get(url).json()["Items"]

itemName = []
itemPrice = []

for item in data:
    itemName.append(item["itemName"])
    itemPrice.append(item["itemPrice"])


df = pd.DataFrame({"商品名": itemName, "商品価格": itemPrice})
df.to_csv("rakuten_api1.csv", encoding='utf-8-sig')
df.head(30)


#%%

# 2. 以下のAPIを使って、任意の商品の最安値と最高値を取得してみましょう
# https://webservice.rakuten.co.jp/api/productsearch/

import requests
import json
import pandas as pd
import pathlib

rakuten_id = "1061452151101776425"
formatVersion = "2"
keyword = "みかん"
url = "https://app.rakuten.co.jp/services/api/Product/Search/20170426?applicationId={id}&formatVersion={formatVersion}&keyword={keyword}"
url = url.format(id=rakuten_id, formatVersion=formatVersion, keyword=keyword)

data = requests.get(url).json()["Products"]

# json_path = pathlib.Path('./sample.txt')
# json_path.write_text(json.dumps(data, ensure_ascii=False))

productName = []
maxPrice = []
minPrice = []

for item in data:
    productName.append(item["productName"])
    maxPrice.append(item["maxPrice"])
    minPrice.append(item["minPrice"])


df = pd.DataFrame({"商品名": productName, "最高値": maxPrice, "最安値": minPrice})
df.to_csv("rakuten_api2.csv", encoding='utf-8-sig')
df.head(30)

#%%

# 3. 以下のAPIを使って、任意のジャンルのランキング一覧を取得し、CSV出力してみましょう
# https://webservice.rakuten.co.jp/api/ichibaitemranking/

import requests
import json
import pandas as pd

rakuten_id = "1061452151101776425"
formatVersion = "2"
genreId = "100283"
url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?applicationId={id}&formatVersion={formatVersion}&genreId={genreId}"
url = url.format(id=rakuten_id, formatVersion=formatVersion, genreId=genreId)

data = requests.get(url).json()["Items"]

itemName = []
itemPrice = []

for item in data:
    itemName.append(item["itemName"])
    itemPrice.append(item["itemPrice"])


df = pd.DataFrame({"商品名": itemName, "商品価格": itemPrice})
df.to_csv("rakuten_api3.csv", encoding='utf-8-sig')
df.head(30)


#%%
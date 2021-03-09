import pandas as pd
# import eel

### デスクトップアプリ作成課題
def kimetsu_search(search_keyword, source_file):
    # 検索対象取得
    try:
        df=pd.read_csv(source_file)
    except:
        return "指定ファイルが存在しません"
    source=list(df["name"])

    # 検索
    if search_keyword in source:
        return "『{}』はあります".format(search_keyword)
    else:
        # 追加
        # add_flg=input("追加登録しますか？(0:しない 1:する)　＞＞　")
        # if add_flg=="1":
        source.append(search_keyword)

        # CSV書き込み
        df=pd.DataFrame(source, columns=["name"])
        df.to_csv(source_file, encoding="utf_8-sig")
        return "『{}』はありません".format(search_keyword)

#%%

### 検索ツールサンプル
### これをベースに課題の内容を追記してください

# １．入力したキーワードで、キャラクターリスト(source)を検索して、存在すれば存在する旨を、存在しなければ存在しない旨をPrint文で表示してみましょう
# ２．１に追加して結果が存在しなかった場合に、キャラクターリスト(source)に追加できるようにしてみましょう
# ３．２に追加してキャラクターリスト(source)をCSVから読み込んで登録できるようにしてみましょう
# ４．３に追加してキャラクターリスト(source)をCSVに書き込めるようにしてみましょう

import pandas as pd

# 検索ソース
# source=["ねずこ","たんじろう","きょうじゅろう","ぎゆう","げんや","かなお","ぜんいつ"]

### 検索ツール
def search1():
    word =input("鬼滅の登場人物の名前を入力してください >>> ")
    
    if word in source:
        print("{}が見つかりました".format(word))
    else:
        print("{}は見つかりませんでした".format(word))

def search2():
    word =input("鬼滅の登場人物の名前を入力してください >>> ")
    
    if word in source:
        print("{}が見つかりました".format(word))
        return source
    else:
        source.append(word)
        print("{}を追加しました".format(word))
        return source

def search3(source):
    word =input("鬼滅の登場人物の名前を入力してください >>> ")
    
    if word in source:
        print("{}が見つかりました".format(word))
        return source
    else:
        source.append(word)
        print("{}を追加しました".format(word))
        return source

if __name__ == "__main__":
    # search1()
    df_source = pd.read_csv("source.csv")
    beforeLen = len(df_source)
    tmp = search3(list(df_source.name))
    df_source = pd.DataFrame({"name": pd.Series(tmp)})
    print(df_source)
    afterLen = len(df_source)
    if beforeLen < afterLen:
        print("source.csvを更新して、終了します")
        df_source.to_csv("source.csv")
    else:
        print("終了します")


#%%


#%%

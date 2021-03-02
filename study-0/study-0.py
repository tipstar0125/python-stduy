#%%

# １ 変数の使い方

name1 = "ねずこ"
name2 = "ぜんいつ"

print("「" + name1 + "」と「" + name2 + "」は仲間です")


#%%

# ２ if文の使い方

name2 = "むざん"

if name2 == "むざん":
    print("「" + name1 + "」と「" + name2 + "」は仲間ではありません")
else:
    print("「" + name1 + "」と「" + name2 + "」は仲間です")


#%%

# ３ 配列の使い方

names = ["たんじろう",
        "ぎゆう",
        "ねずこ",
        "むざん"]

names.append("ぜんいつ")

print(names)
# %%

# ４ for文の使い方

for name in names:
    print(name)

# %%

# ５　関数の使い方

def IsNakama(name1, name2):
    if name2 == "むざん":
        print("「" + name1 + "」と「" + name2 + "」は仲間ではありません")
    else:
        print("「" + name1 + "」と「" + name2 + "」は仲間です")   

name1, name2 = "ねずこ", "ぜんいつ"
IsNakama(name1, name2)

name1, name2 = "ねずこ", "むざん"
IsNakama(name1, name2)

def AddNakama(names, name):
    names.append(name)
    print(names)

names = ["たんじろう",
        "ぎゆう",
        "ねずこ",
        "むざん"]

AddNakama(names, "ぜんいつ")

def LoopNakama(names):
    for name in names:
        print(name)

LoopNakama(names)


#%%

# ６ 引数を使う関数の使い方

# 【仕様】
# 関数名：なんでも良い
# 引数：キャラクターの名前を格納する変数
# 関数で行う処理：キャラクターのリスト（３、４で使ったもの）の中に、
# 引数で入力されたキャラクター名が存在するか確認して結果をprint文で表示させる
# 例）引数が「ぎゆう」→nmaeにぎゆうが存在する→ぎゆうは含まれますと表示


def IsGiyu(names):
    if "ぎゆう" in names:
        print("ぎゆうはふくまれます")
    else:
        print("ぎゆうはふくまれません")

names = ["たんじろう",
        "ぎゆう",
        "ねずこ",
        "むざん"]

IsGiyu(names)

# %%

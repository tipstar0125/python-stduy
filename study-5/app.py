#%%

# 1. オーダー登録した商品の一覧（商品名、価格）を表示できるようにしてください
# 2. オーダーをコンソール（ターミナル）から登録できるようにしてください 登録時は商品コードをキーとする
# 3. 商品マスタをCSVから登録できるようにしてください
# 4. オーダー登録時に個数も登録できるようにしてください
# 5. オーダー登録した商品の一覧（商品名、価格）を表示し、かつ合計金額、個数を表示できるようにしてください
# 6. お客様からのお預かり金額を入力しお釣りを計算できるようにしてください
# 7. 5, 6の内容を、日付時刻をファイル名としたレシートファイル（テキスト）に出力できるようにしてください

#%%

import pandas as pd
from datetime import datetime as dt


### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
        self.receive_money=0
        self.return_money=0
        self.total_cost=0
    
    def get_name(self):
        return self.item_name

    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_master=item_master
        self.df_item_master = pd.DataFrame()
    
    def register_master(self, file_name):
        
        try:
            self.df_item_master = pd.read_csv(file_name, dtype=str)
            item_master=[]
            for row in self.df_item_master.itertuples():
                item_master.append(Item(row.item_code, row.item_name, int(row.price)))
            self.item_master = item_master
            IsFile = True
        except:
            self.item_master = []
            IsFile = False

        return IsFile

    def add_item_order(self,item_code,item_num):
        IsRegisterDone = False
        for item_info in self.item_master:
            if item_code == item_info.item_code:
                IsRegisterDone = True
                self.item_order_list.append({"item_code": item_code, 
                                            "item_num": item_num, 
                                            })
        return IsRegisterDone

    def cancel_item_order(self):

        self.item_order_list.pop(-1)

    def clear_item_order(self):

        self.item_order_list = []

    def view_item_list(self):
        item_code_list = []
        item_name_list = []
        price_list = []
        item_num_list = []
        sum_cost_list = []

        for item in self.item_order_list:
            for item_info in self.item_master:
                if item["item_code"] == item_info.item_code:
                    item_num = int(item["item_num"])
                    sum_cost = item_info.price*item_num

                    item_code_list.append(item["item_code"])
                    item_name_list.append(item_info.item_name)
                    price_list.append(item_info.price)
                    item_num_list.append(item_num)
                    sum_cost_list.append(sum_cost)

        df_order = pd.DataFrame({
            "商品コード": item_code_list,
            "商品名": item_name_list,
            "価格": price_list,
            "個数": item_num_list,
            "小計金額": sum_cost_list,
        })
        df_order.set_index("商品コード", inplace=True)
        return df_order
    
    def calc_total_cost(self):
        df_order = self.view_item_list()
        self.total_cost = df_order["小計金額"].sum()
        return self.total_cost

    def calc_return_money(self, receive_money):
        self.receive_money = int(receive_money)
        # df_order = self.view_item_list()
        # self.total_cost = df_order["小計金額"].sum()
        self.calc_total_cost()
        self.return_money = self.receive_money - self.total_cost

        if self.return_money < 0:
            IsEnough = False
        else:
            IsEnough = True
        
        return self.return_money, IsEnough

    def output_receipt(self):
        max_string = 10
        df_order = self.view_item_list()
        receipt_text = "Receipt\n\n" + "商品コード".ljust(max_string) + "\t"
        for col in df_order.columns:
            receipt_text += col.ljust(max_string) + "\t"
        receipt_text += "\n"

        for row in df_order.itertuples():
            for content in row:
                receipt_text += str(content).ljust(max_string) + "\t"
            receipt_text += "\n"
        receipt_text += "\n"
        receipt_text += "合計金額:{}".format(self.total_cost) + "\n"
        receipt_text += "お預かり金額:{}".format(self.receive_money) + "\n"
        receipt_text += "お釣り:{}".format(self.return_money)

        return(receipt_text)

def item_master_register(file_name):

    try:
        df_item_master = pd.read_csv(file_name, dtype=str)
        item_master=[]
        for row in df_item_master.itertuples():
            item_master.append(Item(row.item_code, row.item_name, int(row.price)))
        order=Order(item_master)
        IsFile = True
    except:
        order=Order([])
        IsFile = False

    return order, IsFile
    
### メイン処理
def main():
    # マスタ登録
    df_item_master = pd.read_csv('商品マスタ.csv', dtype=str)
    item_master=[]
    for row in df_item_master.itertuples():
        item_master.append(Item(row.item_code, row.item_name, int(row.price)))
    
    # オーダー登録
    order=Order(item_master)

    order_number = int(input("オーダ数を入力してください："))
    for _ in range(order_number):
        order.add_item_order(input("オーダを入力してください："),
                            input("個数を入力してください："),
                            )

    # お預かり金額登録
    order.calc_return_money(input("お預かり金額を入力してください："))

    # オーダー表示
    receipt = order.output_receipt()

    with open(dt.now().strftime("%Y%m%d_%H%M") + "_receipt.txt", "w") as f:
        f.write(receipt)

    
if __name__ == "__main__":
    main()

#%%

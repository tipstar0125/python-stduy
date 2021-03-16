import eel
import settings
import app
from datetime import datetime as dt
from logging import getLogger,  FileHandler, StreamHandler, Formatter, DEBUG


app_name="web"
end_point="index.html"
size=(750, 750)

order = app.Order([])

logger = getLogger(__name__)
fomatterSetting = Formatter('[%(asctime)s] %(name)s %(threadName)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
# handler = FileHandler('test.log')
handler = StreamHandler()
# handler = NullHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
handler.setFormatter(fomatterSetting)
logger.addHandler(handler)
logger.propagate = False

@eel.expose
def item_master_register(file_name):

    IsFile = order.register_master(file_name)
    
    if IsFile:
        logger.debug(order.df_item_master)
        eel.register_completed(order.df_item_master.to_dict())
    else:
        eel.view_error('指定ファイルがありません')


@eel.expose
def buy_register(order_code, order_number):
    IsRegisterDone = order.add_item_order(order_code, order_number)
    logger.debug(order.view_item_list())

    if not IsRegisterDone:
        eel.view_error('商品コードが登録されていません')
    else:
        eel.view_total_cost(int(order.calc_total_cost()), order.item_order_list)

@eel.expose
def buy_cancel():

    order.cancel_item_order()
    logger.debug(order.view_item_list())
    eel.view_total_cost(int(order.calc_total_cost()), order.item_order_list)


@eel.expose
def buy_clear():

    order.clear_item_order()
    logger.debug(order.view_item_list())
    eel.view_total_cost(int(order.calc_total_cost()), order.item_order_list)


@eel.expose
def payoff(receive_money):

    return_money, IsEnough = order.calc_return_money(receive_money)

    if IsEnough:
        receipt = order.output_receipt()
        with open(dt.now().strftime("%Y%m%d_%H%M") + "_receipt.txt", "w") as f:
            f.write(receipt)
        eel.view_return_money(int(return_money))
    else:
        eel.view_error('お金が足りません')


def main():
    settings.start(app_name,end_point,size)

if __name__ == "__main__":
    main()


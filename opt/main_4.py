import settings
import datetime
import time
import sys
from pybit import HTTP
from logging import getLogger, config


config.fileConfig('./logging_info.config')
logger = getLogger(__name__)

def find_quantity(total, price):
    quantity = float(total)/ float(price)
    return quantity

#口座残高取得
def balance_coins():
    global usdt_coin
    global coin1
    global coin2
    global coin3
    global coin4

    balance_list = session.get_wallet_balance()['result']['balances']

    #Balance USDT
    usdt_coin = float(next(x for x in balance_list if x['coin'] == 'USDT')['free'])
    usdt_coin = format(usdt_coin, '.8f')
    usdt_coin = find_quantity(usdt_coin, 1)

    #Balance coin1
    coin1 = float(next(x for x in balance_list if x['coin'] == base1)['free'])
    coin1 = format(coin1, '.8f')
    coin1 = find_quantity(coin1, 1)

    #Balance coin2
    coin2 = float(next(x for x in balance_list if x['coin'] == base2)['free'])
    coin2 = format(coin2, '.8f')
    coin2 = find_quantity(coin2, 1)

    #Balance coin3
    coin3 = float(next(x for x in balance_list if x['coin'] == base3)['free'])
    coin3 = format(coin3, '.8f')
    coin3 = find_quantity(coin3, 1)

    #Balance coin4
    coin4 = float(next(x for x in balance_list if x['coin'] == base4)['free'])
    coin4 = format(coin4, '.8f')
    coin4 = find_quantity(coin4, 1)


#残高をUSDTでの価値に換算
def usdt_value():
    #USDT Value Caluculation
    global usdt_coin1
    global usdt_coin2
    global usdt_coin3
    global usdt_coin4
    global total_usdt
    global last_price_coin1
    global last_price_coin2
    global last_price_coin3
    global last_price_coin4

    last_price_coin1 = session.last_traded_price(symbol=sym1)['result']['price']
    last_price_coin1 = float(last_price_coin1)
    last_price_coin2 = session.last_traded_price(symbol=sym2)['result']['price']
    last_price_coin2 = float(last_price_coin2)
    last_price_coin3 = session.last_traded_price(symbol=sym3)['result']['price']
    last_price_coin3 = float(last_price_coin3)
    last_price_coin4 = session.last_traded_price(symbol=sym4)['result']['price']
    last_price_coin4 = float(last_price_coin4)

    #USDT_coin1
    usdt_coin1 = coin1 * last_price_coin1
    usdt_coin1 = float(usdt_coin1)

    #USDT_coin2
    usdt_coin2 = coin2 * last_price_coin2
    usdt_coin2 = float(usdt_coin2)

    #USDT_coin3
    usdt_coin3 = coin3 * last_price_coin3
    usdt_coin3 = float(usdt_coin3)

    #USDT_coin4
    usdt_coin4 = coin4 * last_price_coin4
    usdt_coin4 = float(usdt_coin4)

    #TOTAL_USDT
    total_usdt = usdt_coin1 + usdt_coin2 + usdt_coin3 + usdt_coin4

#各通貨の目標パーセントと差を計算(小数点第二位まで)
def difference():
    #Rebalance Calculation
    global now_coin1perc
    global now_coin2perc
    global now_coin3perc
    global now_coin4perc
    global dif_coin1
    global dif_coin2
    global dif_coin3
    global dif_coin4

    now_coin1perc = (usdt_coin1/total_usdt)*100
    now_coin1perc = format(round(now_coin1perc,2))
    now_coin1perc = float(now_coin1perc)
    dif_coin1 = now_coin1perc-coin1perc
    dif_coin1 = format(round(dif_coin1 ,2))
    dif_coin1 = float(dif_coin1)

    now_coin2perc = (usdt_coin2/total_usdt)*100
    now_coin2perc = format(round(now_coin2perc,2))
    now_coin2perc = float(now_coin2perc)
    dif_coin2 = now_coin2perc-coin2perc
    dif_coin2 = format(round(dif_coin2 ,2))
    dif_coin2 = float(dif_coin2)

    now_coin3perc = (usdt_coin3/total_usdt)*100
    now_coin3perc = format(round(now_coin3perc,2))
    now_coin3perc = float(now_coin3perc)
    dif_coin3 = now_coin3perc-coin3perc
    dif_coin3 = format(round(dif_coin3 ,2))
    dif_coin3 = float(dif_coin3)

    now_coin4perc = (usdt_coin4/total_usdt)*100
    now_coin4perc = format(round(now_coin4perc,2))
    now_coin4perc = float(now_coin4perc)
    dif_coin4 = now_coin4perc-coin4perc
    dif_coin4 = format(round(dif_coin4 ,2))
    dif_coin4 = float(dif_coin4)

#売り注文
def sell_order(sell_coin, sym):
    try:
        session.place_active_order(symbol=sym, side="Sell", type="MARKET", qty=round(sell_coin, 6))
    except:
        try:
            session.place_active_order(symbol=sym, side="Sell", type="MARKET", qty=round(sell_coin, 3))
        except:
            try:
                session.place_active_order(symbol=sym, side="Sell", type="MARKET", qty=round(sell_coin, 2))
            except:
                try:
                    session.place_active_order(symbol=sym, side="Sell", type="MARKET", qty=sell_coin)
                except:
                    sell_coin = sell_coin/2
                    try:
                        session.place_active_order(symbol=sym, side="Sell", type="MARKET", qty=round(sell_coin, 2))
                    except:
                        sell_coin = sell_coin/2
                        try:
                            session.place_active_order(symbol=sym, side="Sell", type="MARKET", qty=round(sell_coin, 2))
                        except Exception as e:
                            logger.warning('failed sell order')
                            logger.warning(e.message)
                            logger.warning(str(sym) + str(sell_coin))

    balance_coins()
    usdt_value()


#買い注文
def buy_order(buy_coin, sym):

    buy_coin = -1*float(buy_coin)

    try:
        session.place_active_order(symbol=sym, side="Buy", type="MARKET", qty=round(buy_coin))
    except:
        buy_coin = buy_coin/2
        try:
            session.place_active_order(symbol=sym, side="Buy", type="MARKET", qty=round(buy_coin))
        except:
            buy_coin = buy_coin/2
            try:
                session.place_active_order(symbol=sym, side="Buy", type="MARKET", qty=round(buy_coin))
            except:
                buy_coin = buy_coin/2
                try:
                    session.place_active_order(symbol=sym, side="Buy", type="MARKET", qty=round(buy_coin))
                except:
                    buy_coin = buy_coin/2
                    try:
                        session.place_active_order(symbol=sym, side="Buy", type="MARKET", qty=round(buy_coin))
                    except Exception as e:
                        logger.warning('failed buy order')
                        logger.warning(e.massage)
                        logger.warning(str(sym) + str(buy_coin))
    balance_coins()
    usdt_value()

def first_buy():
    try:
        session.place_active_order(symbol=sym1, side="Buy", type="MARKET", qty=10)
    except:
        pass
    try:
        session.place_active_order(symbol=sym2, side="Buy", type="MARKET", qty=10)
    except:
        pass
    try:
        session.place_active_order(symbol=sym3, side="Buy", type="MARKET", qty=10)
    except:
        pass
    try:
        session.place_active_order(symbol=sym4, side="Buy", type="MARKET", qty=10)
    except:
        pass



#Main

#キー情報
#動かなくなった場合はKEYを再度作成する

MAIN_URL = settings.MAIN_URL
API_KEY = settings.API_KEY
API_SECRET = settings.API_SECRET

# MAIN_URL = 'https://api.bybit.com/'
# API_KEY = str(sys.argv[1])
# API_SECRET = str(sys.argv[2])
# base1 = str(sys.argv[3])
# base2 = str(sys.argv[4])
# base3 = str(sys.argv[5])
# base4 = str(sys.argv[6])
# rebal = int(sys.argb[7])

session = HTTP(MAIN_URL,
               api_key=API_KEY,
               api_secret=API_SECRET,
               spot=True)

rebal = 0.1
coin1perc = 25
coin2perc = 25
coin3perc = 25
coin4perc = 25

base1 = 'BTC'
base2 = 'ETH'
base3 = 'ATOM'
base4 = 'FIL'

sym1 = base1 + 'USDT'
sym2 = base2 + 'USDT'
sym3 = base3 + 'USDT'
sym4 = base4 + 'USDT'

count = 0
log_count = 0

while count < 181:

    total_usdt=0
    usdt_coin1=0
    usdt_coin2=0
    usdt_coin3=0
    usdt_coin4=0

    #初期買い注文
    if count == 0:
        first_buy()

    balance_coins()

    usdt_value()

    difference()

    #Sell Condition
    if (dif_coin1 > rebal or dif_coin2 > rebal or dif_coin3 > rebal or dif_coin4 > rebal):

        rebalcoin1 = total_usdt*(float(coin1perc)/100)
        rebalcoin1 = usdt_coin1 - rebalcoin1
        sellcoin1 = rebalcoin1/last_price_coin1

        rebalcoin2 = total_usdt*(float(coin2perc)/100)
        rebalcoin2 = usdt_coin2 - rebalcoin2
        sellcoin2 = rebalcoin2/last_price_coin2

        rebalcoin3 = total_usdt*(float(coin3perc)/100)
        rebalcoin3 = usdt_coin3 - rebalcoin3
        sellcoin3 = rebalcoin3/last_price_coin3

        rebalcoin4 = total_usdt*(float(coin4perc)/100)
        rebalcoin4 = usdt_coin4 - rebalcoin4
        sellcoin4 = rebalcoin4/last_price_coin4

        rebalcoin1 = '{0:.3f}'.format(rebalcoin1)
        rebalcoin2 = '{0:.3f}'.format(rebalcoin2)
        rebalcoin3 = '{0:.3f}'.format(rebalcoin3)
        rebalcoin4 = '{0:.3f}'.format(rebalcoin4)

        usdt_coin1 = '{0:.8f}'.format(usdt_coin1)
        usdt_coin2 = '{0:.8f}'.format(usdt_coin2)
        usdt_coin3 = '{0:.8f}'.format(usdt_coin3)
        usdt_coin4 = '{0:.8f}'.format(usdt_coin4)

        if (dif_coin1 > rebal):
            sell_order(sell_coin=sellcoin1,sym=sym1)

        if (dif_coin2 > rebal):
            sell_order(sell_coin=sellcoin2,sym=sym2)

        if (dif_coin3 > rebal):
            sell_order(sell_coin=sellcoin3,sym=sym3)

        if (dif_coin4 > rebal):
            sell_order(sell_coin=sellcoin4,sym=sym4)

        balance_coins()


    #Buy Condition
    if (usdt_coin > 10):

        usdt_value()

        difference()

        rebalcoin1 = total_usdt*(float(coin1perc)/100)
        buycoin1 = usdt_coin1 - rebalcoin1

        rebalcoin2 = total_usdt*(float(coin2perc)/100)
        buycoin2 = usdt_coin2 - rebalcoin2

        rebalcoin3 = total_usdt*(float(coin3perc)/100)
        buycoin3 = usdt_coin3 - rebalcoin3

        rebalcoin4 = total_usdt*(float(coin4perc)/100)
        buycoin4 = usdt_coin4 - rebalcoin4

        usdt_coin1 = '{0:.8f}'.format(usdt_coin1)
        usdt_coin2 = '{0:.8f}'.format(usdt_coin2)
        usdt_coin3 = '{0:.8f}'.format(usdt_coin3)
        usdt_coin4 = '{0:.8f}'.format(usdt_coin4)

        if (buycoin1 < 0):
            buy_order(buy_coin=buycoin1,sym=sym1)

        if (buycoin2 < 0):
            buy_order(buy_coin=buycoin2,sym=sym2)

        if (buycoin3 < 0):
            buy_order(buy_coin=buycoin3,sym=sym3)

        if (buycoin4 < 0):
            buy_order(buy_coin=buycoin4,sym=sym4)

        balance_coins()
    count = count + 1
    log_count = log_count + 1

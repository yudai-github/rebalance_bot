from time import sleep, time
from sys import exit
from pybit import HTTP
from pprint import pprint
import datetime


def find_quantity(total, price):
    quantity = float(total)/ float(price)
    return quantity

#口座残高取得
def balance_coins():
    global usdt_coin
    global coin1
    global coin2

    coin_balance = session.get_wallet_balance()['result']['balances']

    #Balance USDT
    usdt_coin = float(coin_balance[2]['free'])
    usdt_coin = format(usdt_coin, '.8f')
    usdt_coin = find_quantity(usdt_coin, 1)

    #Balance coin1
    coin1 = float(coin_balance[0]['free'])
    coin1 = format(coin1, '.8f')
    coin1 = find_quantity(coin1, 1)

    #Balance coin2
    coin2 = float(coin_balance[1]['free'])
    coin2 = format(coin2, '.8f')
    coin2 = find_quantity(coin2, 1)

#残高をUSDTでの価値に換算
def usdt_value():
    #USDT Value Caluculation
    global usdt_coin1
    global usdt_coin2
    global total_usdt
    global last_price_coin1
    global last_price_coin2

    last_price_coin1 = session.last_traded_price(symbol="BTCUSDT")['result']['price']
    last_price_coin1 = float(last_price_coin1)
    last_price_coin2 = session.last_traded_price(symbol="ETHUSDT")['result']['price']
    last_price_coin2 = float(last_price_coin2)

    #USDT_BTC
    usdt_coin1 = coin1 * last_price_coin1
    usdt_coin1 = float(usdt_coin1)

    #USDT_ETH
    usdt_coin2 = coin2 * last_price_coin2
    usdt_coin2 = float(usdt_coin2)

    #TOTAL_USDT
    total_usdt = usdt_coin + usdt_coin1 + usdt_coin2

#各通貨の目標パーセントと差を計算(小数点第二位まで)
def difference():
    #Rebalance Calculation
    global now_coin1perc
    global now_coin2perc
    global dif_coin1
    global dif_coin2

    now_coin1perc = (usdt_coin1/total_usdt)*100#35
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

#売り注文
def sell_order(sell_coin, sym):
    try:
        session.place_active_order(symbol=sym, side="Sell", type="MARKET", qty=round(sell_coin, 6))
    except Exception as e:
        print(e.message)
        print('小数点第6位まで' + str(round(sell_coin, 6)))
        try:
            session.place_active_order(symbol=sym, side="Sell", type="MARKET", qty=round(sell_coin, 3))
        except Exception as e:
            print(e.message)
            print('小数点第3位まで' + str(round(sell_coin, 3)))
            try:
                session.place_active_order(symbol=sym, side="Sell", type="MARKET", qty=round(sell_coin, 2))
            except Exception as e:
                print(e.message)
                print('小数点第2位まで' + str(round(sell_coin, 2)))
                try:
                    session.place_active_order(symbol=sym, side="Sell", type="MARKET", qty=sell_coin)
                except Exception as e:
                    print(e.message)
                    print('全て失敗')
    balance_coins()
    usdt_value()


#買い注文
def buy_order(buy_coin, sym):

    buy_coin = -1*float(buy_coin)

    try:
        session.place_active_order(symbol=sym, side="Buy", type="MARKET", qty=round(buy_coin))
    except Exception as e:
        print(e.message)
        buy_coin = buy_coin/2
        try:
            session.place_active_order(symbol=sym, side="Buy", type="MARKET", qty=round(buy_coin))
        except Exception as e:
            print(e.message)
            buy_coin = buy_coin/2
            try:
                session.place_active_order(symbol=sym, side="Buy", type="MARKET", qty=round(buy_coin))
            except Exception as e:
                print(e.message)
                buy_coin = buy_coin/2
                try:
                    session.place_active_order(symbol=sym, side="Buy", type="MARKET", qty=round(buy_coin))
                except Exception as e:
                    print(e.message)
                    buy_coin = buy_coin/2
                    try:
                        session.place_active_order(symbol=sym, side="Buy", type="MARKET", qty=round(buy_coin))
                    except Exception as e:
                        print(e.message)
                        print(round(buy_coin))


    balance_coins()
    usdt_value()


#Main

#キー情報
#動かなくなった場合はKEYを再度作成する
API_KEY = "rD0AxleRu4HC0cUlDj"
API_SECRET = "Z26RRUOxZQoBLZMQ8lMqXa3xI4WCwBDMtkcY"
TEST_URL = "https://api-testnet.bybit.com/"

session = HTTP("https://api-testnet.bybit.com", api_key=API_KEY, api_secret=API_SECRET, spot=True)

rebal = 5
coin1perc = 50
coin2perc = 50

balance_coins()
print('USDT残高' + str(usdt_coin))
print('BTC残高' + str(coin1))
print('ETH残高' + str(coin2))

count = 0

while count < 25:

    total_usdt=0
    usdt_coin1=0
    usdt_coin2=0

    #LastPrice
    #COIN1 = BTC
    last_price_coin1 = session.last_traded_price(symbol="BTCUSDT")['result']['price']
    last_price_coin1 = float(last_price_coin1)
    last_price_coin1 = format(last_price_coin1/1, '.8f')
    last_price_coin1 = find_quantity(last_price_coin1, 1)

    #LastPrice
    #COIN2 = ETH
    last_price_coin2 = session.last_traded_price(symbol="ETHUSDT")['result']['price']
    last_price_coin2 = float(last_price_coin2)
    last_price_coin2 = format(last_price_coin2/1, '.8f')
    last_price_coin2 = find_quantity(last_price_coin2, 1)

    usdt_value()
    print('残高BTCをUSDT変換:' + str(usdt_coin1))
    print('残高ETHをUSDT変換:' + str(usdt_coin2))
    print('トータルUSDT:' + str(total_usdt))

    difference()

    print(datetime.datetime.now().time())

    print('目標と現在のBTCの総資産での差:' + str(dif_coin1) + '%')
    print('目標と現在のETHの総資産での差:' + str(dif_coin2) + '%')

    session.query_symbol()

    #Sell Condition
    if (dif_coin1 > rebal or dif_coin2 > rebal):
        #残高USDT全体から目標coin1USDTを算出
        #実際coin1USDTと目標coin1USDTの差を算出
        #差分を現在のcoin1の1枚あたりのUSDTで除算して売る枚数を算出
        rebalcoin1 = total_usdt*(float(coin1perc)/100)
        rebalcoin1 = usdt_coin1 - rebalcoin1
        sellcoin1 = rebalcoin1/last_price_coin1
        print('USDT換算のBTCの差:' + str(rebalcoin1))
        print('BTC売数量:' + str(sellcoin1))

        rebalcoin2 = total_usdt*(float(coin2perc)/100)
        rebalcoin2 = usdt_coin2 - rebalcoin2
        sellcoin2 = rebalcoin2/last_price_coin2
        print('USDT換算のETHの差:' + str(rebalcoin2))
        print('ETH売数量:' + str(sellcoin2))

        #小数点以下3桁
        rebalcoin1 = '{0:.3f}'.format(rebalcoin1)
        rebalcoin2 = '{0:.3f}'.format(rebalcoin2)

        usdt_coin1 = '{0:.8f}'.format(usdt_coin1)
        usdt_coin2 = '{0:.8f}'.format(usdt_coin2)

        if (dif_coin1 > rebal):
            sell_order(sell_coin=sellcoin1,sym='BTCUSDT')

        if (dif_coin2 > rebal):
            sell_order(sell_coin=sellcoin2,sym='ETHUSDT')

        balance_coins()


    #Buy Condition
    if (usdt_coin > 10):

        usdt_value()

        difference()

        rebalcoin1 = total_usdt*(float(coin1perc)/100)
        rebalcoin1 = usdt_coin1 - rebalcoin1
        buycoin1 = rebalcoin1/last_price_coin1
        print('USDT換算のBTCの差:' + str(rebalcoin1))

        rebalcoin2 = total_usdt*(float(coin2perc)/100)
        rebalcoin2 = usdt_coin2 - rebalcoin2
        buycoin2 = rebalcoin2/last_price_coin2
        print('USDT換算のETHの差:' + str(rebalcoin2))

        usdt_coin1 = '{0:.8f}'.format(usdt_coin1)
        usdt_coin2 = '{0:.8f}'.format(usdt_coin2)

        if (buycoin1 < 0 and rebalcoin1 < -0.001):
            buy_order(buy_coin=rebalcoin1,sym='BTCUSDT')

        if (buycoin2 < 0 and rebalcoin2 < -0.001):
            buy_order(buy_coin=rebalcoin2,sym='ETHUSDT')

        balance_coins()
    count = count + 1

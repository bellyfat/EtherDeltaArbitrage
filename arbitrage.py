import time
import sys
import configparser

from etherdeltaclientservice import EtherDeltaClientService

if __name__ == "__main__":

    # Load config
    config = configparser.ConfigParser()
    config.read('config.ini')
    userAccount = config['DEFAULT']['user_wallet_public_key']
    user_wallet_private_key = config['DEFAULT']['user_wallet_private_key']
    token1 = config['DEFAULT']['token_to_trade1']
    token2 = config['DEFAULT']['token_to_trade2']
    token3 = config['DEFAULT']['token_to_trade3']
    token4 = config['DEFAULT']['token_to_trade4']
    token5 = config['DEFAULT']['token_to_trade5']
    token6 = config['DEFAULT']['token_to_trade6']
    token7 = config['DEFAULT']['token_to_trade7']
    token8 = config['DEFAULT']['token_to_trade8']
    token9 = config['DEFAULT']['token_to_trade9']
    token10 = config['DEFAULT']['token_to_trade10']
    tokens = [token1, token2, token3, token4, token5, token6, token7, token8, token9, token10]
    for token in tokens:
        es = EtherDeltaClientService()

        es.start(userAccount, token)
        time.sleep(5)   
        count = 0
        for x in range (0, 100):
            #balance = es.getBalance(token, userAccount)
            #print (balance)
            #balance = es.getBalance('ETH', userAccount)
            #print (balance)
            sells = es.orders_sells
            buys = es.orders_buys

            while len(sells) == 0:
                print ("wait")
                time.sleep(10)
                sells = es.orders_sells
                buys = es.orders_buys

            
            for buy in buys:
                for sell in sells:
                    if (float(buy['price']) > float(sell['price']) ):
                        if float(sell['ethAvailableVolumeBase']) > float(buy['ethAvailableVolumeBase']):
                            if float(buy['ethAvailableVolumeBase']) > es.getBalance('ETH', userAccount):
                                print ("TRADE")
                                count += 1
                                #es.trade(sell, float(es.getBalance('ETH', userAccount)))
                            else:
                                print ("TRADE")
                                count += 1
                                #es.trade(sell, float(buy['ethAvailableVolumeBase']), user_wallet_private_key)
                            while float(es.getBalance(token, userAccount)) == 0:
                                time.sleep(1)
                           # es.trade(buy, float(es.getBalance(token), user_wallet_private_key))
                        else:
                            if float(sell['ethAvailableVolumeBase']) > es.getBalance('ETH', userAccount):
                                print ("TRADE")
                                count += 1
                                #es.trade(sell, float(es.getBalance('ETH', userAccount)))
                            else:
                                print ("TRADE")
                                count += 1
                                #es.trade(sell, float(sell['ethAvailableVolumeBase']), user_wallet_private_key)
                            while float(es.getBalance(token, userAccount)) == 0:
                                time.sleep(1)                    
                            #es.trade(buy, float(sell['ethAvailableVolumeBase']), user_wallet_private_key)
            print ("no opportunities")
            time.sleep(5)        
    print (count)










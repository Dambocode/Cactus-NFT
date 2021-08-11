import webhook, opensea, config


import time
import datetime



def monitorlogic():
    last_request_epoch = int(time.time())
    while True:
        config_data = config.loadconfig()
        collections = config_data["Collections"]
        for collection in collections:
            sales_data = opensea.getsales(collection["Collection Address"], last_request_epoch)
            webhook_url = collection["Webhook"]
            
            try:
                if sales_data["asset_events"] != []:
                    for event in sales_data["asset_events"]:
                        webhook_json = {
                            "Seller": event["seller"],
                            "Buyer": event["winner_account"],
                            "Project": event["asset"],
                            "Payment": event["payment_token"],
                            "Price": event["total_price"]
                            }

                        print("[{}] [{}] New sale found for {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), webhook_json["Project"]["asset_contract"]["symbol"], collection))

                        webhook.newsalehook(webhook_json, webhook_url) # Sends webhook to monitor
                        time.sleep(5)
                

                elif sales_data["asset_events"] == []:
                    print("[{}] [{}] No new sales found, sleeping for 60 seconds".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), collection))

                else:
                    print("[{}] Unknown Error 1".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            except:
                print("[{}] Unknown Error 2".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        last_request_epoch = int(time.time()) # Saves the time of the last request so it can be used to pull up all new products since this time.
        time.sleep(60)
# monitorlogic("0xbb0fa986710dbfadf64d8e3c16b93db06b351136")
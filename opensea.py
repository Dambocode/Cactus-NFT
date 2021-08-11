import requests
import json

import webhook # Custom



def getsales(collection=None, last_request_epoch=None):
    url = "https://api.opensea.io/api/v1/events"


    querystring = {
        "only_opensea":"false",
        "offset":"0",
        "limit":"100",
        "occurred_after": last_request_epoch,
        "event_type": "successful",
        "asset_contract_address": collection
        }


    headers = {
        "Accept": "application/json",
        "X-API-KEY": "8c9e60a4e0c74ede901adc96fdccc370"
        }

    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        try:
            if response == "200" or "204":
                try:
                    parsed = json.loads(response.text)
                    # print(parsed["asset_events"][1]["total_price"])
                    # print(w3.fromWei(int(parsed["asset_events"][1]["total_price"]), 'ether'))
                    return parsed
                except:
                    print(response.text)

        except:
            None

    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        webhook.errorwebhook("Connection Timeout")
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        webhook.errorwebhook("Bad URL")
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        webhook.errorwebhook("Fatal Error Unknown")
        raise SystemExit(e)
getsales()
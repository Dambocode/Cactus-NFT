import requests  # dependency
import config  # Custom
import time

from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/<infura-project-id>"))


def newsalehook(openseadata, webhook_url):

    eth_price = w3.fromWei(int(openseadata["Price"]), "ether")
    eth_usd_conversion = openseadata["Payment"]["usd_price"]
    config_data = config.loadconfig()

    url = webhook_url  # webhook url, from here: https://i.imgur.com/f9XnAew.png

    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data = {
        "content": "",
        "username": "Dambotics Sales Tracker",
        "avatar_url": "https://pbs.twimg.com/profile_images/1404101472489517060/FtUD1NVD_400x400.jpg",
    }

    embed_fields = []
    embed_fields.append(
        {
            "name": "Sale Price",
            "value": "{} Ξ\n${} USD\n".format(
                eth_price, round(float(eth_price) * float(eth_usd_conversion), 2)
            ),
        }
    )

    try:
        embed_fields.append(
            {
                "name": "Buyer",
                "value": "[{}]({})".format(
                    openseadata["Buyer"]["user"]["username"],
                    "https://opensea.io/{}".format(openseadata["Buyer"]["address"]),
                ),
                "inline": True,
            }
        )

    except:
        embed_fields.append(
            {"name": "Buyer", "value": "[{}]({})".format("Null", ""), "inline": True}
        )
    try:
        embed_fields.append(
            {
                "name": "Seller",
                "value": "[{}]({})".format(
                    openseadata["Seller"]["user"]["username"],
                    "https://opensea.io/{}".format(openseadata["Seller"]["address"]),
                ),
                "inline": True,
            }
        )
    except:
        embed_fields.append(
            {"name": "Buyer", "value": "[{}]({})".format("Null", ""), "inline": True}
        )

    thumbnail = {"url": openseadata["Project"]["image_url"]}

    # Timestamp
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    footer = {
        "text": "Dambotics Sales Tracker • {}".format(current_time),
        "icon_url": "https://pbs.twimg.com/profile_images/1404101472489517060/FtUD1NVD_400x400.jpg",
    }

    author = {
        "name": openseadata["Project"]["asset_contract"]["name"],
        "icon_url": openseadata["Project"]["asset_contract"]["image_url"],
        "url": openseadata["Project"]["asset_contract"]["external_link"],
    }

    # leave this out if you dont want an embed
    # for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"] = [
        {
            "description": "",
            "title": "New sale for {}".format(
                openseadata["Project"]["asset_contract"]["name"]
                + " - "
                + openseadata["Project"]["token_id"]
            ),
            "url": openseadata["Project"]["permalink"],
            "color": 16728832,
            "fields": embed_fields,
            "thumbnail": thumbnail,
            "footer": footer,
            "author": author,
        }
    ]

    result = requests.post(url, json=data)

    # try:
    # result.raise_for_status()
    # except requests.exceptions.HTTPError as err:
    # print(err)
    # else:
    # print("Payload delivered successfully, code {}.".format(result.status_code))


# result: https://i.imgur.com/DRqXQzA.png


def errorwebhook(errordata):
    config_data = config.loadconfig()

    url = config_data["Webhooks"]["Error"]

    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data = {
        "content": "",
        "username": "CactusNFT",
        "avatar_url": "https://pbs.twimg.com/profile_images/1412152546618183681/mXJ2GHGv_400x400.jpg",
    }

    embed_fields = [{"name": "Error", "value": errordata}]

    # leave this out if you dont want an embed
    # for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"] = [
        {
            "description": "",
            "title": "Fatal Monitor Error",
            "color": 16711680,
            "fields": embed_fields,
        }
    ]

    result = requests.post(url, json=data)

    print(result.status_code)

import json
import webbrowser
import requests
import time
base_url = 'https://www.supremenewyork.com'
shop_url = base_url + '/shop'
inventory_url = base_url + '/mobile_stock.json'
mobile_user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'


def get_id(item):
  response = requests.get(inventory_url).json()
  drops = response['products_and_categories']['new'] # Only concerned with new drops
  return next((drop['id'] for drop in drops if item in drop["name"]), None)

def watch(item):
  item_id = get_id(item)
  while not item_id:
    item_id = get_id(item)
    print('[INFO] Waiting for drop')
    time.sleep(5)
  return item_id

def open_in_browser(item):
  item_id = watch(item)
  webbrowser.open_new_tab(shop_url + '/{}'.format(item_id))

def add_to_cart(item_id):
  headers = {
    'User-Agent': mobile_user_agent
  }
  req = requests.post(shop_url + f'{item_id}/add.json', headers=headers)
  res = requests.get(shop_url + '/cart_extended.json', headers=headers).json()
  print(res)

def buy(name, color=None, sizing=None):
  general_id = watch(name)
  res = requests.get(base_url + '/shop/{}.json'.format(general_id)).json()
  styles = res['styles']
  print(json.dumps(styles, indent=2, sort_keys=True))
  # Cop the the first colorway in XL if the color and sizing aren't specified
  # TODO refactor to cop the first available item instead
  colorway = next((style for style in styles if color == style['name']), None) if color else styles[0]
  sizes = colorway['sizes']
  size = next((s for s in sizes if sizing == s['name']), None) if sizing else sizes[-1]
  print(size['id'])
  add_to_cart(size['id'])

buy('Mirrored', 'Royal', 'Medium')

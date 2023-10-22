# import requests

# url = 'http://icanhazip.com/'

# proxies = {
#     'http' : 'socks5://127.0.0.1:9050',
#     'https' : 'socks5://127.0.0.1:9050'
# }

# res = requests.get(url,proxies = proxies)

# print(res.text)

import pandas as pd
previous_word = pd.read_csv("/home/ubuntu/mecab-ko-dic-2.1.1-20180720/user-dic/nnp.csv")
previous_word = previous_word.iloc[:,0].to_list()
print(previous_word)


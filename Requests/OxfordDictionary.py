
# for more information on how to install requests# http://docs.python-requests.org/en/master/user/install/#install
import  requests
import json

# TODO: replace with your own app_id and app_key
app_id = '01993288'
app_key = '54200225d71891a07577574d80ac570c'
language = 'en'
word_id = 'play'

url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/'  + language + '/'  + word_id.lower()
#url Normalized frequency
urlFR = 'https://od-api.oxforddictionaries.com:443/api/v1/stats/frequency/word/'  + language + '/?corpus=nmc&lemma=' + word_id.lower()
r = requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})
# print("code {}\n".format(r.status_code))
print("text \n" + r.text)
# print("json \n" + json.dumps(r.json()))

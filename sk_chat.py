from conf import confGet
import requests
import json

def balance_check(KEY=str):
    url = "https://api.deepseek.com/user/balance"
    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': 'Bearer {}'.format(KEY)
    }
    rsp = requests.request("GET", url, headers=headers, data=payload)
    if rsp.status_code == requests.codes.ok:
        return '{} {}'.format(json.loads(rsp.text)['balance_infos'][0]['total_balance'],json.loads(rsp.text)['balance_infos'][0]['currency'])
    else:
        return '{} {}'.format(rsp.status_code,json.loads(rsp.text)['error']['message'])

def data_gen(msg=list,temp=float,stream=bool):
    payload = json.dumps({
      "messages": msg,
      "model": "deepseek-chat",
      "max_tokens": 8192,
      "temperature": temp,
      "stream": stream
    })
    return payload

def usr_get(rnd=int):
    usr = input('User #{}\n'.format(rnd))
    if usr == '':
        print('Aborted.')
        return False
    msg.append({'role': 'user', 'content': usr})
    return True

conf = confGet('sk.json')
# conf['KEY']
# conf['stream']

url = "https://api.deepseek.com/chat/completions"
rnd = 0

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {}'.format(conf['KEY'])
}
msg = []

while True:
    try:
        temp = input('Temperature: ')
        if temp == '':
            temp = 1.0
            break
        temp = round(float(temp),1)
        if not 0 <= temp <= 2:
            raise
        break
    except:
        print('Invalid temperature. Should be a float between 0.0 and 2.0, inclusive of the boundaries.')

sys = input('     System: ')
if sys == '':
    sys = 'You are a helpful assistant.'
msg.append({'role': 'system', 'content': sys})

print()

while True:
    rnd += 1
    if not usr_get(rnd):
        break
    print()
    print('Assistant #{}'.format(rnd))
    rsp = requests.request("POST", url, headers=headers, data=data_gen(msg,temp,conf['stream']))
    ast = json.loads(rsp.text)['choices'][0]['message']['content']
    msg.append({'role': 'assistant', 'content': ast})
    print(ast)
    print()

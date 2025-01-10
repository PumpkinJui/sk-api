from conf import confGet
import requests
import json

def balance_check(KEY):
    url = "https://api.deepseek.com/user/balance"
    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': 'Bearer {}'.format(KEY)
    }
    response = requests.request("GET", url, headers=headers, data=payload)

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

url = "https://api.deepseek.com/chat/completions"
rnd = 0

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {}'.format(KEY)
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
    print('Assistant #{}'.format(rnd))
    rsp = requests.request("POST", url, headers=headers, data=data_gen(msg,temp,stream))
    ast = json.loads(rsp.text)['choices'][0]['message']['content']
    msg.append({'role': 'assistant', 'content': ast})
    print(ast)
    print()

import requests
import json

url = "https://api.deepseek.com/chat/completions"
KEY = "sk-REMOVED"
rnd = 0

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {}'.format(KEY)
}
msg = []

def data_gen(msg=list,temp=float):
    payload = json.dumps({
      "messages": msg,
      "model": "deepseek-chat",
      "max_tokens": 8192,
      "temperature": temp
    })
    return payload

def usr_gen(rnd):
    usr = input('User #{}\n'.format(rnd))
    if usr == '':
        print('Aborted.')
        return False
    msg.append({'role': 'user', 'content': usr})
    return True

while True:
    try:
        temp = input('Temperature: ')
        if temp == '':
            temp = 1.0
        temp = float(temp)
        if not 0 <= temp <= 2:
            raise
        break
    except:
        print('Invalid temperature.')

sys = input('     System: ')
if sys == '':
    sys = 'You are a helpful assistant.'
msg.append({'role': 'system', 'content': sys})

print()

while True:
    rnd += 1
    if not usr_gen(rnd):
        break
    print('Assistant #{}'.format(rnd))
    response = requests.request("POST", url, headers=headers, data=data_gen(msg,temp))
    ast = json.loads(response.text)['choices'][0]['message']['content']

    print(ast)
    print()

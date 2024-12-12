import requests
import json

url = "http://localhost:8090/predict"
params = {'conversation': 'میتونی بهم از هوای روزای بعد بگی؟ بله حتما چه شهری هستی؟ اصفهانم  هوای اصفهان توی روزهای پیشرو به این شکله API', 'turn':'به یوان چین'}
response = requests.get(url, params=params)
result_NLU = response.json()
print(f'NLU')
print(json.dumps(result_NLU, indent=4, ensure_ascii=False))



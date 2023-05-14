import requests

url = 'https://api.threatbook.cn/v3/file/report'
params = {
    'apikey': 'e12e1de6cd624c9983831153b536f28fa608c78a2d6d42b4b5871fe9c11d79a5',
    'sandbox_type': 'win10_1903_enx64_office2016',
    'sha256': '5ae3939ab33427edd737ab2957e8019e637ab10daef1ea57285097cb5d4f63f9'
}
response = requests.get(url, params=params)
print(response.json())

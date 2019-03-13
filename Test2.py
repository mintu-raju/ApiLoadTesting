from bs4 import BeautifulSoup
import requests

url = "https://v2staging.weavedin.com/index/"
session = requests.session()
soup = BeautifulSoup(session.get(url).text, "html.parser")
csrfToken = soup.find(attrs={"id": "csrf_token"})
params = {'email': 'admin@weavedin.com', 'password': 'weavedindemo76k', 'csrf_token': csrfToken['value'],
          'signIn': "Sign in"}
print(params)

response = session.post(url, data=params, headers=dict(referer=url))

print(response.status_code)
url_dashboard = 'https://v2staging.weavedin.com/index/#/dashboard'
result = session.get(url_dashboard, headers=dict(referer=url_dashboard))
print(result.headers['Set-Cookie'],"STATUS:   "+str(result.status_code))

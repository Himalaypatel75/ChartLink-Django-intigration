import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from django.shortcuts import render
from django.http import JsonResponse

def fetch_stock_data():
    url = "https://chartink.com/screener/process"
    condition = {"scan_clause": "({cash} ( latest volume > 4 weeks ago volume))", "debug_clause": "groupcount( 1 where daily volume > 4 weeks ago volume)"}

    with requests.session() as s:
        r_data = s.get(url)
        soup = bs(r_data.content, "lxml")
        meta = soup.find("meta", {"name": "csrf-token"})["content"]

        header = {"x-csrf-token": meta}
        data = s.post(url, headers=header, data=condition).json()

        stock_list = pd.DataFrame(data["data"])
        return stock_list.sort_values(by='per_chg', ascending=False)

def index(request):
    return render(request, 'index.html')

def load_data(request):
    stock_list = fetch_stock_data()
    data = stock_list.to_dict(orient='records')
    return JsonResponse(data, safe=False)

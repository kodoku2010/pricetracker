from django.shortcuts import render, HttpResponseRedirect
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from .forms import AddNewItemForm
from .models import Item


def tracker_view(request):
    items = Item.objects.order_by('-id')
    form = AddNewItemForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            url = form.cleaned_data.get('url')
            requested_price = form.cleaned_data.get('requested_price')
            # crawling data
            crawled_data = crawl_data(url)
            # creating object in database
            Item.objects.create(
                url=url,
                title = crawled_data['title'],
                requested_price = requested_price,
                last_price = crawled_data['last_price'],
                discount_price = "No Discount Yet",
            )
            return HttpResponseRedirect('')
        else:
            form = AddNewItemForm()
    context = {
        'items': items,
        'form': form
    }
    return render(request, 'tracker.html', context)


def crawl_data(url):
    # User Agent is to prevent 403 Forbiddent Error
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bs = BeautifulSoup(html, 'html.parser')

    title = bs.find('h1', id='itemTitle').get_text().replace('Details about', '')
    price = bs.find('span', id='mm-saleDscPrc').get_text()
    clean_price = float(price.strip().replace('US', '').replace('$', '').replace(',', '.'))
    return {'title': title, 'last_price': clean_price}
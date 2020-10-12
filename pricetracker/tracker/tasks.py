import time
from celery import shared_task
from .models import Item
from .views import crawl_data

@shared_task
# do something heavy
def track_for_dicsount():
    items = Item.objects.all()
    for item in items:
        # crawl item url
        data = crawl_data(item.url)
        # check for discount
        if data['last_price'] < item.requested_price:
            print(f'Discount for {data["title"]}')
            item_discount = Item.objects.get(id=item.id)
            item_discount.discount_price = f'DISCOUNT! The price is {data["last_price"]}'
            item_discount.save() 

def track_for_not_discount():
    items = Item.objects.all()
    for item in items:
        data = crawl_data(item.url)
        if data["last_price"] > item.requested_price:
            print(f'Discount finished for {data["title"]}')
            item_discount_finished = Item.objects.get(id=item.id)
            item_discount_finished.discount_price = 'No Discount Yet'
            item_discount_finished.save()

while True:
    track_for_dicsount()
    time.sleep(15)
    track_for_not_discount()
    time.sleep(15)
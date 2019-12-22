import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models

# Create your views here.
BASE_CRAIGSLIST_URL = 'https://venice.craigslist.org/search/sss?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, template_name='base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'}) # find all <li> tags where class is result-row
    
    final_posting = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href') # find tag <a> and get url adress from it
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image = post.find(class_='result-image').get('data-ids').split(',')[0]
            post_image_url = BASE_IMAGE_URL.format(post_image[2:])
        else:
            post_image_url = 'https://www.ancienthouse.co.uk/content/2018/07/plain-white-background-300x200.jpg'
     
        final_posting.append((post_title, post_url, post_price, post_image_url))


    stuff_for_frontend = {
        'search': search,
        'final_posting': final_posting,
    }
    return render(request, template_name='my_app/new_search.html', context=stuff_for_frontend)
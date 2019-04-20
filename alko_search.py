# -*- coding: utf-8 -*-

'''
Alko Search Tool 0.2
Made by Matheos Mattsson 2018

PYTHON 3 ONLY

Requirements:
- BeautifulSoup4
- requests
- lxml

Feel free to reuse in any way shape or form you may want!
'''

import requests
from bs4 import BeautifulSoup
from textwrap import wrap

client = requests.session()

# defaults
get_url = 'https://www.alko.fi/tuotteet?SearchTerm='
sorting = 'name-asc'  # By name, ascending
SEARCH_URL_DEFAULT = "https://www.alko.fi/INTERSHOP/web/WFS/Alko-OnlineShop-Site/fi_FI/-/EUR/ViewParametricSearch-" \
                     "ProductPagingRandom?Context=ViewParametricSearch-ProductPagingRandom"


def set_sorting(option):
    global sorting
    if option == '1':
        sorting = 'name-asc'
        return True
    elif option == '2':
        sorting = 'name-desc'
        return True
    elif option == '3':
        sorting = 'priceWithPant-asc'
        return True
    elif option == '4':
        sorting = 'priceWithPant-desc'
        return True
    return False


def get_result_as_array(uri, search_term, nr_of_pages):
    result_string = ""
    product_no = 1
    for nr in range(nr_of_pages):
        url = uri + '&PageNumber=' + str(nr)
        page = client.get(url)
        parsed = BeautifulSoup(page.content, 'lxml')
        products_html_list = parsed.findAll('div', attrs={'role': 'listitem'})
        result_string += ("{n}**************Search term: '" + search_term + "' Page number: " +
                          str(nr + 1) + "/" + str(nr_of_pages) + "**************{n}{n}")
        for p in products_html_list:
            result_string += str(product_no) + ". "
            product_name = p.find('h4', attrs={'class': 'product-name-aria'})
            if product_name is not None:
                result_string += str(product_name.text.strip()) + " "
            product_volume = p.find('div', attrs={'class': 'mc-volume'})
            if product_volume is not None:
                result_string += str(product_volume.text.strip()) + "  "
            product_price = p.find('span', attrs={'itemprop': 'price'})
            if product_price is not None:
                result_string += str(product_price.get('content')) + " €{n}"

            result_string += "-------------------------------------------------------------{n}"
            product_no += 1

    return wrap(result_string, 1999)


def search(search_term):
    url = get_url + search_term
    page = client.get(url)
    parsed = BeautifulSoup(page.content, 'lxml')
    # search_url = str(parsed.find('form', attrs={'name': 'paginating'}).get('action'))
    search_url = SEARCH_URL_DEFAULT
    search_parameter = str(parsed.find('input', attrs={'name': 'SearchParameter'}).get('value'))
    nr_of_pages = int(
        int(parsed.find('span', attrs={'class': 'color-primary'}).text.strip()) / 12) + 1  # Paging starts at 0
    search_url += '&SearchTerm=' + search_term + '&PageSize=12&SearchParameter=' + search_parameter + \
                  '&SortingAttribute=' + sorting
    return get_result_as_array(search_url, search_term, nr_of_pages)


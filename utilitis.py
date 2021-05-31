import sys

from bs4 import BeautifulSoup
import urllib.request as request
import re
from datetime import date
import os
import urllib.error




brandP = '/'
modelP = '/'
fromYearP = '/od-'
fromPriceP = '&search%5Bfilter_float_price%3Afrom%5D='
toPriceP = '&search%5Bfilter_float_price%3Ato%5D='
toYearP = '&search%5Bfilter_float_year%3Ato%5D='
mileageFromP = '&search%5Bfilter_float_mileage%3Afrom%5D='
mileageToP = '&search%5Bfilter_float_mileage%3Ato%5D='
fuelTypeP = '&search%5Bfilter_enum_fuel_type%5D%5B0%5D='
pageNumberP = '&page='



# confgFile = 'X:\ProgramFiles\JetBrains\PycharmProjects\projektTest\confg.txt'





def getOffersLinks(link):
    try:
        response = request.urlopen(link)
        sourceCode = response.read()
    except urllib.error.URLError as urle:
        print(urle, file=sys.stderr)
    else:
        soup = BeautifulSoup(sourceCode, 'html.parser')
        allOffersFound = soup.find_all(attrs={'class': 'offer-title__link'})

        offersLinks = []
        pattern = re.compile('"https://www.otomoto.pl/.*?"')

        for offer in allOffersFound:
            offersLinks.append(re.findall(pattern, str(offer)))

        return [item[1:-1] for tab in offersLinks for item in tab]


def createLink(brand, model, yearFrom, priceFrom, priceTo, yearTo, mileageFrom, mileageTo, fuelType):

    brand = '-'.join(brand.split()).lower()
    model = '-'.join(model.split()).lower()
    yearFrom = ''.join(yearFrom.split())
    priceFrom = ''.join(priceFrom.split())
    priceTo= ''.join(priceTo.split())
    yearTo = ''.join(yearTo.split())
    mileageFrom = ''.join(mileageFrom.split())
    mileageTo = ''.join(mileageTo.split())

    link = ''
    if brand != '':
        link += brand + '/'

    if model != '':
        link += model + '/'

    if yearFrom == '':
        link += '?'
    elif yearFrom.isdigit() and (yearTo.isdigit() and int(yearFrom) <=int(yearTo) <= date.today().year or yearTo == ''):
        link += f'od-{yearFrom}/?'

    if priceFrom.isdigit() and (priceTo.isdigit() and int(priceFrom) <= int(priceTo) or priceTo == ''):
        link += fromPriceP + priceFrom

    if priceTo.isdigit() and (priceFrom.isdigit() and int(priceFrom) <= int(priceTo) or priceFrom == ''):
        link += toPriceP + priceTo

    if yearTo.isdigit() and (yearFrom.isdigit() and int(yearFrom) <= int(yearTo) <= date.today().year or yearFrom == ''):
        link += toYearP + yearTo

    if mileageFrom.isdigit() and (mileageTo.isdigit() and int(mileageFrom) <= int(mileageTo) or mileageTo == ''):
        link += mileageFromP + mileageFrom

    if mileageTo.isdigit() and (mileageFrom.isdigit() and int(mileageFrom) <= int(mileageTo) or mileageFrom == ''):
        link += mileageToP + mileageTo

    if fuelType != '' and fuelType != 'all':
        link += fuelTypeP + fuelType
    return link


def checkIfExists(link, allow_redirect=False):
    if link == '':
        return False
    try:
        req = request.urlopen(link)
        if allow_redirect:
            return True
        else:
            return req.geturl() == link
    except urllib.error.URLError:
        return False

def countChars(string, finalChar, acc):
    if string[-1] == finalChar:
        return acc
    else:
        return countChars(string[:-1], finalChar, acc + 1)

def nextPage(link, previousPage=False):


    if not previousPage:
        if re.match('.*&page=\d+', link) is None:
            link += '&page=2'
        else:
            numbers = countChars(link, '=', 0)
            pageNumber = int(link[-numbers:]) + 1
            link = link[:-numbers] + str(pageNumber)
        return link
    else:
        if re.match('.*&page=\d+', link) is None:
            return ''
        else:
            numbers = countChars(link, '=', 0)
            pageNumber = int(link[-numbers:]) - 1
            return link[:-numbers] + str(pageNumber)



def getFavoriteLinks():
    favLinks = []
    with open(os.getcwd() + '\\Projekt\\favorite.txt', 'r') as file:
        for line in file:
            favLinks.append(line[:-1])

    return favLinks


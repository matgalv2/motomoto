import sys
import urllib.error
from bs4 import BeautifulSoup
import urllib.request as request
import re
import os
import shutil


class Offer:
    # __path = 'X:\\Dokumenty\\PWr\\Projekt'
    __path = os.getcwd() + '\\Projekt'
    __id = 0

    def __init__(self, link):
        self.__link = link
        self.__specification = {}
        self.__folderPath = ''
        self.id = self.__id
        Offer.__id += 1
        self.shortenedSpec = {}
        self.imagesNumber = 0


    def getData(self):
        self.prepareSpecification()
        self.prepareReprImage()
        self.shortenedSpec = self.getOffersInformations()


    def prepareImages(self):
        try:
            self.downloadImages(self.getLinksToImages())
        except urllib.error.URLError:
            pass


    def removeImages(self):
        for i in range(self.imagesNumber):
            try:
                os.remove(self.__folderPath + f'\\{i+1}')
            except FileNotFoundError:
                pass
        self.imagesNumber = 0


    @property
    def path(self):
        return Offer.__path

    @path.setter
    def path(self, newPath):
        Offer.__path = newPath


    @property
    def specification(self):
        return self.__specification


    @property
    def folderPath(self):
        return self.__folderPath


    @property
    def link(self):
        return self.__link


    def isEmpty(self):
        return self.__link == 'empty'


    def prepareEmpty(self):
        if not self.isEmpty():
            return
        else:
            self.__folderPath = Offer.__path + '\\Empty'

    # 10 last elements of every link is unique code, so to compare 2 links we have to get [:-10]
    # [:-11] beacues of the '\n' at the end of the line
    def checkIfFavorite(self):
        with open(Offer.__path + '\\favorite.txt', 'r') as file:
            for line in file:
                if line[:-11] == self.__link[:-10]:
                    return True
        return False


    def addToFavorite(self):
        if not self.checkIfFavorite():
            with open(Offer.__path + '\\favorite.txt', 'a') as file:
                file.write(self.__link + '\n')


    def removeFromFavorite(self):
        file = open(Offer.__path + '\\favorite.txt', 'r')
        lines = file.readlines()
        file.close()
        with open(Offer.__path + '\\favorite.txt', 'w') as file:
            for line in lines:
                if line[:-11] != self.__link[:-10]:
                    file.write(line)


    def updateSpecification(self, specification):
        for param in specification:
            self.__specification[param[0]] = param[1]


    def downloadRepresentativeImage(self, links):
        if links:
            try:
                request.urlretrieve(links[0], f'{self.__folderPath}\\{0}.jpg')
            # except (ValueError, urllib.error.URLError):
            except urllib.error.URLError:
                pass
                # print(file=sys.stderr)

        else:
            try:
                shutil.copyfile(self.__path + '\\0.jpg', self.__folderPath + '\\0.jpg')
            except FileNotFoundError:
                pass


    def getOffersInformations(self):
        shortenedSpec = {}
        names = ('Marka pojazdu', 'Model pojazdu', 'Rok produkcji', 'Przebieg',
                 'Moc', 'Typ', 'Kolor', 'Wersja', 'Rodzaj paliwa', 'Skrzynia biegów', 'Napęd', 'Cena', 'Stan', 'Pojemność skokowa')

        for label in names:
            if label in self.specification:
                shortenedSpec[label] = self.specification[label]
            elif label == 'Pojemność skokowa':
                shortenedSpec[label] = ''
            else:
                shortenedSpec[label] = 'Brak informacji'
        return shortenedSpec


    def downloadImages(self, links):
        self.imagesNumber = len(links)
        links = links[1:]
        for i in range(len(links)):
            try:
                request.urlretrieve(links[i], f'{self.__folderPath}\\{i+1}.jpg')
            except urllib.error.URLError as urle:
                print(urle, file=sys.stderr)



    def makeFolder(self):
        try:
            self.__folderPath = f'{Offer.__path}\\{self.id}'
            os.mkdir(self.__folderPath)
        except FileNotFoundError:
            pass


    def removeFolder(self):
        try:
            shutil.rmtree(self.__folderPath, ignore_errors=True)
            self.__folderPath = ''
        except FileNotFoundError:
            pass


    def getLinksToImages(self):
        try:
            response = request.urlopen(self.__link)
            sourceCode = response.read()
        except urllib.error.URLError as urle:
            print(urle, file=sys.stderr)
        else:
            soup = BeautifulSoup(sourceCode, 'html.parser')
            allOffersFound = soup.find_all(attrs={'class': 'photo-item'})

            photosLinks = []

            pattern = re.compile('"https://.*?"')

            for offer in allOffersFound:
                photosLinks.append(re.findall(pattern, str(offer)))

            links = [item[1:-1] for tab in photosLinks for item in tab]
            return links


    def getSpecification(self):
        try:
            response = request.urlopen(self.__link)
            sourceCode = response.read()
        except urllib.error.HTTPError as urle:
            print(urle, file=sys.stderr)
        else:
            soup = BeautifulSoup(sourceCode, 'html.parser')
            allOffersFound = soup.find_all(attrs={'class': 'offer-params__item'})

            labelPattern = re.compile('>.*</span>')
            valuePattern = re.compile('>\n.*?</a>|>\n.*?</div>')


            labelValue = []

            for offer in allOffersFound:

                label = re.findall(labelPattern, str(offer))
                value = re.findall(valuePattern, str(offer))

                if label and value:
                    value = value[0].split()
                    value.pop(-1)
                    value.pop(0)
                    fullValue = ' '.join(value)
                    labelValue.append((label[0][1:-7], fullValue))

            return labelValue


    def getPrice(self):
        try:
            response = request.urlopen(self.__link)
            sourceCode = response.read()
        except urllib.error.HTTPError as urle:
            print(urle, file=sys.stderr)
        else:
            soup = BeautifulSoup(sourceCode, 'html.parser')
            # priceClass = soup.find_all(attrs={'class': 'offer-price'})
            priceClass = soup.find_all(attrs={'class': 'price-wrapper'})
            if priceClass:
                price = re.findall('data-price="\d+?.*?"', str(priceClass[0]))
                return price[0][12:-1] + ' zł'
            else:
                return 'Nieznana'


    def prepareSpecification(self):
        self.updateSpecification(self.getSpecification())
        self.__specification['Cena'] = self.getPrice()


    def prepareReprImage(self):
        self.makeFolder()
        self.downloadRepresentativeImage(self.getLinksToImages())


    def __del__(self):
        if not self.isEmpty():
            self.removeFolder()
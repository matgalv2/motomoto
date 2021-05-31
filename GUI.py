import os
import time
import tkinter.filedialog
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from utilitis import *
from Offer import *
import pyperclip

DEFAULT_LINK = 'https://www.otomoto.pl/osobowe/'
link = ''
chosenType = ''

starAscii = u"\u2605"

emptyOffer: Offer = Offer('empty')
emptyOffer.specification['Cena'] = 'Cena'
emptyOffer.specification['Marka'] = 'Marka'
emptyOffer.specification['Model'] = 'Model'

currentOffer: Offer = emptyOffer
carToCompare1 = emptyOffer
carToCompare2 = emptyOffer

offers = []
offersLinks = []

# confgFile = 'X:\ProgramFiles\JetBrains\PycharmProjects\projektTest\confg.txt'




class MainWindow(Tk):

    __frames = {}

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.container = Frame(self)

        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.title('MotoMoto')

        self.geometry('1280x720')
        self.resizable(height=False, width=False)


        for F in (StartPage, ParametersPage):
            self.addPage(F)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.__frames[cont]
        frame.tkraise()

    @property
    def frames(self):
        return self.__frames

    def addPage(self, Page, *args):
        if Page == BrowsingPage:
            frame = Page(self.container, self, args[0])
        else:
            frame = Page(self.container, self)
        self.__frames[Page] = frame
        frame.grid(row=0, column=0, sticky='nsew')

    def removePage(self, Page):
        if Page in self.__frames:
            self.__frames.pop(Page)


class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        image = Image.open(os.getcwd() + '\\Projekt\logo.png')
        image1 = ImageTk.PhotoImage(image)

        label1 = Label(self, image=image1)
        label1.image = image1
        label1.place(x=0, y=0, relwidth=1, relheight=1)

        button = ttk.Button(self, text="Szukaj pojazdów", command=lambda: controller.show_frame(ParametersPage))
        button.pack(side='left', pady=300)


        button2 = ttk.Button(self, text="Porównaj", command=lambda: compareVehicles())
        button2.pack(side='right', pady=300)

        button3 = ttk.Button(self, text="Wyjście", command=controller.destroy)
        button3.pack(side='bottom')

        favoriteButton = ttk.Button(self, text='Ulubione',command=lambda: browseFavorite())
        favoriteButton.pack(side='top')

        infoLabel = Label(self, text='', bg='white')
        infoLabel.place(x=570,y=280)

        def browseFavorite():

            global offersLinks, offers, currentOffer
            offersLinks = getFavoriteLinks()
            for offerLink in offersLinks:
                offer = Offer(offerLink)
                offer.getData()
                offers.append(offer)

            if offers:
                currentOffer = offers[0]
                controller.removePage(BrowsingPage)
                controller.addPage(BrowsingPage, True)
                controller.show_frame(BrowsingPage)
            else:
                infoLabel.configure(text='Brak ulubionych')
                controller.after(2000, lambda: infoLabel.configure(text=''))

        def compareVehicles():
            if not carToCompare1.isEmpty() and not carToCompare2.isEmpty():
                controller.addPage(ComparePage)
                controller.show_frame(ComparePage)
            else:
                infoLabel.configure(text='Brak samochodów do porównania')
                controller.after(2000,lambda: infoLabel.configure(text=''))


#
# def changeFolder():
#     path = tkinter.filedialog.askdirectory(initialdir=getFolder(), title="Select a directory")
#     if path != '':
#         with open(confgFile, 'w') as file:
#             file.write(path)
#
#
# def getFolder():
#     with open(confgFile, 'r') as file:
#         return str(file.read())
#

class ParametersPage(Frame):
    fuelNames = ('Benzyna', 'Diesel', 'Elektryczny', 'Hybryda', 'Benzyna+LPG', 'Wszystkie')

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)


        def backButton():
            global link, DEFAULT_LINK
            link = DEFAULT_LINK
            controller.show_frame(StartPage)

        button1 = ttk.Button(self, text="Powrót", command=backButton)
        button1.pack(side='bottom')

        Label(self, text='Marka').place(x=400, y=300)
        brandE = Entry(self)
        brandE.place(x=480, y=300)

        Label(self, text='Model').place(x=400, y=330)
        modelE = Entry(self)
        modelE.place(x=480, y=330)

        Label(self, text='Od roku').place(x=400, y=360)
        fromYearE = Entry(self)
        fromYearE.place(x=480, y=360)

        Label(self, text='Do roku').place(x=400, y=390)
        toYearE = Entry(self)
        toYearE.place(x=480, y=390)

        Label(self, text='Cena od').place(x=400, y=420)
        fromPriceE = Entry(self)
        fromPriceE.place(x=480, y=420)

        Label(self, text='Cena do').place(x=400, y=450)
        toPriceE = Entry(self)
        toPriceE.place(x=480, y=450)

        Label(self, text='Przebieg od').place(x=400, y=480)
        fromMileageE = Entry(self)
        fromMileageE.place(x=480, y=480)

        Label(self, text='Przebieg do').place(x=400, y=510)
        toMileageE = Entry(self)
        toMileageE.place(x=480, y=510)

        Label(self, text='Rodzaj paliwa').place(x=700, y=300)


        fuelTypeL = Listbox(self)
        fuelTypeL.place(x=700, y=330, height=100, width=80)

        for i in range(len(ParametersPage.fuelNames)):
            fuelTypeL.insert(i, ParametersPage.fuelNames[i])

        search = ttk.Button(self, text='Wyszukaj',
                        command=lambda: searchF(brandE.get(), modelE.get(), fromYearE.get(), fromPriceE.get(),
                                                     toPriceE.get(), toYearE.get(), fromMileageE.get(),
                                                     toMileageE.get(), fuelTypeL.get(ANCHOR)))


        search.place(x=700, y=500)


        txt = ''
        informationLabel = Label(self, text=txt)
        informationLabel.place(x=580, y=180)

        def searchF(brand, model, yearFrom, priceFrom, priceTo, yearTo, mileageFrom, mileageTo, fuelType):
            informationLabel.configure(text='Trwa wyszukiwanie ofert.')
            searchButton(brand, model, yearFrom, priceFrom, priceTo, yearTo, mileageFrom, mileageTo, fuelType)



        def searchButton(brand, model, yearFrom, priceFrom, priceTo, yearTo, mileageFrom, mileageTo, fuelType):
            global link, offers, offersLinks, currentOffer

            fuelTypes = {'Benzyna': 'petrol', 'Diesel': 'diesel', 'Elektryczny': 'electric', 'Hybryda': 'hybrid',
                         'Benzyna+LPG': 'petrol-lpg', 'Wszystkie': 'all'}


            controller.removePage(BrowsingPage)

            informationLabel.configure(text='Trwa wyszukiwanie ofert.')

            if not currentOffer.isEmpty():
                controller.addPage(BrowsingPage, False)
                controller.show_frame(BrowsingPage)
            fuelType = fuelTypes[fuelType] if fuelType != '' else ''

            link = DEFAULT_LINK + createLink(brand, model, yearFrom, priceFrom, priceTo, yearTo, mileageFrom, mileageTo, fuelType)


            for entry in (brandE, modelE, fromYearE, fromPriceE, toPriceE, toYearE, fromMileageE, toMileageE):
                entry.delete(0, END)

            offersLinks = getOffersLinks(link)


            if not offersLinks:
                informationLabel.configure(text='Nie znaleziono żadnych ofert.')
                link = DEFAULT_LINK
                controller.after(4000,lambda: informationLabel.configure(text=''))
                return



            currentOffer = emptyOffer

            for offerLink in offersLinks:
                offer = Offer(offerLink)
                offer.getData()
                offers.append(offer)


            currentOffer = offers[0]

            controller.removePage(BrowsingPage)
            controller.addPage(BrowsingPage, False)
            informationLabel.configure(text='')
            controller.show_frame(BrowsingPage)


def updateOffers(newLink):
    global offers, offersLinks, link, currentOffer
    offersLinks = getOffersLinks(newLink)
    offers = []
    for offerLink in offersLinks:
        offer = Offer(offerLink)
        offer.getData()
        offers.append(offer)

class BrowsingPage(Frame):
    img = None

    def __init__(self, parent, controller, favorite):
        Frame.__init__(self, parent)

        buttonBack = ttk.Button(self, text="Powrót", command=lambda: back_and_clear_params())
        buttonBack.pack(side='bottom')

        buttonNext = ttk.Button(self, text='Następna', command=lambda: nextButtonComm())
        buttonNext.pack(side='right')

        def nextButtonComm():
            global currentOffer, offers
            if not favorite:
                getNextOffer(info)
            else:
                currentOffer = offers[(offers.index(currentOffer)+1) % len(offers)]
            updateInfo()


        buttonPrevious = ttk.Button(self, text='Poprzednia', command=lambda: previousButtonComm())
        buttonPrevious.pack(side='left')


        def previousButtonComm():
            global currentOffer, offers
            if not favorite:
                getPreviousOffer(info)
            else:
                currentOffer = offers[(offers.index(currentOffer) + len(offers) - 1) % len(offers)]
            updateInfo()


        def updateInfo():
            image = loadImage(currentOffer.folderPath + '\\0.jpg')
            BrowsingPage.img = image
            vehicleImage.configure(image=image)

            vehiclePrice.configure(text='Cena: ' + currentOffer.shortenedSpec['Cena'])
            vehicleBrand.configure(text='Marka: ' + currentOffer.shortenedSpec['Marka pojazdu'])
            vehicleModel.configure(text='Model: ' + currentOffer.shortenedSpec['Model pojazdu'])
            vehicleMileage.configure(text='Przebieg: ' + currentOffer.shortenedSpec['Przebieg'])

        # def updateOffers(newLink):
        #     global offers, offersLinks, link, currentOffer
        #     offersLinks = getOffersLinks(newLink)
        #     offers = []
        #     for offerLink in offersLinks:
        #         offer = Offer(offerLink)
        #         offer.getData()
        #         offers.append(offer)

        def getNextOffer(labelWarning: Label):
            global currentOffer, offers, link
            if currentOffer.isEmpty() or currentOffer not in offers:
                currentOffer = offers[0]
            elif offers.index(currentOffer) < len(offers) - 1:
                currentOffer = offers[offers.index(currentOffer) + 1]
            else:
                if checkIfExists(nextPage(link)):
                    link = nextPage(link)
                    currentOffer = emptyOffer
                    updateOffers(link)

                    currentOffer = offers[0]


                else:
                    labelWarning.configure(text="Brak kolejnej ofery.")
                    controller.after(2500, lambda: labelWarning.configure(text=''))

        def getPreviousOffer(labelWarning: Label):
            global currentOffer, offers, link
            if currentOffer.isEmpty() or currentOffer not in offers:
                currentOffer = offers[len(offers) - 1]
            elif offers.index(currentOffer) > 0:
                currentOffer = offers[offers.index(currentOffer) - 1]
            else:
                if checkIfExists(nextPage(link, previousPage=True), allow_redirect=True):
                    link = nextPage(link, previousPage=True)
                    currentOffer = emptyOffer
                    updateOffers(link)

                    currentOffer = offers[len(offers) - 1]

                else:
                    labelWarning.configure(text="Brak wcześniejszej ofery.")
                    controller.after(2500, lambda: labelWarning.configure(text=''))

        buttonOffer = ttk.Button(self, text="Szczegóły", command=lambda: detailsButton())
        buttonOffer.pack(side='top')

        vehicleImage = Label(self)


        # self.img = loadImage("X:\\Dokumenty\\PWr\\Projekt\\Empty\\0.jpg")
        self.img = loadImage(os.getcwd() + "\\Projekt\\Empty\\0.jpg")
        vehicleImage.configure(image=self.img)

        # showImage(self.img, vehicleImage)

        vehicleImage.place(x=440, y=180)


        vehiclePrice = Label(self, text='Cena')
        vehiclePrice.place(x=590, y=500)

        vehicleBrand = Label(self, text='Marka')
        vehicleBrand.place(x=590, y=520)

        vehicleModel = Label(self, text='Model')
        vehicleModel.place(x=590, y=540)

        vehicleMileage = Label(self, text='Przebieg')
        vehicleMileage.place(x=590, y=560)

        info = Label(self, text='')
        info.pack(side='top')

        updateInfo()



        def back_and_clear_params():

            global link, DEFAULT_LINK, chosenType, offers, currentOffer, emptyOffer
            link = DEFAULT_LINK + chosenType + '/'
            offers = []
            currentOffer = emptyOffer
            if favorite:
                controller.show_frame(StartPage)
            else:
                controller.show_frame(ParametersPage)

        def detailsButton():
            controller.removePage(OfferPage)
            if not currentOffer.isEmpty():
                currentOffer.prepareImages()
                controller.addPage(OfferPage)
                controller.show_frame(OfferPage)




class OfferPage(Frame):
    img = None
    currentImageIndex = 0

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)



        backButton = ttk.Button(self, text="Powrót", command=lambda: backAndRemImgsButton())
        backButton.pack(side='bottom')

        def backAndRemImgsButton():
            currentOffer.removeImages()
            controller.show_frame(BrowsingPage)

        favoriteAddButton = ttk.Button(self, text="Dodaj do ulubionych", command=lambda: addToFavButton())
        favoriteAddButton.place(x=490)

        favoriteRemButton = ttk.Button(self, text="Usuń z ulubionych", command=lambda:remFromFavButton())
        # favoriteRemButton.pack()
        favoriteRemButton.place(x=640)

        favoriteLabel = ttk.Label(self,text=starAscii if currentOffer.checkIfFavorite() else '', font=('Arial',32))
        favoriteLabel.place(x=605, y=80)

        copyLinkButton = ttk.Button(self, text='Skopiuj link', command=pyperclip.copy(currentOffer.link))
        copyLinkButton.place(x=1000, y=550)

        addToCompareButton=ttk.Button(self, text='Dodaj do porównania', command=lambda:addToCompare())
        addToCompareButton.place(x=170, y=550)

        compareLabel = Label(self,text='')
        compareLabel.place(x=170, y=530)

        def addToCompare():
            global currentOffer, carToCompare1, carToCompare2

            if currentOffer == carToCompare1 or currentOffer == carToCompare2:
                compareLabel.configure(text='Samochód już jest dodany do porównania.')
                controller.after(3000, lambda: compareLabel.configure(text=''))
                return

            if carToCompare1.isEmpty():
                carToCompare1= offers[offers.index(currentOffer)]
            elif carToCompare2.isEmpty():
                carToCompare2 = offers[offers.index(currentOffer)]
            else:
                carToCompare1 = carToCompare2
                carToCompare2 = currentOffer

            compareLabel.configure(text='Dodano do porównania.')
            controller.after(2000, lambda: compareLabel.configure(text=''))



        def addToFavButton():
            currentOffer.addToFavorite()
            favoriteLabel.configure(text=starAscii)

        def remFromFavButton():
            currentOffer.removeFromFavorite()
            favoriteLabel.configure(text='')



        imgLabel = Label(self)
        self.img = loadImage(currentOffer.folderPath+ '\\0.jpg')
        imgLabel.configure(image=self.img)

        imgLabel.place(x=440, y=180)

        priceLabel = Label(self, text='Cena: ' + currentOffer.shortenedSpec['Cena'])
        priceLabel.place(x=470,y=500)

        brandLabel = Label(self, text='Marka: ' + currentOffer.shortenedSpec['Marka pojazdu'])
        brandLabel.place(x=470,y=520)

        modelLabel = Label(self, text='Model: ' + currentOffer.shortenedSpec['Model pojazdu'])
        modelLabel.place(x=470,y=540)

        yearLabel = Label(self, text='Rok produkcji: ' + currentOffer.shortenedSpec['Rok produkcji'])
        yearLabel.place(x=470,y=560)

        mileageLabel = Label(self, text='Przebieg: ' + currentOffer.shortenedSpec['Przebieg'])
        mileageLabel.place(x=470,y=580)

        powerLabel = Label(self, text='Moc: ' + currentOffer.shortenedSpec['Moc'])
        powerLabel.place(x=470,y=600)

        typeLabel = Label(self, text='Typ: ' + currentOffer.shortenedSpec['Typ'])
        typeLabel.place(x=470,y=620)

        versionLabel = Label(self, text='Wersja: ' + currentOffer.shortenedSpec['Wersja'])
        versionLabel.place(x=650, y=500)

        fuelLabel = Label(self, text='Rodzaj paliwa: ' + currentOffer.shortenedSpec['Rodzaj paliwa'])
        fuelLabel.place(x=650, y=520)


        capacityLabel = Label(self, text='Pojemność skokowa: ' + currentOffer.shortenedSpec['Pojemność skokowa'])

        y = 0
        if currentOffer.shortenedSpec['Pojemność skokowa'] != '':
            capacityLabel.place(x=650, y=540)
            y = 20



        gearboxLabel = Label(self, text='Skrzynia biegów: ' + currentOffer.shortenedSpec['Skrzynia biegów'])
        gearboxLabel.place(x=650, y=540 + y)

        driveLabel = Label(self, text='Napęd: ' + currentOffer.shortenedSpec['Napęd'])
        driveLabel.place(x=650, y=560 + y)

        colorLabel = Label(self, text='Kolor: ' + currentOffer.shortenedSpec['Kolor'])
        colorLabel.place(x=650, y=580 + y)

        stateLabel = Label(self, text='Stan: ' + currentOffer.shortenedSpec['Stan'])
        stateLabel.place(x=650, y=600 + y)

        nextPhotoButton = ttk.Button(self, text='Następne zdjęcie', command=lambda: nextPhoto())
        nextPhotoButton.place(x=875, y=300)

        previousPhotoButton = ttk.Button(self, text='Poprzednie zdjęcie', command=lambda: previousPhoto())
        previousPhotoButton.place(x=300, y=300)

        def nextPhoto():
            self.currentImageIndex = (self.currentImageIndex + 1) % currentOffer.imagesNumber
            self.img = loadImage(currentOffer.folderPath + f'\\{self.currentImageIndex}.jpg')
            imgLabel.configure(image=self.img)

        def previousPhoto():
            self.currentImageIndex = (self.currentImageIndex + currentOffer.imagesNumber - 1) % currentOffer.imagesNumber
            self.img = loadImage(currentOffer.folderPath + f'\\{self.currentImageIndex}.jpg')
            imgLabel.configure(image=self.img)

class ComparePage(Frame):

    img1 = None
    img2 = None

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        def addToFavButton(offer,label):
            offer.addToFavorite()
            label.configure(text=starAscii)

        def remFromFavButton(offer,label):
            offer.removeFromFavorite()
            label.configure(text='')

        favorite1AddButton = ttk.Button(self, text="Dodaj do ulubionych", command=lambda: addToFavButton(carToCompare1, favorite1Label))
        favorite1AddButton.place(x=220)

        favorite1RemButton = ttk.Button(self, text="Usuń z ulubionych", command=lambda: remFromFavButton(carToCompare1, favorite1Label))
        favorite1RemButton.place(x=370)

        favorite1Label = ttk.Label(self, text=starAscii if carToCompare1.checkIfFavorite() else '', font=('Arial', 32))
        favorite1Label.place(x=335, y=80)

        img1Label = Label(self)
        self.img1 = loadImage(carToCompare1.folderPath + '\\0.jpg')
        img1Label.configure(image=self.img1)



        img1Label.place(x=150, y=180)

        price1Label = Label(self, text='Cena: ' + carToCompare1.shortenedSpec['Cena'])
        price1Label.place(x=170, y=500)

        brand1Label = Label(self, text='Marka: ' + carToCompare1.shortenedSpec['Marka pojazdu'])
        brand1Label.place(x=170, y=520)

        model1Label = Label(self, text='Model: ' + carToCompare1.shortenedSpec['Model pojazdu'])
        model1Label.place(x=170, y=540)

        year1Label = Label(self, text='Rok produkcji: ' + carToCompare1.shortenedSpec['Rok produkcji'])
        year1Label.place(x=170, y=560)

        mileage1Label = Label(self, text='Przebieg: ' + carToCompare1.shortenedSpec['Przebieg'])
        mileage1Label.place(x=170, y=580)

        power1Label = Label(self, text='Moc: ' + carToCompare1.shortenedSpec['Moc'])
        power1Label.place(x=170, y=600)

        type1Label = Label(self, text='Typ: ' + carToCompare1.shortenedSpec['Typ'])
        type1Label.place(x=170, y=620)

        version1Label = Label(self, text='Wersja: ' + carToCompare1.shortenedSpec['Wersja'])
        version1Label.place(x=330, y=500)

        fuel1Label = Label(self, text='Rodzaj paliwa: ' + carToCompare1.shortenedSpec['Rodzaj paliwa'])
        fuel1Label.place(x=330, y=520)

        capacity1Label = Label(self, text='Pojemność skokowa: ' + carToCompare1.shortenedSpec['Pojemność skokowa'])

        y1 = 0
        if carToCompare1.shortenedSpec['Pojemność skokowa'] != '':
            capacity1Label.place(x=330, y=540)
            y1 = 20

        gearbox1Label = Label(self, text='Skrzynia biegów: ' + carToCompare1.shortenedSpec['Skrzynia biegów'])
        gearbox1Label.place(x=330, y=540 + y1)

        drive1Label = Label(self, text='Napęd: ' + carToCompare1.shortenedSpec['Napęd'])
        drive1Label.place(x=330, y=560 + y1)

        color1Label = Label(self, text='Kolor: ' + carToCompare1.shortenedSpec['Kolor'])
        color1Label.place(x=330, y=580 + y1)

        state1Label = Label(self, text='Stan: ' + carToCompare1.shortenedSpec['Stan'])
        state1Label.place(x=330, y=600 + y1)

        #drugi pojazd

        favorite2AddButton = ttk.Button(self, text="Dodaj do ulubionych", command=lambda: addToFavButton(carToCompare2, favorite2Label))
        favorite2AddButton.place(x=780)

        favorite2RemButton = ttk.Button(self, text="Usuń z ulubionych", command=lambda: remFromFavButton(carToCompare2, favorite2Label))
        favorite2RemButton.place(x=930)

        favorite2Label = ttk.Label(self, text=starAscii if carToCompare2.checkIfFavorite() else '', font=('Arial', 32))
        favorite2Label.place(x=895, y=80)

        img2Label = Label(self)
        self.img2 = loadImage(carToCompare2.folderPath + '\\0.jpg')
        img2Label.configure(image=self.img2)

        img2Label.place(x=730, y=180)

        price2Label = Label(self, text='Cena: ' + carToCompare2.shortenedSpec['Cena'])
        price2Label.place(x=750, y=500)

        brand2Label = Label(self, text='Marka: ' + carToCompare2.shortenedSpec['Marka pojazdu'])
        brand2Label.place(x=750, y=520)

        model2Label = Label(self, text='Model: ' + carToCompare2.shortenedSpec['Model pojazdu'])
        model2Label.place(x=750, y=540)

        year2Label = Label(self, text='Rok produkcji: ' + carToCompare2.shortenedSpec['Rok produkcji'])
        year2Label.place(x=750, y=560)

        mileage2Label = Label(self, text='Przebieg: ' + carToCompare2.shortenedSpec['Przebieg'])
        mileage2Label.place(x=750, y=580)

        power2Label = Label(self, text='Moc: ' + carToCompare2.shortenedSpec['Moc'])
        power2Label.place(x=750, y=600)

        type2Label = Label(self, text='Typ: ' + carToCompare2.shortenedSpec['Typ'])
        type2Label.place(x=750, y=620)

        version2Label = Label(self, text='Wersja: ' + carToCompare2.shortenedSpec['Wersja'])
        version2Label.place(x=930, y=500)

        fuel2Label = Label(self, text='Rodzaj paliwa: ' + carToCompare2.shortenedSpec['Rodzaj paliwa'])
        fuel2Label.place(x=930, y=520)

        capacity2Label = Label(self, text='Pojemność skokowa: ' + carToCompare2.shortenedSpec['Pojemność skokowa'])

        y2 = 0
        if carToCompare2.shortenedSpec['Pojemność skokowa'] != '':
            capacity2Label.place(x=930, y=540)
            y2 = 20

        gearbox2Label = Label(self, text='Skrzynia biegów: ' + carToCompare2.shortenedSpec['Skrzynia biegów'])
        gearbox2Label.place(x=930, y=540 + y2)

        drive2Label = Label(self, text='Napęd: ' + carToCompare2.shortenedSpec['Napęd'])
        drive2Label.place(x=930, y=560 + y2)

        color2Label = Label(self, text='Kolor: ' + carToCompare2.shortenedSpec['Kolor'])
        color2Label.place(x=930, y=580 + y2)

        state2Label = Label(self, text='Stan: ' + carToCompare2.shortenedSpec['Stan'])
        state2Label.place(x=930, y=600 + y2)

        backButton = ttk.Button(self, text='Powrót', command=lambda:back_clear())
        backButton.pack(side='bottom')

        def back_clear():

            controller.show_frame(StartPage)
            controller.removePage(ComparePage)



def loadImage(path, dimensions=(400, 300)):
    image = Image.open(path)
    resized_image = image.resize(dimensions)
    img = ImageTk.PhotoImage(resized_image)
    return img



app = MainWindow()
app.mainloop()
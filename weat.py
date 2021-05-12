import requests
import datetime
import time
from bs4 import BeautifulSoup
from scipy.interpolate import interp1d
import numpy as np
import matplotlib
from numpy import array
import string
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import (Qt, pyqtSlot)
from PyQt5.QtWidgets import (QWidget, QMessageBox, QPushButton, QComboBox, QCheckBox, QRadioButton,  
    QVBoxLayout, QLabel, QGridLayout, QLineEdit, QApplication, QTableWidget,QTableWidgetItem)
import matplotlib.pyplot as plt
    
class Program(QWidget):
    #ustalanie zmiennych globalnych aby przekazywac informacje przez radiobuttony oraz checkboxy
    global godz, minut, fx0, fx1, fx2, fx3, fx4, fx5
    godz=minut=0    
    fx0=fx1=fx2=fx3=fx4=fx5= "not_checked"    
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.bs1="Dzisiaj"
        #wielkosc okna
        self.setGeometry(300,300,450,150)
        #tytul okna
        self.setWindowTitle('3 dniowa prognoza pogody PROJEKT MN')
        #definicja siatki
        siatka=QGridLayout()
        siatka.setSpacing(10)
        self.setLayout(siatka)
        #etykiety tekstowe
        self.label0=QLabel('Podaj miasto:')
        self.label1=QLabel('POGODA DLA 3 DNI')
        self.label3=QLabel('Wybierz dzień:')
        self.label4=QLabel('Wybierz czas:')
        self.label5=QLabel('                           Godz:')
        self.label6=QLabel('                           Min:')
        self.label7=QLabel('Wybierz wykres:') 
        self.label10=QLabel('Temperatura:')
        self.label11=QLabel('Temperatura odczuwalna:')
        self.label12=QLabel('Opady:')
        self.label13=QLabel('Ciśnienie:')
        self.label14=QLabel('Wilgotność:')
        self.label15=QLabel('Wiatr:')
        self.label20=QLabel('Pogoda dla: miasto z dnia: data')
        self.label21=QLabel('o godzinie: godz:min.')
        self.label_interp=QLabel('Wartości interpolowane:')
        #przycisk
        self.button1=QPushButton('Sprawdź pogodę')
        #pole tekstowe
        self.text1=QLineEdit()
        self.text10=QLineEdit()
        self.text11=QLineEdit()
        self.text12=QLineEdit()
        self.text13=QLineEdit()
        self.text14=QLineEdit()
        self.text15=QLineEdit()
        #riadobuttony
        self.radiobutton = QRadioButton("Dzisiaj")
        self.radiobutton.setChecked(True)
        self.radiobutton.co = "Dzisiaj"
        self.radiobutton.toggled.connect(self.btnstate1)
        siatka.addWidget(self.radiobutton, 3, 8)        
        self.radiobutton = QRadioButton("Jutro")
        self.radiobutton.co = "Jutro"
        self.radiobutton.toggled.connect(self.btnstate1)
        siatka.addWidget(self.radiobutton, 4, 8)        
        self.radiobutton = QRadioButton("Pojutrze")
        self.radiobutton.co = "Pojutrze"
        self.radiobutton.toggled.connect(self.btnstate1)
        #checkboxy
        self.cb0=QCheckBox('Temperatura')
        self.cb0.stateChanged.connect(self.cbox0_changed)
        self.cb0.toggle()
        self.cb1=QCheckBox('Temperatura odczuwalna')        
        self.cb1.stateChanged.connect(self.cbox1_changed)
        self.cb2=QCheckBox('Opady')
        self.cb2.stateChanged.connect(self.cbox2_changed)
        self.cb3=QCheckBox('Ciśnienie')
        self.cb3.stateChanged.connect(self.cbox3_changed)
        self.cb4=QCheckBox('Wilgotność')
        self.cb4.stateChanged.connect(self.cbox4_changed)
        self.cb5=QCheckBox('Wiatr')
        self.cb5.stateChanged.connect(self.cbox5_changed)
        #wyswietlanie widgetow
        siatka.addWidget(self.cb0, 10, 8)
        siatka.addWidget(self.cb1, 11, 8)
        siatka.addWidget(self.cb2, 12, 8)
        siatka.addWidget(self.cb3, 13, 8)
        siatka.addWidget(self.cb4, 14, 8)
        siatka.addWidget(self.cb5, 15, 8) 
        siatka.addWidget(self.label7, 9, 8)         
        siatka.addWidget(self.radiobutton, 5, 8)
        siatka.addWidget(self.label0, 2, 2)
        siatka.addWidget(self.label1, 0, 5)
        siatka.addWidget(self.label3, 2, 8)
        siatka.addWidget(self.label4, 2, 6)
        siatka.addWidget(self.label5, 3, 5)
        siatka.addWidget(self.label6, 4, 5) 
        siatka.addWidget(self.text1, 3, 2)
        siatka.addWidget(self.button1, 4, 2)
        siatka.addWidget(self.label10, 10, 2)
        siatka.addWidget(self.label11, 11, 2)
        siatka.addWidget(self.label12, 12, 2)
        siatka.addWidget(self.label13, 13, 2)
        siatka.addWidget(self.label14, 14, 2)
        siatka.addWidget(self.label15, 15, 2)
        siatka.addWidget(self.label20, 5, 2)
        siatka.addWidget(self.label21, 5, 5)
        siatka.addWidget(self.label_interp, 9, 2)
        siatka.addWidget(self.text10, 10, 5)
        siatka.addWidget(self.text11, 11, 5)
        siatka.addWidget(self.text12, 12, 5)
        siatka.addWidget(self.text13, 13, 5)
        siatka.addWidget(self.text14, 14, 5)
        siatka.addWidget(self.text15, 15, 5)        
        #zdarzenie przycisku
        self.button1.clicked.connect(self.button1Clicked)
        #combobox (lista rozwijana)
        self.combo = QComboBox()
        #nadanie wartosci 0-23
        for ii in range (0,24):
            if ii >=0 and ii <10:
                zm=str(ii)
                zm2=("0"+zm)
                self.combo.addItem(zm2)
            if ii >=10:
                zm3=str(ii)
                self.combo.addItem(zm3)          
        siatka.addWidget(self.combo, 3, 6)
        #zdarzenie comboboxa
        self.combo.activated[str].connect(self.onActivated)
        self.combo1=QComboBox(self)
        #nadanie wartosci 0-59
        for ii in range (0,60):
            if ii >=0 and ii <10:
                zm=str(ii)
                zm2=("0"+zm)
                self.combo1.addItem(zm2)
            if ii >=10:
                zm3=str(ii)
                self.combo1.addItem(zm3) 
        siatka.addWidget(self.combo1, 4, 6)
        #zdarzenie comboboxa2
        self.combo1.activated[str].connect(self.onActivated_combo1)
        self.show()
    #funkcje do checkboxow (zmieniaja wartosci zmiennych)
    def cbox0_changed(self, state):
        checkbox = self.sender()
        global fx0
        if (checkbox.isChecked()):
            fx0 = checkbox.text()
        else:
            fx0 = "not_checked"
    def cbox1_changed(self, state):
        checkbox = self.sender()
        global fx1
        if (checkbox.isChecked()):
            fx1 = checkbox.text()
        else:
            fx1 = "not_checked"
    def cbox2_changed(self, state):
        checkbox = self.sender()
        global fx2
        if (checkbox.isChecked()):
            fx2 = checkbox.text()
        else:
            fx2 = "not_checked"
    def cbox3_changed(self, state):
        checkbox = self.sender()
        global fx3
        if (checkbox.isChecked()):
            fx3 = checkbox.text()
        else:
            fx3 = "not_checked"
    def cbox4_changed(self, state):
        checkbox = self.sender()
        global fx4
        if (checkbox.isChecked()):
            fx4 = checkbox.text()
        else:
            fx4 = "not_checked"
    def cbox5_changed(self, state):
        checkbox = self.sender()
        global fx5
        if (checkbox.isChecked()):
            fx5 = checkbox.text()
        else:
            fx5 = "not_checked"
    #2 funkcje do zmiany wartosci comboboxy
    def onActivated(self, text):
        global godz
        godzina=text
        godz=int(godzina)
    def onActivated_combo1(self, text):
        global minut
        minuty=text
        minut=int(minuty)
    #3 funkcje zmiana wartosci dla radiobuttonow
    def btnstate1(self):
        radiobutton = self.sender()
        if radiobutton.isChecked():
               self.bs1=radiobutton.co
    #zdarzenie po wcisnieciu buttona
    def button1Clicked(self):
        if (self.text1.text()==""):
            # if jesli puste pole
            QMessageBox.information(self, 'Wiadomość', "Nie wpisales miasta!", QMessageBox.Ok, QMessageBox.Ok)
        else:
            #glowny program
            #pobranie tekstu z pola tekstowego
            x=self.text1.text()
            #usuwanie spacji
            x2=(x.replace(" ", ""))
            #generowanie adresu url
            URL = "https://www.meteoprog.pl/pl/meteograms/"+x2+"/"
            print(URL)
            #pobranie danych ze stronki
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            seven_day = soup.find(id="meteoforecast")
            forecast_items = seven_day.find_all(class_="colorRow")
            forecast_city = seven_day.find(class_="nameCity")
            tonight = forecast_items[0]
            todaycity = forecast_city.get_text()
            #print(tonight.prettify())            
            #pobranie wartosci ze znacznikow td
            period_tags = seven_day.select("td")
            periods = [pt.get_text() for pt in period_tags]
            #print(periods)
            #ilosc wyrazow w tablicy
            #print(len(periods))
            #167 wyraz ostatni liczac od 0 dla danego dnia
            #print(periods[503])
            #generowanie tablic
            dzien1, dzien2, dzien3=[], [], []
            czas1, czas2, czas3=[], [], []
            temperatura1, temperatura2, temperatura3=[], [], []
            odczuwalna_temp1, odczuwalna_temp2, odczuwalna_temp3=[], [], []
            opady1, opady2, opady3=[], [], []
            cisnienie1, cisnienie2, cisnienie3=[], [], []
            wilgotnosc1, wilgotnosc2, wilgotnosc3=[], [], []
            wiatr1, wiatr2, wiatr3=[], [], []
            #podzial danych na 3 dni i zapis do tablic
            for i in range(0,168):
                dzien1.insert(i, periods[i])
            for k in range(168,336):
                dzien2.insert(k, periods[k])
            for m in range(336,504):
                dzien3.insert(m, periods[m])    
            for d in range(0,168,7):
                czas1.insert(d,dzien1[d])
                czas2.insert(d,dzien2[d])
                czas3.insert(d,dzien3[d])
                temperatura1.insert(d+1,dzien1[d+1])
                temperatura2.insert(d+1,dzien2[d+1])
                temperatura3.insert(d+1,dzien3[d+1])
                odczuwalna_temp1.insert(d+2,dzien1[d+2])
                odczuwalna_temp2.insert(d+2,dzien2[d+2])
                odczuwalna_temp3.insert(d+2,dzien3[d+2])
                opady1.insert(d+3,dzien1[d+3])
                opady2.insert(d+3,dzien2[d+3])
                opady3.insert(d+3,dzien3[d+3])
                cisnienie1.insert(d+4,dzien1[d+4])
                cisnienie2.insert(d+4,dzien2[d+4])
                cisnienie3.insert(d+4,dzien3[d+4])
                wilgotnosc1.insert(d+5,dzien1[d+5])
                wilgotnosc2.insert(d+5,dzien1[d+5])
                wilgotnosc3.insert(d+5,dzien1[d+5])
                wiatr1.insert(d+6,dzien1[d+6])
                wiatr2.insert(d+6,dzien2[d+6])
                wiatr3.insert(d+6,dzien3[d+6])
            #generowanie tablic dla inta i float
            temperatura1_int, temperatura2_int, temperatura3_int = [], [], []
            odczuwalna_temp1_int, odczuwalna_temp2_int, odczuwalna_temp3_int = [], [], []
            opady1_float, opady2_float, opady3_float = [], [], []
            cisnienie1_int, cisnienie2_int, cisnienie3_int = [], [], []
            wilgotnosc1_int, wilgotnosc2_int, wilgotnosc3_int = [], [], []
            wiatr1_int, wiatr2_int, wiatr3_int = [], [], []
            #usuwanie elementow string i zamiana na int oraz float
            for ki in range(24):
                temperatura1_int.append(int(temperatura1[ki].replace("°C", "")))
                temperatura2_int.append(int(temperatura2[ki].replace("°C", "")))
                temperatura3_int.append(int(temperatura3[ki].replace("°C", "")))
                odczuwalna_temp1_int.append(int(odczuwalna_temp1[ki].replace("°C", "")))
                odczuwalna_temp2_int.append(int(odczuwalna_temp2[ki].replace("°C", "")))
                odczuwalna_temp3_int.append(int(odczuwalna_temp3[ki].replace("°C", "")))
                op1=(opady1[ki].replace(",", "."))
                opady1_float.append(float(op1.replace(" mm", "")))
                op2=(opady2[ki].replace(",", "."))
                opady2_float.append(float(op2.replace(" mm", "")))
                op3=(opady3[ki].replace(",", "."))
                opady3_float.append(float(op3.replace(" mm", "")))
                cisnienie1_int.append(int(cisnienie1[ki].replace(" mmHg", "")))
                cisnienie2_int.append(int(cisnienie2[ki].replace(" mmHg", "")))
                cisnienie3_int.append(int(cisnienie3[ki].replace(" mmHg", "")))
                wilgotnosc1_int.append(int(wilgotnosc1[ki].replace("%", "")))
                wilgotnosc2_int.append(int(wilgotnosc2[ki].replace("%", "")))
                wilgotnosc3_int.append(int(wilgotnosc3[ki].replace("%", "")))
                wiatr1_int.append(int(wiatr1[ki].replace(" m/s", "")))
                wiatr2_int.append(int(wiatr2[ki].replace(" m/s", "")))
                wiatr3_int.append(int(wiatr3[ki].replace(" m/s", "")))   
            #dopisanie ostatniego indeksu do tablic (w przypadku godziny powyzej 23)
            temperatura1_int.append(temperatura1_int[23])
            temperatura2_int.append(temperatura2_int[23])
            temperatura3_int.append(temperatura3_int[23])
            odczuwalna_temp1_int.append(odczuwalna_temp1_int[23])
            odczuwalna_temp2_int.append(odczuwalna_temp2_int[23])
            odczuwalna_temp3_int.append(odczuwalna_temp3_int[23])
            opady1_float.append(opady1_float[23])
            opady2_float.append(opady2_float[23])
            opady3_float.append(opady3_float[23])
            cisnienie1_int.append(cisnienie1_int[23])
            cisnienie2_int.append(cisnienie2_int[23])
            cisnienie3_int.append(cisnienie3_int[23])
            wilgotnosc1_int.append(wilgotnosc1_int[23])
            wilgotnosc2_int.append(wilgotnosc2_int[23])
            wilgotnosc3_int.append(wilgotnosc3_int[23])
            wiatr1_int.append(wiatr1_int[23])
            wiatr2_int.append(wiatr2_int[23])
            wiatr3_int.append(wiatr3_int[23])
            #interpolacja
            x_a=np.arange(0,25, 1)                   
            f_temp1=interp1d(x_a,temperatura1_int, kind='cubic')
            f_temp2=interp1d(x_a,temperatura2_int, kind='cubic')
            f_temp3=interp1d(x_a,temperatura3_int, kind='cubic')
            f_o_temp1=interp1d(x_a,odczuwalna_temp1_int, kind='cubic')
            f_o_temp2=interp1d(x_a,odczuwalna_temp2_int, kind='cubic')
            f_o_temp3=interp1d(x_a,odczuwalna_temp3_int, kind='cubic')
            f_opady1=interp1d(x_a,opady1_float, kind='cubic')
            f_opady2=interp1d(x_a,opady2_float, kind='cubic')
            f_opady3=interp1d(x_a,opady3_float, kind='cubic')
            f_cisn1=interp1d(x_a,cisnienie1_int, kind='cubic')
            f_cisn2=interp1d(x_a,cisnienie2_int, kind='cubic')
            f_cisn3=interp1d(x_a,cisnienie3_int, kind='cubic')
            f_wilg1=interp1d(x_a,wilgotnosc1_int, kind='cubic')
            f_wilg2=interp1d(x_a,wilgotnosc2_int, kind='cubic')
            f_wilg3=interp1d(x_a,wilgotnosc3_int, kind='cubic')
            f_wiatr1=interp1d(x_a,wiatr1_int, kind='cubic')
            f_wiatr2=interp1d(x_a,wiatr2_int, kind='cubic')
            f_wiatr3=interp1d(x_a,wiatr3_int, kind='cubic')                   
            xinterp=np.arange(0,24,(1/60))        
            #wartosci funkcji
            yf_temp1=f_temp1(xinterp)
            yf_temp2=f_temp2(xinterp)
            yf_temp3=f_temp3(xinterp)
            yf_o_temp1=f_o_temp1(xinterp)
            yf_o_temp2=f_o_temp2(xinterp)
            yf_o_temp3=f_o_temp3(xinterp)
            yf_opady1=f_opady1(xinterp)
            yf_opady2=f_opady2(xinterp)
            yf_opady3=f_opady3(xinterp)
            yf_cisn1=f_cisn1(xinterp)
            yf_cisn2=f_cisn2(xinterp)
            yf_cisn3=f_cisn3(xinterp)
            yf_wilg1=f_wilg1(xinterp)
            yf_wilg2=f_wilg2(xinterp)
            yf_wilg3=f_wilg3(xinterp)
            yf_wiatr1=f_wiatr1(xinterp)
            yf_wiatr2=f_wiatr2(xinterp)
            yf_wiatr3=f_wiatr3(xinterp)
            #obliczanie indeksu dla wartosci interpolowanej 1440 indexow 60*24
            idx=(godz*60)+minut              
            self.label21.setText("o godzinie: %d:%d." %(godz, minut))
            #tworzenie dat
            today = datetime.date.today()            
            tomorrow = today + datetime.timedelta(days=1)          
            tomorrow2 = today + datetime.timedelta(days=2)
            #wyswietlanie wykreosw w zaleznosci od zaznaczonych buttonow oraz wpisywanie wartosci do pol
            if (self.bs1=="Dzisiaj"):
                self.label20.setText("Pogoda dla: "+todaycity+" z dnia: "+today.strftime("%Y-%m-%d"))
                self.text10.setText(str(round(yf_temp1[idx],2))+"° C")
                self.text11.setText(str(round(yf_o_temp1[idx],2))+" °C")
                self.text12.setText(str(round(yf_opady1[idx],2))+" mm")
                self.text13.setText(str(round(yf_cisn1[idx],2))+" mmHg")
                self.text14.setText(str(round(yf_wilg1[idx],2))+" %")
                self.text15.setText(str(round(yf_wiatr1[idx],2))+" m/s")
                if (fx0=="Temperatura"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, temperatura1_int, '^r', xinterp, yf_temp1, '.b')
                    plt.title("Temperatura dzisiaj (°C)")
                    plt.show()
                if (fx1=="Temperatura odczuwalna"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, odczuwalna_temp1_int, '^r', xinterp, yf_o_temp1, '.b')
                    plt.title("Temperatura odczuwalna dzisiaj (°C)")
                    plt.show()
                if (fx2=="Opady"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, opady1_float, '^r', xinterp, yf_opady1, '.b')
                    plt.title("Opady dzisiaj (mm)")
                    plt.show()
                if (fx3=="Ciśnienie"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, cisnienie1_int, '^r', xinterp, yf_cisn1, '.b')
                    plt.title("Cisnienie dzisiaj (mmHg)")
                    plt.show()
                if (fx4=="Wilgotność"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, wilgotnosc1_int, '^r', xinterp, yf_wilg1, '.b')
                    plt.title("Wilgotnosc dzisiaj (%)")
                    plt.show()
                if (fx5=="Wiatr"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, wiatr1_int, '^r', xinterp, yf_wiatr1, '.b')
                    plt.title("Wiatr dzisiaj (m/s)")
                    plt.show()                    
            if (self.bs1=="Jutro"):
                self.label20.setText("Pogoda dla: "+todaycity+" z dnia: "+tomorrow.strftime("%Y-%m-%d"))
                self.text10.setText(str(round(yf_temp2[idx],2))+"° C")
                self.text11.setText(str(round(yf_o_temp2[idx],2))+" °C")
                self.text12.setText(str(round(yf_opady2[idx],2))+" mm")
                self.text13.setText(str(round(yf_cisn2[idx],2))+" mmHg")
                self.text14.setText(str(round(yf_wilg2[idx],2))+" %")
                self.text15.setText(str(round(yf_wiatr2[idx],2))+" m/s")
                if (fx0=="Temperatura"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, temperatura2_int, '^r', xinterp, yf_temp2, '.b')
                    plt.title("Temperatura jutro (°C)")
                    plt.show()
                if (fx1=="Temperatura odczuwalna"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, odczuwalna_temp2_int, '^r', xinterp, yf_o_temp2, '.b')
                    plt.title("Temperatura odczuwalna jutro (°C)")
                    plt.show()
                if (fx2=="Opady"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, opady2_float, '^r', xinterp, yf_opady2, '.b')
                    plt.title("Opady jutro (mm)")
                    plt.show()
                if (fx3=="Ciśnienie"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, cisnienie2_int, '^r', xinterp, yf_cisn2, '.b')
                    plt.title("Cisnienie jutro (mmHg)")
                    plt.show()
                if (fx4=="Wilgotność"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, wilgotnosc2_int, '^r', xinterp, yf_wilg2, '.b')
                    plt.title("Wilgotnosc jutro (%)")
                    plt.show()
                if (fx5=="Wiatr"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, wiatr2_int, '^r', xinterp, yf_wiatr2, '.b')
                    plt.title("Wiatr jutro (m/s)")
                    plt.show()              
            if (self.bs1=="Pojutrze"):
                self.label20.setText("Pogoda dla: "+todaycity+" z dnia: "+tomorrow2.strftime("%Y-%m-%d"))
                self.text10.setText(str(round(yf_temp3[idx],2))+"° C")
                self.text11.setText(str(round(yf_o_temp3[idx],2))+" °C")
                self.text12.setText(str(round(yf_opady3[idx],2))+" mm")
                self.text13.setText(str(round(yf_cisn3[idx],2))+" mmHg")
                self.text14.setText(str(round(yf_wilg3[idx],2))+" %")
                self.text15.setText(str(round(yf_wiatr3[idx],2))+" m/s")
                if (fx0=="Temperatura"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, temperatura3_int, '^r', xinterp, yf_temp3, '.b')
                    plt.title("Temperatura pojutrze (°C)")
                    plt.show()
                if (fx1=="Temperatura odczuwalna"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, odczuwalna_temp3_int, '^r', xinterp, yf_o_temp3, '.b')
                    plt.title("Temperatura odczuwalna pojutrze (°C)")
                    plt.show()
                if (fx2=="Opady"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, opady3_float, '^r', xinterp, yf_opady3, '.b')
                    plt.title("Opady pojutrze (mm)")
                    plt.show()
                if (fx3=="Ciśnienie"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, cisnienie3_int, '^r', xinterp, yf_cisn3, '.b')
                    plt.title("Cisnienie pojutrze (mmHg)")
                    plt.show()
                if (fx4=="Wilgotność"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, wilgotnosc3_int, '^r', xinterp, yf_wilg3, '.b')
                    plt.title("Wilgotnosc pojutrze (%)")
                    plt.show()
                if (fx5=="Wiatr"):
                    plt.xticks(np.arange(25))
                    plt.grid()
                    plt.plot(x_a, wiatr3_int, '^r', xinterp, yf_wiatr3, '.b')
                    plt.title("Wiatr pojutrze (m/s)")
                    plt.show()
    #funkcja od zamykania programu
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Wiadomość',
            "Czy napewno chcesz wyjść?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
#main programu
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Program()
    sys.exit(app.exec_())

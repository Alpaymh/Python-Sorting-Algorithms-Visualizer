#Gerekli olan kütüphaneler import ediliyor.
import os
import random
import sys
import time
import math

from matplotlib.backends.backend_qt5agg import \
NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class MatplotlibWidget(QMainWindow):

    xdata = None
    ydata = None
    loop_state = False
    karsilastirma = 0
    basladur = 0

    def __init__(self):
        QMainWindow.__init__(self)
        
        # Ui dosyası okutuluyor.
        loadUi("qt_designer.ui",self)
        
        #Uygulamanın icon resmi koyuluyor.
        self.setWindowIcon(QtGui.QIcon("icon.jpg"))

        self.initial_graph()
        self.MplWidget.canvas.axes.get_xaxis().set_visible(False)
        self.MplWidget.canvas.axes.get_yaxis().set_visible(False)
        self.MplWidget.canvas.axes.get_yaxis().set_visible(False)
        self.btn_Manuel.hide()


        #Butonlar metotlara bağlanıyor.
        self.btn_Bubble.clicked.connect(self.bubble_sort)
        self.btn_Quick.clicked.connect(self.quick_sort)
        self.btn_Insertion.clicked.connect(self.insert_sort)
        self.btn_Merge.clicked.connect(self.merge_sort)
        self.btn_Selection.clicked.connect(self.select_sort)
        self.radioBtn_manuel.clicked.connect(self.radio_manuel)
        self.radioBtn_oto.clicked.connect(self.radio_oto)
        self.pushButton_sifirla.clicked.connect(self.clean_application)
        self.pushButton_dur.clicked.connect(self.dur)
        self.pushButton_basla.clicked.connect(self.basla)



        #İlk önce liste değerleri girileceği için sıralama algoritmaların enable özelliği 'False' Yapılıyor.
        self.btn_Bubble.setEnabled(False)
        self.btn_Quick.setEnabled(False)
        self.btn_Insertion.setEnabled(False)
        self.btn_Merge.setEnabled(False)
        self.btn_Selection.setEnabled(False)

        # Grafiğin boyutunu ayarlamak için bağlanıyor.
        self.spnBars.valueChanged.connect(self.update_new_graph)

        # Oluştur butonuna basıldığında grafikte istenilen bilgilere göre sütunlar karıştırılır. 
        self.btn_Random.clicked.connect(self.scramble_bars)
        self.btn_Manuel.clicked.connect(self.manuel_bars)

    
    def clean_application(self):
           # Sıfırlama butonuna basıldığında girilen değerlerin temizlenmesi için gerekli kodlar giriliyor.
           self.textEdit_degerekle.clear()
           self.spnBars.setValue(10)
           self.sldAnim_speed.setValue(50)
           self.comboBox_grafik.setCurrentIndex(0)
           self.label_karsilastirma.setText("0")
           self.label_zamankar.setText("0")
           self.karsilastirma = 0 
           self.update_new_graph()
           self.btn_Random.setEnabled(True)




    def manuel_bars(self):
        self.MplWidget.canvas.axes.clear()

         # Liste değerlinin girişi yapıldığı için Sıralama Algoritmalarının Enable özelliği 'True' yapılıyor 
        self.btn_Bubble.setEnabled(True)
        self.btn_Quick.setEnabled(True)
        self.btn_Insertion.setEnabled(True)
        self.btn_Merge.setEnabled(True)
        self.btn_Selection.setEnabled(True)

        # Kullanıcıdan aldığı değerleri grafiğe geçiriliyor.
        input_text = self.textEdit_degerekle.toPlainText()
        num_list = list(map(int, input_text.split()))
        scram_ys = num_list
        ys = scram_ys.copy()
        
        # Değerleri saymak için gerekli kodlar oluşturuluyor.
        value_counts = {}
        for value in ys:
            if value in value_counts:
                value_counts[value] += 1
            else:
                value_counts[value] = 1
        deger = 0
        for value, count in value_counts.items():
            deger += count

        scram_xs = [i for i in range(1, deger +1)]
        xs = scram_xs.copy()
        

        # Yeni veriler, sınıf değişkenlerine (self.ydata ve self.xdata) kopyalanır. Bu veriler, çubuk grafiğinin çiziminde kullanılacak.
        self.ydata = ys.copy()
        self.xdata = xs.copy()

        # draw_graph adlı başka bir metodu çağırarak, yeni verilerin grafiğe çizilmesi sağlanır.
        self.draw_graph(xs, ys, None)


     
            
                
            
    # Grafik oluştuktan sonra butonların enable durumları ayarlanıyor.
    def buttons(self, tfstate):
        self.btn_Bubble.setEnabled(tfstate)
        self.btn_Quick.setEnabled(tfstate)
        self.btn_Insertion.setEnabled(tfstate)
        self.btn_Merge.setEnabled(tfstate)
        self.btn_Selection.setEnabled(tfstate)

    def basla(self):
        basladur = 0
        self.basladur = basladur
        self.btn_Random.setEnabled(True)


    def dur(self):
        basladur = 1
        self.basladur = basladur
        self.btn_Random.setEnabled(True)
        
   

         
    #Kullanıcı Liste Giriş Tercihini manuel yaptığımızda boyut girişini engellemek için enable özelliği 'False' yapıldı.
    #Listteye değer girişi için 'Listeye Ekle' butonu ve spinbox kullanımı 'True' yapıldı.
    def radio_manuel(self):
        self.spnBars.setEnabled(False)

        self.btn_Manuel.setVisible(True)
        self.btn_Random.hide()


    
    #Kullanıcı Liste Giriş Tercihini otomatik yaptığımızda Listteye değer girişini engellemek için 'Listeye Ekle' butonu ve spinbox'un enable özelliği 'False' yapıldı.
    #Listenin otomatik oluşmasında boyut girişi için enable özelliği 'True' yapıldı.
    def radio_oto(self):
        self.spnBars.setEnabled(True)

        self.btn_Random.setVisible(True)
        self.btn_Manuel.hide()
    

app = QApplication([])
# MatplotlibWidget sınıfından bir pencere (widget) objesi oluşturuluyor.
window = MatplotlibWidget()
window.show()
app.exec_()
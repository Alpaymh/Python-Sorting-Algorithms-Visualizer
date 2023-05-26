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



# Animasyon oluşturma metodu.
    def new_frame(self, highlight_bar):
         
        # self.ani_time() değişkeninin değeri tarafından belirtilen bir süre boyunca duraklatır.
        time.sleep(self.ani_time())
        # self.MplWidget nesnesiyle ilişkili Matplotlib şeklinin eksenlerini temizler.
        self.MplWidget.canvas.axes.clear()

        # Sutünların renkleri belirtiliyor.
        bar_color = ["#ff0000"] * (len(self.ydata)-1)
        bar_color.insert(highlight_bar,"#ffa500")
        self.draw_graph(self.xdata, self.ydata, bar_color)

        # Uygulamanın kullanıcı arayüzünün tepki vermesi sağlanıyor ve uygulamanın donmamasını veya yanıt vermemesini engelleniyor.
        QtCore.QCoreApplication.processEvents()


    def ani_time(self):
        # Çubuğun değerine göre bir değer alınır.
        ani_speed = self.sldAnim_speed.value()

        # Hız süreye çevriliyor.
        ani_interval = (-1/295)*ani_speed + 0.336

        # Hız süresi 'return' ifadesiyle geri döndürülür.
        return(ani_interval)
    
         #Sütunların Karıştırma Metodu
    def scramble_bars(self):
        # Matplotlib grafiği temizlenir.
        self.MplWidget.canvas.axes.clear()

        # Liste değerlinin girişi yapıldığı için Sıralama Algoritmalarının Enable özelliği 'True' yapılıyor 
        self.btn_Bubble.setEnabled(True)
        self.btn_Quick.setEnabled(True)
        self.btn_Insertion.setEnabled(True)
        self.btn_Merge.setEnabled(True)
        self.btn_Selection.setEnabled(True)

        # Sütunların sayısı alınıyor.
        bar_count = self.spnBars.value()
        
        # scram_ys adlı liste, 1'den bar_count'a kadar olan sayıları içerir.
        scram_ys = [i for i in range(1, bar_count +1)]
        xs = scram_ys.copy()
        #scram_ys listesindeki elemanların yerlerini rastgele değiştirilir. Bu, çubukların sıralamasını rastgele bir şekilde karıştırır.
        for j in range(0, len(scram_ys)-1):
            target = random.randint(j, len(scram_ys)-1)
            scram_ys[j] , scram_ys[target] = scram_ys[target], scram_ys[j]
        
        
        # Karıştırılmış çubukların yeri belirleniyor.
        self.ydata = scram_ys.copy()
        self.xdata = xs.copy()

        # draw_graph adlı başka bir metodu çağırarak, yeni verilerin grafiğe çizilmesi sağlanır.
        self.draw_graph(xs,scram_ys,None)

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


     
            
    #Uygulama açıldığındaki ilk grafiğin metodu.
    def update_new_graph(self):
        # Matplotlib grafiği temizlenir.
        self.MplWidget.canvas.axes.clear()

        # Çubuk sayısı alınıyor.
        bar_count = self.spnBars.value()

        # ys adlı liste, 1'den bar_count'a kadar olan sayıları içerir. 
        ys = [i for i in range(1, bar_count +1)]
        xs = ys

        # Yeni veriler, sınıf değişkenlerine (self.ydata ve self.xdata) kopyalanır. Bu veriler, çubuk grafiğinin çiziminde kullanılacak.
        self.ydata = ys.copy()
        self.xdata = xs.copy()

        # draw_graph adlı başka bir metodu çağırarak, yeni verilerin grafiğe çizilmesi sağlanır.
        self.draw_graph(xs, ys, None)
        
    #Uygulama başladığında ilk olarak çağrılan bir metoddur. Bu metot, boş bir grafik yerine sütunları olan bir grafikle başlamayı sağlar.
    def initial_graph(self):
        self.update_new_graph()
        return


    def draw_graph(self, xs, ys, bar_color):
        # Grafik Türleri Yazan Combobox'ta hangisi seçili ise ona göre grafik vermesi sağlanıyor.
        selected_text = self.comboBox_grafik.currentText()
        if selected_text == "Sütun (Bar) Grafiği":
            # Grafiğin sürun renkleri ayarlanıyor.
            if bar_color is None:
                self.MplWidget.canvas.axes.bar(xs, ys, color="#ff0000")
            else:
                self.MplWidget.canvas.axes.bar(xs, ys, color='#ff0000')

            self.MplWidget.canvas.draw()

        elif selected_text == "Kök (Stem) Grafiği":
            # Grafiğin sürun renkleri ayarlanıyor.
            if bar_color is None:
                self.MplWidget.canvas.axes.plot(xs, ys, color="#ff0000")
            else:
                self.MplWidget.canvas.axes.plot(xs, ys, color='#ff0000')

            self.MplWidget.canvas.draw()

        elif selected_text == "Dağılım (Scatter) Grafiği":
            # Grafiğin sürun renkleri ayarlanıyor.
            if bar_color is None:
                self.MplWidget.canvas.axes.scatter(xs, ys, color="#ff0000")
            else:
                self.MplWidget.canvas.axes.scatter(xs, ys, color='#ff0000')
            self.MplWidget.canvas.draw()
            
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
        
        # Bubble (Kabarcık) Sıralamasının Kodu.
    def bubble_sort(self):
        yarray = self.ydata.copy()
        copy = yarray.copy()

        # Butonların kullanımı kısıtlanıyor.
        self.buttons(False)
        self.btn_Random.setEnabled(False)
        
        # Zaman karmasikligi için bilgiler giriliyor.
        zdeg = (len(yarray))*(len(yarray))
        self.label_zamankar.setText("O(" + str(zdeg) + ")"+" - O(n2)")
        self.basladur = 0
        for i in range(len(yarray)):

            endp = len(yarray) - i
            
            for j in range(0 , endp):
                if self.basladur == 1:
                    self.start_delay()
                if j+1 == len(yarray):
                    pass    
                else:
                    if yarray[j] > yarray[j+1]:
                        # Swap işlemi gerçekleştiriliyor
                        yarray[j], yarray[j+1] = yarray[j+1], yarray[j]

                        # Veri güncelleniyor
                        self.ydata = yarray
                        
                        # Yeni frame oluşturuluyor
                        self.new_frame(j+1)
                        # Karşılaştırma sayısı artırılıyor ve ekrana yazdırlıyor.
                        self.karsilastirma += 1 
                        self.label_karsilastirma.setText(str(self.karsilastirma))
        self.karsilas(copy,yarray)
        
        self.btn_Random.setEnabled(True)

    # Insert (Eklemeli) Sıralamasının Kodu.
    def insert_sort(self):
        yarray = self.ydata.copy()
        copy = yarray.copy()
        # Butonların kullanımı kısıtlanıyor.
        self.buttons(False)
        self.btn_Random.setEnabled(False)
        # Zaman karmasikligi için bilgiler giriliyor.
        zdeg = (len(yarray))*(len(yarray))
        self.label_zamankar.setText("O(" + str(zdeg) + ")"+" - O(n2)")
        self.basladur = 0
        for i in range(len(yarray)):
            if self.basladur == 1:
                    self.start_delay()
            if (i+1) == len(yarray):
                break 
            else:
                if yarray[i] > yarray[i+1]:
                    # Elemanlar karşılaştırılıyor ve gerektiğinde yer değiştiriliyor
                    for k in reversed(range(i+1)):
                        self.karsilastirma += 1 
                        self.label_karsilastirma.setText(str(self.karsilastirma))
                        if yarray[k+1] < yarray[k]:
                            yarray[k], yarray[k+1] = yarray[k+1] , yarray[k]
                            
                            # Veri güncelleniyor
                            self.ydata = yarray

                            # Yeni frame oluşturuluyor
                            self.new_frame(k)
                        else:
                            break
        self.karsilas(copy,yarray)
        # Oluşturma butonu enable özelliği aktif ediliyor.
        self.btn_Random.setEnabled(True)

    mergcopy = ""
    #  Bu metot, merge sort algoritmasının başlatılmasını sağlar. İşlemler sırasında kullanılan ara metotları 
    #  çağırır ve sonuçları geri döndürür.
    def merge_sort(self):
        yarray = self.ydata.copy()
        self.mergcopy = yarray.copy()
        # Butonların kullanımı kısıtlanıyor.
        self.buttons(False)
        self.btn_Random.setEnabled(False)

        yarray = self.merge_split(yarray)

        # Zaman karmasikligi için bilgiler giriliyor.
        zdeg = (len(yarray))*math.log((len(yarray)))
        self.label_zamankar.setText("O(" + str(zdeg) + ")"+" - O(n log (n) )")

        # Veri güncelleniyor
        self.ydata = yarray
        # Yeni frame oluşturuluyor.
        self.new_frame(0)
        # Oluşturma butonu enable özelliği aktif ediliyor.
        self.btn_Random.setEnabled(True)

    # Bu metot, verilen diziyi ikiye bölen ve bölünmüş dizileri sıralamak için merge metoduyla birleştiren rekürsif bir işlemdir.
    # Her bir bölünmüş dizi için merge_update metodu çağırılır ve ardından sıralanmış diziler merge metodu kullanılarak birleştirilir.
    def merge_split(self, arr):
        
        length = len(arr)

        # Eğer listenin uzunluğu 1 ise, listenin kendisini döndür.
        # Bu durumda, listenin parçalanması sonlanır ve sıralama işlemi başlar.
        if length == 1:
            return(arr)
        
        # Listenin orta noktası hesaplanır.
        midp = length//2

        # Sol yarıdaki elemanlar için merge_split metodu tekrar çağrılır.
        # Bu işlem, listenin sol yarısını parçalara ayırır ve sıralamayı gerçekleştirir.
        arr_1 = self.merge_split(arr[:midp])
        self.merge_update(arr_1, self.ydata)

        # Sağ yarıdaki elemanlar için merge_split metodu tekrar çağrılır.
        # Bu işlem, listenin sağ yarısını parçalara ayırır ve sıralamayı gerçekleştirir.
        arr_2 = self.merge_split(arr[midp:])
        self.merge_update(arr_2, self.ydata)

        # Yeni frame oluşturulur
        self.new_frame(0)

        # Sıralanmış sol ve sağ yarıları birleştirmek için merge metodu çağrılır.
        # Bu işlem, merge sort'un birleştirme (merge) adımını gerçekleştirir.
        return(self.merge(arr_1, arr_2))

    # Bu metot, bir alt listedeki elemanların ana listedeki sıralı konumunu bulur ve ana listeden bu elemanları kaldırır.
    # Ardından, alt listedeki elemanları sırasıyla ana liste içerisine yerleştirir.
    def merge_update(self, sub_list, main_list):
        # Alt listenin elemanlarının ana listedeki konumlarını belirlemek için bir 'pos' listesi oluşturuluyor.
        pos = []
        for value in sub_list:
            pos.append(main_list.index(value))

        # Alt listenin elemanları ana listeden çıkarılır.
        for v in sub_list:
            main_list.remove(v)

        # 'pos' listesindeki en büyük ve en küçük değerler 'high' ve 'low' değişkenlerine atanır.
        high = max(pos)
        low = min(pos)

        # 'low' ve 'high' aralığındaki indekslere döngü ile gidilir ve alt liste ana liste içerisine yerleştirilir.
        for i in range(low, high+1):
            main_list.insert(i, sub_list[i-low])

    # Bu metot, iki sıralı listeyi birleştirerek tek bir sıralı liste oluşturur. 
    # İki liste üzerinde sıralı olarak gezinir ve elemanları karşılaştırarak küçük olanı sonuç listesine ekler. 
    def merge(self, arr_1, arr_2):
        sorted_arr = []
        copy = self.mergcopy.copy()
        # Her iki alt liste de boş olmadığı sürece döngü devam eder.
        while arr_1 and arr_2:
            # İki alt listenin ilk elemanlarının karşılaştırması yapılır.
            # Daha küçük olan eleman sıralanmış liste sonuna eklenir ve o alt listeden çıkarılır.
            if arr_1[0] < arr_2[0]:
                sorted_arr.append(arr_1.pop(0))
                
            else:
                sorted_arr.append(arr_2.pop(0))
        self.karsilastirma += 1 
        self.label_karsilastirma.setText(str(self.karsilastirma)) 
        # Bir alt liste hala eleman içeriyorsa, kalan elemanlar sıralanmış liste sonuna eklenir.
        while arr_1:
            sorted_arr.append(arr_1.pop(0))
            self.karsilastirma += 1 
            self.label_karsilastirma.setText(str(self.karsilastirma)) 

        while arr_2:
            sorted_arr.append(arr_2.pop(0))
            self.karsilastirma += 1 
            self.label_karsilastirma.setText(str(self.karsilastirma)) 
            self.karsilas(copy,sorted_arr)
        return(sorted_arr)

        
    # Selection (Seçmeli) Sıralamasının Kodu.
    def select_sort(self):
        yarray = self.ydata.copy()
        copy = yarray.copy()
        # Butonların kullanımı kısıtlanıyor.
        self.buttons(False)
        self.btn_Random.setEnabled(False)

        # Zaman karmasikligi için bilgiler giriliyor.
        zdeg = (len(yarray))*(len(yarray))
        self.label_zamankar.setText("O(" + str(zdeg) + ")"+" - O(n2)")

        
        for i in range(len(yarray)):

            holder = None

            # Minimum elemanı bulmak için iç içe geçmiş bir döngü kullanılıyor.
            # İç döngü, i'den başlayarak dizinin sonuna kadar ilerliyor.
            for j in range(i,len(yarray)):
                
                if (not holder):
                    holder = yarray[j]
                    self.karsilastirma -= 1 
                    self.label_karsilastirma.setText(str(self.karsilastirma))   
                elif yarray[j] < holder:
                    holder = yarray[j]
                    
                # Karşılaştırma sayısı güncelleniyor ve ekranda gösteriliyor.
                self.karsilastirma += 1 
                self.label_karsilastirma.setText(str(self.karsilastirma))   
                self.new_frame(j)
            
            # Minimum elemanın indeksi bulunuyor.
            shifter_index = yarray.index(holder)

            # Minimum elemanı listeden çıkarıp, doğru konuma yerleştiriliyor.
            yarray.pop(shifter_index)
            yarray.insert(i, holder)
            
            self.ydata = yarray
            
            # Grafiği güncelle.
            self.new_frame(shifter_index)
        self.karsilas(copy,yarray)
        self.btn_Random.setEnabled(True)

    # Quick (Hızlı) Sıralamasının Kodu.
    def quick_sort(self):
        yarray = self.ydata.copy()
        copy = yarray.copy()
        # Butonların kullanımı kısıtlanıyor.
        self.buttons(False)
        self.btn_Random.setEnabled(False)

        # Zaman karmasikligi için bilgiler giriliyor.
        zdeg = (len(yarray))*math.log((len(yarray)))
        self.label_zamankar.setText("O(" + str(zdeg) + ")"+" - O(n log (n) )")

        # Quick Sort'u çağır
        self.quick_sort_recursive(yarray, 0, len(yarray) - 1)
        self.karsilas(copy,yarray)
        self.btn_Random.setEnabled(True)


    def quick_sort_recursive(self, arr, low, high):
        if low < high:
            # Partition işlemi
            pivot_index = self.partition(arr, low, high)

            # Sol ve sağ tarafı ayrı ayrı sırala
            self.quick_sort_recursive(arr, low, pivot_index - 1)
            self.quick_sort_recursive(arr, pivot_index + 1, high)
        self.btn_Random.setEnabled(True)


    def partition(self, arr, low, high):
        # Pivot olarak son elemanı seç
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                # Swap işlemi
                arr[i], arr[j] = arr[j], arr[i]
                self.ydata = arr.copy() 
                self.new_frame(j)
            self.karsilastirma += 1 
            self.label_karsilastirma.setText(str(self.karsilastirma))  

        # Pivot'un doğru konuma getirilmesi için swap işlemi
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self.ydata = arr.copy()
        self.new_frame(high)
        return+1

    def karsilas(self, copy, yarray):
        if copy == yarray:
            self.karsilastirma = len(yarray) - 1
            self.label_karsilastirma.setText(str(self.karsilastirma))
        if self.karsilastirma == 1:
            self.karsilastirma = len(yarray)
            self.label_karsilastirma.setText(str(self.karsilastirma))
        elif self.karsilastirma == 2:
            self.karsilastirma = len(yarray) + 1
            self.label_karsilastirma.setText(str(self.karsilastirma))
        elif self.karsilastirma == 3:
            self.karsilastirma = len(yarray) + 2
            self.label_karsilastirma.setText(str(self.karsilastirma))

    def start_delay(self):
        delay_seconds = 10000
        start_time = time.time()
        while time.time() - start_time < delay_seconds:
            QApplication.processEvents()
            if self.basladur == 0:
                break

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
from PyQt5.QtWidgets import*

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure

    
class MplWidget(QWidget):
    
    def _init_(self, parent = None):
        # QWidget sınıfının başlatıcı metodunu çağırıyoruz.
        QWidget._init_(self, parent)
        
        # Bir FigureCanvas objesi oluşturuyoruz ve bir Figure nesnesine bağlıyoruz.
        self.canvas = FigureCanvas(Figure())

        # Dikey bir düzen oluşturmak için QVBoxLayout sınıfından bir obje oluşturuyoruz.
        vertical_layout = QVBoxLayout()
        # Oluşturduğumuz canvas nesnesini dikey düzene ekliyoruz.
        vertical_layout.addWidget(self.canvas)
        
        # FigureCanvas nesnesine bağlı olan Figure nesnesi üzerinde bir alt-çizim nesnesi ekliyoruz.
        self.canvas.axes = self.canvas.figure.add_subplot(111)

        # Widget'ın düzenini dikey düzenleme olarak ayarlıyoruz.
        self.setLayout(vertical_layout)
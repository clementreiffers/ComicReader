#APPLICATION MINIMALE
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import edition as e
import comics as c
import page as p
import sys
from PyQt5 import QtGui

class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Liseuse')

        self.setGeometry(200, 200, 1140, 500)


        self.setWindowIcon(QtGui.QIcon('spidermanicon.png'))

        self.setGeometry(200, 200, 1035, 500)


        self.filename = ""
        self.BDtabs = []

        self.toolbar = QToolBar("Bar d'outils")
        self.addToolBar(self.toolbar)

        self.ouvrir = QAction("Ouvrir", self)
        self.ouvrir.triggered.connect(self.charger)
        self.ouvrir.setStatusTip("Pour ouvrir un fichier")
        self.ouvrir.setIcon(QIcon("icons8-fichier-48.png"))

        self.biblio = QAction("Bibliothèque", self)
        self.biblio.triggered.connect(self.afficher_biblio)
        self.biblio.setStatusTip("Pour afficher la bibliothèque")

        self.quit = QAction("exit", self)
        self.quit.triggered.connect(self.quitter)
        self.quit.setStatusTip("Pour quitter")

        self.barreDeMenu = self.menuBar()
        self.menuFichier = self.barreDeMenu.addMenu("&Fichier")
        self.menuFichier.addAction(self.ouvrir)
        self.menuFichier.addAction(self.biblio)
        self.menuFichier.addAction(self.quit)
        self.menuFichier.addSeparator()

        self.menuEdition = self.barreDeMenu.addMenu("&Edition")
        self.menuEdition.addSeparator()

        self.menuAffichage = self.barreDeMenu.addMenu("&Affichage")
        self.menuAffichage.addSeparator()

        self.menuLire = self.barreDeMenu.addMenu("&Lire")
        self.menuLire.addSeparator()

        self.menuAide = self.barreDeMenu.addMenu("&Aide")
        self.menuAide.addSeparator()

        self.ouvrir.setShortcut(QKeySequence("ctrl+o"))
        self.biblio.setShortcut(QKeySequence("ctrl+b"))
        self.quit.setShortcut(QKeySequence("ctrl+q"))


        self.biblio = self.lire_bibliotheque()
        self.afficher_biblio(self.biblio)

    def quitter(self):
        exit()

    def au_revoir(self):
        partir = QAction('&Exit',self)
        partir.setShortcut('Ctrl+Q')
        partir.setStatusTip('Exit App')
        partir.triggered.connect(self.closeEvent)
        return partir


    def closeEvent(self,event):
        reply = QMessageBox.question(self,'Attention','Êtes vous sûr de vouloir quitter la liseuse.',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)

        if reply == QMessageBox.Yes :
            qApp.quit()
        else :
            try:
                event.ignore()
            except AttributeError:
                pass



    def afficher_onglets(self):
        self.tabs=QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setTabsClosable(True)

        nom = ""
        for i in self.filename[::-1]:
            if i == "/" : break
            nom += i
        nom = nom[::-1]

        for i in self.BDtabs:
            self.tabs.addTab(p.Page(i), nom[0:-4])
            self.setCentralWidget(self.tabs)


    def lire_bibliotheque(self):
        file = open("biblio.txt", 'r')
        biblio = file.read()
        T = [[]]
        a = ''
        lv = 0
        for i in biblio :
            a+= i
            if i =='$':
                a = a[0:-1]
                T[lv].append(a)
                a = ''
            if i == "\n":
                a = a[0:-1]
                T[lv].append(a)
                a = ''
                T.append([])
                lv+=1
        return T
    def afficher_biblio(self, T=None):
        T = self.lire_bibliotheque()
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setRowCount(len(T))

        self.tableWidget.setItem(0, 0, QTableWidgetItem("cover"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("source"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("title"))
        self.tableWidget.setItem(0, 3 , QTableWidgetItem("author"))
        self.tableWidget.setItem(0, 4 , QTableWidgetItem("creation_time"))
        self.tableWidget.setItem(0, 5 , QTableWidgetItem("year"))
        self.tableWidget.setItem(0, 6 , QTableWidgetItem("tags"))
        self.tableWidget.setItem(0, 7 , QTableWidgetItem("quality"))
        self.tableWidget.setItem(0, 8 , QTableWidgetItem("ouvrir"))
        self.tableWidget.setItem(0, 9 , QTableWidgetItem("editer"))
        self.tableWidget.setItem(0, 10 , QTableWidgetItem("delete"))
        header = self.tableWidget.verticalHeader()
        for i in range(len(T)-1):
            self.btn = QAction("lire " + T[i][2], self)
            self.btn.triggered.connect(self.lire)
            self.btn.setStatusTip("Lire cette Ouvrage")
            self.menuLire.addAction(self.btn)

            for j in range(len(T[i])+10):
                if j == 0 :
                    info = QVBoxLayout()
                    h = QHBoxLayout()
                    n = 0
                    txt = ''
                    self.label = QLabel()
                    self.pixmap= QPixmap("./"+str(T[0][2])+ "/" + T[0][0])
                    self.scaledPixmap= self.pixmap.scaledToWidth(self.width() * 0.1)
                    self.label.setPixmap(self.scaledPixmap)
                    info = QLabel(txt)
                    h.addWidget(self.label)
                    h.addWidget(info)
                    widget = QWidget()
                    widget.setLayout(h)
                    self.tableWidget.setCellWidget(i+1, j, widget)
                    header.setSectionResizeMode(i+1, QHeaderView.Stretch)

                elif j == len(T)+6:
                    self.btn = QPushButton("lire\n" + str(T[i][2]))
                    self.btn.clicked.connect(self.lire)
                    self.tableWidget.setCellWidget(i+1, j, self.btn)

                elif j == len(T)+7:
                    self.btn = QPushButton("editer\n"+ str(T[i][2]))
                    self.btn.clicked.connect(self.editer)
                    self.tableWidget.setCellWidget(i+1, j, self.btn)

                elif j >= len(T)+8:
                    self.btn = QPushButton("delete")
                    #self.btn.clicked.connect(self.delete)
                    self.tableWidget.setCellWidget(i+1, j, self.btn)

                elif j<len(T)+6:
                    self.tableWidget.setItem(i+1, j, QTableWidgetItem(T[i][j]))

            self.vBoxLayout = QVBoxLayout()
            self.vBoxLayout.addWidget(self.tableWidget)
            widget = QWidget()
            widget.setLayout(self.vBoxLayout)
            self.setCentralWidget(widget)

    def editer(self):
        texte = self.sender().text()
        self.filename = texte[7:len(texte)]
        T = self.lire_bibliotheque()
        for i in T :
            for j in i :
                if j == self.filename :
                    book = T.index(i)
                    break
        widget = QWidget()
        qv = QVBoxLayout()
        qv.addWidget(QLabel("titre"))
        titre = QLineEdit()
        titre.setText(T[book][2])
        qv.addWidget(titre)
        qv.addWidget(QLabel("auteur"))
        author = QLineEdit()
        author.setText(T[book][3])
        qv.addWidget(author)
        qv.addWidget(QLabel("date de création"))
        creation_time = QLineEdit()
        creation_time.setText(T[book][4])
        qv.addWidget(creation_time)
        qv.addWidget(QLabel("année"))
        year = QLineEdit()
        year.setText(T[book][5])
        qv.addWidget(year)
        qv.addWidget(QLabel("tags"))
        self.tag = QLineEdit()
        self.tag.setText(T[book][6])
        add = QPushButton("ajouter")
        qv.addWidget(self.tag)
        qv.addWidget(add)
        qv.addWidget(QLabel("Quality"))
        quality = QLineEdit()
        quality.setText(T[book][7])
        qv.addWidget(quality)
        qv.addWidget(QLabel("source"))
        source = QPushButton("source")
        source.clicked.connect(self.changer_source)
        qv.addWidget(source)
        annuler = QPushButton("annuler")
        valider = QPushButton("valider")
        qh = QHBoxLayout()
        qh.addWidget(annuler)
        qh.addWidget(valider)
        w = QWidget()
        w.setLayout(qh)
        qv.addWidget(w)
        widget.setLayout(qv)
        self.setCentralWidget(widget)

    def changer_source(self):
        dialogue = QFileDialog()
        self.source_temp = dialogue.getOpenFileName(self,'Ouvrir fichier',filter='Comic Book Zip (*.cbz);;Comic Book Rar (*.cbr)')[0]


    def charger(self):
        dialogue = QFileDialog()
        self.filename = dialogue.getOpenFileName(self,'Ouvrir fichier',filter='Comic Book Zip (*.cbz);;Comic Book Rar (*.cbr)')[0]
        livre = c.COMICParser(self.filename)
        livre.read_book()
        livre.generate_metadata(author='<Unknown>', isbn = None, tags=[], quality=0, src=self.filename)
        self.BDtabs.append(self.filename)
        self.afficher_onglets()

    def lire(self):
        texte = self.sender().text()
        self.filename = texte[5:len(texte)]
        T = self.lire_bibliotheque()
        for i in T :
            for j in i :
                if j == self.filename :
                    emplacement = T[T.index(i)][1]
                    break
        livre = c.COMICParser(emplacement)
        livre.read_book()
        self.BDtabs.append(emplacement)
        self.afficher_onglets()





app = QCoreApplication.instance()
if app == None:
    app = QApplication([''])

window = FenetrePrincipale()
window.show()

app.exec()

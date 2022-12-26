from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import sys, sqlite3, random, datetime, dics, utils

conn = sqlite3.connect('verbs.db')
personen = ["1PS","2PS", "3PS", "1PP", "2PP", "3PP"]


currentExerciseID = -1

class abfrageFenster(QMainWindow):
    def __init__(self, lang, tenses, verbs, parent=None):
        super(abfrageFenster, self).__init__(parent)

        icon = QIcon()
        sers = QPixmap("icon.svg")
        icon.addPixmap(sers)
        self.setWindowIcon(icon)

        self.verbs = verbs
        self.lang = lang
        self.tenses = tenses

        self.setWindowTitle("Verbkonjugation")
        self.cform = ""
        self.cverb = ""
        self.ctense = ""

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.gridLayoutEingabe = QGridLayout()
        # Verb eingeben
        self.lblVerb1 = QLabel("Verb:")
        self.gridLayoutEingabe.addWidget(self.lblVerb1, 0, 0)
        self.lblVerb2 = QLabel("Fehler.")
        self.gridLayoutEingabe.addWidget(self.lblVerb2, 0, 1)

        # Verform
        self.lblVerbform1 = QLabel("Verbform:")
        self.gridLayoutEingabe.addWidget(self.lblVerbform1, 1, 0)
        self.lblVerbform2 = QLabel("Fehler.")
        self.gridLayoutEingabe.addWidget(self.lblVerbform2, 1, 1)

        # Zeitform
        self.lblZeitform1 = QLabel("Zeitform:")
        self.gridLayoutEingabe.addWidget(self.lblZeitform1, 2, 0)
        self.lblZeitform2 = QLabel("Fehler.")
        self.gridLayoutEingabe.addWidget(self.lblZeitform2, 2, 1)

        # Eingabe
        self.lblPronomen = QLabel("Fehler.")
        myFont=QFont()
        myFont.setBold(True)
        self.lblPronomen.setFont(myFont)
        self.gridLayoutEingabe.addWidget(self.lblPronomen, 3, 1)
        self.tbEingabe = QLineEdit()
        self.gridLayoutEingabe.addWidget(self.tbEingabe, 3, 2)

        # Button und Feedback
        self.btnEingabe = QPushButton("Eingabe")
        self.btnEingabe.clicked.connect(self.loadFeedback)
        self.tbEingabe.returnPressed.connect(self.btnEingabe.click)
        self.btnNextVerb = QPushButton("Nächstes Verb...")
        self.btnNextVerb.setVisible(False)
        self.btnNextVerb.clicked.connect(self.loadNewVerb)
        
        self.btnAnalysis = QPushButton("Beenden und analysieren")
        self.btnAnalysis.clicked.connect(analasys)

        self.gLayout2 = QGridLayout()
        self.gLayout2.addWidget(self.btnEingabe, 0, 1)
        self.gLayout2.addWidget(self.btnNextVerb, 0, 1)
        self.gLayout2.addWidget(self.btnAnalysis, 1, 1)
        self.lblFeedback = QLabel()
        self.lblFeedback2 = QLabel()
        self.gLayout2.addWidget(self.lblFeedback, 0, 0)
        self.gLayout2.addWidget(self.lblFeedback2, 1, 0)

        # Rest
        self.centrallayout = QVBoxLayout()
        self.centrallayout.addLayout(self.gridLayoutEingabe)
        self.centrallayout.addLayout(self.gLayout2)
        self.centralwidget.setLayout(self.centrallayout)
        self.loadNewVerb()
        self.show()

    def loadFeedback(self):
        correctForm = conjugateVerb(self.cverb, self.cform, self.ctense, self.lang)
        eingabe = self.tbEingabe.text().strip()
        if eingabe == correctForm:
            self.lblFeedback.setText("La stufa scalda bene!")
            self.lblFeedback.setStyleSheet("background-color: lime; color: black;")
            self.lblFeedback2.setText("")
            writeToResults(correctForm, eingabe, True)
        else:
            self.lblFeedback.setText(f'Che schifo!')
            self.lblFeedback.setStyleSheet("background-color: rgb(250, 52, 52); color: white;")
            self.lblFeedback2.setText(f'Coretto: {utils.highlight_differences(correctForm, eingabe)}')
            writeToResults(correctForm, eingabe, False)

        # Die Feedbackform wird geladen, die Eingabeform rausgeladen
        self.tbEingabe.setReadOnly(True)
        self.tbEingabe.setStyleSheet("background-color: lightgray;")
        try: self.tbEingabe.returnPressed.disconnect(self.btnEingabe.click)
        except: pass
        self.tbEingabe.returnPressed.connect(self.btnNextVerb.click)
        self.btnEingabe.setVisible(False)
        self.btnNextVerb.setVisible(True)

    def loadNewVerb(self):
        for i in [self.lblFeedback, self.lblFeedback2]:
            i.setText("")
            i.setStyleSheet("")
        rVerb = getRandomVerb(self.verbs, dics.personcount[self.lang], self.tenses)
        # ['sentire', 1, 'passato prossimo']
        self.cverb = rVerb[0]
        self.lblVerb2.setText(self.cverb)
        self.cform = rVerb[1]
        self.cformF = dics.personDict[self.lang][self.cform]
        self.lblVerbform2.setText(self.cformF)
        self.ctense = rVerb[2]
        self.lblZeitform2.setText(self.ctense)
        self.lblPronomen.setText(dics.pronomenDic[self.lang][self.cform])
        curc = conjugateVerb(self.cverb, self.cform, self.ctense, self.lang)
        if "_" in curc:
            print("<<<<< FEHLER >>>>>")
            print(curc)
            print("^^^^^^^^^^^^^^^^^^")
        #try: print(conjugateVerb(self.cverb, self.cform, self.ctense))
        #except: print("Error while conjugating")

        # Die Eingabeform wird geladen, die Feedbackform rausgeladen
        try: self.tbEingabe.returnPressed.disconnect(self.btnNextVerb.click)
        except: pass
        self.tbEingabe.returnPressed.connect(self.btnEingabe.click)
        self.tbEingabe.setText("")
        self.tbEingabe.setReadOnly(False)
        self.tbEingabe.setStyleSheet("background-color: white;")
        self.btnNextVerb.setVisible(False)
        self.btnEingabe.setVisible(True)

class mainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        # Willkommen
        self.lblWelcome = QLabel("<h1>Wilkommen.</h1>")
        # Sprache
        self.lblChooseLang = QLabel("Bitte Wählen Sie ihre Sprache aus.")
        self.comboBoxLang = QComboBox()
        self.loadLangs(self.comboBoxLang)
        # Verben
        self.lblVerbs = QLabel("Bitte wählen Sie hier Ihre Verben aus:")
        self.listBoxVerbs = QListWidget()
        self.btnMostImportantVerbs = QPushButton("10 Wichtigste")
        self.btnMostImportantVerbs.clicked.connect(self.selectVIPVerbs)
        self.btnNoVerbs = QPushButton("Keins")
        self.btnNoVerbs.clicked.connect(self.UncheckAllVerbs)
        self.btnAllVerbs = QPushButton("Alle")
        self.btnAllVerbs.clicked.connect(self.CheckAllVerbs)
        self.hlayoutverboptions = QHBoxLayout()
        self.hlayoutverboptions.addWidget(self.btnMostImportantVerbs)
        self.hlayoutverboptions.addWidget(self.btnNoVerbs)
        self.hlayoutverboptions.addWidget(self.btnAllVerbs)
        self.comboBoxLang.currentTextChanged.connect(self.loadVerbs)
        self.comboBoxLang.currentTextChanged.connect(self.loadTenses)
        self.loadVerbs()
        # Zeiten
        self.lblTenses = QLabel("Wählen Sie hier bitte die abzufragenden Zeiten aus:")
        self.listBoxTenses = QListWidget()
        self.btnNoTenses = QPushButton("Keine")
        self.btnAllTenses = QPushButton("Alle")
        self.btnNoTenses.clicked.connect(self.UncheckAllTenses)
        self.btnAllTenses.clicked.connect(self.CheckAllTenses)
        self.hlayouttenseoptions = QHBoxLayout()
        self.hlayouttenseoptions.addWidget(self.btnAllTenses)
        self.hlayouttenseoptions.addWidget(self.btnNoTenses)
        self.loadTenses()

        # Go
        self.btnGo = QPushButton("Los")
        self.btnGo.clicked.connect(self.go)

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.lblWelcome)
        self.vlayout.addWidget(self.lblChooseLang)
        self.vlayout.addWidget(self.comboBoxLang)
        self.vlayout.addWidget(self.lblVerbs)
        self.vlayout.addWidget(self.listBoxVerbs)
        self.vlayout.addLayout(self.hlayoutverboptions)
        self.vlayout.addWidget(self.lblTenses)
        self.vlayout.addWidget(self.listBoxTenses)
        self.vlayout.addLayout(self.hlayouttenseoptions)
        self.vlayout.addWidget(self.btnGo)
        self.centralwidget.setLayout(self.vlayout)
        
        self.show()
    
    def CheckAllTenses(self):
        for i in self.tenseItems:
            i.setCheckState(Qt.CheckState.Checked)
    def UncheckAllTenses(self):
        for i in self.tenseItems:
            i.setCheckState(Qt.CheckState.Unchecked)
    def UncheckAllVerbs(self):
        for i in self.verbListItems:
            i.setCheckState(Qt.CheckState.Unchecked)
    def CheckAllVerbs(self):
        for i in self.verbListItems:
            i.setCheckState(Qt.CheckState.Checked)
    def loadLangs(self, cb: QComboBox):
        for i in dics.supported_languages.keys():
            cb.addItem(i)
        self.currentlang = dics.supported_languages[cb.currentText()]
    def selectVIPVerbs(self):
        # Alle Verben deaktivieren und nur die wichtigsten (dics.most_important_verbs) aktivieren
        vipverbs = dics.most_important_verbs[self.currentlang]
        for i in self.verbListItems:
            i.setCheckState(Qt.CheckState.Unchecked)
            if i.text() in vipverbs:
                i.setCheckState(Qt.CheckState.Checked)
    def loadVerbs(self):
        self.currentlang = dics.supported_languages[self.comboBoxLang.currentText()]
        self.listBoxVerbs.clear()
        cur = conn.cursor()
        cur.execute(f'SELECT infinitive FROM {dics.supported_languages[self.comboBoxLang.currentText()]}')
        res = cur.fetchall()
        self.verbListItems = []
        for i in range(len(res)):
            self.verbListItems.insert(i, QListWidgetItem(self.listBoxVerbs))
            self.verbListItems[i].setText(res[i][0])
            self.verbListItems[i].setCheckState(Qt.CheckState.Checked)

        self.listBoxVerbs.sortItems(Qt.SortOrder.AscendingOrder)
    def loadTenses(self):
        self.listBoxTenses.clear()
        lang = dics.supported_languages[self.comboBoxLang.currentText()]
        tenses = dics.tenses[lang]
        self.tenseItems = []
        for i in range(len(tenses)):
            self.tenseItems.insert(i, QListWidgetItem(self.listBoxTenses))
            self.tenseItems[i].setText(dics.tensenames[lang][tenses[i]])
            self.tenseItems[i].setCheckState(Qt.CheckState.Checked)

    def go(self):
        golang = self.currentlang
        goverbs = []
        for i in self.verbListItems:
            if i.checkState() == Qt.CheckState.Checked:
                goverbs.append(i.text())
        gotenses = []
        for i in self.tenseItems:
            if i.checkState() == Qt.CheckState.Checked:
                currentTenseName = getTenseIDByName(i.text(), golang)
                gotenses.append(currentTenseName)

        aw = abfrageFenster(golang, gotenses, goverbs, self)
        aw.show()

def getTenseIDByName(tensename, lang):
        dic = dics.tensenames
        for i in dic[lang].keys():
            sers = dic[lang][i]
            if sers == tensename:
                return i

def getCExerciseID() -> int:
    cur = conn.cursor()
    res = cur.execute("SELECT MAX(exercise_id) FROM results")
    res = res.fetchone()[0]
    if res in [None, 0]: currentExerciseID = 1
    else: currentExerciseID = res+1
    return(currentExerciseID)

def writeToResults(verb, input, success):
    global currentExerciseID
    if currentExerciseID in [-1, None]: currentExerciseID = getCExerciseID()
    cur = conn.cursor()
    if success == True: success2 = 1
    elif success == False: success2 = 0
    sql = f'INSERT INTO results (exercise_id, verb, input, correct, timestamp) '
    sql += f'VALUES ({currentExerciseID}, "{verb}", "{input}", {success2}, "{datetime.datetime.now().isoformat()}")'
    cur.execute(sql)
    conn.commit()

def getRandomVerb(inputVerbs, inputPersons, inputTenses):
    idRandomVerb = random.randint(0, len(inputVerbs)-1)
    idRandomPerson = random.randint(0, inputPersons-1)
    idRandomTense = random.randint(0, len(inputTenses)-1)

    return([inputVerbs[idRandomVerb], idRandomPerson, inputTenses[idRandomTense]])

def conjugateVerb(infinitive, person, tense, lang):
    cur = conn.cursor()
    #ntense = getTenseIDByName(tense, lang)
    #except KeyError: ntense = tense
    ntense = tense
    nperson = ""
    try: nperson = dics.personenDictDB[lang][person]
    except: pass
    spalte = f'"{ntense}_{nperson}"'
    cur.execute(f'SELECT {spalte} from {lang} WHERE infinitive="{infinitive}"')
    resp = cur.fetchone()
    return(resp[0])

def analasys():
    if currentExerciseID in [-1, None]: return
    cur = conn.cursor()
    cur.execute(f'SELECT verb, input, correct FROM results WHERE exercise_id={currentExerciseID}')
    res = cur.fetchall()

    self = QDialog()
    self.centrallayout = QVBoxLayout()
    self.setLayout(self.centrallayout)
    
    correctCount = 0
    wrongCount = 0
    totalCount = 0
    for i in res:
        totalCount += 1
        if i[2] == 0: wrongCount +=1
        else: correctCount += 1

    # Überschrift und Text
    restext = f"Insgesamt haben Sie <b>{totalCount}</b> Verben geübt.\n" 
    restext += f"Davon waren <b>{wrongCount}</b> falsch, <b>{correctCount}</b> richtig."
    self.lblHeader = QLabel("<h2> Auswertung </h2>")
    self.lblResults = QLabel()
    self.lblResults.setText(restext)
    self.centrallayout.addWidget(self.lblHeader)
    self.centrallayout.addWidget(self.lblResults)

    # TableView


    self.exec()


app = QApplication(sys.argv)
window = mainWindow()
window.show()
app.exec()
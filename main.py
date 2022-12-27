from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import sys, sqlite3, random, datetime, dics, utils, json

conn = sqlite3.connect('verbs.db')
currentExerciseID = -1

class menuButton(QPushButton):
    def __init__(self, caption, actions, parent=None):
        super().__init__(parent)
        
        self.setText(caption)

        # Erstelle ein QMenu-Objekt und füge Einträge hinzu
        self.menu = QMenu(self)
        for i in actions:
            self.menu.addAction(f'{i}')
        
        # Weise das QMenu dem Button mit der Methode setMenu zu
        self.setMenu(self.menu)

    def clearMenuItems(self):
        self.menu.clear()
    def newAction(self, str):
        self.menu.addAction(f'{str}')

class QLine(QFrame):
    def __init__(self, parent=None):
        super(QLine, self).__init__(parent)
        self.setObjectName(u"line")
        self.setGeometry(QRect(130, 150, 471, 51))
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)

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
        self.gridLayoutEingabe.addWidget(QLine(self), 3, 0, 1, 3)

        # Eingabe
        self.lblPronomen = QLabel("Fehler.")
        myFont=QFont()
        myFont.setBold(True)
        self.lblPronomen.setFont(myFont)
        self.gridLayoutEingabe.addWidget(self.lblPronomen, 4, 0)
        self.tbEingabe = QLineEdit()
        self.gridLayoutEingabe.addWidget(self.tbEingabe, 4, 1)

        # Button und Feedback
        self.btnEingabe = QPushButton("Eingabe")
        self.btnEingabe.clicked.connect(self.loadFeedback)
        self.tbEingabe.returnPressed.connect(self.btnEingabe.click)
        self.btnNextVerb = QPushButton("Nächstes Verb...")
        self.btnNextVerb.setVisible(False)
        self.btnNextVerb.clicked.connect(self.loadNewVerb)
        
        self.btnAnalysis = QPushButton("Beenden und analysieren")
        self.btnAnalysis.clicked.connect(analasys)

        self.gridLayoutEingabe.addWidget(self.btnEingabe, 5, 1)
        self.gridLayoutEingabe.addWidget(self.btnNextVerb, 5, 1)
        self.gridLayoutEingabe.addWidget(self.btnAnalysis, 6, 1)
        self.lblFeedback = QLabel()
        self.lblFeedback2 = QLabel()
        self.gridLayoutEingabe.addWidget(self.lblFeedback, 5, 0)
        self.gridLayoutEingabe.addWidget(self.lblFeedback2, 6, 0)

        # Rest
        self.centrallayout = QVBoxLayout()
        self.centrallayout.addLayout(self.gridLayoutEingabe)
        self.centralwidget.setLayout(self.centrallayout)
        self.loadNewVerb()
        self.show()
    def loadFeedback(self):
        correctForm = conjugateVerb(self.cverb, self.cform, self.ctense, self.lang)
        eingabe = self.tbEingabe.text().strip()

        # Falls keine Eingabe, mittels MessageBox nach Bestätigung fragen
        if eingabe in [" ", "", None]:
            if self.confirmDialog() != True:
                return False

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
    def confirmDialog(self) -> bool:
        msgBox = QMessageBox()
        ret = msgBox.question(self, "Bestätigen?", "Ihre Eingabe scheint leer zu sein. Wollen Sie fortfahren?")
        if ret == 16384:
            return True
        else:
            return False
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
        self.lblZeitform2.setText(dics.tensenames[self.lang][self.ctense])
        self.lblPronomen.setText(dics.pronomenDic[self.lang][self.cform])
        curc = conjugateVerb(self.cverb, self.cform, self.ctense, self.lang)
        print(curc)
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
        # Presets
        self.btnPresets = menuButton("Preset laden...", ["Keine Presets vorhanden"], self)
        self.loadPresets()
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

        # Preset speichern
        self.btnSavePreset = QPushButton("Als Preset speichern")
        self.btnSavePreset.clicked.connect(self.savePreset)
        self.btnSavePreset.setToolTip("Hiermit können Sie die aktuell ausgewählten Zeitformen\n" +
            "und Verben in einem Preset speichern,\num sie später ganz einfach wieder zu laden\n" +
            "und damit einfach bestimmte Vokabeln festigen.")

        # Go
        self.btnGo = QPushButton("Los")
        self.btnGo.clicked.connect(self.go)

        # Layouts
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.lblWelcome)
        self.vlayout.addWidget(self.btnPresets)
        self.vlayout.addWidget(self.lblChooseLang)
        self.vlayout.addWidget(self.comboBoxLang)
        self.vlayout.addWidget(self.lblVerbs)
        self.vlayout.addWidget(self.listBoxVerbs)
        self.vlayout.addLayout(self.hlayoutverboptions)
        self.vlayout.addWidget(self.lblTenses)
        self.vlayout.addWidget(self.listBoxTenses)
        self.vlayout.addLayout(self.hlayouttenseoptions)
        self.vlayout.addWidget(self.btnSavePreset)
        self.vlayout.addWidget(self.btnGo)
        self.centralwidget.setLayout(self.vlayout)

        # Icon & Titel
        icon = QIcon()
        iconPixmap = QPixmap("icon.svg")
        icon.addPixmap(iconPixmap)
        self.setWindowIcon(icon)
        self.setWindowTitle("Verbtrainer")
        
        self.show()
    def loadPreset(self, presetName):
        cur = conn.cursor()
        cur.execute(f'SELECT settings FROM presets WHERE name="{presetName}"')
        res = cur.fetchone()[0]
        try:
            preset = json.loads(res)
            self.comboBoxLang.setCurrentText(dics.supported_languages_2[preset["lang"]])
            for i in self.verbListItems:
                i.setCheckState(Qt.CheckState.Unchecked)
            for i in preset["verbs"]:
                for y in self.verbListItems:
                    if y.text() == i:
                        y.setCheckState(Qt.CheckState.Checked)
            # Tenses
            for i in self.tenseItems:
                i.setCheckState(Qt.CheckState.Unchecked)
            for i in preset["tenses"]:
                for y in self.tenseItems:
                    if getTenseIDByName(y.text(), preset["lang"]) == i:
                        y.setCheckState(Qt.CheckState.Checked)
        except Exception as e: 
            print(e)
            msgBox = QMessageBox()
            msgBox.warning(None, "Fehlerhafte Speicherung", \
                "Achtung: Das Preset ist fehlerhaft gespeichert worden. Der Vorgang wurde abgebrochen", \
                    QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
    def savePreset(self):
        presetName = []
        presetTenses = []
        presetVerbs = []
        presetLang = dics.supported_languages[self.comboBoxLang.currentText()]
        presetName = ""
        text, ok = QInputDialog().getText(self, "Name des Presets",
                                     "Bitte geben Sie hier den Namen des Presets ein:", 
                                     QLineEdit.EchoMode.Normal)
        if text and ok: 
            presetName = text
        else:
            h = QMessageBox()
            h.setText("Sie haben keinen Presetnamen eingegeben, Aktion abgebrochen.")
            h.setWindowIcon(QIcon(QPixmap("icon.svg")))
            h.setWindowTitle("Aktion abgebrochen")
            h.exec()
            return
        for i in self.tenseItems:
            if i.checkState() == Qt.CheckState.Checked:
                presetTenses.append(getTenseIDByName(i.text(), presetLang))
        for i in self.verbListItems:
            if i.checkState() == Qt.CheckState.Checked:
                presetVerbs.append(i.text())
        presetSettings = json.dumps({"lang": presetLang, "verbs": presetVerbs, "tenses": presetTenses})
        cur = conn.cursor()
        sql = f'INSERT INTO presets (name, settings, saved) '
        sql += f"VALUES ('{presetName}', '{str(presetSettings)}', '{datetime.datetime.now().isoformat()}')"
        try:
            cur.execute(sql)
            conn.commit()
            self.loadPresets()
        except sqlite3.IntegrityError: # Falls Preset bereits vorhanden
            yn = QMessageBox().question(None, "Achtung", "Es ist schon ein Preset mit diesem Namen vorhanden. Wollen Sie es überschreiben?")
            if yn == 16384: # Falls ja geklickt wurde
                try:
                    sql = f"UPDATE presets SET settings='{str(presetSettings)}', saved='{datetime.datetime.now().isoformat()}'"
                    sql += f"WHERE name='{presetName}'"
                    print(sql)
                    cur.execute(sql)
                    conn.commit()
                    self.loadPresets()
                except: 
                    QMessageBox().warning(None, "Fehler", "Fehler beim Speichern.")
    def loadPresets(self):
        cur = conn.cursor()
        cur.execute("SELECT * FROM presets")
        res = cur.fetchall()
        if len(res) == 0: return
        self.btnPresets.clearMenuItems()
        self.presetActions = []
        for i in range(len(res)):
            def create_action(i):
                action = QAction(res[i][0])
                action.triggered.connect(lambda:self.loadPreset(res[i][0]))
                return action
            self.presetActions.insert(i, create_action(i))
            self.btnPresets.menu.addAction(self.presetActions[i])
    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        newAct = contextMenu.addAction("New")
        openAct = contextMenu.addAction("Open")
        quitAct = contextMenu.addAction("Quit")
        action = contextMenu.exec(self.mapToGlobal(event.pos()))
        if action == quitAct:
            self.close()
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
    self.setWindowIcon(QIcon(QPixmap("icon.svg")))
    self.setWindowTitle("Ergebnisauswertung")

    # TableView
    self.table = QTableWidget()
    self.table.verticalHeader().setVisible(False)
    self.table.horizontalHeader().setVisible(True)
    self.table.setColumnCount(3)
    self.table.setHorizontalHeaderLabels(["Korrekt", "Eingabe", "Status"])
    self.table.setRowCount(totalCount)  
    for i in range(totalCount):
        self.table.setItem(i, 0, QTableWidgetItem(res[i][0]))
        self.table.setItem(i, 1, QTableWidgetItem(res[i][1]))
        cor = ""
        if res[i][2] == 1: cor = "Richtig"
        if res[i][2] == 0: cor = "Falsch"
        self.table.setItem(i, 2, QTableWidgetItem(cor))
        self.table.setRowHeight(i, 16)
    self.centrallayout.addWidget(self.table)

    self.exec()


app = QApplication(sys.argv)
window = mainWindow()
window.show()
app.exec()
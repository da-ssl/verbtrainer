from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import sys, sqlite3, random, datetime, difflib, utils

conn = sqlite3.connect('verbs.db')
zeiten = ["presente", "futuro", "passato prossimo","imperfetto","congiuntivo"]
personen = ["1PS","2PS", "3PS", "1PP", "2PP", "3PP"]
personenDic = {
    "1PS": "1. Person Singular",
    "2PS": "2. Person Singular",
    "3PS": "3. Person Singular",
    "1PP": "1. Person Plural",
    "2PP": "2. Person Plural",
    "3PP": "3. Person Plural"
}
pronomenDic = {
    "1PS": "io",
    "2PS": "tu",
    "3PS": "lei/lui",
    "1PP": "noi",
    "2PP": "voi",
    "3PP": "loro"
}
currentExerciseID = -1

class abfrageFenster(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        icon = QIcon()
        sers = QPixmap("icon.svg")
        icon.addPixmap(sers)
        self.setWindowIcon(icon)


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
        correctForm = conjugateVerb(self.cverb, self.cform, self.ctense)
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
        rVerb = getRandomVerb()
        self.cverb = rVerb[0]
        self.lblVerb2.setText(self.cverb)
        self.cform = rVerb[1]
        self.cformF = personenDic[rVerb[1]]
        self.lblVerbform2.setText(self.cformF)
        self.ctense = rVerb[2]
        self.lblZeitform2.setText(self.ctense)
        self.lblPronomen.setText(pronomenDic[rVerb[1]])
        print(conjugateVerb(self.cverb, self.cform, self.ctense))

        # Die Eingabeform wird geladen, die Feedbackform rausgeladen
        try: self.tbEingabe.returnPressed.disconnect(self.btnNextVerb.click)
        except: pass
        self.tbEingabe.returnPressed.connect(self.btnEingabe.click)
        self.tbEingabe.setText("")
        self.tbEingabe.setReadOnly(False)
        self.tbEingabe.setStyleSheet("background-color: white;")
        self.btnNextVerb.setVisible(False)
        self.btnEingabe.setVisible(True)

def getCExerciseID() -> int:
    cur = conn.cursor()
    res = cur.execute("SELECT MAX(exercise_id) FROM results")
    res = res.fetchone()[0]
    if res in [None, 0]: currentExerciseID = 1
    else: currentExerciseID = res+1
    print(currentExerciseID)
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

def getRandomVerb():
    
    cur = conn.cursor()
    cur.execute('SELECT infinitivo FROM it')
    resp = cur.fetchall()

    anzahlVerben = len(resp)-1
    idRandomVerb = random.randint(0,anzahlVerben)
    
    idRandomPerson = random.randint(0, 5)
    idRandomTense = random.randint(0, 4)

    done = [resp[idRandomVerb][0], personen[idRandomPerson], zeiten[idRandomTense]]
    
    return(done)

def conjugateVerb(infinitive, person, tense):
    cur = conn.cursor()
    spalte = f'"{person} {tense}"'
    cur.execute(f'SELECT {spalte} from it WHERE infinitivo="{infinitive}"')
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
window = abfrageFenster()
window.show()
app.exec()
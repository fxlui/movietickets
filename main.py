#!python3.6
# @imnotpopo

# Importing modules
import sys, csv, base64, re
from PyQt5 import uic, QtCore, QtWidgets, QtGui, QtWebEngineWidgets
from PyQt5.QtWidgets import (QWidget, QApplication, QMessageBox)
from PyQt5.QtGui import QPixmap

# Read CSV files, create lists
movieDetails = []
cinemaDetails = []
sessionDetails = []
with open('file.csv', encoding="utf-8") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',', quotechar = '"')
    for row in readCSV:
        movieDetails.append( (row[ 0 ],row[ 1 ],row[ 2 ],row[ 3 ],row[ 4 ]) )
movieNumbers = movieDetails[-1]
movieNumbers = int(movieNumbers[0]) + 1
with open('cinema.csv', encoding="utf-8") as csvfile:
    readCSV2 = csv.reader(csvfile, delimiter=',', quotechar = '"')
    for row in readCSV2:
        cinemaDetails.append(row)
with open('session.csv', encoding="utf-8") as csvfile:
    readCSV3 = csv.reader(csvfile, delimiter=',', quotechar = '"')
    for row in readCSV3:
        sessionDetails.append(row)
global ifcinema, ifmovie
ifcinema = -1
ifmovie = -1

# Used for sorting lists
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]

class Ui(QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)
        # Load logo
        mainlogo = QPixmap('images/logo.svg')
        self.logo.setPixmap(mainlogo)
        # Load movie posters and titles
        for movieorder, movienames, moviedesc, movielink, mrating in movieDetails:
            movieorder = int(movieorder)
            self.setInfo(movieorder, movienames, moviedesc, movielink, mrating)
        # Load cinema info
        self.mapbox = QtWebEngineWidgets.QWebEngineView(self.cinemaShow)
        self.mapbox.setGeometry(QtCore.QRect(25, 50, 351, 211))
        for cid, name, desc, phone, address, mapid in cinemaDetails:
            self.dropdown.addItem(name)
        self.cineInfo(cinemaDetails)
        self.dropdown.currentTextChanged.connect(lambda: self.cineInfo(cinemaDetails))
        # Set area of Scroll Area 1
        scrollSize = int(movieNumbers) * 185 + 14
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(scrollSize,0))
        # Load the first tab
        if ifmovie == -1:
            self.tabWidget.setCurrentWidget(self.nowShow)
        else:
            self.tabWidget.setCurrentWidget(self.cinemaShow)
        self.show()

    def setInfo(self, mnum, mname, mdesc, mlink, mrating):
        # Creates poster and title automatically
        poster = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        poster.setObjectName('poster%d' % mnum)
        posImage = QPixmap('images/%d.jpg' % mnum)
        poster.setIcon(QtGui.QIcon(posImage))
        poster.setIconSize(posImage.rect().size())
        poster.setFixedSize(posImage.rect().size())
        if mnum == 0:
            posLength = 0
        else:
            posLength = mnum * 185
        posLength = 13 + posLength
        poster.setGeometry(QtCore.QRect(posLength, 10, 185, 281))
        posName = mname
        poster.setToolTip(posName)
        poster.clicked.connect(lambda: self.movInfo(mnum, mname, mdesc, mlink, mrating))

    def cineInfo(self, clist):
        c = self.dropdown.currentIndex()
        if c == -1:
            c = 0
        else:
            pass
        infol = clist[c]
        # Remove previous linked connections
        try: self.buyButton.clicked.disconnect()
        except Exception: pass
        self.buyButton.clicked.connect(lambda: self.buyTic(ifmovie, c))
        self.cinemaNam.setText(infol[1])
        self.cinemaDes.setText(infol[2])
        self.cinemaPho.setText(infol[3])
        self.cinemaAdd.setText(infol[4])
        mapurl = """<iframe width="336" height="196" frameborder="0" style="border:0" 
        src="https://www.google.com/maps/embed/v1/place?q=%s"></iframe>""" % infol[5]
        self.mapbox.setHtml(mapurl)

    def movInfo(self, order, name, desc, link, rating):
        # Load movie info UI
        self.close()
        super(Ui, self).__init__()
        uic.loadUi('movinfo.ui', self)
        # Initalize poster, name, desc
        posImage = QPixmap('images/%d.jpg' % order)
        self.poster.setPixmap(posImage)
        self.poster.setFixedSize(posImage.rect().size())
        self.filmName.setText(str(name) + "(" + str(rating) + ")")
        self.filmDesc.setText(str(desc))
        # Create trailer video widget
        self.video = QtWebEngineWidgets.QWebEngineView(self.trailerTab)
        self.video.setGeometry(QtCore.QRect(0, 0, 761, 381))
        self.video.setUrl(QtCore.QUrl("https://www.youtube.com/embed/" + link))
        self.video.setObjectName("video")
        self.backButton.clicked.connect(self.returnHome)
        # Set window title to the movie name
        windowTitle = "Movie Details - " + str(name) + "(" + str(rating) + ")"
        window.setWindowTitle(windowTitle)
        if ifcinema == -1:
            self.selectMovie = QtWidgets.QPushButton(self.infoTab)
            self.selectMovie.setGeometry(QtCore.QRect(510, 330, 231, 41))
            self.selectMovie.setObjectName("selectMovie")
            self.selectMovie.setText("Select this movie")
            try: self.selectMovie.clicked.disconnect()
            except Exception: pass
            self.selectMovie.clicked.connect(lambda: self.buyTic(order, ifcinema))
        else:
            self.buyTickets = QtWidgets.QPushButton(self.infoTab)
            self.buyTickets.setGeometry(QtCore.QRect(510, 330, 231, 41))
            self.buyTickets.setObjectName("buyTickets")
            self.buyTickets.setText("Buy Tickets Now!")
            try: self.buyTickets.clicked.disconnect()
            except Exception: pass
            self.buyTickets.clicked.connect(lambda: self.buyTic(order, ifcinema))
        self.show()

    def buyTic(self, mindex, cindex):
        # Check if movie/cinema is selected
        if mindex == -1:
            choice = QMessageBox.question(self, 'No Movie Selected!',
                "No Movie Selected. \nSelect movie now?", QMessageBox.Cancel | QMessageBox.Yes,
                 QMessageBox.Yes)
            if choice == QMessageBox.Yes:
                global ifcinema
                ifcinema = cindex
                self.tabWidget.setCurrentWidget(self.nowShow)
            elif choice == QMessageBox.Cancel:
                pass
        elif cindex == -1:
            choice = QMessageBox.question(self, 'No Cinema Selected!',
                "No Cinema Selected. \nSelect cinema now?", QMessageBox.Cancel | QMessageBox.Yes,
                 QMessageBox.Yes)
            if choice == QMessageBox.Yes:
                global ifmovie
                ifmovie = mindex
                self.returnHome()
                #self.tabWidget.setCurrentWidget(self.cinemaShow)
            elif choice == QMessageBox.Cancel:
                pass
        else:
            n = len(sessionDetails)
            ilist = []
            for i in range(n):
                forlist = sessionDetails[i]
                if forlist[0] == str(cindex) and forlist[1] == str(mindex):
                    ilist.append(i)
            # Check if there are sessions for this movie
            if not ilist:
                choice = QMessageBox.question(self, 'No sessions for this movie!',
                    "No sessions for this movie.\nPlease select a different movie/cinema.", QMessageBox.Ok, QMessageBox.Ok)
                #self.returnHome()
            else:
                self.close()
                super(Ui, self).__init__()
                uic.loadUi('payment.ui', self)
                self.filmName.setText(movieDetails[mindex][1])
                self.cinemaName.setText(cinemaDetails[cindex][1])
                self.backButton.clicked.connect(self.returnHome)
                self.continueB.clicked.connect(lambda: self.buyTic2(mindex, cindex, ilist))
                self.checkTab.setTabEnabled(1, False)
                self.checkTab.setTabEnabled(2, False)
                self.checkTab.setTabEnabled(3, False)
                self.checkTab.setTabEnabled(4, False)
                self.dateSelect.currentTextChanged.connect(lambda: self.setTime(cindex, mindex))
                for i in range(1,13):
                    if i <= 9:
                        i = "0" + str(i)
                    self.exmm.addItem(str(i))
                for i in range(17,21):
                    self.exyy.addItem(str(i))
                duplist = []
                for l in ilist:
                    forlist = sessionDetails[l]
                    duplist.append(forlist[2])
                    #self.timeSelect.addItem(forlist[3])
                dup = list(set(duplist))
                dup.sort(key=natural_keys)
                for i in list(dup):
                    self.dateSelect.addItem(i)
                self.setTime(cindex, mindex)
                for l in range(0,11):
                    for m in range(1,9):
                        ticnumbox = getattr(self, "tbox%d" % m)
                        l = str(l)
                        ticnumbox.addItem(l)
                self.show()

    def setTime(self, cid, mid):
        date = self.dateSelect.currentText()
        n = len(sessionDetails)
        timelist = []
        try: self.timeSelect.clear()
        except Exception: pass
        for i in range(n):
            forlist = sessionDetails[i]
            if forlist[0] == str(cid) and forlist[1] == str(mid) and forlist[2] == date:
                timelist.append(forlist[3])
        timelist.sort(key=natural_keys)
        for times in timelist:
            self.timeSelect.addItem(times)

    def buyTic2(self, mindex, cindex, ilist):
        ct1 = self.dateSelect.currentText()
        ct2 = self.timeSelect.currentText()
        ticlist = []
        # Check selected session
        for row in ilist:
            if ct1 == sessionDetails[row][2] and ct2 == sessionDetails[row][3]:
                details = sessionDetails[row]
        row = sessionDetails.index(details)
        sslist = sessionDetails[row]
        seatTaken = sslist[4].split("/")
        seatTaken = list(filter(None, seatTaken))
        for m in range(1,9):
            ticnumbox = getattr(self, "tbox%d" % m)
            ticnum = int(ticnumbox.currentText())
            ticlist.append(ticnum)
        # Check if conditions are met
        if ct1 == "" or ct2 == "":
            choice = QMessageBox.question(self, 'No date and time selected.',
                "No date and time selected.", 
                QMessageBox.Ok, QMessageBox.Ok)
            proceed = False
        elif sum(ticlist) > 10:
            choice = QMessageBox.question(self, 'Ticket number exceeded.',
                "Ticket number exceeded. \nYou can buy a maximum of 10 tickets per transaction.", 
                QMessageBox.Ok, QMessageBox.Ok)
            proceed = False
        elif sum(ticlist) <= 0:
            choice = QMessageBox.question(self, 'No ticket selected.',"No ticket selected.",
             QMessageBox.Ok, QMessageBox.Ok)
            proceed = False
        elif len(seatTaken) >= 18:
            choice = QMessageBox.question(self, 'Ticket number exceeded.',
                "Ticket number exceeded. \nThere are no seats available in this session.",
                 QMessageBox.Ok, QMessageBox.Ok)
            proceed = False
        elif sum(ticlist) > (18 - len(seatTaken)):
            choice = QMessageBox.question(self, 'Ticket number exceeded.',
                "Ticket number exceeded. \nThere are only %d seat(s) left in this session." % (18 - len(seatTaken)),
                 QMessageBox.Ok, QMessageBox.Ok)
            proceed = False
        else:
            proceed = True
            pass
        if proceed == True:
            pricelist = [19.00,13.00,13.00,11.50,14.50,12.00,9.50,8.50]
            self.checkTab.setTabEnabled(1, True)
            try: self.selectMovie.clicked.disconnect()
            except Exception: pass
            self.backButton_2.clicked.connect(lambda: self.checkTab.setTabEnabled(0, True))
            self.backButton_2.clicked.connect(lambda: self.checkTab.setCurrentWidget(self.timeTab))
            self.backButton_2.clicked.connect(lambda: self.checkTab.setTabEnabled(1, False))
            self.checkTab.setCurrentWidget(self.viewTab)
            self.checkTab.setTabEnabled(0, False)
            self.filmName_2.setText(movieDetails[mindex][1])
            self.cinemaName_2.setText(cinemaDetails[cindex][1])
            self.dateC.setText(ct1)
            self.timeC.setText(ct2)
            totalprice = []
            # Calculate the price of tickets chosen
            for m in range(1,9):
                ticlabel = getattr(self, "nlabel%d" % m)
                ticlabel.setText(str(ticlist[m-1]))
                ticprice = getattr(self, "tolabel%d" % m)
                price = float(ticlist[m-1]) * float(pricelist[m-1])
                ticprice.setText("$%d" % price)
                totalprice.append(price)
            totalprice = sum(totalprice)
            self.tqlabel.setText(str(sum(ticlist)))
            self.totallabel.setText("$%d" % totalprice)
            dt = [ct1, ct2]
            self.continueB2.clicked.connect(lambda: self.buyTic3(mindex, cindex, ilist, sum(ticlist), dt, seatTaken, totalprice))
    

    def buyTic3(self, mindex, cindex, ilist, ticnum, dt, st, tp):
        # Choosing Seat
        self.checkTab.setTabEnabled(1, False)
        self.checkTab.setTabEnabled(2, True)
        try: self.continueB3.clicked.disconnect()
        except Exception: pass
        self.backButton_3.clicked.connect(lambda: self.checkTab.setTabEnabled(1, True))
        self.backButton_3.clicked.connect(lambda: self.checkTab.setTabEnabled(2, False))
        self.backButton_3.clicked.connect(lambda: self.checkTab.setCurrentWidget(self.viewTab))
        self.checkTab.setCurrentWidget(self.seatTab)
        self.continueB3.clicked.connect(lambda: self.buyTic4(mindex, cindex, ilist, ticnum, dt, tp))
        self.filmName_3.setText(movieDetails[mindex][1])
        self.cinemaName_3.setText(cinemaDetails[cindex][1])
        self.dateC_2.setText(dt[0])
        self.timeC_2.setText(dt[1])
        for sbt in range(1,19):
            seatbutton = getattr(self, "ss%d" % sbt)
            seatbutton.setCheckable(True)
            greenseat = QPixmap('images/green.png')
            seatbutton.setIcon(QtGui.QIcon(greenseat))
        for tk in ilist:
            forlist = sessionDetails[tk]
            seatTaken = forlist[4].split("/")
            seatTaken = list(filter(None, seatTaken))
        for s in st:
            takenseat = getattr(self, "ss%s" % s)
            takenseat.setCheckable(False)
            redseat = QPixmap('images/red.png')
            takenseat.setIcon(QtGui.QIcon(redseat))

    def buyTic4(self, mindex, cindex, ilist, ticnum, dt, tp):
        # Validating seat
        choseSeat = []
        for sbt in range(1,19):
            seatbutton = getattr(self, "ss%d" % sbt)
            if seatbutton.isChecked() == True:
                choseSeat.append(str(sbt))
        if len(choseSeat) == 0:
            warning = QMessageBox.question(self, 
                '''No seats selected.''','''No seats selected. \nYou need to select %d seat(s) for this session.''' 
                % ticnum, QMessageBox.Ok, QMessageBox.Ok)
            proceed = False
        elif len(choseSeat) > ticnum:
            warning = QMessageBox.question(self, 
                'Ticket number exceeded.',"Ticket number exceeded. \nYou can only select " + str(ticnum) + 
                " seat(s) in this session. \nYou have selected "+ str(len(choseSeat)) + ".", QMessageBox.Ok, QMessageBox.Ok)
            proceed = False
        else:
            proceed = True
        if proceed == True:
            self.checkTab.setTabEnabled(2, False)
            self.checkTab.setTabEnabled(3, True)
            self.backButton_4.clicked.connect(lambda: self.checkTab.setTabEnabled(2, True))
            self.backButton_4.clicked.connect(lambda: self.checkTab.setTabEnabled(3, False))
            self.backButton_4.clicked.connect(lambda: self.checkTab.setCurrentWidget(self.seatTab))
            try: self.continueB4.clicked.disconnect()
            except Exception: pass
            self.continueB4.clicked.connect(lambda: self.buyTic5(mindex, cindex, ilist, choseSeat, dt, tp))

    def buyTic5(self, mindex, cindex, ilist, seat, dt, tp):
        # Making sure payment details are correct + update CSV files
        fname = str(self.fnbox.text())
        lname = str(self.lnbox.text())
        phone = str(self.pnbox.text())
        ccn1 = str(self.ccn1.text())
        ccn2 = str(self.ccn2.text())
        ccn3 = str(self.ccn3.text())
        ccn4 = str(self.ccn4.text())
        exmm = str(self.exmm.currentText())
        exyy = str(self.exyy.currentText())
        excvv = str(self.excvv.text())
        if phone.isdigit() == False or phone[:2] != "04" or len(phone) != 10:
            warning = QMessageBox.question(self, 
                'Wrong phone number format.',"Wrong phone number format.\nPlease enter your phone number in the format of 04XXXXXXXX without space.",
                 QMessageBox.Ok, QMessageBox.Ok)
            proceed = False
        elif ccn1.isdigit() == False or ccn2.isdigit() == False\
        or ccn3.isdigit() == False or ccn4.isdigit() == False or \
        exmm.isdigit() == False or exyy.isdigit() == False or \
        excvv.isdigit() == False or len(ccn1) != 4 or len(ccn2) != 4\
        or len(ccn3) != 4 or len(ccn4) != 4 or len(excvv) != 3:
            warning = QMessageBox.question(self, 
                'Wrong credit card number format.',"Wrong credit card number format.\nPlease make sure you entered the correct digits.",
                 QMessageBox.Ok, QMessageBox.Ok)
            proceed = False
        elif len(fname) == 0 or len(lname) == 0 or \
        fname.isdigit() == True or lname.isdigit() == True:
            warning = QMessageBox.question(self, 
                'Please enter your name.',"Name is incorrect. Please enter your name.",
                 QMessageBox.Ok, QMessageBox.Ok)
            proceed = False
        else:
            proceed = True
        # Update Session CSV file
        if proceed == True:
            window.setWindowTitle("Booking Successful")
            for row in ilist:
                if dt[0] == sessionDetails[row][2] and dt[1] == sessionDetails[row][3]:
                    details = sessionDetails[row]
            row = sessionDetails.index(details)
            details[4] = details[4] + "/".join(seat) + "/"
            overrow = {row:details}
            ssnum = row
            with open('session.csv', 'w') as b:
                writer = csv.writer(b, delimiter=',', quotechar = '"')
                for line, row in enumerate(sessionDetails):
                    data = overrow.get(line, row)
                    writer.writerow(data)
            # Generate Session ID and Update Bookings CSV
            phone = base64.b64encode(phone.encode())
            from time import localtime, strftime
            from random import randint
            sid = strftime("%Y%m%d%H%M%S", localtime()) + str(randint(100, 999))
            with open('booking.csv','a',newline='') as f:
                writer = csv.writer(f, dialect='excel')
                writer.writerow([sid, ssnum, fname, lname, phone])
            self.bbidl.setText("Please take note of your booking ID: "+ sid)
            self.checkTab.setTabEnabled(3, False)
            self.checkTab.setTabEnabled(4, True)
            self.seats.setText(str(len(seat)) + ' ticket(s)')
            self.price.setText('$' + str(tp))
            self.filmName_4.setText(movieDetails[mindex][1])
            self.cinemaName_4.setText(cinemaDetails[cindex][1])
            self.dateC_3.setText(dt[0])
            self.timeC_3.setText(dt[1])
            self.backHomeX.clicked.connect(self.exitP)

    def returnHome(self):
        self.close()
        self.__init__()

    def exitP(self):
        sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window is the widget
    window = Ui()
    sys.exit(app.exec_())
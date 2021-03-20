import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from RegistrationUi import *

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

global cursorsDb
global connectDb

import sqlite3
connectDb=sqlite3.connect('YourDataBaseName.db')
cursorsDb=connectDb.cursor()
connectDb.commit() 

#--------- ADD -----------------------------------------------------------------#
def Clear():
    ui.lneStudentIdent.clear()
    ui.lneStudentName.clear()
    ui.lneStudentSurname.clear()
    ui.lneStudentSchool.clear()
    ui.lneStudentPhnNumber.clear()
    ui.lneStudentAdress.clear()

def Add():
    studentNum = ui.lneStudentIdent.text()
    studentName = ui.lneStudentName.text()
    studentSurname = ui.lneStudentSurname.text()
    studentSchool = ui.lneStudentSchool.text()
    studentPhonNum = ui.lneStudentPhnNumber.text()
    studentAdress = ui.lneStudentAdress.text()
    try:
        cursorsDb.execute("INSERT INTO TableName \
                        (Number,Name,Surname,School,Phone,Adress) \
                            VALUES(?,?,?,?,?,?)", \
                                (studentNum,studentName,studentSurname,studentSchool,studentPhonNum,studentAdress))
        Clear()
    
    except Exception:
        ui.statusbar.showMessage("Student Number must be unique!")

    connectDb.commit()
    Lists()

#--------- LIST -----------------------------------------------------------------#

def Lists():
    ui.tblwListen.clear()
    ui.tblwListen.setHorizontalHeaderLabels(('Id','Number','Student Name','Student Surname','School','Phone','Adress'))
    ui.tblwListen.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    cursorsDb.execute("SELECT * FROM TableName")
    for rowIndex, rowData in enumerate(cursorsDb):
            for columnIndex, columnData in enumerate(rowData):
                ui.tblwListen.setItem(rowIndex,columnIndex,QtWidgets.QTableWidgetItem(str(columnData)))
    Clear()

#--------- DELETE -----------------------------------------------------------------#

def Delete():
    question = QtWidgets.QMessageBox.question(MainWindow,"Delete Registration","Are You Sure You Want To Delete The Selected Record?",\
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

    if question==QtWidgets.QMessageBox.Yes:
        try:
            selected = ui.tblwListen.selectedItems()
            deleted = selected[1].text()
            cursorsDb.execute("DELETE FROM TableName WHERE Number='%s'" %(deleted))
            connectDb.commit()
            ui.statusbar.showMessage("Registration Successfully Deleted!")
            Clear()
            Lists()

        except Exception as exception:
            ui.statusbar.showMessage("Error : " + str(exception))
    
    else:
        ui.statusbar.showMessage("Deletion has been canceled!")

#--------- SEARCH -----------------------------------------------------------------#

def Search():
    ui.tblwListen.clear()
    searchStudentNum = ui.lneStudentPhnNumber.text()
    searchStudentName = ui.lneStudentName.text()
    cursorsDb.execute("SELECT * FROM TableName WHERE Number=? OR Name=?",(searchStudentNum,searchStudentName))
    connectDb.commit()
    for rowIndex, rowData in enumerate(cursorsDb):
            for columnIndex, columnData in enumerate(rowData):
                ui.tblwListen.setItem(rowIndex,columnIndex,QtWidgets.QTableWidgetItem(str(columnData)))
                Clear()


#--------- UPDATE -----------------------------------------------------------------#

def Update():
    question = QtWidgets.QMessageBox.question(MainWindow,"Update Registration","Are You Sure You Want to Update the Selected Record?",\
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    if question==QtWidgets.QMessageBox.Yes:
        try:
            selected = ui.tblwListen.selectedItems()
            id = int(selected[0].text())
            sttudentNum = ui.lneStudentIdent.text()
            studentName = ui.lneStudentName.text()
            studentSurename = ui.lneStudentSurname.text()
            studentSchool = ui.lneStudentSchool.text()
            studentPhNum = ui.lneStudentPhnNumber.text()
            studentAdress = ui.lneStudentAdress.text()
            cursorsDb.execute("UPDATE TableName SET Number=?, Name=?, Surname=?, School=?, Phone=?,Adress=? WHERE Id=?",\
                (sttudentNum,studentName,studentSurename,studentSchool,studentPhNum,studentAdress,id))
            connectDb.commit()
            Clear()
            Lists()

        except Exception as exception:
            ui.statusbar.showMessage("Error : " + str(exception))
    else:
        ui.statusbar.showMessage("The update process has been canceled!")

#--------- QUIT -----------------------------------------------------------------#

def Exit():
    question = QtWidgets.QMessageBox.question(MainWindow,"Quit the program","Are You Sure You Want To Quit The Program?",\
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    if question==QtWidgets.QMessageBox.Yes:
        connectDb.close()
        sys.exit(app.exec_())
    else:
        MainWindow.show()
def Met():
    try:
        selected=ui.tblwListen.selectedItems()
        ui.lneStudentIdent.setText(selected[1].text())
        ui.lneStudentName.setText(selected[2].text())
        ui.lneStudentSurname.setText(selected[3].text())
        ui.lneStudentSchool.setText(selected[4].text())
        ui.lneStudentPhnNumber.setText(selected[5].text())
        ui.lneStudentAdress.setText(selected[6].text())
    except Exception:
        ui.statusbar.showMessage("Please choose from the numbered field on the left side of the list.") 
#--------- TRANSFER FUNCTIONS TO BUTTONS -----------------------------------------------------------------#
ui.btnAdd.clicked.connect(Add)
ui.btnDelete.clicked.connect(Delete)
ui.btnLists.clicked.connect(Lists)
ui.btnSearch.clicked.connect(Search)
ui.btnUpdate.clicked.connect(Update)
ui.btnExit.clicked.connect(Exit)
ui.tblwListen.itemSelectionChanged.connect(Met)
sys.exit(app.exec_())
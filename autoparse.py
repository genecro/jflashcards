        # -*- coding: UTF-8 -*-
    
from Tkinter import *
import pyexcel
import json
import tkMessageBox
import Tkinter
import kana_conversion

class JFlashCards:
    

    def __init__(self, master):
        self.topTop = master;
        self.topTop.title("Kanji Flashcard Creator")

        # get vocab spreadsheet
        wordListName = raw_input('Enter the path of the spreadsheet containing the word list: ')
        wordSheet = pyexcel.get_sheet(file_name=wordListName)
        self.wordSheetArray = wordSheet.to_array()
    
        # get kanji spreadsheet
        kanjiListName = raw_input('Enter the path of the spreadsheet containing the kanji list: ')
        kanjiSheet = pyexcel.get_sheet(file_name=kanjiListName)
        self.kanjiSheetArray = kanjiSheet.to_array()

        # make a hash map of kanji to readings
        self.makeKanjiDict()
    
        # get output file or make a new one
        filechoice = raw_input('If you already have a spreadsheet started, type the path. Otherwise type create:')
    
        if filechoice == 'create': #make a new one
            self.outputFileName = raw_input('Enter the path of the new spreadsheet you want to create: ')
            sheet = self.createNewSheet(self.outputFileName)
        else:                      #load existing
            self.outputFileName = filechoice
            sheet = pyexcel.get_sheet(file_name=self.outputFileName)
    
        self.sheetArray = sheet.to_array()

    def makeFlashCards(self):
        rowNum=0
    
        #loop through lines in output file
        for line in self.sheetArray:
            #find rows that haven't been completed
            if len(line) == 1 or line[1] == "":
                #make a frame in the winodow to hold all widgets
                self.top = Frame(self.topTop)
                self.top.pack()

                #make lists to store procedurally generated widgets
                self.checkboxArray = []
                self.frameArray = []
                self.textArray = []
    
                #make a large centered label displaying the current kanji
                currentKanji = line[0]
                L = Label(
                    self.top,
                    text=currentKanji,
                    font=("Helvetica", 25))
                L.pack()
    
                #make a label displaying the number of the current kanji over the total number
                progressLabel = Label(
                                    self.top,
                                    text=str(rowNum + 1) + "/" + str(len(self.kanjiDict)))
                progressLabel.pack()
    
                #make a frame to contain the widgets making up the lines for each matching vocab word
                self.entriesFrame = Frame(self.top)
                self.entriesFrame.pack()
    
                #search for vocab words containing the current kanji
                for vocabLine in self.wordSheetArray:
                    if currentKanji in vocabLine[0]:
    
                        #make a frame for a single line, store it in the frame array so it can be accessed later
                        frame = Frame(self.entriesFrame)
                        frame.pack()
                        self.frameArray.append(frame)
    
                        #make a checkbutton with text equal to the current matching vocab word, store it in array
                        checkvar = IntVar()
                        C = Checkbutton(
                            frame, 
                            text=vocabLine[0], 
                            variable=checkvar,
                            font=("Helvetica", 15))
                        C.pack(side=LEFT)
                        self.checkboxArray.append(checkvar)
    
                        #make a label with the reading of the word
                        ReadingLabel = Label(
                            frame,
                            text=vocabLine[1])
                        ReadingLabel.pack(side=LEFT)

                        #make a label with the translation of the word
                        EnglishLabel = Label(
                            frame,
                            text=vocabLine[2])
                        EnglishLabel.pack(side=LEFT)

                        #make a textbox that will contain the text to be inserted into the spreadsheet, add it to array
                        T = Text(
                            frame,
                            height=1,
                            width=10)
                        #initial contents: the current vocab word with the current kanji replaced by its reading in brackets
                        T.insert(INSERT, self.replaceKanji(
                                             currentKanji, 
                                             self.kanjiDict[currentKanji][0] + self.kanjiDict[currentKanji][1], 
                                             vocabLine[0], 
                                             vocabLine[1]))
                        T.pack(side=LEFT)
                        self.textArray.append(T)
    
                #make a frame to store the "Add blank line" and "Add to sheet" buttons
                ButtonsFrame = Frame(self.top)
                ButtonsFrame.pack()
    
                #this button adds a new line with a checkbutton and a text box
                newLineButton = Tkinter.Button(
                    ButtonsFrame,
                    text="Add blank line",
                    command=self.addNewLine)
                newLineButton.pack(side=LEFT)
    
                #this button saves all of the text in the text boxes with checked checkbuttons, then moves onto the next kanji
                B = Tkinter.Button(
                    ButtonsFrame, 
                    text="Add to sheet", 
                    command=lambda:self.print_close(rowNum))
                B.pack(side=RIGHT)
    
                #loop here until widgets are killed
                self.topTop.mainloop()
            rowNum += 1
    
    #this function is called by the new line button, it adds a new blank line to the frame containing the other lines
    #stores the references to the new frame, the new checkbutton, and the new text box
    def addNewLine(self):
        frame = Frame(self.entriesFrame)
        frame.pack()
        self.frameArray.append(frame)
        checkvar = IntVar()
        Checkbutton(frame, variable=checkvar).pack(side=LEFT)
        self.checkboxArray.append(checkvar)
        T = Text(frame, height=1, width=10)
        T.pack(side=RIGHT)
        self.textArray.append(T)
    
    #this function converts an array to a dictionary:
    #[[kanjiA, onyomiA, kunyomiA], [kanjiB, onyomiB, kunyomiB]]
    #-->
    #{"kanjiA":"onyomiA kunyomiA", "kanjiB":"onyomiB, kunyomiB"}
    def makeKanjiDict(self):
        self.kanjiDict = {}
        for entry in self.kanjiSheetArray:
            self.kanjiDict[entry[0].strip()] = entry[1:]
             
    #this function is basically the raison d'etre of this script
    #it takes a vocabulary word containing kanji and replaces a specified kanji
    #with its reading for that particular word.
    #four arguments are needed: the word in kanji, the reading of the entire word in hiragana,
    #the kanji to be replace, and an array containing all potential readings of the kanji
    #in katakana and/or hiragana
    def replaceKanji(self, kanji2Replace, kanjiReadings, wordKanji, wordReading):
    
        #normalize the readings by converting everything to hiragana
        kanjiReadings = kana_conversion.kata2Hira(kanjiReadings).split(' ')
    
        #start building the string which will replace the kanji
        insertString = "["
    
        #search for a reading of the kanji (from items in the reading list) which exists
        #in the reading of the word
        for reading in kanjiReadings:
            testReading = reading
    
            #if a . exists in the reading, only look at the characters that come before it
            try:
                testReading = testReading[0:testReading.index('.')]
            except:
                pass
    
            #the database I used for kanji readings didn't included readings where a terminal つ is converted to っ
            #example 決定 is read けってい but the list of readings only contains けつ for 決
            #this section checks to see if the final character of the reading is つ and also checks for the same reading
            #with a っ instead
            if len(testReading) > 1 and testReading[len(testReading)-1] == "つ".decode('utf-8'):
                if testReading[0:testReading.index("つ".decode('utf-8'))] + "っ".decode('utf-8') in wordReading:
                    insertString += testReading[0:testReading.index("つ".decode('utf-8'))] + "っ".decode('utf-8')
                    break
    
            #if the kanji reading is found within the word reading, add the kanji reading to the
            #replacement string and stop looking
            if testReading in wordReading:
                insertString += testReading
                break
    
        #add the closing bracket and return the string
        insertString += "]"
        return wordKanji.replace(kanji2Replace, insertString)
    
    #this function saves the text in all text boxes with checked checkbuttons into the current row of the spreadsheet
    def print_close(self, rowNum):
        #collect all checked textboxes into single string separated by a newline character
        entryString = ""
        for i in range(0, len(self.checkboxArray)):
            if self.checkboxArray[i].get() == 1:
                entryString += self.textArray[i].get('1.0', 'end-1c') + "\n"
        
        #append if there is only one column in the row, or overwrite if there is more than one
        if len(self.sheetArray[rowNum]) == 1:
            self.sheetArray[rowNum].append(entryString.rstrip())
        else:
            self.sheetArray[rowNum][1] = entryString.rstrip()
    
        #write to file
        pyexcel.Sheet(self.sheetArray).save_as(self.outputFileName)
    
        #destroy widgets in top frame to break mainloop and move to the next kanji
        self.top.quit()
        self.top.destroy()    
    
    #this function creates a new .xls file with one kanji per row to be used as the output file
    #if one does not already exist
    def createNewSheet(self, name):
        newSheetArray = []
        for line in self.kanjiSheetArray:
            newSheetArray.append([line[0].strip()])
        newSheet = pyexcel.Sheet(newSheetArray)
        newSheet.save_as(name)
    
        return newSheet
    
root = Tkinter.Tk()
flashcard_gui = JFlashCards(root)
flashcard_gui.makeFlashCards()


# Automated Japanese flashcard creation tool

## Background

I wanted to create a deck of flash cards, one for each kanji that may appear on the JLPT N1. The back (answer side) would just contain the kanji. The front would have a few words that each contain the kanji of the current card. I wanted the current kanji to be replaced by hiragana in square brackets showing its reading. Example:

Front: <br />
定[しょく]<br />
[た]べる<br />
[く]う

Back:<br />
食

I found two spreadsheets: one containing all <a href=http://www.tanos.co.uk/jlpt/jlpt1/kanji/combined/>kanji</a> that could appear on JLPT N1 along with their readings and another containing all the <a href=www.tanos.co.uk/jlpt/jlpt1/vocab/combined/>vocabulary</a> words that could appear on the JLPT N1. For each kanji in the kanji sheet I would search the words in the vocab sheet to find ones containing that kanji, then decide which ones I wanted to put on the card, typing each line and doing the kanji replacement manually.

This would have taken quite a long time so I decided to write a tool to automate the process.

## Input requirements and dependencies:

This tool uses <a href=https://wiki.python.org/moin/TkInter>Tkinter</a>, <a href=https://github.com/pyexcel/pyexcel>pyexcel</a>, and <a href=https://github.com/genecro/kana_conversion>kana_conversion</a>.

The kanji spreadsheet must have these columns in the following order:
Kanji | On'yomi | Kun'yomi (the readings may be in katakana and/or hiragana)

The vocab spreadsheet must have these columns:
Word (kanji) | Reading (hiragana) | Translation

These spreadsheets should be xls files.

## How to use this tool:

Run `python autoparse.py`

You will be asked to enter the path to the kanji spreadsheet and then the path to the vocabulary spreadsheet. Just type or paste them normally without quotes or anything. Next you will be asked to type the path to the output file or "create" to make a new one based on the kanji in the kanji spreadsheet.

After these steps the tool will find the first empty entry in the output file and display a window for the corresponding kanji. It searches the vocabulary list for any entries containing the kanji, and then replaces the instance of the kanji in the word with its reading surrounded by square brackets. Here is a sample screen:

![Sample Screen](/img/sample1.png?raw=true "Sample Screen")

Use the checkbuttons on the left to select the words you want to add to your flashcard for the current kanji. If the automated process of constructing the word with the kanji replaced by its reading in square brackets was done incorrectly, the textbox is editable so you may manually adjust it if necessary.

If you want to add a word that wasn't contained in the vocabulary list, click the "Add blank line" button:

![New Line Added](/img/sample2.png?raw=true "New Line Added")

Choose the words you want to insert and then click "Add to sheet" to save the selected words to the current row in the output file. The screen for the next kanji will automatically open.

If you don't finish going through all kanji in one sitting, the tool will resume with the earliest kanji with an empty cell in the output file.

The output file contains the following columns:
Kanji (back) | Word list (front)

## Future improvements

-Sometimes a kanji will have two readings, one of which is a substring of the other. If the shorter one appears on the list of readings first, it will get inserted into the brackets even if the longer version is present (e.g., the kanji has し and　しゃ in its list of readings, the word contains しゃ, but し gets inserted into the brackets). A potential solution would be to sort the readings from longest to shortest when performing the check.

-Implement the ability to rearrage the position of each line to control the order the words appear in on the flashcard.

-Allow the ability to use other formats for input spreadsheets. For example, maybe you would want to use a spreadsheet without a column for English transltions of the words. Using such a spreadsheet with the current version would cause an error.

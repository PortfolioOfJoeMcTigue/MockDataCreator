from abc import update_abstractmethods
from multiprocessing import Value
from operator import contains
import tkinter as tk
from tkinter import END, StringVar, ttk
import tkinter.scrolledtext as tkst
from tkinter import simpledialog
import os
from datetime import datetime

import FileReadOperations as reader
import FileWriteOperations as writer
import ListOperations as listOp
import DictionaryOperations as dicts
import ServiceOperations as service

class DisplayFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.r = reader.FileReadOperations()
        self.w = writer.FileWriteOperations()
        self.l = listOp.ListOperations()
        self.s = service.ServiceOperations()
        self.d = dicts.DictionaryOperations()

        self.current_file_dict = {}
        self.columnsList = []
        self.columnsTitlesList = []
        self.columnsValuesList = []
        self.columnsTypesList = []
        self.columnsFormatsList = []
        self.masterColValues = []
        self.headerList = []
        self.valueList = []
        self.formatList = []
        self.typeList = []
        self.valueCheck = []
        self.typeCheck = []
        self.formatCheck = []
        self.fileData = []
        self.recordFileType = ""
        self.newFileName = ""
        self.recordColumnAmount = 0
        self.recordsInConfig = 0

        self.columnName = ""
        self.columnCustomName = ""
        self.columnValue = ""
        self.columnCustomValue = ""
        self.columnValueType = ""
        self.columnCustomValueType = ""
        self.columnFormat = ""
        self.columnCustomFormat = ""
        #self.columnData = ""
        self.currentRecord = ""
        self.recordData = ""
        
#-------Style components start here ---------------
        
        # fonts for buttons
        self.buttonConfigFontHel22 = ttk.Style()
        self.buttonConfigFontHel22.configure('buttonConfigFontHel22.TButton', font = ("Helvetica", 22, 'bold'))
        self.buttonConfigFontHel16 = ttk.Style()
        self.buttonConfigFontHel16.configure('buttonConfigFontHel16.TButton', font = ("Helvetica", 16, 'bold'))
        self.buttonConfigFontHel14 = ttk.Style()
        self.buttonConfigFontHel14.configure('buttonConfigFontHel14.TButton', font = ("Helvetica", 14, 'bold'))
        self.buttonConfigFontHel12 = ttk.Style()
        self.buttonConfigFontHel12.configure('buttonConfigFontHel12.TButton', font = ("Helvetica", 12, 'bold'))
        self.buttonConfigFontHel11 = ttk.Style()
        self.buttonConfigFontHel11.configure('buttonConfigFontHel11.TButton', font = ("Helvetica", 11))

        # background for checkboxes
        self.checkboxConfigBackground = ttk.Style()
        self.checkboxConfigBackground.configure('checkboxConfigBackground.TCheckbutton', background = "#9AB6EA")

#-------GUI components start here ----------------

        # Adding label for file format.
        self.formatLabel = tk.Label(container, text="Select Data File\nFormat to Create:", bg="#9AB6EA", fg="Black", font=('Verdana', 12, 'bold'))
        self.formatLabel.place(x=30, y=25)
        # Adding radio buttons for output file format.
        self.format_var = tk.StringVar()
        self.format_var.set(0)
        self.formatChoiceOne = tk.Radiobutton(container, background = "#9AB6EA", text = 'CSV Format', font = ('Verdana', 12), variable = self.format_var, value = 0, command = lambda name="csv":self.set_record_file_type(name))
        self.formatChoiceTwo = tk.Radiobutton(container, background = "#9AB6EA", text = 'Parquet Format', font = ('Verdana', 12), variable = self.format_var, value = 1, command = lambda name="parquet":self.set_record_file_type(name))
        self.formatChoiceThree = tk.Radiobutton(container, background = "#9AB6EA", text = 'JSON Format', font = ('Verdana', 12), variable = self.format_var, value = 2, command = lambda name="json":self.set_record_file_type(name))
        self.formatChoiceFour = tk.Radiobutton(container, background = "#9AB6EA", text = 'SQL Format', font = ('Verdana', 12), variable = self.format_var, value = 3, command = lambda name="sql":self.set_record_file_type(name))
        self.formatChoiceOne.place(x=60, y=70)
        self.formatChoiceTwo.place(x=60, y=90)
        self.formatChoiceThree.place(x=60, y=110)
        self.formatChoiceFour.place(x=60, y=130)

        # Add button for updating the type 
        self.updateFormatChoiceBtn = ttk.Button(container, text = " Update Format Choice ", style = 'buttonConfigFontHel11.TButton', command = lambda name = "updateFormatChoiceBtn":self.button_clicked(name))
        self.updateFormatChoiceBtn.place(x=60, y=165)

        # Adding label for number of records selection.
        self.recordsNeededtLabel = tk.Label(container, text="Number of Records         \nRequired For Output File:", bg="#9AB6EA", fg="Black", font=('Verdana', 12, 'bold'))
        self.recordsNeededtLabel.place(x=310, y=40)
        # Adding dropdown selection for number of records needed.
        columnNumbersArray = self.get_array_of_numbers() 
        self.numOfRecordsNeeded = tk.StringVar()
        self.numOfRecordsNeeded.set('Select a Number')
        self.numOfRecordsNeededCmbo = ttk.Combobox(container, values = columnNumbersArray, state = "readonly", textvariable = self.numOfRecordsNeeded, justify = "center", width = 25, height = 20, font = ("Helvetica", 12, 'bold'))
        self.numOfRecordsNeededCmbo.place(x=315, y=100)

        # Adding a button for updating the number of records needed.
        self.updateRecordsNeededBtn = ttk.Button(container, text = " Update Records Required ", style = 'buttonConfigFontHel11.TButton', command = lambda name = "updateRecordsNeededBtn":self.button_clicked(name))
        self.updateRecordsNeededBtn.place(x=340, y=150)

        # Adding directive for select config section.
        self.configFileSelectiontLabel = tk.Label(container, text="Select, Create, Initialize or Delete a Config File:", bg="#9AB6EA", fg="Black", font=('Verdana', 12, 'bold'))
        self.configFileSelectiontLabel.place(x=35, y=235)

        # Adding dropdown selection to either choose a preexisting config file or create a new one.
        self.configFileNamesArray = self.r.get_list_of_config_files_in_home_dir()
        self.selectedConfigFile = tk.StringVar()
        self.selectedConfigFile.set(self.configFileNamesArray[0])
        self.configFileNamesCmbo = ttk.Combobox(container, textvariable = self.selectedConfigFile, state = "readonly", values = self.configFileNamesArray, justify = "left", width = 55, height = 25, font = ("Helvetica", 12, 'bold'))
        self.configFileNamesCmbo.bind("<<ComboboxSelected>>", self.selectedConfigFile)
        self.configFileNamesCmbo.place(x=45, y=280)

        # Adding button to create a new config file.
        self.createConfigFileBtn = ttk.Button(container, text = "     Create\n  Config File  ", style = 'buttonConfigFontHel12.TButton', command = lambda name = "createConfigFileBtn":self.button_clicked(name))
        self.createConfigFileBtn.place(x=60, y=320)

        # Adding button to intialize data from config dropdown selection choice.
        self.initializeDataBtn = ttk.Button(container, text = "    Initialize\n Config Data  ", style = 'buttonConfigFontHel12.TButton', command = lambda name = "initializeDataBtn":self.button_clicked(name))
        self.initializeDataBtn.place(x=185, y=320)

        # Adding button to clone a new config file.
        self.cloneConfigFileBtn = ttk.Button(container, text = "     Clone\n  Config File  ", style = 'buttonConfigFontHel12.TButton', command = lambda name = "cloneConfigFileBtn":self.button_clicked(name))
        self.cloneConfigFileBtn.place(x=310, y=320)

        # Adding button to delete the config selected in the dropdown choice.
        self.deleteConfigFileBtn = ttk.Button(container, text = "     Delete\n  Config File  ", style = 'buttonConfigFontHel12.TButton', command = lambda name = "deleteConfigFileBtn":self.button_clicked(name))
        self.deleteConfigFileBtn.place(x=435, y=320)

        # Adding label for AWS S3 deployment options.
        self.awsS3ConfigLabel = tk.Label(container, text="Set Configuration for AWS S3 Deployments:", bg="#9AB6EA", fg="Black", font=('Verdana', 12, 'bold'))
        self.awsS3ConfigLabel.place(x=35, y=440)

        # Adding combobox dropdown selection for output data file for AWS S3 deployment.
        self.outputFileNamesArray = ["Select an Output Data File to Deploy"] #self.r.get_list_of_data_output_files_in_output_dir()
        self.selectedOutputFile = tk.StringVar()
        self.selectedOutputFile.set(self.outputFileNamesArray[0])
        self.outputFileNamesCmbo = ttk.Combobox(container, textvariable = self.selectedOutputFile, state = "readonly", values = self.outputFileNamesArray, justify = "left", width = 55, height = 25, font = ("Helvetica", 12, 'bold'))
        self.outputFileNamesCmbo.bind("<<ComboboxSelected>>", self.selectedOutputFile)
        self.outputFileNamesCmbo.place(x=35, y=485)

        # Adding combobox dropdown selection for S3 bucket path for AWS S3 deployment.
        self.s3BucketPathArray = ["Select an S3 bucket path to Deploy to"] 
        self.selectedBucketPath = tk.StringVar()
        self.selectedBucketPath.set(self.s3BucketPathArray[0])
        self.selectedBucketPathCmbo = ttk.Combobox(container, textvariable = self.selectedBucketPath, state = "readonly", values = self.s3BucketPathArray, justify = "left", width = 55, height = 25, font = ("Helvetica", 12, 'bold'))
        self.selectedBucketPathCmbo.bind("<<ComboboxSelected>>", self.selectedBucketPath)
        self.selectedBucketPathCmbo.place(x=35, y=530)

        # Adding create & deploy output data file to AWS S3 bucket button.
        self.createAndDeployAWSS3DataFileBtn = ttk.Button(container, text = " Deploy Data File ", style = 'buttonConfigFontHel16.TButton', command = lambda name='createAndDeployAWSS3DataFileBtn':self.button_clicked(name))
        self.createAndDeployAWSS3DataFileBtn.place(x=30, y=575)

        # Add new deployment location to selection list.
        self.addNewDeploymentLocationBtn = ttk.Button(container, text = " Add New Deployment Selection ", style = 'buttonConfigFontHel16.TButton', command = lambda name='addNewDeploymentLocationBtn':self.button_clicked(name))
        self.addNewDeploymentLocationBtn.place(x=230, y=575)
#------------
        # Adding help button to bring up instructions if needed for the user.
        self.helpBtn = ttk.Button(container, text = "  Instructions  ", style = 'buttonConfigFontHel16.TButton', command = lambda name='helpBtn':self.button_clicked(name))
        self.helpBtn.place(x=1185, y=25)

        # Adding the Build, Edit or Delete Config label.
        self.buildEditConfigLabel = tk.Label(container, text="Build, Edit or Delete Config Records:", bg="#9AB6EA", fg="Black", font=('Verdana', 12, 'bold'))
        self.buildEditConfigLabel.place(x=630, y=25)

        # Adding a Combobox for selecting column headers.
        self.columnNamesArray = ["Select a Column Title"]
        self.columnName = tk.StringVar()
        self.columnName.set(self.columnNamesArray[0])
        self.columnNamesCmbo = ttk.Combobox(container, textvariable = self.columnName, values = self.columnNamesArray, state = "readonly", justify = "left", width = 35, height = 35, font = ("Helvetica", 10, 'bold'))
        self.columnNamesCmbo.place(x=650, y=70)

        # Adding 'or' label to allow for user understandability.
        self.titleOrLabel = tk.Label(container, text="or", bg="#9AB6EA", fg="Black", font=('Verdana', 12, 'bold'))
        self.titleOrLabel.place(x=925, y=70)

        # Adding Entry text box for column header custom names to be entered.
        self.customNameEdit = tk.StringVar()
        self.customNameEdit.set('')
        self.columnNameEditedEntry = tk.Entry(container, textvariable = self.customNameEdit, relief = "sunken", justify = "center", font = ("Calibri", 11), width = 33)
        self.columnNameEditedEntry.place(x=960, y=70)

        # Adding a Combobox for selecting column values.
        columnValuesArray = ["Select a Column Value"]
        self.columnValue = tk.StringVar()
        self.columnValue.set(columnValuesArray[0])
        self.columnValuesCmbo = ttk.Combobox(container, textvariable = self.columnValue, values = columnValuesArray, state = "readonly", justify = "left", width = 35, height = 35, font = ("Helvetica", 10, 'bold'))
        self.columnValuesCmbo.place(x=650, y=100)

        # Adding 'or' label to allow for user understandability.
        self.valueOrLabel = tk.Label(container, text="or", bg="#9AB6EA", fg="Black", font=('Verdana', 12, 'bold'))
        self.valueOrLabel.place(x=925, y=100)

        # Adding Entry text box for column custom values to be entered.
        self.customValueEdit = tk.StringVar()
        self.customValueEdit.set('')
        self.columnValueEditedEntry = tk.Entry(container, textvariable = self.customValueEdit, relief = "sunken", justify = "center", font = ("Calibri", 11), width = 33)
        self.columnValueEditedEntry.place(x=960, y=100)

        # Adding a Combobox for selecting column value types.
        columnValueTypesArray = ["Select a Column Type"]
        self.columnValueTypes = tk.StringVar()
        self.columnValueTypes.set(columnValueTypesArray[0])
        self.columnValueTypesCmbo = ttk.Combobox(container, textvariable = self.columnValueTypes, state = "readonly", values = columnValueTypesArray, justify = "left", width = 35, height = 35, font = ("Helvetica", 10, 'bold'))
        self.columnValueTypesCmbo.place(x=650, y=130)

        # Adding 'or' label to allow for user understandability.
        self.typeOrLabel = tk.Label(container, text="or", bg="#9AB6EA", fg="Black", font=('Verdana', 12, 'bold'))
        self.typeOrLabel.place(x=925, y=130)

        # Adding Entry text box for column custom value types to be entered.
        self.customValueTypeEdit = tk.StringVar()
        self.customValueTypeEdit.set('')
        self.customValueTypeEditEntry = tk.Entry(container, textvariable = self.customValueTypeEdit, relief = "sunken", justify = "center", font = ("Calibri", 11), width = 33)
        self.customValueTypeEditEntry.place(x=960, y=130)

        # Adding a Combobox for selecting column value formats.
        columnValueFormatArray = ["Select a Column Format"]
        self.columnValueFormats = tk.StringVar()
        self.columnValueFormats.set(columnValueFormatArray[0])
        self.columnValueFormatsCmbo = ttk.Combobox(container, textvariable = self.columnValueFormats, state = "readonly", value = columnValueFormatArray, justify = "left", width = 35, height = 35, font = ("Helvetica", 10, 'bold'))
        self.columnValueFormatsCmbo.place(x=650, y=160)

        # Adding 'or' label to allow for user understandability.
        self.formatOrLabel = tk.Label(container, text="or", bg="#9AB6EA", fg="Black", font=('Verdana', 12, 'bold'))
        self.formatOrLabel.place(x=925, y=160)

        # Adding Entry text box for column custom value formats to be entered.
        self.customValueFormatEdit = tk.StringVar()
        self.customValueFormatEdit.set('')
        self.customValueFormatEditEntry = tk.Entry(container, textvariable = self.customValueFormatEdit, relief = "sunken", justify = "center", font = ("Calibri", 11), width = 33)
        self.customValueFormatEditEntry.place(x=960, y=160)

        # Adding the button to add additional formats to column.
        self.additionalFormatBtn = ttk.Button(container, text = " Add Formats ", style = 'buttonConfigFontHel12.TButton', command = lambda name="additionalFormatBtn":self.button_clicked(name))
        self.additionalFormatBtn.place(x=1200, y=157)
#----------
        # Adding previous column button for column navigation.
        self.prevColumnBtn = ttk.Button(container, text = "<", style = 'buttonConfigFontHel12.TButton', width = 2, command = lambda name="prevColumnBtn":self.button_clicked(name))
        self.prevColumnBtn.place(x=650, y=195)

        # Adding current column Numner display entry.
        self.currentColumnNumberEntry = tk.Entry(container, relief = "sunken", justify = "center", font = ("Calibri, 14"), width = 4)
        self.currentColumnNumberEntry.place(x=680, y=196)

        # Adding the next column button for column navigation.
        self.nextColumnBtn = ttk.Button(container, text = ">", style = 'buttonConfigFontHel12.TButton', width = 2, command = lambda name="nextColumnBtn":self.button_clicked(name))
        self.nextColumnBtn.place(x=730, y=195)

        # Adding the goto button for column navigation.
        self.goToColumnBtn = ttk.Button(container, text = "+", style = 'buttonConfigFontHel12.TButton', width = 2, command = lambda name="goToColumnBtn":self.button_clicked(name))
        self.goToColumnBtn.place(x=760, y=195)

        # Adding column navigation label to allow for user understandability.
        self.columnValueLabel = tk.Label(container, text="Column of:", bg="#9AB6EA", fg="Black", font=('Verdana', 12, 'bold'))
        self.columnValueLabel.place(x=790, y=199)

        # Adding column navigation label to allow for user understandability.
        self.col_num_var = StringVar()
        self.col_num_var.set("19")
        self.totalColumnsLabel = tk.Label(container, text = "0", bg="#9AB6EA", fg="Black", font=('Verdana', 12, 'bold'))
        self.totalColumnsLabel.place(x=885, y=199)

        # Adding previous button for record navigation.
        self.prevRecBtn = ttk.Button(container, text = "<", style = 'buttonConfigFontHel12.TButton', width = 2, command = lambda name = "prevRecBtn":self.button_clicked(name))
        self.prevRecBtn.place(x=945, y=195)

        # Adding textbox to display current record number.
        self.currentRecNumberEntry = tk.Entry(container, relief = "sunken", justify = "center", font = ("Calibri, 14"), width = 4)
        self.currentRecNumberEntry.place(x=974, y=196)

        # Adding next button for record navigation.
        self.nextRecBtn = ttk.Button(container, text = ">", style = 'buttonConfigFontHel12.TButton', width = 2, command = lambda name = "nextRecBtn":self.button_clicked(name))
        self.nextRecBtn.place(x=1025, y=195)

        # Adding goto button for fast record navigation.
        self.goToRecBtn = ttk.Button(container, text = "+", style = 'buttonConfigFontHel12.TButton', width = 2, command = lambda name = "goToRecBtn":self.button_clicked(name))
        self.goToRecBtn.place(x=1055, y=195)

        # Adding column navigation label to allow for user understandability.
        self.recordValueLabel = tk.Label(container, text="Record of:", bg="#9AB6EA", fg="Black", font=('Verdana', 12, 'bold'))
        self.recordValueLabel.place(x=1085, y=199)

        # Adding record navigation label to allow for user understandability.
        self.rec_num_var = StringVar()
        self.rec_num_var.set("0")
        self.totalRecordsLabel = tk.Label(container, text = "0", bg="#9AB6EA", fg="Black", font=('Verdana', 12, 'bold'))
        self.totalRecordsLabel.place(x=1180, y=199)    

        # Adding label this record is to affect in final output data file.
        self.recordValueLabel = tk.Label(container, text="Number of output Data Records to affect:", bg="#9AB6EA", fg="Black", font=('Verdana', 12, 'bold'))
        self.recordValueLabel.place(x=640, y=235)

        # Adding textbox to display current "records to affect" number which is editable.
        self.recordsToAffectNumberEntry = tk.Entry(container, relief = "sunken", justify = "center", font = ("Calibri", 14), width = 7)
        self.recordsToAffectNumberEntry.place(x=1010, y=232)

        # Adding button to update number of "records to affect" to user entry.
        self.recordsToAffectBtn = ttk.Button(container, text = "Update Records to Affect", style = 'buttonConfigFontHel11.TButton', width = 22, command = lambda name = "recordsToAffectBtn":self.button_clicked(name))
        self.recordsToAffectBtn.place(x=1095, y=232)

        # Adding label for SQL table, insert/updates and ancor variable.
        self.recordValueLabel = tk.Label(container, text="For SQL files only, choose the table to affect and select the type of        \naction and the anchor variable required for data created by this record.", bg="#9AB6EA", fg="Black", font=('Verdana', 10, 'bold'))
        self.recordValueLabel.place(x=640, y=265)

        # Adding textbox for sql table name entry.
        self.recordTableNameEntry = tk.Entry(container, relief = "sunken", justify = "center", font = ("Calibri", 11), width = 30)
        self.recordTableNameEntry.place(x=645, y=305)

        # Adding button to update sql table name to use in user entry.
        self.updateSQLitemsBtn = ttk.Button(container, text = "Update SQL Settings", style = 'buttonConfigFontHel11.TButton', width = 18, command = lambda name = "updateSQLitemsBtn":self.button_clicked(name))
        self.updateSQLitemsBtn.place(x=1163, y=270)

        # Adding a Combobox for insert or update sql selection.
        recordSqlActionList = ["Select SQL Action", "NONE", "INSERT", "UPDATE"]
        self.recordSqlAction = tk.StringVar()
        self.recordSqlAction.set(recordSqlActionList[0])
        self.recordSqlActionCmbo = ttk.Combobox(container, textvariable = self.recordSqlAction, state = "readonly", value = recordSqlActionList, justify = "left", width = 20, height = 35, font = ("Helvetica", 10, 'bold'))
        self.recordSqlActionCmbo.place(x=910, y=307)

        # Adding a Combobox for anchor name for sql UPDATE selection.
        recordSqlAnchorList = ["Select SQL Anchor", "NONE"]
        self.recordSqlAnchor = tk.StringVar()
        self.recordSqlAnchor.set(recordSqlAnchorList[0])
        self.recordSqlAnchorCmbo = ttk.Combobox(container, textvariable = self.recordSqlAnchor, state = "readonly", value = recordSqlAnchorList, justify = "left", width = 20, height = 35, font = ("Helvetica", 10, 'bold'))
        self.recordSqlAnchorCmbo.place(x=1150, y=307)

        # Adding the text area for user validation and editing.
        self.selectedTextArea = tkst.ScrolledText(container, width = 85, height = 15, relief = "sunken", wrap = tk.WORD)
        self.selectedTextArea.pack(padx = 10, pady = 10, fill = tk.BOTH, expand = True)
        self.selectedTextArea.insert(tk.INSERT, """""")
        self.selectedTextArea.place(x=630, y=338)

        # Adding the preview column button to see column entry in text area.
        self.previewColumnForRecordBtn = ttk.Button(container, text = "  Preview Column ", style = 'buttonConfigFontHel12.TButton', command = lambda name = "previewColumnForRecordBtn":self.button_clicked(name))
        self.previewColumnForRecordBtn.place(x=700, y=585)

        # Adding the Edit Column button to allow user to save edits in text area.
        self.editColumnInRecordBtn = ttk.Button(container, text = " Update Column ", style = 'buttonConfigFontHel12.TButton', command = lambda name = "editColumnInRecordBtn":self.button_clicked(name))
        self.editColumnInRecordBtn.place(x=870, y=585)

        # Adding the Add Column to Record button.
        self.addColumnToRecordBtn = ttk.Button(container, text = " Add Column ", style = 'buttonConfigFontHel12.TButton', command = lambda name = "addColumnToRecordBtn":self.button_clicked(name))
        self.addColumnToRecordBtn.place(x=1030, y=585)

        # Adding the delete column from record button.
        self.deleteColumnFromRecordBtn = ttk.Button(container, text = " Delete Column ", style = 'buttonConfigFontHel12.TButton', command = lambda name = "deleteColumnFromRecordBtn":self.button_clicked(name))
        self.deleteColumnFromRecordBtn.place(x=1160, y=585)

        # Adding the add record to configuration file button.
        self.addRecordToFileBtn = ttk.Button(container, text = "     Add a Record     ", style = 'buttonConfigFontHel14.TButton', command = lambda name = "addRecordToFileBtn":self.button_clicked(name))
        self.addRecordToFileBtn.place(x=740, y=635)

        # Adding the delete record from config file button.
        self.deleteRecordFromFileBtn = ttk.Button(container, text = "  Delete this Record  ", style = 'buttonConfigFontHel14.TButton', command = lambda name = "deleteRecordFromFileBtn":self.button_clicked(name))
        self.deleteRecordFromFileBtn.place(x=1020, y=635)

        # Adding the create data output file button.
        self.createDataOutputFileBtn = ttk.Button(container, text = "  Create Data File ", style = 'buttonConfigFontHel22.TButton', command = lambda name = "createDataOutputFileBtn":self.button_clicked(name))
        self.createDataOutputFileBtn.place(x=200, y=660)

# ------ from here starts the gui functions --------------------

        self.initialize_all_for_new_file("Select a Config File")

    def initialize_all_for_new_file(self, file_name):
        print("inside: initialize_all_for_new_file")
        self.columnsTitlesList  = []
        self.columnsValuesList  = []
        self.columnsTypesList   = []
        self.columnsFormatsList = []
        self.columnNamesCmbo.delete(0, tk.END)
        self.columnValuesCmbo.delete(0, tk.END)
        self.columnValueTypesCmbo.delete(0, tk.END)
        self.columnValueFormatsCmbo.delete(0, tk.END)
        self.columnsTitlesList.append("Select a Column Title")
        self.columnsValuesList.append("Select a Column Value")
        self.columnsTypesList.append("Select a Column Type")
        self.columnsFormatsList.append("Select a Column Format")
        self.columnNamesCmbo['values'] = [ self.columnsTitlesList ]
        self.columnValuesCmbo['values'] = [ self.columnsValuesList ]
        self.columnValueTypesCmbo['values'] = [ self.columnsTypesList ]
        self.columnValueFormatsCmbo['values'] = [ self.columnsFormatsList ]
        self.columnNamesCmbo.set(self.columnsTitlesList[0])
        self.columnValuesCmbo.set(self.columnsValuesList[0])
        self.columnValueTypesCmbo.set(self.columnsTypesList[0])
        self.columnValueFormatsCmbo.set(self.columnsFormatsList[0])
        self.recordsToAffectNumberEntry.delete(0, tk.END)
        self.recordsToAffectNumberEntry.insert(0, '0') 
        self.currentColumnNumberEntry.delete(0, tk.END)
        self.currentColumnNumberEntry.insert(0, '0')
        self.currentRecNumberEntry.delete(0, tk.END)
        self.currentRecNumberEntry.insert(0, '0')
        self.recordTableNameEntry.delete(0, tk.END)
        self.recordTableNameEntry.insert(0, 'None')
        self.recordSqlActionCmbo.current(1)
        self.recordSqlAnchorCmbo.current(1)
        config_file_name_index = self.get_config_file_name_index(file_name)
        self.configFileNamesCmbo.current(config_file_name_index)
        self.update_total_records_label('0')
        self.update_total_columns_label('0')
        self.set_number_of_records_needed_combo('Select a Number') 
        self.format_var.set(0)
        print("leaving: initialize_all_for_new_file")

    def get_config_file_name_index(self, file_name):
        print("inside: get_config_file_name_index")
        config_file_list = self.r.get_list_of_config_files_in_home_dir()
        config_file_index = 0
        num = 0
        for name in config_file_list:
            if name == file_name:
                config_file_index = num
                break
            num += 1
        print("leaving: get_config_file_name_index")
        return config_file_index
    
    def get_scrolltext_from_text_area(self):
        print("inside: get_scrolltext_from_text_area")
        text_str = self.selectedTextArea.get("1.0", END)
        textAreaFilterList = text_str.split("\n")
        column_element_list = []
        for row in textAreaFilterList:
            row = row.strip()
            if len(row) > 1:
                temp_cols = row.split(":")
                filter_tmp = temp_cols[1].replace("\n", "")
                filter_tmp = filter_tmp.strip()
                column_element_list.append(filter_tmp)
        print("leaving: get_scrolltext_from_text_area")
        return column_element_list
    
    def refresh_combobox_configuration_file_list(self, file_name):
        print("inside: refresh_combobox_configuration_file_list")
        file_list = self.r.get_list_of_config_files_in_home_dir()
        self.configFileNamesCmbo['values'] = file_list
        self.selectedConfigFile.set(file_name)
        print("leaving: refresh_combobox_configuration_file_list")

    def set_record_file_type(self, record_file_type):
        print("inside: set_record_file_type")
        self.recordFileType = record_file_type
        print("leaving: set_record_file_type")
    
    def create_output_file_name(self, user_given_name, file_type):
        print("inside: create_output_file_name")
        result = ""
        if 'None' not in user_given_name:
            now = datetime.now()
            str_date = now.strftime("%m-%d-%Y-%H_%M")
            str_sid = os.environ.get('USERNAME')
            result = '{}_{}_{}.{}'.format(str_sid, user_given_name, str_date, file_type)
        print("leaving: create_output_file_name")
        return result
    
    def clear_config_data_from_entry_textboxes(self):
        print("inside: clear_config_data_from_entry_textboxes")
        self.columnNameEditedEntry.delete(0, tk.END)
        self.columnValueEditedEntry.delete(0, tk.END)
        self.customValueTypeEditEntry.delete(0, tk.END)
        self.customValueFormatEditEntry.delete(0, tk.END)
        print("leaving: clear_config_data_from_entry_textboxes")
    
    def clear_column_custom_entryboxes_and_reload_comboboxes(self):
        print("inside: clear_column_custom_entryboxes_and_reload_comboboxes")
        self.columnNameEditedEntry.delete(0, tk.END)
        self.columnValueEditedEntry.delete(0, tk.END)
        self.customValueTypeEditEntry.delete(0, tk.END)
        self.customValueFormatEditEntry.delete(0, tk.END)
        self.add_list_to_combo_drop_down(self.columnsTitlesList, "Title") 
        self.add_list_to_combo_drop_down(self.columnsValuesList, "Value")
        self.add_list_to_combo_drop_down(self.columnsTypesList, "Type")
        self.add_list_to_combo_drop_down(self.columnsFormatsList, "Format")
        print("leaving: clear_column_custom_entryboxes_and_reload_comboboxes")
    
    def initialize_config_file_selection_and_column_selection(self, file_name, record_index, clone_flag):
        print("inside: initialize_config_file_selection_and_column_selection")
        self.r = reader.FileReadOperations()
        self.d = dicts.DictionaryOperations()
        self.f = reader.FileReadOperations()
        columns_in_order_list = []
        file_dict = {}
        print(f"clone_flag=====> ", clone_flag)
        print(f"file_name======> ", file_name)
        if file_name != "Create New Configuration File" and clone_flag is True:
            file_dict = self.current_file_dict
        elif file_name != "Create New Configuration File" and clone_flag is False:
            file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
        else:
            print("NO FILE_DICT WAS INITIALIZED!")

        if file_name != "Create New Configuration File":
            records_needed = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 0, "records_needed")
            file_format = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 1, "file_format")
            config_records = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 3, "config_records")
            columns_per_record = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 4, "columns_per_record")
            sql_table = self.d.retrieve_sql_table_from_dictionary(file_dict, record_index)
            sql_action = self.d.retrieve_sql_action_from_dictionary(file_dict, record_index)
            sql_anchor = self.d.retrieve_sql_anchor_from_dictionary(file_dict, record_index)
            records_to_affect = self.d.retrieve_records_to_affect_from_dictionary(file_dict, record_index)
            titles_list = self.d.retrieve_all_column_titles_from_record(file_dict, record_index)
            titles_list.insert(0, "Select SQL Anchor")
            self.recordSqlAnchorCmbo['values'] = titles_list
        
            self.set_number_of_records_needed_combo(records_needed)
            self.currentColumnNumberEntry.delete(0, tk.END)
            self.currentColumnNumberEntry.insert(0, 1)
            self.currentRecNumberEntry.delete(0, tk.END)
            self.currentRecNumberEntry.insert(0, 1)
            self.recordsToAffectNumberEntry.delete(0, tk.END)
            self.recordsToAffectNumberEntry.insert(0, records_to_affect)
            self.set_file_format_for_output_file(file_format)
            self.update_sql_table_name_entry(sql_table)
            self.set_record_sql_action_combo(sql_action)
            self.set_record_sql_anchor_combo(sql_anchor, titles_list)
            
            record_one_records_to_affect = self.d.retrieve_records_to_affect_from_dictionary(file_dict, record_index)
            record_one_sql_table = self.d.retrieve_sql_table_from_dictionary(file_dict, record_index)
            record_one_sql_action = self.d.retrieve_sql_action_from_dictionary(file_dict, record_index)
            record_one_sql_anchor = self.d.retrieve_sql_anchor_from_dictionary(file_dict, record_index)
            
            title_index = 0
            value_index = 1
            type_index = 2
            format_index = 3
            number_of_columns = int(columns_per_record)
            for column_index in range(0, number_of_columns):
                print(f"column on:", str(column_index))
                columns_in_order_list.append( self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, title_index, "TITLE") )
                columns_in_order_list.append( self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, value_index, "VALUE") )
                columns_in_order_list.append( self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, type_index, "TYPE") )
                columns_in_order_list.append( self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, format_index, "FORMAT") )
            self.initialize_titles_values_types_formats_when_config_is_selected(records_needed, file_format, columns_in_order_list, record_one_sql_table, record_one_sql_action, record_one_sql_anchor, config_records, columns_per_record, record_one_records_to_affect)
            self.current_file_dict = file_dict
        print("leaving: initialize_config_file_selection_and_column_selection")

    def initialize_saved_config_file_selection_and_column_selection(self, file_name, record_index):
        print("initialize_saved_config_file_selection: file_name --> "+file_name)
        self.r = reader.FileReadOperations()
        self.d = dicts.DictionaryOperations()
        
        columns_in_order_list = []
        record_one_sql_table = ""
        record_one_sql_action = ""
        record_one_sql_anchor = ""
        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)

        if file_name != "":
            records_needed = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 0, "records_needed")
            file_format = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 1, "file_format")
            config_records = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 3, "config_records")
            columns_per_record = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 4, "columns_per_record")
            records_to_affect = self.d.retrieve_records_to_affect_from_dictionary(file_dict, record_index)
            record_one_sql_table = self.d.retrieve_sql_table_from_dictionary(file_dict, record_index)
            record_one_sql_action = self.d.retrieve_sql_action_from_dictionary(file_dict, record_index)
            record_one_sql_anchor = self.d.retrieve_sql_anchor_from_dictionary(file_dict, record_index)
            print(f"total record count:", config_records)
            for y in range(0, int(columns_per_record)):
                print(f"column on:", str(y))
                columns_in_order_list.append( self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, y, 0, "TITLE") )
                columns_in_order_list.append( self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, y, 1, "VALUE") )
                columns_in_order_list.append( self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, y, 2, "TYPE") )
                columns_in_order_list.append( self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, y, 3, "FORMAT") )
            self.initialize_titles_values_types_formats_when_config_is_selected(records_needed, file_format, columns_in_order_list, record_one_sql_table, record_one_sql_action, record_one_sql_anchor, config_records, columns_per_record, records_to_affect)
            self.current_file_dict = file_dict
        print("leaving: initialize_saved_config_file_selection_and_column_selection")

    def initialize_titles_values_types_formats_when_config_is_selected(self, records_needed, file_format, columns_in_order_list, record_one_sql_table, record_one_sql_action, record_one_sql_anchor, config_records, columns_per_record, record_one_records_to_affect):
        print("inside: initialize_titles_values_types_formats_when_config_is_selected")
        unique_titles_list  = []
        unique_values_list  = []
        unique_types_list   = []
        unique_formats_list = []
        for y in range(0, len(columns_in_order_list), 4):
            if columns_in_order_list[y] not in unique_titles_list:
                unique_titles_list.append(columns_in_order_list[y])          
            if columns_in_order_list[(y+1)] not in unique_values_list:
                unique_values_list.append(columns_in_order_list[(y+1)])                
            if columns_in_order_list[(y+2)] not in unique_types_list:
                unique_types_list.append(columns_in_order_list[(y+2)])                
            if columns_in_order_list[(y+3)] not in unique_formats_list:
                unique_formats_list.append(columns_in_order_list[(y+3)])
        # add unique titles list to dropdown
        self.add_list_to_combo_drop_down(unique_titles_list, "Title")            
        # add unique values list to dropdown
        self.add_list_to_combo_drop_down(unique_values_list, "Value")    
        # add unique types list to dropdown
        self.add_list_to_combo_drop_down(unique_types_list, "Type")            
        # add unique format list to dropdown
        self.add_list_to_combo_drop_down(unique_formats_list, "Format")
        # set total records label.
        self.update_total_records_label(config_records)
        # set total columns label.
        self.update_total_columns_label(columns_per_record)
        # populate records to affect textbox.
        self.update_records_to_affect_amount(record_one_records_to_affect, 0)
        # populate sql table textbox if sql format is selected.
        self.update_sql_table_name_entry(str(record_one_sql_table))
        # auto-select sql action if selected.
        self.set_record_sql_action_combo(str(record_one_sql_action))
        # auto-select sql anchor if selected.
        self.set_record_sql_anchor_combo(str(record_one_sql_anchor), unique_titles_list)
        # auto-select data records needed
        self.set_number_of_records_needed_combo(str(records_needed)) 
        # auto-select format requested
        self.set_file_format_for_output_file(file_format)
        print("leaving: initialize_titles_values_types_formats_when_config_is_selected")
    
    def set_file_format_for_output_file(self, file_format):
        print("inside: set_file_format_for_output_file")
        if file_format == "csv":
            self.format_var.set(0)
        elif file_format == "parquet":
            self.format_var.set(1)
        elif file_format == "json":
            self.format_var.set(2)
        elif file_format == "sql":
            self.format_var.set(3)
        print("leaving: set_file_format_for_output_file")

    def get_file_file_format_by_number(self, format_number):
        print("inside: get_format_by_number")
        match str(format_number):
            case "0":
                return "csv"
            case "1":
                return "parquet"
            case "2":
                return "json"
            case "3":
                return "sql"
        print("leaving: get_format_by_number")

    def set_record_sql_action_combo(self, sql_action):
        print("inside: set_record_sql_action_combo")
        actions_list = ["Select SQL Action", "NONE", "INSERT", "UPDATE"]
        index_number = 0
        for word in actions_list:
            if word == sql_action:
                break
            index_number += 1
        self.recordSqlActionCmbo.current(index_number)
        print("leaving: set_record_sql_action_combo")

    def set_record_sql_anchor_combo(self, sql_anchor, unique_titles_list):
        print("inside: set_record_sql_anchor_combo")
        unique_titles_list.pop(0)
        unique_titles_list.insert(0, "NONE")
        unique_titles_list.insert(0, "Select SQL Anchor")
        self.recordSqlAnchorCmbo['values'] = unique_titles_list
        index_number = 0
        for word in unique_titles_list:
            print("word: "+word)
            if word == sql_anchor:
                break
            index_number += 1
        self.recordSqlAnchorCmbo.current(index_number)
        print("leaving: set_record_sql_anchor_combo")

    def set_column_combo_to_column(self, record_number, file_dict, set_value, component_name):
        print("inside: set_column_combo_to_column")
        message = 'Select a Column {}'.format(component_name)
        list = []
        match component_name:
            case "Title":
                list = self.d.retrieve_all_column_titles_from_record(file_dict, record_number)
            case "Value":
                list = self.d.retrieve_all_column_values_from_record(file_dict, record_number)
            case "Type":
                list = self.d.retrieve_all_column_types_from_record(file_dict, record_number)
            case "Format":
                list = self.d.retrieve_all_column_formats_from_record(file_dict, record_number)
        list.insert(0, message)
        new_list = []
        for member in list:
            if member not in new_list:
                new_list.append(member)
        combo_index = 0
        num = 0
        for word in new_list:
            if word == set_value:
                break
            num += 1
        combo_index = num
        print("leaving: set_column_combo_to_column")
        return combo_index    

    def set_number_of_records_needed_combo(self, records_needed):
        print("inside: set_number_of_records_needed_combo")
        self.numOfRecordsNeededCmbo.set(str(records_needed))
        print("leaving: set_number_of_records_needed_combo")

    def update_sql_table_name_entry(self, record_sql_table_name):
        print("inside: update_sql_table_name_entry")
        self.recordTableNameEntry.delete(0, tk.END)
        self.recordTableNameEntry.insert(0, str(record_sql_table_name))
        print("leaving: update_sql_table_name_entry")

    def update_total_columns_label(self, total_columns_per_record):
        print("inside: update_total_columns_label")
        self.totalColumnsLabel.config( text = str(total_columns_per_record))
        self.totalColumnsLabel.update()
        print("leaving: update_total_columns_label")

    def update_total_records_label(self, total_records_number):
        print("inside: update_total_records_label")
        self.totalRecordsLabel.config( text = str(total_records_number))
        self.totalRecordsLabel.update()
        print("leaving: update_total_records_label")
    
    def add_list_to_combo_drop_down(self, unique_list, component_name):
        print("inside: add_list_to_combo_drop_down")
        message = 'Select a Column {}'.format(component_name)
        unique_list.insert(0, message)
        match component_name:
            case "Title":
                self.columnNamesCmbo['values'] = unique_list
                self.columnNamesCmbo.set(unique_list[0])
            case "Value":
                self.columnValuesCmbo['values'] = unique_list
                self.columnValuesCmbo.set(unique_list[0])
            case "Type":
                self.columnValueTypesCmbo['values'] = unique_list
                self.columnValueTypesCmbo.set(unique_list[0])
            case "Format":
                self.columnValueFormatsCmbo['values'] = unique_list
                self.columnValueFormatsCmbo.set(unique_list[0])
        print("leaving: add_list_to_combo_drop_down")
        
    def have_user_create_a_new_file_name(self):
        print("inside: have_user_create_a_new_file_name")
        user_input = simpledialog.askstring(title = 'Name New Config File', prompt = "format example: 'AttendanceData'")
        file_name = self.create_output_file_name(user_input, "cfg")
        if len(file_name) > 0:
            if file_name not in self.configFileNamesCmbo['values']:
                self.configFileNamesCmbo['values'] = (*self.configFileNamesCmbo['values'], file_name)
                result = self.w.create_new_configuration_file(file_name)
                if not result:
                    print("Log: Could Not Create: "+file_name)
                    print("leaving: have_user_create_a_new_file_name")
                else:
                    print("leaving: have_user_create_a_new_file_name")
                    return file_name
        return
    
    def get_array_of_numbers(self):
        print("inside: get_array_of_numbers")
        number_list = []
        for x in range(1, 10001):
            number_list.append(x)
        print("leaving: get_array_of_numbers")
        return number_list
    
    def get_number_of_total_records_in_file(self, file_name):
        print("inside: get_number_of_total_records_in_file")
        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
        record_count = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 3, "config_records")
        print("leaving: get_number_of_total_records_in_file")
        return record_count
    
    def get_total_columns_per_record(self, file_name):
        print("inside: get_total_columns_per_record")
        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
        current_column_count = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 4, "columns_per_record")
        print("leaving: get_total_columns_per_record")
        return current_column_count

    def get_record_count_for_config_file(self):
        print("inside: get_record_count_for_config_file")
        total_rec_cnt = len(self.masterColNames)
        print("leaving: get_record_count_for_config_file")
        return total_rec_cnt
    
    def add_additional_format_to_column(self):
        print("inside: add_additional_format_to_column")
        self.columnFormat = self.columnValueFormatsCmbo.get()
        if self.columnFormat == 'Select a Column Format':
            self.columnFormat = self.customValueFormatEdit.get()
        # gather text from scrolled text area.
        text_content = self.selectedTextArea.get("1.0", tk.END)
        rows = text_content.split("\n")
        new_title  = '{}\n'.format(rows[0])
        new_value = '{}\n'.format(rows[1])
        new_type  = '{}\n'.format(rows[2])
        new_format = '{}@{}\n'.format(rows[3], self.columnFormat)
        # clear textarea, reset combos and editboxs.
        self.selectedTextArea.delete('1.0', tk.END)
        self.clear_config_data_from_entry_textboxes()
        # update view of data in textarea.
        self.selectedTextArea.insert(tk.INSERT, new_title)
        self.selectedTextArea.insert(tk.INSERT, new_value)
        self.selectedTextArea.insert(tk.INSERT, new_type)
        self.selectedTextArea.insert(tk.INSERT, new_format)
        #self.fill_comboboxes_with_selectable_data()
        print("leaving: add_additional_format_to_column")
            
    def update_records_to_affect_amount(self, records_to_affect, record_index):
        print("inside: update_records_to_affect_amount")
        file_name = self.configFileNamesCmbo.get()
        if file_name != "Create New Configuration File":
            file_name = self.configFileNamesCmbo.get()
            file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
            file_dict = self.d.update_records_to_affect_in_dictionary(file_dict, record_index, records_to_affect)
            self.current_file_dict = file_dict
            self.recordsToAffectNumberEntry.delete(0, tk.END)
            self.recordsToAffectNumberEntry.insert(0, records_to_affect)
        print("leaving: update_records_to_affect_amount\n")
        
    def initialize_column_and_record_navigation(self,  recordNumber, columnNumber):
        print("inside: initialize_column_and_record_navigation")
        self.currentColumnNumberEntry.delete(0, END)
        self.currentRecNumberEntry.delete(0, END)
        self.currentColumnNumberEntry.insert(0, str(columnNumber))
        self.currentRecNumberEntry.insert(0, str(recordNumber))
        print("leaving: initialize_column_and_record_navigation")
    
    def display_column_data_in_textarea(self):
        print("inside: display_column_data_in_textarea")
        self.columnName = self.columnNamesCmbo.get()
        self.columnValue = self.columnValuesCmbo.get()
        self.columnType = self.columnValueTypesCmbo.get()
        self.columnFormat = self.columnValueFormatsCmbo.get()
        # clear out everything from comboboxes.
        self.columnNamesCmbo['values'] = []
        self.columnValuesCmbo['values'] = []
        self.columnValueTypesCmbo['values'] = []
        self.columnValueFormatsCmbo['values'] = []
        # check to see if we are selecting from combos or creating new values in custom textboxes.
        if self.columnName == 'Select a Column Title':
            self.columnName = self.customNameEdit.get()
        if self.columnValue == 'Select a Column Value':
            self.columnValue = self.customValueEdit.get()
        if self.columnType == 'Select a Column Type':
            self.columnType = self.customValueTypeEdit.get()
        if self.columnFormat == 'Select a Column Format':
            self.columnFormat = self.customValueFormatEdit.get()
        # Formating and Adding config data to textarea display.
        new_name   = '{}: {}\n'.format('Column Title  ', self.columnName)
        new_value  = '{}: {}\n'.format('Column Value  ', self.columnValue)
        new_type   = '{}: {}\n'.format('Column Type   ', self.columnType)
        new_format = '{}: {}\n\n'.format('Column Format ', self.columnFormat)
        
        self.selectedTextArea.insert(tk.INSERT, new_name)
        self.selectedTextArea.insert(tk.INSERT, new_value)
        self.selectedTextArea.insert(tk.INSERT, new_type)
        self.selectedTextArea.insert(tk.INSERT, new_format)
        self.columnsTitlesList.append(self.columnName)
        self.columnsValuesList.append(self.columnValue)
        self.columnsTypesList.append(self.columnType)
        self.columnsFormatsList.append(self.columnFormat)
        # clear column custom emtrytextboxes.
        self.clear_column_custom_entryboxes_and_reload_comboboxes()
        self.add_new_data_to_column_combos("Title")
        self.add_new_data_to_column_combos("Value")
        self.add_new_data_to_column_combos("Type")
        self.add_new_data_to_column_combos("Format")
        print("leaving: display_column_data_in_textarea")
       
    def increment_total_record_count(self, records_per_file):
        print("inside: increment_total_record_count")
        self.totalRecordsLabel.config( text = str(records_per_file) )
        self.totalRecordsLabel.update()
        print("leaving: increment_total_record_count")

    def clear_column_config_from_text_area(self):
        print("inside: clear_column_config_from_text_area")
        self.selectedTextArea.delete('1.0', tk.END)
        print("leaving: clear_column_config_from_text_area")
        
    def create_new_config_file(self):
        print("inside: create_new_config_file")
        self.clear_config_data_from_entry_textboxes()
        file_name = self.have_user_create_a_new_file_name()
        if len(file_name) > 0:
            self.refresh_combobox_configuration_file_list(file_name)
            record_number = 0
            column_number = 0
            self.initialize_column_and_record_navigation(record_number, column_number)
            self.initialize_all_for_new_file(file_name)
        print("leaving: create_new_config_file")
        
    def go_straight_to_column_of_record(self):
        print("inside: go_straight_to_column_of_record")
        file_name = self.configFileNamesCmbo.get()
        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
        record_number_check = str(self.currentRecNumberEntry.get())
        column_number_check = str(self.currentColumnNumberEntry.get())
        if column_number_check.isdigit() == False or record_number_check.isdigit() == False:
            return
        record_number = int(record_number_check)
        column_number = int(column_number_check)
        total_columns = int(self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 4, "columns_per_record"))
        
        if column_number >= 1 and column_number <= total_columns:
            column_index = (column_number - 1) 
            record_index = (record_number - 1)
            column_name   = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 0, "TITLE")       
            column_value  = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 1, "VALUE")
            column_type   = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 2, "TYPE")
            column_format = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 3, "FORMAT")          
            title_index = self.set_column_combo_to_column(record_index, file_dict, column_name, "Title")
            value_index = self.set_column_combo_to_column(record_index, file_dict, column_value, "Value")
            type_index = self.set_column_combo_to_column(record_index, file_dict, column_type, "Type")
            format_index = self.set_column_combo_to_column(record_index, file_dict, column_format, "Format") 
            self.columnNamesCmbo.current(title_index)
            self.columnValuesCmbo.current(value_index)
            self.columnValueTypesCmbo.current(type_index)
            self.columnValueFormatsCmbo.current(format_index)
            self.currentRecNumberEntry.delete(0, END)
            self.currentRecNumberEntry.insert(0, str(record_number))
            self.currentColumnNumberEntry.delete(0, END)
            self.currentColumnNumberEntry.insert(0, str(column_number))
            self.totalColumnsLabel .configure( text = str(total_columns) )
            self.totalColumnsLabel.update()
            self.current_file_dict = file_dict
        print("leaving: go_straight_to_column_of_record\n")

    def go_to_column_by_direction(self, directional_flag):
        print("inside: go_to_column_by_direction")
        file_name = self.configFileNamesCmbo.get()
        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
        total_columns = int(self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 4, "columns_per_record"))
        record_number = int(self.currentRecNumberEntry.get())
        column_number = int(self.currentColumnNumberEntry.get())
        safe_flag = False
        if directional_flag == "previous":
            if column_number > 1 and column_number <= total_columns:
                column_number -= 1
                safe_flag = True
        elif directional_flag == "next":
            if column_number >= 1 and column_number < total_columns:
                column_number += 1
                safe_flag = True
        if safe_flag is True:  
            column_index = (column_number - 1) 
            record_index = (record_number - 1)
            print(f"---->column_index:", column_index)
            column_name   = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 0, "TITLE")       
            column_value  = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 1, "VALUE")
            column_type   = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 2, "TYPE")
            column_format = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 3, "FORMAT") 
            print(f"---->column_name:", column_name)   
            print(f"---->column_value:", column_value)
            print(f"---->column_type:", column_type)   
            print(f"---->column_format:", column_format)     
            title_index = self.set_column_combo_to_column(record_index, file_dict, column_name, "Title")
            value_index = self.set_column_combo_to_column(record_index, file_dict, column_value, "Value")
            type_index = self.set_column_combo_to_column(record_index, file_dict, column_type, "Type")
            format_index = self.set_column_combo_to_column(record_index, file_dict, column_format, "Format") 
            self.columnNamesCmbo.current(title_index)
            self.columnValuesCmbo.current(value_index)
            self.columnValueTypesCmbo.current(type_index)
            self.columnValueFormatsCmbo.current(format_index)
            self.currentRecNumberEntry.delete(0, END)
            self.currentRecNumberEntry.insert(0, str(record_number))
            self.currentColumnNumberEntry.delete(0, END)
            self.currentColumnNumberEntry.insert(0, str(column_number))
            self.totalColumnsLabel.configure( text = str(total_columns) )
            self.totalColumnsLabel.update()
            self.current_file_dict = file_dict
        print("leaving: go_to_column_by_direction\n")

    def go_to_record_by_direction(self, directional_flag):
        print("inside: go_to_record_by_direction")
        file_name = self.configFileNamesCmbo.get()
        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
        file_name = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 2, "file_name")
        total_records = int(self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 3, "config_records"))
        record_number = int(self.currentRecNumberEntry.get())
        record_index = (record_number - 1)
        safe_flag = False
        if directional_flag == "previous":
            if record_number > 1 and record_number <= total_records:
                record_number -= 1
                safe_flag = True
        elif directional_flag == "next":
            print("inside next condition")
            if record_number < total_records and record_number >= 0:
                record_number += 1
                safe_flag = True
        if safe_flag is True: # and record_number <= total_records:
            # empty combos 
            self.clear_config_data_from_entry_textboxes()
            record_index = (record_number - 1)
            print(f"record_index----> ", record_index)
            # intialize combos
            self.initialize_config_file_selection_and_column_selection(file_name, record_index, False)
            column_name   = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, 0, 0, "TITLE")       
            column_value  = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, 0, 1, "VALUE")
            column_type   = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, 0, 2, "TYPE")
            column_format = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, 0, 3, "FORMAT") 
            records_to_affect = self.d.retrieve_records_to_affect_from_dictionary(file_dict, record_index)
            title_index = self.set_column_combo_to_column(record_index, file_dict, column_name, "Title")
            value_index = self.set_column_combo_to_column(record_index, file_dict, column_value, "Value")
            type_index = self.set_column_combo_to_column(record_index, file_dict, column_type, "Type")
            format_index = self.set_column_combo_to_column(record_index, file_dict, column_format, "Format") 
            self.columnNamesCmbo.current(title_index)
            self.columnValuesCmbo.current(value_index)
            self.columnValueTypesCmbo.current(type_index)
            self.columnValueFormatsCmbo.current(format_index)  
            self.currentColumnNumberEntry.delete(0, tk.END)
            self.currentColumnNumberEntry.insert(0, '1')
            self.currentRecNumberEntry.delete(0, tk.END)
            self.currentRecNumberEntry.insert(0, str(record_number))
            self.recordsToAffectNumberEntry.delete(0, tk.END)
            self.recordsToAffectNumberEntry.insert(0, str(records_to_affect))
        self.current_file_dict = file_dict
        print("leaving: go_to_record_by_direction\n")
            
    def go_straight_to_record(self):
        print("inside: go_straight_to_record")
        file_name = self.configFileNamesCmbo.get()
        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
        record_number_check = str(self.currentRecNumberEntry.get())
        column_number_check = str(self.currentColumnNumberEntry.get())
        if column_number_check.isdigit() == False or record_number_check.isdigit() == False:
            return
        file_name = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 2, "file_name")
        record_number = int(record_number_check)
        column_number = int(column_number_check)
        total_records = int(self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 3, "config_records"))
        total_columns = int(self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 4, "columns_per_record"))
        if (record_number >= 1 and record_number <= total_records) and (column_number <= total_columns and column_number > 0):
            column_index = (column_number - 1) 
            record_index = (record_number - 1)
            self.clear_config_data_from_entry_textboxes()
            # intialize combos
            self.initialize_config_file_selection_and_column_selection(file_name, record_index, True)
            column_name   = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 0, "TITLE")       
            column_value  = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 1, "VALUE")
            column_type   = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 2, "TYPE")
            column_format = self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 3, "FORMAT") 
            records_to_affect = self.d.retrieve_records_to_affect_from_dictionary(file_dict, record_index)
            title_index = self.set_column_combo_to_column(record_index, file_dict, column_name, "Title")
            value_index = self.set_column_combo_to_column(record_index, file_dict, column_value, "Value")
            type_index = self.set_column_combo_to_column(record_index, file_dict, column_type, "Type")
            format_index = self.set_column_combo_to_column(record_index, file_dict, column_format, "Format") 
            self.columnNamesCmbo.current(title_index)
            self.columnValuesCmbo.current(value_index)
            self.columnValueTypesCmbo.current(type_index)
            self.columnValueFormatsCmbo.current(format_index)  
            self.currentColumnNumberEntry.delete(0, END)
            self.currentColumnNumberEntry.insert(0, str(column_number))
            self.currentRecNumberEntry.delete(0, END)
            self.currentRecNumberEntry.insert(0, str(record_number))
            self.recordsToAffectNumberEntry.delete(0, END)
            self.recordsToAffectNumberEntry.insert(0, str(records_to_affect))
        self.current_file_dict = file_dict
        print("leaving: go_straight_to_record\n")
    
    def get_size_of_file(self, file_name):
        print("inside: get_size_of_file")
        size_of_file = self.r.get_size_of_file(file_name)
        print("leaving: get_size_of_file")
        return size_of_file
    
    def add_new_data_to_column_combos(self, component_name):
        check_list = []
        component_list = []
        new_list = []
        component = self.columnNamesCmbo
        match component_name:
            case "Title":
                component_list = self.columnsTitlesList
                component = self.columnNamesCmbo
            case "Value":
                component_list = self.columnsValuesList
                component = self.columnValuesCmbo
            case "Type":
                component_list = self.columnsTypesList
                component = self.columnValueTypesCmbo
            case "Format":
                component_list = self.columnsFormatsList
                component = self.columnValueFormatsCmbo
        
        for element in component_list:
            message = 'element: {}'.format(element)
            print(message)
            if element not in check_list:
                check_list.append(element)
                new_list.append(element)
        component['values'] = new_list   
        component.set(new_list[0])

    def set_records_to_affect_and_column_data_in_record(self, record_number, column_number):
        print("inside: set_records_to_affect_and_column_data_in_record")
        file_name = self.configFileNamesCmbo.get()
        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
        title_string  = str(self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_number, column_number, 0, "TITLE"))
        value_string  = str(self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_number, column_number, 1, "VALUE"))
        type_string   = str(self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_number, column_number, 2, "TYPE"))
        format_string = str(self.d.retrieve_a_column_value_of_a_record_in_dictionary(file_dict, record_number, column_number, 3, "FORMAT"))
        records_to_affect = str(self.d.retrieve_records_to_affect_from_dictionary(file_dict, record_number))
        self.columnNamesCmbo.set(title_string)
        self.columnValuesCmbo.set(value_string)
        self.columnValueTypesCmbo.set(type_string)
        self.columnValueFormatsCmbo.set(format_string)
        self.recordsToAffectNumberEntry.delete(0, END)
        self.recordsToAffectNumberEntry.insert(0, records_to_affect)
        self.currentColumnNumberEntry.delete(0, END)
        column_number += 1
        self.currentColumnNumberEntry.insert(0, str(column_number))
        self.currentRecNumberEntry.delete(0, END)
        record_number += 1
        self.currentRecNumberEntry.insert(0, str(record_number))
        # total_records = str(self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 3, "config_records"))
        # self.update_total_records_label(total_records)
        self.current_file_dict = file_dict
        print("leaving: set_records_to_affect_and_column_data_in_record")

    def create_cloned_file(self, old_file_name):
        new_file_name = self.have_user_create_a_new_file_name()
        self.w.copy_selected_file_and_rename_copy(old_file_name, new_file_name)
        self.configFileNamesCmbo.set(new_file_name)
        self.initialize_config_file_selection_and_column_selection(new_file_name, 0, True)
        self.set_records_to_affect_and_column_data_in_record(0, 0)
        return new_file_name

    def get_contents_from_text_area(self):
        print("inside: get_contents_from_text_area")
        num = 1
        titles = []
        values = []
        types  = []
        formats= []
        text = self.get_scrolltext_from_text_area()
        for element in text:
            match num:
                case 1:
                    titles.append(element)
                    num += 1
                case 2:
                    values.append(element)
                    num += 1
                case 3:
                    types.append(element)
                    num += 1
                case 4:
                    formats.append(element)
                    num = 1
        print("leaving: get_contents_from_text_area")
        return (titles, values, types, formats)

    def add_text_area_contents_to_add_additional_record_to_file(self):
        print("inside: add_text_area_contents_to_add_additional_record_to_file")
        file_name = self.configFileNamesCmbo.get()
        current_record_count = int(self.totalRecordsLabel.cget("text"))
        print(f"previous record count:", current_record_count)
        current_record_count += 1
        record_list = []
        titles = []
        values = []
        types  = []
        formats= []
        (titles, values, types, formats) = self.get_contents_from_text_area()
        records_to_affect = self.recordsToAffectNumberEntry.get()
        record_list.append(records_to_affect)
        sql_table = self.recordTableNameEntry.get()
        record_list.append(sql_table)
        sql_action = self.recordSqlActionCmbo.get()
        record_list.append(sql_action)
        sql_anchor = self.recordSqlAnchorCmbo.get()
        record_list.append(sql_anchor)

        file_list = self.r.get_list_from_from_user_config_file(file_name)
        file_list = self.l.add_additional_record_to_file_list(file_list, record_list, titles, values, types, formats, str(current_record_count))
        # remove old file and create new file with added data.
        result = self.w.delete_unwanted_file(file_name, "user-config-path")
        if result is True:
            self.w.write_list_to_file("user-config-path", file_name, file_list)
        else:
            print("=====> problem deleting old user-config-file.")
        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
        self.increment_total_record_count(current_record_count)
        # update file dict for total records 
        file_dict = self.d.update_a_file_statistic_in_dictionary(file_dict, 3, "config_records", current_record_count)
        self.current_file_dict = file_dict
        print("leaving: add_text_area_contents_to_add_additional_record_to_file")

    def add_contents_of_text_area_to_create_a_new_record(self, number_of_records):
        print("inside: add_contents_of_text_area_to_create_a_new_record")
        general_list = []
        record_list = []
        titles = []
        values = []
        types  = []
        formats= []
        records_needed = self.numOfRecordsNeededCmbo.get()
        general_list.append(records_needed)
        file_format = self.recordFileType
        general_list.append(file_format)
        file_name = self.configFileNamesCmbo.get()
        general_list.append(file_name)
        general_list.append(number_of_records)     
        (titles, values, types, formats) = self.get_contents_from_text_area()
        columns_per_record = len(titles)
        general_list.append(columns_per_record)
        records_to_affect = self.recordsToAffectNumberEntry.get()
        record_list.append(records_to_affect)
        sql_table = self.recordTableNameEntry.get()
        record_list.append(sql_table)
        sql_action = self.recordSqlActionCmbo.get()
        record_list.append(sql_action)
        sql_anchor = self.recordSqlAnchorCmbo.get()
        record_list.append(sql_anchor)
        file_list = self.l.create_and_return_new_file_list_from_data_lists(general_list, record_list, titles, values, types, formats)
        self.w.write_list_to_file("user-config-path", file_name, file_list)
        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
        self.current_file_dict = file_dict
        print("leaving: add_contents_of_text_area_to_create_a_new_record")

    def add_new_column_to_all_records(self, new_column_list):
        print("inside: add_new_column_to_all_records")
        file_name = self.configFileNamesCmbo.get()
        general_list = [5]
        records_needed = self.numOfRecordsNeededCmbo.get()
        general_list.append(records_needed)
        file_format = self.recordFileType
        general_list.append(file_format)
        file_name = self.configFileNamesCmbo.get()
        general_list.append(file_name)
        number_of_records = int(self.get_number_of_total_records_in_file(file_name))
        general_list.append(number_of_records)
        columns_per_record = int(self.get_total_columns_per_record(file_name))
        new_columns_per_record = (columns_per_record + 1)
        general_list.append(new_columns_per_record)
        new_file_list = self.l.add_additional_column_to_all_records_in_file_list(new_column_list, general_list)
        result = self.w.delete_unwanted_file(file_name, "user-config-path")
        if result is True:
            self.w.write_list_to_file("user-config-path", file_name, new_file_list)
        else:
            print("=====> problem deleting old user-config-file.")
        # update number of columns per record in file dict
        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
        file_dict = self.d.update_a_file_statistic_in_dictionary(file_dict, 5, "columns_per_record", str(new_columns_per_record))
        self.current_file_dict = file_dict
        print("leaving: add_new_column_to_all_records")

    def update_column_in_record(self):
        print("inside: update_column_in_record")
        column_number = int(self.currentColumnNumberEntry.get())
        record_number = int(self.currentRecNumberEntry.get())
        file_name = self.configFileNamesCmbo.get()
        column_index = column_number - 1
        record_index = record_number - 1
        print(f"column_index", column_index)
        print(f"record_index", record_index)
        column_elements = self.get_scrolltext_from_text_area()
        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
        file_dict = self.d.update_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 0, "TITLE", column_elements[0] )
        file_dict = self.d.update_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 1, "VALUE", column_elements[1] )
        file_dict = self.d.update_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 2, "TYPE",  column_elements[2] )
        file_dict = self.d.update_a_column_value_of_a_record_in_dictionary(file_dict, record_index, column_index, 3, "FORMAT", column_elements[3] )
        file_list = self.l.create_a_list_from_dictionary(file_dict)
        result = self.w.delete_unwanted_file(file_name, "user-config-path")
        if result is True:
            self.w.write_list_to_file("user-config-path", file_name, file_list)
        else:
            print("=====> problem deleting old user-config-file.")
        self.current_file_dict = file_dict
        self.initialize_saved_config_file_selection_and_column_selection(file_name, record_index)
        self.clear_column_config_from_text_area()
        print("leaving: update_column_in_record")

    def remove_current_column_from_all_records_of_config_file(self):
        print("inside: remove_current_column_from_all_records_of_config_file")
        file_name = self.configFileNamesCmbo.get()
        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
        total_records = int(self.get_number_of_total_records_in_file(file_name))
        columns_per_record = int(self.get_total_columns_per_record(file_name))
        column_number = int(self.currentColumnNumberEntry.get())
        if (total_records - columns_per_record) == 0:
            # delete file
            self.w.delete_unwanted_file(file_name, 'user-config-file')
        else:
            column_index = (column_number - 1)
            file_dict = self.d.delete_all_column_elements_matching_given_column_index_from_dictionary(file_dict, column_index)
            file_list = self.l.create_a_list_from_dictionary(file_dict)
            self.w.write_list_to_file("user-config-path", file_name, file_list)
            self.current_file_dict = file_dict
            self.initialize_saved_config_file_selection_and_column_selection(file_name, column_index)
            self.clear_column_config_from_text_area()
        print("leaving: remove_current_column_from_all_records_of_config_file")

    def delete_user_configuration_file(self):
        print("inside: delete_user_configuration_file")
        file_name = str(self.configFileNamesCmbo.get())
        print(file_name)
        result = self.w.delete_unwanted_file(file_name, "user-config-path")
        if result:
            self.refresh_combobox_configuration_file_list("Create New Configuration File")
        else:
            print("Log: Could Not Delete: "+str(file_name))
        print("leaving: delete_user_configuration_file")
    
    def update_statistic_in_user_config_file_file(self, element_index, element_key, new_value):
        print("inside: update_statistic_in_user_config_file_file")
        file_name = self.configFileNamesCmbo.get()
        file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
        old_value = self.d.retrieve_a_file_statistic_in_dictionary(file_dict, 1, "file_format")
        if element_key == "file_format" and new_value != "sql" and old_value == "sql":
            file_dict = self.d.update_all_sql_table_action_and_anchor_in_dictionary_to_default(file_dict)
        file_dict = self.d.update_a_file_statistic_in_dictionary(file_dict, element_index, element_key, new_value)
        self.w.delete_unwanted_file(file_name, 'user-config-path')
        file_list = self.l.create_a_list_from_dictionary(file_dict)
        self.w.write_list_to_file("user-config-path", file_name, file_list)
        self.current_file_dict = file_dict
        print("leaving: update_statistic_in_user_config_file_file")

    def update_sql_table_action_and_anchor(self):
        print("inside: update_sql_table_action_and_anchor")
        file_dict = {}
        file_name = self.configFileNamesCmbo.get()
        if file_name != "Create New Configuration File":
            current_record = int(self.currentRecNumberEntry.get())
            record_index = (current_record - 1)
            table_name = self.recordTableNameEntry.get()
            action_name = self.recordSqlActionCmbo.get()
            anchor_name = self.recordSqlAnchorCmbo.get()
            file_dict = self.r.retrieve_dictionary_from_json_file(file_name)
            file_dict = self.d.update_sql_table_in_dictionary(file_dict, record_index, table_name)
            file_dict = self.d.update_sql_action_in_dictionary(file_dict, record_index, action_name)
            file_dict = self.d.update_sql_anchor_in_dictionary(file_dict, record_index, anchor_name)
            self.w.delete_unwanted_file(file_name, 'user-config-path')
            file_list = self.l.create_a_list_from_dictionary(file_dict)
            for line in file_list:
                print(line)
            self.w.write_list_to_file("user-config-path", file_name, file_list)
            self.current_file_dict = file_dict
        print("leaving: update_sql_table_action_and_anchor")

    def update_file_name_in_file(self, new_file_name):
        print("inside: update_file_name_in_file")
        file_dict = self.r.retrieve_dictionary_from_json_file(new_file_name)
        file_dict = self.d.update_a_file_statistic_in_dictionary(file_dict, 2, "file_name", new_file_name)
        file_list = self.l.create_a_list_from_dictionary(file_dict)
        self.w.write_list_to_file("user-config-path", new_file_name, file_list)
        self.current_file_dict = file_dict
        print("leaving: update_file_name_in_file")

    # Adding button_clicked function to handle buttons.
    def button_clicked(self, name):
        match name:
            case "updateRecordsNeededBtn":
                print("button clicked was: "+name)
                required_number = str(self.numOfRecordsNeededCmbo.get())
                element_index = 0
                element_key = "records_needed"
                self.update_statistic_in_user_config_file_file(element_index, element_key, required_number)
            case "updateFormatChoiceBtn":
                print("button clicked was: "+name)
                format_number = self.format_var.get()
                file_format = self.get_file_file_format_by_number(format_number)
                element_index = 1
                element_key = "file_format"
                self.update_statistic_in_user_config_file_file(element_index, element_key, file_format)
            case "createConfigFileBtn":
                print("button clicked was: "+name)
                self.create_new_config_file()
            case "initializeDataBtn":
                print("button clicked was: "+name)
                file_name = self.configFileNamesCmbo.get()
                if file_name != "Create New Configuration File":
                    self.initialize_config_file_selection_and_column_selection(file_name, 0, False)
                    self.set_records_to_affect_and_column_data_in_record(0, 0)         
            case "cloneConfigFileBtn":
                print("button clicked was: "+name)
                old_file_name = self.configFileNamesCmbo.get()
                if old_file_name != "Create New Configuration File":
                    new_file_name = self.create_cloned_file(old_file_name)
                    self.update_file_name_in_file(new_file_name)
            case "deleteConfigFileBtn":
                print("button clicked was: "+name)
                self.delete_user_configuration_file()
            case "createAndDeployAWSS3DataFileBtn":
                print("button clicked was: "+name)
            case "addNewDeploymentLocationBtn":
                print("button clicked was: "+name)
            case "helpBtn":
                print("button clicked was: "+name)
                self.s.open_html_file_in_chrome()
            case "additionalFormatBtn":
                print("button clicked was: "+name)
                self.add_additional_format_to_column()
            case "prevColumnBtn":
                print("button clicked was: "+name)
                self.go_to_column_by_direction("previous")
            case "nextColumnBtn":
                print("button clicked was: "+name)
                self.go_to_column_by_direction("next")
            case "goToColumnBtn":
                print("button clicked was: "+name)
                self.go_straight_to_column_of_record()
            case "prevRecBtn":
                print("button clicked was: "+name)
                self.go_to_record_by_direction("previous")
            case "nextRecBtn":
                print("button clicked was: "+name)
                self.go_to_record_by_direction("next")
            case "goToRecBtn":
                print("button clicked was: "+name)
                self.go_straight_to_record()
            case "recordsToAffectBtn":
                print("button clicked was: "+name)
                record_number = self.currentRecNumberEntry.get()
                record_index = (int(record_number) - 1)
                records_to_affect = self.recordsToAffectNumberEntry.get()
                self.update_records_to_affect_amount(int(records_to_affect), record_index)
            case "updateSQLitemsBtn":
                self.update_sql_table_action_and_anchor()
            case "previewColumnForRecordBtn":
                print("button clicked was: "+name)
                self.display_column_data_in_textarea()
            case "editColumnInRecordBtn":
                print("button clicked was: "+name)
                self.update_column_in_record()
            case "addColumnToRecordBtn":
                print("button clicked was: "+name)
                new_column_list = self.get_scrolltext_from_text_area()
                self.add_new_column_to_all_records(new_column_list)
                self.clear_column_config_from_text_area()
            case "deleteColumnFromRecordBtn":
                print("button clicked was: "+name)
                self.remove_current_column_from_all_records_of_config_file()
            case "addRecordToFileBtn":
                file_name = self.configFileNamesCmbo.get()
                file_size = self.r.get_size_of_file(file_name)
                if int(file_size) > 0:
                    print("file size is greater than zero.")
                    self.add_text_area_contents_to_add_additional_record_to_file()
                else:
                    self.add_contents_of_text_area_to_create_a_new_record(1)
                self.clear_column_config_from_text_area()
                #self.increment_total_record_count()
                print("button clicked was: "+name)
            case "deleteRecordFromFileBtn":
                print("button clicked was: "+name)
                #self.decrement_total_record_count()
            case "createDataOutputFileBtn":
                print("button clicked was: "+name)


class AppUI(tk.Tk):

    def __init__(self):
        super().__init__()

        # setting title of frame.
        self.title('Mock Data Creator - making life a little easier, by Joe McTigue')
        # setting width and height of frame.
        width = 1360
        height = 720
        # adjusting placement on computer screen to be centered.
        c_screen_width = self.winfo_screenwidth()
        c_screen_height = self.winfo_screenheight()
        x = (c_screen_width/2) - (width/2)
        y = (c_screen_height/2) - (height/2)
        self.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.resizable(False, False)
        # define background image location.
        self.bg_image = tk.PhotoImage(file = ".\\images\\background-data-image.png")
        # creating an image label and binding it to frame (self).
        self.limg = tk.Label(self, i=self.bg_image)
        # attaching frame to window.
        self.limg.pack(fill = None, expand = False)

# starting up the application code.
if __name__ == "__main__":
    app = AppUI()
    DisplayFrame(app)
    app.mainloop()
                
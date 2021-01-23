import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def search(item, columnNo):
    '''
    returns all the records received from database on searching the given string in the given column 
    \nitem - The string to be searched for
    \ncolumnNo - The column of database in which value has to be searched
        \n\t2 - first name
        \n\t3 - description
        \n\t4 - contact number
        \n\t5 - email id
    '''

    item = item.upper()

    conn = sqlite3.connect('AllContacts.db')
    cur = conn.cursor()

    if columnNo == 2:
        cur.execute(
            'SELECT * FROM Contact WHERE UPPER(first_name) = ?', (item,))
    elif columnNo == 3:
        cur.execute('SELECT * FROM Contact WHERE UPPER(company) = ?', (item,))
    elif columnNo == 4:
        cur.execute('SELECT * FROM Contact WHERE contact_number = ?', (item,))
    elif columnNo == 5:
        cur.execute('SELECT * FROM Contact WHERE UPPER(email) = ?', (item,))

    result = cur.fetchall()

    conn.commit()
    conn.close()

    if not(result):
        return('No record found')
    else:
        return(result)

def nothing(id):
    print ('Doing nothing')

def deleteContactGUI(id):
    toDelete = tk.messagebox.askyesno (message='Are you sure you want to delete?', title='Delete', icon='warning')
    print (toDelete)

    if toDelete:
        conn = sqlite3.connect('AllContacts.db')
        cur = conn.cursor()

        cur.execute('DELETE FROM Contact WHERE id = ?', (id,))
        result = cur.fetchone()
        print (result)

        conn.commit()
        conn.close()

        print('Record has been deleted')

def buildGUI():

    root = tk.Tk()

    def editContactScreen (id):
        print ('Editing a single record')
        print ('id: ', id)
        i=0

        editScreen = tk.Toplevel (root)
        frame = ttk.Frame (editScreen)

        infoLabel = ttk.Label (frame, text = 'Edit the contact in the text boxes given below')
        nameLabel = ttk.Label(frame, text='Name: ')
        nameBox = ttk.Entry(frame, width=15)
        descLabel = ttk.Label(frame, text='Description: ')
        descBox = ttk.Entry(frame, width=15)
        phoneLabel = ttk.Label(frame, text='Phone Number: ')
        phoneBox = ttk.Entry(frame, width=15)
        emailLabel = ttk.Label(frame, text='E-Mail: ')
        emailBox = ttk.Entry(frame, width=15)
        submit = ttk.Button(frame, text='Submit', command=lambda: submitCallback())
        close = ttk.Button(frame, text='Close', command=lambda: closeCallback())

        frame.grid (row=0, column=0, sticky='news')

        infoLabel.grid (row=0, column=0, columnspan=2)
        nameLabel.grid (row=1, column=0)
        nameBox.grid (row=1, column=1)
        descLabel.grid (row=2, column=0)
        descBox.grid (row=2, column=1)
        phoneLabel.grid (row=3, column=0)
        phoneBox.grid (row=3, column=1)
        emailLabel.grid (row=4, column=0)
        emailBox.grid (row=4, column=1)
        submit.grid (row=5, column=0)
        close.grid (row=5, column=1)

        editScreen.rowconfigure (0, weight=1, minsize=800)
        editScreen.columnconfigure (0, weight=1, minsize=1200)

        for i in range(0, 2):
            frame.columnconfigure (i, weight=1)
        for i in range (0, 6):
            frame.rowconfigure (i, weight=1)

        conn = sqlite3.connect('AllContacts.db')
        cur = conn.cursor()

        cur.execute('SELECT * FROM Contact WHERE id = ?', (id,))
        result = cur.fetchall()

        conn.commit()
        conn.close()

        nameBox.insert (0, result[0][1])
        descBox.insert (0, result[0][2])
        phoneBox.insert (0, result[0][3])
        emailBox.insert (0, result[0][4])

        def submitCallback ():
            conn = sqlite3.connect('AllContacts.db')
            cur = conn.cursor()

            name = nameBox.get()
            description = descBox.get()
            phoneNo = phoneBox.get()
            email = emailBox.get()

            if (not name) or (not description) or (not phoneNo) or (not email):
                print("\nData not saved to Database")
                print("One or more fields was empty")
            else:
                print ('Data saved to database')
                cur.execute('UPDATE Contact SET first_name = ? WHERE id = ?', (name, id))
                cur.execute('UPDATE Contact SET company = ? WHERE id = ?', (description, id))
                cur.execute('UPDATE Contact SET contact_number = ? WHERE id = ?', (phoneNo, id))
                cur.execute('UPDATE Contact SET email = ? WHERE id = ?', (email, id))

            conn.commit()
            conn.close()

        def closeCallback():
            editScreen.destroy()

    def searchScreen(labelText, actionText, actionMethod, searchType):

        print("In search screen function")
        newWind = tk.Toplevel(root)

        topFrame = tk.Frame(newWind)

        searchLabel = tk.Label(topFrame, text=labelText)
        searchBox = tk.Entry(topFrame, width=30)
        searchButton = tk.Button(topFrame, text='Search', command=lambda: searchButtonCallback())
        destroy = tk.Button(topFrame, text='Close', command=lambda: newWind.destroy())

        searchLabel.grid (row=0, column=0, columnspan=3)
        searchBox.grid (row=1, column=0)
        searchButton.grid (row=1, column=1)
        destroy.grid (row=1, column=2)
        
        bottomFrame = tk.Frame(newWind, padx=20, pady=20)

        topFrame.grid(row=0, column=0, sticky='ew')
        bottomFrame.grid(row=1, column=0, sticky='ew')

        newWind.rowconfigure (0, weight=1, minsize=300)
        newWind.rowconfigure (1, weight=2, minsize=600)
        newWind.columnconfigure (0, weight=1, minsize=1200)

        topFrame.rowconfigure (0, weight=1, minsize=100)
        topFrame.rowconfigure (1, weight=1, minsize=100)
        topFrame.columnconfigure (0, weight=2)
        topFrame.columnconfigure (1, weight=1)
        topFrame.columnconfigure (2, weight=1)

        def actionCallback(id):
            # newWind.destroy ()
            actionMethod (id)

        def searchButtonCallback():
            searchQuery = searchBox.get()
            result = search(searchQuery, searchType)

            total_rows = len(result)
            total_columns = len(result[0])

            for i in range(total_rows):
                for j in range(total_columns):

                    if (j == 0):
                        id = result [i][j]
                    else:

                        e = tk.Label(bottomFrame, text=result[i][j])
                        e.grid(row=i, column=j-1)

                        if j == total_columns-1:
                            action = tk.Button(bottomFrame, text=actionText, padx=5, command=lambda: actionCallback(id))
                            action.grid(row=i, column=j)

            for i in range (total_rows):
                bottomFrame.rowconfigure (i, weight=1)
            for i in range (total_columns):
                bottomFrame.columnconfigure (i, weight=1)

    def addContactCallback():
        newWind = tk.Toplevel(root, )

        textFrame = tk.LabelFrame(newWind, text='New Contact', padx=10, pady=10)
        textFrame.grid(row=0, column=0, sticky='news')

        nameLabel = tk.Label(textFrame, text='Name: ')
        nameBox = ttk.Entry(textFrame, width=30)
        descLabel = tk.Label(textFrame, text='Description: ')
        descBox = ttk.Entry(textFrame, width=30)
        phoneLabel = tk.Label(textFrame, text='Phone Number: ')
        phoneBox = tk.Entry(textFrame, width=30)
        emailLabel = tk.Label(textFrame, text='E-Mail: ')
        emailBox = ttk.Entry(textFrame, width=30)
        submit = tk.Button(textFrame, text='Submit', command=lambda: submitCallback())

        nameLabel.grid(row=0, column=0)
        nameBox.grid(row=0, column=1)
        descLabel.grid(row=1, column=0)
        descBox.grid(row=1, column=1)
        phoneLabel.grid(row=2, column=0)
        phoneBox.grid(row=2, column=1)
        emailLabel.grid(row=3, column=0)
        emailBox.grid(row=3, column=1)
        submit.grid(row=4, column=0, columnspan=2)

        newWind.rowconfigure (0, weight=1, minsize=800)
        newWind.columnconfigure (0, weight=1, minsize=1200)
        textFrame.rowconfigure (0, weight=1)
        textFrame.rowconfigure (1, weight=1)
        textFrame.rowconfigure (2, weight=1)
        textFrame.rowconfigure (3, weight=1)
        textFrame.rowconfigure (4, weight=2)
        textFrame.columnconfigure (0, weight=1)
        textFrame.columnconfigure (1, weight=1)
        
        print("\nIn Add Contact Callback")

        def submitCallback():
            print("\nIn Submit Callback")
            name = nameBox.get()
            description = descBox.get()
            phoneNo = phoneBox.get()
            email = emailBox.get()
            print(name + " " + description + " " + phoneNo + " " + email)

            conn = sqlite3.connect('AllContacts.db')
            cur = conn.cursor()

            params = (name, description, phoneNo, email)
            if (not name) or (not description) or (not phoneNo) or (not email):
                print("\nData not saved to Database")
                print("One or more fields was empty")
            else:
                cur.execute(
                    'INSERT INTO Contact (id, first_name, company, contact_number, email) VALUES (NULL, ?, ?, ?, ?)', params)
                print("\nData saved to Database")

            conn.commit()
            conn.close()

            newWind.destroy()

    def searchContact1Callback():
        '''
        Make a window 
        - One textbox on top for searching
        - Table below that to show search results
        '''
        print("\nIn Search by Name Callback")

        searchScreen('Enter the name you want to search', 'Found it!', nothing, 2)

    def searchContact2Callback():
        print("\nIn Search by Number Callback")

        searchScreen('Enter the phome number you want to search', 'Found it!', nothing, 4)

    def updateCallback():
        '''
        first call searchScreen function with following parameters
        ('Enter the name of the contact to update', 'Edit', editContactScreen, 2)

        make new function editContactScreen() which does the following:
        - it is the callback for the button in the searchScreen
        - it makes a new window with 4 entries with the current database data inserted into the entrys
        - user edits the entrys and clicks submit
        - then the data from the entrys gets updated to database
        '''

        print("In Update Callback")

        searchScreen ('Enter the name of the contact to update', 'Edit', editContactScreen, 2)

    def viewAllCallback():
        print("View All Contacts Callback")

        newWind = tk.Toplevel(root)
        topFrame = tk.Frame(newWind, padx=20, pady=20)

        conn = sqlite3.connect('AllContacts.db')
        cur = conn.cursor()

        cur.execute('SELECT * FROM Contact')

        result = cur.fetchall()

        conn.commit()
        conn.close()

        total_rows = len(result)
        total_columns = len(result[0])

        for i in range(total_rows):
            for j in range(total_columns):
                if (j == 0):
                    pass
                else:
                    if j == total_columns-1:
                        wid = 30
                    else:
                        wid = 15

                    e = tk.Label(topFrame, text=str(result[i][j]), width=wid)
                    e.grid(row=i, column=j-1)

        destroy = tk.Button(topFrame, text="Close Window", padx=15, command=lambda: newWind.destroy())

        topFrame.grid(row=0, column=0, sticky='news')
        destroy.grid(row=(total_rows), column=0, columnspan=total_columns)

        newWind.rowconfigure (0, weight=1)
        newWind.columnconfigure (0, weight=1)

        for i in range (total_rows):
            topFrame.rowconfigure (i, weight=1)
        
        topFrame.rowconfigure (total_rows, weight=2)
        
        for i in range (total_columns-1):
            topFrame.columnconfigure (i , weight=1)

    def deleteCallback ():
        print ("In delete contact callback")

        searchScreen('Enter the name of contact to delete', 'Delete', deleteContactGUI, 2)

    buttonFrame = tk.LabelFrame(root, padx=20, pady=20) #, height=800, width=600)
    buttonFrame.grid(row=0, column=0, sticky='news')

    addContact = ttk.Button(buttonFrame, text="Add New Contact", command=addContactCallback, width=30)
    searchContact1 = ttk.Button(buttonFrame, text="Search by Name", command=searchContact1Callback, width=30)
    searchContact2 = ttk.Button(buttonFrame, text="Search by Contact Number", command=searchContact2Callback, width=30)
    updateContact = ttk.Button(buttonFrame, text="Update Contact", command=updateCallback, width=30)
    viewAll = ttk.Button(buttonFrame, text="View All Contacts", command=viewAllCallback, width=30)
    deleteContact = ttk.Button(buttonFrame, text="Delete a Contact", command=deleteCallback, width=30)
    
    addContact.grid(row=0, column=0)
    searchContact1.grid(row=1, column=0)
    searchContact2.grid(row=2, column=0)
    updateContact.grid(row=3, column=0)
    viewAll.grid(row=4, column=0)
    deleteContact.grid(row=5, column=0)

    root.columnconfigure (0, weight=1, minsize=600)
    root.rowconfigure (0, weight=1, minsize=800)

    buttonFrame.columnconfigure (0, weight=1)
    buttonFrame.rowconfigure (0, weight=1)
    buttonFrame.rowconfigure (1, weight=1)
    buttonFrame.rowconfigure (2, weight=1)
    buttonFrame.rowconfigure (3, weight=1)
    buttonFrame.rowconfigure (4, weight=1)
    buttonFrame.rowconfigure (5, weight=1)

    root.mainloop()


if __name__ == '__main__':
    buildGUI()

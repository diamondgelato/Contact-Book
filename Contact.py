import sqlite3
import tkinter as tk
from tkinter import ttk


def search(item, columnNo):  # returns all the item received from database search (exactly what I wanted)
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


class Contact:

    # Member functions
    def __init__(self):
        self.firstName = input('\n\nEnter name of contact: ')
        self.company = input('Enter company for contact: ')
        self.contactNumber = input('Enter contact number for contact: ')
        self.emailID = input('Enter email for contact: ')

    # def addContact(self):
    #     conn = sqlite3.connect('AllContacts.db')
    #     cur = conn.cursor()

    #     params = (self.firstName, self.company,
    #               self.contactNumber, self.emailID)
    #     cur.execute(
    #         'INSERT INTO Contact (id, first_name, company, contact_number, email) VALUES (NULL, ?, ?, ?, ?)', params)

    #     conn.commit()
    #     conn.close()

    #     print("\nData saved to Database")

    def display(self):
        print("""
        First Name: {0}
        Company: {1}
        Contact Number: {2}
        E-mail ID: {3}""" .format(self.firstName, self.company, self.contactNumber, self.emailID))


def searchByContactNumber():  # sorted
    contactno = input(
        '\nInput contact no. of the contact you want to search: ')

    if not(contactno.isnumeric()):
        print('Invalid contact no.')
    else:
        # printRecords(search(contactno,4))
        pass


def searchByFirstName():  # sorted
    fname = input('\nInput the name of the contact you want to search: ')
    # printRecords(search(fname,2))


def deleteContact():
    # dependent on search() [sorted], also deletes without confirming which contact to delete [sorted]
    # Search the thing you want, extract id then delete record

    print('To delete the record you must first search it and then confirm if you really want to delete it')
    print('Enter the code for which category you want to search\n')
    # choice = printingForSearch()

    item = input('Enter what you want you search: ')

    # printRecords(search(item, (choice+1)))

    id = input('Enter the ID for the contact you want to delete: ')

    conn = sqlite3.connect('AllContacts.db')
    cur = conn.cursor()

    cur.execute('DELETE FROM Contact WHERE id = ?', (id,))
    result = cur.fetchone()

    conn.commit()
    conn.close()

    print('Record has been deleted')


def updateContact(choice2):
    # dependent on search() [sorted], also updates without confirming which contact to update [sorted] and doesnt print the changed value [also sorted]
    # First search, then ask what to change and then change that

    print('To edit the record, you must first search it, select what you want to edit and then confirm if you really want to edit it')
    print('Enter the code for which category you want to search\n')
    # choice1 = printingForSearch()

    searchStr = input('\nEnter what has to be searched: ')

    # printRecords(search(searchStr, (choice1+1)))

    id = input('\nEnter the ID for the contact to be edited: ')

    print('\nEnter the code for what field you want to edit')
    # choice2 = printingForSearch()

    newStr = input('\nEnter new value for that field: ')

    conn = sqlite3.connect('AllContacts.db')
    cur = conn.cursor()

    if choice2 == 1:
        cur.execute(
            'UPDATE Contact SET first_name = ? WHERE id = ?', (newStr, id))
    if choice2 == 2:
        cur.execute('UPDATE Contact SET company = ? WHERE id = ?', (newStr, id))
    if choice2 == 3:
        cur.execute(
            'UPDATE Contact SET contact_number = ? WHERE id = ?', (newStr, id))
    if choice2 == 4:
        cur.execute('UPDATE Contact SET email = ? WHERE id = ?', (newStr, id))

    conn.commit()

    cur.execute('SELECT * FROM Contact WHERE id = ?', (id,))
    result = cur.fetchone()

    print('\nThis is the updated contact:')
    print(result)

    conn.close()


def main():

    isRunning = True

    while (isRunning):
        print('\n\nWelcome to your Contact Book\n')
        print('Enter the number before the function you want to perform\n')
        print('1: Add Contact')
        print('2: View all Contacts')
        print('3: Search Contact by Name')
        print('4: Search Contact by Contact Number')
        print('5: Delete Contact')
        print('6: Update Contact')
        print('10: Exit')
        choice = int(input('\nEnter your choice: '))

        if choice == 1:
            contact = Contact()
            contact.addContact()
        elif choice == 2:
            # printAll()
            pass
        elif choice == 3:
            searchByFirstName()
        elif choice == 4:
            searchByContactNumber()
        elif choice == 5:
            deleteContact()
        elif choice == 6:
            pass
            # updateContact()
        elif choice == 10:
            isRunning = False
        else:
            print('\nInvalid Input')


def buildGUI():

    global lastButtonPress
    root = tk.Tk()
    lastButtonPress = 0

    def searchScreen(labelText, actionText):
        print ("In search screen function")
        newWind = tk.Toplevel(root)

        topFrame = tk.Frame(newWind, height=200, width=500)

        searchLabel = tk.Label(
            topFrame, text=labelText)
        searchLabel.place(relx=0.5, rely=0.25, anchor='n')

        searchBox = tk.Entry(topFrame, width=30)
        searchBox.place(relx=0.4, rely=0.6, anchor='center')

        searchButton = tk.Button(
            topFrame, text='Search', command=lambda: print(searchBox.get()))
        searchButton.place(relx=0.7, rely=0.6, anchor='center')

        topFrame.grid(row=0, column=0)

        bottomFrame = tk.Frame (newWind, padx = 20, pady = 20)

        '''
        Code for 'SELECT * FROM Contact' query to database here
        '''

        testdata = [('Mugdha', 'Me', '8237193773', 'mugdha@topmail.com'),
                    ('Ashu', 'Mom', '7233944717', 'ashu1@topmail.com'),
                    ('Makarand', 'Dad', '2138471233', 'mak@topmail.com'),
                    ('Lalita', 'Grandma', '0921364643', '-')]

        total_rows = len(testdata)
        total_columns = len(testdata[0])

        for i in range(total_rows): 
            for j in range(total_columns): 
                  
                if j == total_columns-1:
                    wid = 30
                else:
                    wid = 15
                
                e = tk.Label(bottomFrame, text=testdata[i][j] , width=wid)
                e.grid(row=i, column=j) 
                # e.insert(tk.END, testdata[i][j]) 

                if j == total_columns-1:
                    action = tk.Button (bottomFrame, text=actionText, padx = 5)
                    action.grid (row=i, column=(j+1))

        bottomFrame.grid (row=1, column=0)

    def addContactCallback():
        newWind = tk.Toplevel(root)

        textFrame = tk.LabelFrame(newWind, padx=10, pady=10,
                                  bd=2, height=400, width=500)
        textFrame.grid(row=0, column=1)

        nameLabel = tk.Label(textFrame, text='Name: ')
        nameLabel.place(relx=0.1, rely=0.1, anchor='w')

        # name = tk.StringVar()
        nameBox = ttk.Entry(textFrame, width=30, state='disabled')
        nameBox.place(relx=0.5, rely=0.1, anchor='w')

        descLabel = tk.Label(textFrame, text='Description: ')
        descLabel.place(relx=0.1, rely=0.3, anchor='w')

        # description = tk.StringVar()
        descBox = ttk.Entry(textFrame, width=30, state='disabled')
        descBox.place(relx=0.5, rely=0.3, anchor='w')

        phoneLabel = tk.Label(textFrame, text='Phone Number: ')
        phoneLabel.place(relx=0.1, rely=0.5, anchor='w')

        # phoneNo = tk.StringVar()
        phoneBox = tk.Entry(textFrame, width=30, state='disabled')
        phoneBox.place(relx=0.5, rely=0.5, anchor='w')

        emailLabel = tk.Label(textFrame, text='E-Mail: ')
        emailLabel.place(relx=0.1, rely=0.7, anchor='w')

        # email = tk.StringVar()
        emailBox = ttk.Entry(textFrame, width=30, state='disabled')
        emailBox.place(relx=0.5, rely=0.7, anchor='w')

        submit = tk.Button(textFrame, text='Submit',
                           command=lambda: submitCallback(lastButtonPress))
        submit.place(relx=0.4, rely=0.85)

        print("\nIn Add Contact Callback")
        nameBox.config(state=tk.NORMAL)
        descBox.config(state=tk.NORMAL)
        phoneBox.config(state=tk.NORMAL)
        emailBox.config(state=tk.NORMAL)
        # global lastButtonPress
        # lastButtonPress = 1   # for add contact button

        def submitCallback(lastButtonPress):
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

            newWind.destroy ()

    '''
    Make a window 
    - One textbox on top for searching
    - Table below that to show search results
    '''
    def searchContact1Callback():
        print("\nIn Search by Name Callback")

        searchScreen('Enter the name you want to search', 'Search')
        
    def searchContact2Callback():
        print("\nIn Search by Number Callback")

    def updateCallback():

        def updateNameCallback():
            print("In Update Name Callback")

        def updateDescCallback():
            print("In Update Description Callback")

        def updatePhoneCallback():
            print("In Update Phone Number Callback")

        def updateEmailCallback():
            print("In Update Email Callback")

        print("In Update Callback")

        newWind = tk.Toplevel(root, height=400, width=300)

        choiceLabel = tk.Label(
            newWind, text="Click the button for the option to be updated:")
        choiceLabel.place(relx=0.5, rely=0.25, anchor='n')

        nameChoice = tk.Button(newWind, text="Name",
                               padx=15, command=updateNameCallback)
        nameChoice.place(relx=0.5, rely=0.35, anchor='n')

        descChoice = tk.Button(newWind, text="Description",
                               padx=15, command=updateDescCallback)
        descChoice.place(relx=0.5, rely=0.45, anchor='n')

        phoneChoice = tk.Button(
            newWind, text="Phone Number", padx=15, command=updatePhoneCallback)
        phoneChoice.place(relx=0.5, rely=0.55, anchor='n')

        emailChoice = tk.Button(newWind, text="Email",
                                padx=15, command=updateEmailCallback)
        emailChoice.place(relx=0.5, rely=0.65, anchor='n')

        destroy = tk.Button(newWind, text="Destroy Window",
                            padx=15, command=lambda: newWind.destroy())
        destroy.place(relx=0.5, rely=0.8, anchor='n')

    def viewAllCallback():
        print("View All Contacts Callback")

        newWind = tk.Toplevel(root)
        topFrame = tk.Frame (newWind, padx = 20, pady = 20)

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
                  
                if j == total_columns-1:
                    wid = 30
                else:
                    wid = 15
                
                e = tk.Label(topFrame, text=str(result[i][j]) , width=wid)
                print (result[i][j])
                e.grid(row=i, column=j) 

        topFrame.grid (row=0, column=0)

        bottomFrame = tk.Frame (newWind, height=100, width=600, padx=20, pady=20)

        destroy = tk.Button(bottomFrame, text="Close Window",
                            padx=15, command=lambda: newWind.destroy())
        destroy.place(relx=0.5, rely=0.5, anchor='center')

        bottomFrame.grid (row=1, column=0)

    buttonFrame = tk.LabelFrame(root, padx=10, pady=10, height=400, width=300)
    buttonFrame.grid(row=0, column=0)

    addContact = tk.Button(
        buttonFrame, text="Add New Contact", command=addContactCallback)
    addContact.place(relx=0.5, rely=0.1, anchor='n')

    searchContact1 = tk.Button(
        buttonFrame, text="Search by Name", command=searchContact1Callback)
    searchContact1.place(relx=0.5, rely=0.3, anchor='n')

    searchContact2 = tk.Button(
        buttonFrame, text="Search by Contact Number", command=searchContact2Callback)
    searchContact2.place(relx=0.5, rely=0.5, anchor='n')

    updateContact = tk.Button(
        buttonFrame, text="Update Contact", command=updateCallback)
    updateContact.place(relx=0.5, rely=0.7, anchor='n')

    viewAll = tk.Button(
        buttonFrame, text="View All Contacts", command=viewAllCallback)
    viewAll.place(relx=0.5, rely=0.9, anchor='n')

    root.mainloop()


if __name__ == '__main__':
    buildGUI()

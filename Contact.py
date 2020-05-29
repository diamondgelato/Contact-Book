import sqlite3

def search(item, columnNo):   #returns all the item received from database search (exactly what I wanted)
    item = item.upper()

    conn = sqlite3.connect('AllContacts.db')
    cur = conn.cursor()

    if columnNo == 2:
        cur.execute('SELECT * FROM Contact WHERE UPPER(first_name) = ?', (item,))
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

def printRecords(records):
    i = 0

    while True:
        try:
            print(records[i])
            i+=1
        except IndexError:
            break


class Contact:

    #Member functions
    def __init__(self):
        self.firstName = input('\n\nEnter name of contact: ')
        self.company = input('Enter company for contact: ')
        self.contactNumber = input('Enter contact number for contact: ')
        self.emailID = input('Enter email for contact: ')

    def addContact(self):
        conn = sqlite3.connect('AllContacts.db')
        cur = conn.cursor()

        params = (self.firstName, self.company, self.contactNumber, self.emailID)
        cur.execute('INSERT INTO Contact (id, first_name, company, contact_number, email) VALUES (NULL, ?, ?, ?, ?)' , params)

        conn.commit()
        conn.close()

        print("\nData saved to Database")

    def display(self):
        print("""
        First Name: {0}
        Company: {1}
        Contact Number: {2}
        E-mail ID: {3}""" .format(self.firstName, self.company, self.contactNumber, self.emailID))


def searchByContactNumber():    #sorted
    contactno = input('\nInput contact no. of the contact you want to search: ')

    if not(contactno.isnumeric()):
        print('Invalid contact no.')
    else:
        printRecords(search(contactno,4))


def searchByFirstName():    #sorted
    fname = input('\nInput the name of the contact you want to search: ')
    printRecords(search(fname,2))


def deleteContact():
    #dependent on search() [sorted], also deletes without confirming which contact to delete [sorted]
    #Search the thing you want, extract id then delete record

    print('To delete the record you must first search it and then confirm if you really want to delete it')
    print('Enter the code for which category you want to search\n')
    choice = printingForSearch()

    item = input('Enter what you want you search: ')

    printRecords(search(item, (choice+1)))

    id = input ('Enter the ID for the contact you want to delete: ')

    conn = sqlite3.connect('AllContacts.db')
    cur = conn.cursor()

    cur.execute('DELETE FROM Contact WHERE id = ?', (id,))
    result = cur.fetchone()

    conn.commit()
    conn.close()

    print('Record has been deleted')


def updateContact():
    #dependent on search() [sorted], also updates without confirming which contact to update [sorted] and doesnt print the changed value [also sorted]
    #First search, then ask what to change and then change that

    print('To edit the record, you must first search it, select what you want to edit and then confirm if you really want to edit it')
    print('Enter the code for which category you want to search\n')
    choice1 = printingForSearch()

    searchStr = input('\nEnter what has to be searched: ')

    printRecords(search(searchStr, (choice1+1)))

    id = input('\nEnter the ID for the contact to be edited: ');

    print('\nEnter the code for what field you want to edit')
    choice2 = printingForSearch()

    newStr = input('\nEnter new value for that field: ')

    conn = sqlite3.connect('AllContacts.db')
    cur = conn.cursor()

    if choice2 == 1:
    	cur.execute('UPDATE Contact SET first_name = ? WHERE id = ?', (newStr,id))
    if choice2 == 2:
    	cur.execute('UPDATE Contact SET company = ? WHERE id = ?', (newStr,id))
    if choice2 == 3:
    	cur.execute('UPDATE Contact SET contact_number = ? WHERE id = ?', (newStr,id))
    if choice2 == 4:
    	cur.execute('UPDATE Contact SET email = ? WHERE id = ?', (newStr,id))

    conn.commit()

    cur.execute('SELECT * FROM Contact WHERE id = ?', (id,))
    result = cur.fetchone()

    print('\nThis is the updated contact:')
    print(result)

    conn.close()


def printingForSearch():
    while True:
        print('1: First name')
        print('2: Company')
        print('3: Contact Number')
        print('4: Email ID')

        try:
            choice = int(input('\n> '))
            break
        except ValueError:
            print('Invalid Input')
            continue

    return choice


def printAll():    #same here
    conn = sqlite3.connect('AllContacts.db')
    cur = conn.cursor()

    cur.execute('SELECT * FROM Contact');
    printRecords(cur.fetchall())

    conn.commit()
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
            printAll()
        elif choice == 3:
            searchByFirstName()
        elif choice == 4:
            searchByContactNumber()
        elif choice == 5:
            deleteContact()
        elif choice == 6:
            updateContact()
        elif choice == 10:
            isRunning = False
        else:
            print('\nInvalid Input')


if __name__ == '__main__':
    main()

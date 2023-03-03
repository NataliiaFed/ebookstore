# import SQLite3 and tabule modules
import sqlite3
from tabulate import tabulate

#==========Functions ==============
def print_menu():
    '''Displays the main menu on the console.'''

    output = "MENU:\n"
    output += "1 - View all\n"
    output += "2 - Enter book\n"
    output += "3 - Update book\n"
    output += "4 - Delete book\n"
    output += "5 - Search books\n"
    output += "0 - Exit"
    print(output)


def view_all():
    '''Prints out the book table on the console in a user-friendly format'''

    # create a list to store an output  table with a heading
    table = [['ID', 'Title', 'Author', 'Qty']]

    # get a cursor object, execute a SELECT SQL statement against the cursor object to retrieve all the data from the table
    # then iterate through cursor object and store the data into the output table by rows
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books")
    for row in cursor:
        row = [row[0], row[1], row[2], row[3]]
        table.append(row)

    # print out the table
    print(tabulate(table, headers="firstrow", tablefmt="fancy_outline"))


def enter_book():
    '''Adds a book to the book table'''

    # request title, author from a user
    title = input("Enter title: ")
    author = input("Enter author: ")

    # check if the user entered both title and author of a book
    # do not use a while-loop so that intentional empty input could be used to exit the function
    if title == '' or author == '':
        print("Book can't be added without a title and/or an author.")
    else:
        # if title and author is entered correctly, request quantity and ensure it's a digit
        while True:
            try:
                quantity = int(input("Enter quantity: "))
                break
            except ValueError:
                print("Invalid option. Please, enter a number.")

        # get a cursor object, add the data to the table and save the changes
        cursor = db.cursor()
        cursor.execute('INSERT INTO books(title, author, qty) VALUES(?,?,?)', (title, author, quantity))
        db.commit()

        print("Book has been added.")


def update_book():
    '''Updates quantity of a book'''

    # request id of a book from a user
    update_id = input("Enter id: ")

    # get a cursor object, retrieve the book data from the table and store it into a variable
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (update_id,))
    result = cursor.fetchone()

    # verify the result
    if result == None:
        print(f"No book found with id {update_id}.")
    else:
        # if the book is found, request new quantity from a user and ensure it's a digit
        while True:
            try:
                new_quantity = int(input("Enter new quantity: "))
                break
            except ValueError:
                print("Invalid option. Please, enter a number.")

        # get a cursor object, UPDATE the data in the table and save the changes
        cursor = db.cursor()
        cursor.execute('UPDATE books SET qty = ? WHERE id = ?', (new_quantity, update_id))
        db.commit()

        print("Book has been updated.")


def delete_book():
    '''Deletes a book from the table'''

    # request id of a book from a user
    delete_id = input("Enter book id: ")

    # get a cursor object, retrieve the book data from the table and store it into a variable
    cursor = db.cursor()
    cursor.execute('SELECT title, author FROM books WHERE id = ?', (delete_id,))
    result = cursor.fetchone()

    # request the confirmation of book removal from a user
    # ensure the book the user wants to delete exists
    while True:
        try:
            confirmation = input(f'Are you sure you want to delete book №{delete_id} "{result[0]}" by {result[1]}? Y/N: ').lower()
        except TypeError:
            print(f"No book found with id {delete_id}.")
            break
        else:
            # if removal confirmed, get a cursor object, delete the book from the table and save the changes
            if confirmation == 'y':
                cursor = db.cursor()
                cursor.execute('DELETE FROM books WHERE id = ?', (delete_id,))
                db.commit()
                print("Book has been deleted.")
                break
            elif confirmation == 'n':
                break
            else:
                print("You have made a wrong choice, Please Try again")


def search_by_id():
    '''Searches a book in the table by its ID'''

    # request id of a book from a user
    search_id = input("Enter id: ")

    # get a cursor object, retrieve the book data from the table and store it into a variable
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (search_id,))
    result = cursor.fetchone()

    # print out the result
    if result == None:
        print("No book found.")
    else:
        table = [['ID', 'Title', 'Author', 'Qty'], [result[0], result[1], result[2], result[3]]]
        print(tabulate(table, headers="firstrow", tablefmt="fancy_outline"))


def search_by_title():
    '''Searches a book in the table by its title'''

    # request a title from a user, eliminate the letter case
    search_title = input("Enter a title / part of a title: ").lower()

    # declare a boolean variable to state if the book has been found
    book_found = False

    # create a list to store an output  table with a heading
    table = [['ID', 'Title', 'Author', 'Qty']]

    # get a cursor object, execute a SELECT SQL statement to retrieve all title from the table
    # then iterate through cursor object and check if each title contains a search string (eliminate the letter case)
    cursor = db.cursor()
    cursor.execute('SELECT title FROM books')
    for row in cursor:

        # if title contains a search string, store into a variable
        # get a cursor object, retrieve the book data with this title from the table
        # and store it into the output table
        if search_title in row[0].lower():
            book_title = row[0]

            cursor = db.cursor()
            cursor.execute("SELECT * FROM books WHERE title = ?", (book_title,))
            result = cursor.fetchone()
            row = [result[0], result[1], result[2], result[3]]
            table.append(row)

            book_found = True

    # print out the result
    if book_found == True:
        print(tabulate(table, headers="firstrow", tablefmt="fancy_outline"))
    else:
        print("No book found.")


def search_by_author():
    '''Searches a book in the table by its author'''

    # request an author from a user, eliminate the letter case
    search_author = input("Enter an author (full name or its part): ").lower()
    book_found = False

    # create a list to store an output table with a heading
    table = [['ID', 'Title', 'Author', 'Qty']]

    # get a cursor object, execute a SELECT SQL statement to retrieve all authors from the table
    # then iterate through cursor object and check if each author contains a search string (eliminate the letter case)
    cursor = db.cursor()
    cursor.execute('SELECT author FROM books')
    for row in cursor:

        # if author contains a search string, store into a variable
        # get a cursor object, retrieve the book data with this author from the table
        # and store it into the output table
        if search_author in row[0].lower():
            book_author = row[0]

            cursor = db.cursor()
            cursor.execute("SELECT * FROM books WHERE author = ?", (book_author,))
            result = cursor.fetchone()
            row = [result[0], result[1], result[2], result[3]]
            table.append(row)

            book_found = True

    # print out the result
    if book_found == True:
        print(tabulate(table, headers="firstrow", tablefmt="fancy_outline"))
    else:
        print("No book found.")


#==========Initialising of a database=============
# create/open a file with a SQLite3 DB and connect to the database
db = sqlite3.connect('ebookstore')

# get a cursor object to make changes to the database
cursor = db.cursor()

# create a books table with id, name, and grade columns if doesn't exist yet
table_books = '''
    CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    qty INTEGER)'''
cursor.execute(table_books)

# call the commit function to save changes
db.commit()

# store five students' data into a list
books_data = [
    (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
    (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
    (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
    (3004, 'The Lord of the Rings', 'J.R.R Tolkie', 37),
    (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
]

# check whether the books table is empty
cursor.execute('SELECT count(id) FROM books')
result = cursor.fetchall()

# if the table is empty, add the data into the table
if result == [(0,)]:
    cursor.executemany('INSERT INTO books VALUES(?,?,?,?)', books_data)
    db.commit()
    print('Data inserted.')


#==========Main Menu=============
# presenting main menu to a user
print_menu()

while True:
    # request an option to execute from the user
    menu = input("Select an option: ")

    if menu == '1':
        '''View all book'''
        view_all()
        print_menu()

    elif menu == '2':
        '''Enter book'''
        enter_book()
        print_menu()

    elif menu == '3':
        '''Update book'''
        update_book()
        print_menu()

    elif menu == '4':
        '''Delete book'''
        delete_book()
        print_menu()

    elif menu == '5':
        '''Search books'''
        while True:
            # request a search option from the user
            search_option = input("Search by id (1), title (2), by author (3) or go back (0)? ")
            if search_option == '1':
                search_by_id()
                break
            elif search_option == '2':
                search_by_title()
                break
            elif search_option == '3':
                search_by_author()
                break
            elif search_option == '0':
                break
            else:
                print("You have made a wrong choice, Please Try again")
        print_menu()

    elif menu == '0':
        db.close()
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
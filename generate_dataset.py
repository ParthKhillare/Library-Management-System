import csv
import random
from datetime import datetime, timedelta

# Sample book data for library management system
books_data = [
    {
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'isbn': '9780743273565',
        'category': 'Fiction',
        'publication_year': 1925,
        'total_copies': 5,
        'available_copies': 3
    },
    {
        'title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'isbn': '9780061120084',
        'category': 'Fiction',
        'publication_year': 1960,
        'total_copies': 8,
        'available_copies': 6
    },
    {
        'title': '1984',
        'author': 'George Orwell',
        'isbn': '9780451524935',
        'category': 'Dystopian Fiction',
        'publication_year': 1949,
        'total_copies': 10,
        'available_copies': 4
    },
    {
        'title': 'Pride and Prejudice',
        'author': 'Jane Austen',
        'isbn': '9780141439518',
        'category': 'Romance',
        'publication_year': 1813,
        'total_copies': 6,
        'available_copies': 5
    },
    {
        'title': 'The Catcher in the Rye',
        'author': 'J.D. Salinger',
        'isbn': '9780316769488',
        'category': 'Fiction',
        'publication_year': 1951,
        'total_copies': 7,
        'available_copies': 2
    },
    {
        'title': 'Animal Farm',
        'author': 'George Orwell',
        'isbn': '9780451526342',
        'category': 'Political Satire',
        'publication_year': 1945,
        'total_copies': 12,
        'available_copies': 8
    },
    {
        'title': 'Lord of the Flies',
        'author': 'William Golding',
        'isbn': '9780571191475',
        'category': 'Fiction',
        'publication_year': 1954,
        'total_copies': 9,
        'available_copies': 6
    },
    {
        'title': 'Brave New World',
        'author': 'Aldous Huxley',
        'isbn': '9780060850524',
        'category': 'Science Fiction',
        'publication_year': 1932,
        'total_copies': 5,
        'available_copies': 3
    },
    {
        'title': 'The Hobbit',
        'author': 'J.R.R. Tolkien',
        'isbn': '9780618260300',
        'category': 'Fantasy',
        'publication_year': 1937,
        'total_copies': 15,
        'available_copies': 10
    },
    {
        'title': 'Harry Potter and the Sorcerer\'s Stone',
        'author': 'J.K. Rowling',
        'isbn': '9780439708180',
        'category': 'Fantasy',
        'publication_year': 1997,
        'total_copies': 20,
        'available_copies': 5
    },
    {
        'title': 'The Da Vinci Code',
        'author': 'Dan Brown',
        'isbn': '9780307474278',
        'category': 'Mystery',
        'publication_year': 2003,
        'total_copies': 8,
        'available_copies': 4
    },
    {
        'title': 'The Alchemist',
        'author': 'Paulo Coelho',
        'isbn': '9780061122415',
        'category': 'Fiction',
        'publication_year': 1988,
        'total_copies': 11,
        'available_copies': 7
    },
    {
        'title': 'Life of Pi',
        'author': 'Yann Martel',
        'isbn': '9780156027321',
        'category': 'Adventure',
        'publication_year': 2001,
        'total_copies': 6,
        'available_copies': 4
    },
    {
        'title': 'The Kite Runner',
        'author': 'Khaled Hosseini',
        'isbn': '9781594631939',
        'category': 'Fiction',
        'publication_year': 2003,
        'total_copies': 9,
        'available_copies': 5
    },
    {
        'title': 'Gone Girl',
        'author': 'Gillian Flynn',
        'isbn': '9780307588371',
        'category': 'Mystery',
        'publication_year': 2012,
        'total_copies': 7,
        'available_copies': 3
    },
    {
        'title': 'The Girl with the Dragon Tattoo',
        'author': 'Stieg Larsson',
        'isbn': '9780307949486',
        'category': 'Mystery',
        'publication_year': 2005,
        'total_copies': 5,
        'available_copies': 2
    },
    {
        'title': 'The Hunger Games',
        'author': 'Suzanne Collins',
        'isbn': '9780439023528',
        'category': 'Science Fiction',
        'publication_year': 2008,
        'total_copies': 18,
        'available_copies': 8
    },
    {
        'title': 'Divergent',
        'author': 'Veronica Roth',
        'isbn': '9780062024039',
        'category': 'Science Fiction',
        'publication_year': 2011,
        'total_copies': 10,
        'available_copies': 6
    },
    {
        'title': 'The Fault in Our Stars',
        'author': 'John Green',
        'isbn': '9780142424179',
        'category': 'Young Adult',
        'publication_year': 2012,
        'total_copies': 12,
        'available_copies': 4
    },
    {
        'title': 'Wonder',
        'author': 'R.J. Palacio',
        'isbn': '9780375869020',
        'category': 'Young Adult',
        'publication_year': 2012,
        'total_copies': 8,
        'available_copies': 6
    }
]

# Generate more diverse book data
categories = ['Fiction', 'Non-Fiction', 'Science Fiction', 'Fantasy', 'Mystery', 'Romance', 'Biography', 'History', 'Self-Help', 'Technology', 'Business', 'Psychology']

authors = [
    'Stephen King', 'Agatha Christie', 'Isaac Asimov', 'Arthur C. Clarke', 
    'Philip K. Dick', 'Ursula K. Le Guin', 'Ray Bradbury', 'Robert Heinlein',
    'Frank Herbert', 'William Gibson', 'Neil Gaiman', 'Terry Pratchett'
]

# Generate additional books
for i in range(30):
    book = {
        'title': f'Book Title {i+21}',
        'author': random.choice(authors),
        'isbn': f'978{random.randint(1000000000, 9999999999)}',
        'category': random.choice(categories),
        'publication_year': random.randint(1950, 2023),
        'total_copies': random.randint(1, 15),
        'available_copies': random.randint(0, 10)
    }
    books_data.append(book)

# Write to CSV
with open('books_dataset.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'author', 'isbn', 'category', 'publication_year', 'total_copies', 'available_copies']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for book in books_data:
        writer.writerow(book)

print(f"Generated {len(books_data)} books in books_dataset.csv")

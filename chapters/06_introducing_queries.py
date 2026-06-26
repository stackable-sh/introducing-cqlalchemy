import json
from datetime import date, time
from rich import print

import cqlalchemy
from cqlalchemy.connection.functions import row, r
from cqlalchemy.core.builtins import unquote
from cqlalchemy.core.models import Model, UUID, Reference, Pointer
from cqlalchemy.core.commons import String, Email, Reference, Double, Currency
from cqlalchemy.connection.table import Schema


cqlalchemy.configure(keyspace="Chapter06",servers=["localhost",], debug=False)

try:
    Schema.destroy(keyspace="Chapter06")
except Exception as e:
    pass 

print("\n")
print("Chapter 6: Queries I")


class Author(Model):
    """An Author Entity"""
    id = UUID(primary=True)
    name = String(required=True, index=True)
    email = Email(required=True, index=True)
    publisher = String(required=True, index=True)


class Book(Model):
    """A Book Entity"""
    id = UUID(primary=True)
    title = String(required=True, index=True)
    price = Double(required=True, index=True)
    currency = Currency(required=True, index=True)
    author = Reference(Author, required=True, index=True)


person = Author.create(name="Sam Harris", email="reach@samharris.org", publisher="Penguin Random House")
book = Book.create(title="The End of Faith", price=24.99, author=person, currency="USD")


print("[bold blue]1. Let's execute some common query patterns.[/bold blue]\n")

print("1(a) You can count using Author.objects.count().get()") 
author_count = Author.objects.count().get()
book_count = Book.objects.count().get()

print("\n")
print("Book Count: %s" % (book_count))
print("Author Count: %s" % (author_count))
print("\n")


print("1(b) You can find all the Authors by using Author.objects.all() ...\n")
for author in Author.objects.all():
    print("Author ID: %s" % author.id)
    print("Author Name: %s" % author.name)
    print("Author Email: %s" % author.email)
    print("Author Publisher: %s" % author.publisher)
print("\n")

print("1(c) You can find a specific Entity by using Author.objects.where() method\n")
author = (
    Author
        .objects
        .where(
            name="Sam Harris", 
            email="reach@samharris.org"
        )
        .filter()
    .get()
)

print("Author ID: %s" % author.id)
print("Author Name: %s" % author.name)
print("Author Email: %s" % author.email)
print("Author Publisher: %s" % author.publisher)
print("\n")

print("1(d) You can skip the filter() function by using the Author.objects.filter_by() method\n")
author = (
    Author
        .objects
        .filter_by(
            name="Sam Harris", 
            email="reach@samharris.org"
        )
    .get()
)

print("Author ID: %s" % author.id)
print("Author Name: %s" % author.name)
print("Author Email: %s" % author.email)
print("Author Publisher: %s" % author.publisher)
print("\n")


print("1(e) You can also query against references/pointers naturally.\n")
author = (
    Book
        .objects
        .where(author=person)
        .filter()
    .get()
)

print("Book ID: %s" % book.id)
print("Book Title: %s" % book.title)
print("Book Price: %s" % book.price)
print("Book Currency: %s" % book.currency)
print("Book Author: %s" % book.author)
print("\n")


print("2(a) You can use the row() notation to apply specific comparison operators.\n")
book = (
    Book
        .objects
        .filter_by(
            row('price') >= 10.0,
            row('currency') == 'USD'
        )
    .first()
)

print("Book ID: %s" % book.id)
print("Book Title: %s" % book.title)
print("Book Price: %s" % book.price)
print("Book Currency: %s" % book.currency)
print("Book Author: %s" % book.author)
print("\n")


print("2(b) Or use the abbreviated r() notation\n")
book = (
    Book
        .objects
        .filter_by(
            r('price') <= 30.00,
            r('currency') == 'USD'
        )
    .first()
)

print("Book ID: %s" % book.id)
print("Book Title: %s" % book.title)
print("Book Price: %s" % book.price)
print("Book Currency: %s" % book.currency)
print("Book Author: %s" % book.author)
print("\n")



try:
    print("Cleaning up...")
    Schema.destroy(keyspace="Chapter06")
except Exception as e:
    pass 
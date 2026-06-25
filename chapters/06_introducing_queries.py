import json
from datetime import date, time
from rich import print

import cqlalchemy
from cqlalchemy.core.builtins import unquote
from cqlalchemy.core.models import Model, UUID, Reference, Pointer
from cqlalchemy.core.commons import String, Email, Reference, Double, Currency
from cqlalchemy.connection.table import Schema


cqlalchemy.configure(keyspace="Chapter06",servers=["localhost",], debug=False)

try:
    Schema.destroy(keyspace="Chapter06")
except Exception as e:
    pass 

print("Chapter 6: Queries I")
print("\n")


# Define an Author 
class Author(Model):
    """An Author Entity"""
    id = UUID(primary=True)
    name = String(required=True, index=True)
    email = Email(required=True, index=True)
    publisher = String(required=True, index=True)


# Define a Book, and Model a Relationship with the Author Model using Reference 
class Book(Model):
    """A Book Entity"""
    id = UUID(primary=True)
    title = String(required=True, index=True)
    price = Double(required=True, index=True)
    currency = Currency(required=True, index=True)
    author = Reference(Author, required=True)

print("1. Let's create a Book with an Author attached to it.")

person = Author.create(name="Sam Harris", email="reach@samharris.org", publisher="Penguin Random House")
book = Book.create(title="The End of Faith", price=24.99, author=person, currency="USD")


print("2. Let's execute some common queries against our stored data.")
num_of_authors = Author.objects.count()
num_of_books = Book.objects.count()

print("Book Count: %s" % (num_of_books))
print("Author Count: %s" % (num_of_authors))
print("\n")




try:
    print("Cleaning up...")
    Schema.destroy(keyspace="Chapter06")
except Exception as e:
    pass 
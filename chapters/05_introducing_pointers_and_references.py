import json
from datetime import date, time
from rich import print

import cqlalchemy
from cqlalchemy.core.builtins import unquote
from cqlalchemy.core.models import Model, UUID, Reference, Pointer
from cqlalchemy.core.commons import String, Email, Reference, Double, Currency
from cqlalchemy.connection.table import Schema


cqlalchemy.configure(keyspace="Chapter05",servers=["localhost",], debug=False)

try:
    Schema.destroy(keyspace="Chapter05")
except Exception as e:
    pass 

print("Chapter 5: Introducing Pointers and References!")
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
    price = Double(required=True)
    currency = Currency(required=True, index=True)
    author = Reference(Author, required=True)


person = Author.create(name="Sam Harris", email="reach@samharris.org", publisher="Penguin Random House")
assert person.saved()
assert isinstance(person.key, Pointer)

print(f"1. Every Model has a Pointer: {person.key}")
pointer = person.key

print("2. You can read any Model from C* using only its Pointer")
print("\n")

found = Author.read(pointer)
assert found == person
print(f"Found Author: {found}")
print("\n")


"""
You can now store a Pointer (or a Model) directly in another Model.
through the Reference property, which allows you to store and transparently read
Models in a type-safe manner.
"""

print("3. Let's create a Book with an Author attached to it.")

book = Book.create(title="The End of Faith", price=24.99, author=person, currency="USD")
pointer = book.key

print("4. Let's read the Book and retrieve the Author using the Reference property")
instance = Book.read(pointer)
author = instance.author 
assert isinstance(author, Author)
assert person == instance.author
print("\n")


print("5. Book")
print("=======")
print(f"ID:        {instance.id}")
print(f"Title:     {instance.title}")
print(f"Price:     {instance.price}")
print(f"Currency:  {instance.currency}")
print(f"Author:    {instance.author}")
print("\n")

print("6. Author")
print("=========")
print(f"ID:        {author.id}")
print(f"Name:      {author.name}")
print(f"Email:     {author.email}")
print(f"Publisher: {author.publisher}")
print("\n")


print("7. A Pointer is stored as a JSON string in the database")
print("\n")
raw = unquote(author.key.convert())
struct = json.loads(raw)
print(f"Author Pointer: {struct}")
print("\n")


try:
    print("Cleafning up...")
    Schema.destroy(keyspace="Chapter05")
except Exception as e:
    pass 
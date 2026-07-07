from rich import print

import cqlalchemy
from cqlalchemy.connection.cql import Atom, Session
from cqlalchemy.core.models import Model, UUID
from cqlalchemy.core.commons import String, Email, Reference, Double, Currency
from cqlalchemy.connection.table import Schema 
from cqlalchemy.core.serialization import ModelSchema


cqlalchemy.configure(keyspace="Chapter12",servers=["localhost",], debug=False)

try:
    Schema.destroy(keyspace="Chapter12")
except Exception as e:
    pass 

print("\n")
print("Chapter 11: Introducing the Unit of Work Pattern!")

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


class BookSchema(ModelSchema, entity=Book):
    pass 

schema = BookSchema()
session = Session()

person = Author(name="Sam Harris", email="reach@samharris.org", publisher="Penguin Random House")
book = Book(title="The End of Faith", price=24.99, author=person, currency="USD")

print("[cyan]1. Creating Book and Person...[/cyan]")

session.add(book)
session.add(person)
session.save()

print("\n[cyan]Serialising Book to JSON[/cyan]")
result = schema.dump(book)
print(result)
print("\n")

print("[cyan]2. Deserialising Book from JSON to Model Instance[/cyan]")
found = schema.load(result)
assert isinstance(found, Book)

print("\n[cyan]3. Checking if the objects are the same.[/cyan]")
assert found == book 
assert found.author == person 
print("[bold green]The two objects are the same.[/bold green]")
print("\n")

print("Author ID:", found.author.id)
print("Name:", found.author.name)
print("Email:", found.author.email)
print("Publisher:", found.author.publisher)
print("\n")


print("Book ID:", found.id)
print("Title:", found.title)
print("Price:", found.price)
print("Currency:", found.currency)
print("\n")


try:
    print("Cleaning up...")
    Schema.destroy(keyspace="Chapter12")
except Exception as e:
    pass 
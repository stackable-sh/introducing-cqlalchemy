from datetime import datetime
from rich import print

import cqlalchemy
from cqlalchemy.connection.cql import Atom
from cqlalchemy.core.models import Model, UUID
from cqlalchemy.core.commons import String, Currency, Double, Reference, Integer
from cqlalchemy.connection.table import Schema


cqlalchemy.configure(keyspace="Chapter10",servers=["localhost",], debug=True)

try:
    Schema.destroy(keyspace="Chapter10")
except Exception as e:
    pass 

print("\n")
print("Chapter 10: Introducing Atomic Transactions with Accord!")


class Author(Model):
    id = UUID(primary=True)
    name = String(index=True, required=True)
    age = Integer(required=True, index=True)
    

class Book(Model):
    name = String(index=True, required=True)
    publisher = String(index=True, required=True)
    price = Double(required=True, index=True)
    currency = Currency(required=True, index=True)
    author = Reference(Author, index=True)

print("\n[cyan]Creating a Book & Author[/cyan]")

author = Author.create(
    name = "Charles Dickens", 
    age=65, 
)

print(f"[bold green]Author Created: {author.name}[/bold green]")
print(f"[bold green]Author Age: {author.age}[/bold green]")
print("\n")

book = Book.create(
    name="A Tale of Two Cities", 
    publisher="Harper Collins",
    price=24.99,
    currency="USD",
    author=author
)

print(f"[bold green]Book Created: {book.name}[/bold green]")
print(f"[bold green]Book Publisher: {book.publisher}[/bold green]")
print(f"[bold green]Book Price: {book.price}[/bold green]")
print(f"[bold green]Book Author: {book.author}[/bold green]")
print(f"[bold green]Book Currency: {book.currency}[/bold green]")
print("\n")

print("[cyan]Attempting to change the publisher and price atomically![/cyan]")
try:
    with Atom() as atom:
        title = atom.var(Book.objects.where(id=book.id))
        person = atom.var(Author.objects.where(id=author.id))

        with atom.when(
            title.name == "A Tale of Two Cities",
            person.age <= 70,
            title.price >= 20.00,
            title.author == author
        ):
            book.publisher = "Penguin Random House"
            book.price = 28.99
            book.save()
except Exception as e:
    print(f"[bold red]Accord Transaction Failed: {e}[/bold red]")

print("\n[bold green]Checking to see if the update took effect...[/bold green]")

instance = Book.objects.where(publisher="Penguin Random House").first()

print("\n")
print("[bold green]Book ID: %s[/bold green]" % instance.id)
print("[bold green]Book Name: %s[/bold green]" % instance.name)
print("[bold green]Book Publisher: %s[/bold green]" % instance.publisher)
print("[bold green]Book Author: %s[/bold green]" % instance.author)
print("[bold green]Book Currency: %s[/bold green]" % instance.currency)
print("[bold green]Book Price: %s[/bold green]" % instance.price)
print("\n")

try:
    print("Cleaning up...")
    Schema.destroy(keyspace="Chapter10")
except Exception as e:
    pass 
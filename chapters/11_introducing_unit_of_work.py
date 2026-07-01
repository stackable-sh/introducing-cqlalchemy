from datetime import datetime
from rich import print

import cqlalchemy
from cqlalchemy.connection.cql import Atom, Session
from cqlalchemy.core.models import Model, UUID
from cqlalchemy.core.commons import String, Email, Reference, Double, Currency
from cqlalchemy.connection.table import Schema


cqlalchemy.configure(keyspace="Chapter11",servers=["localhost",], debug=True)

try:
    Schema.destroy(keyspace="Chapter11")
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

session = Session()

person = Author(name="Sam Harris", email="reach@samharris.org", publisher="Penguin Random House")
book = Book(title="The End of Faith", price=24.99, author=person, currency="USD")

print("[cyan]1. Saving Book and Person...[/cyan]")

session.add(book)
session.add(person)
session.save()

print("\n[cyan]Book & Author Created[/cyan]")
print("\n")

assert session.contains(book)
assert session.contains(person)

assert person.saved()
assert book.saved()

print("[cyan]2. Updating Book and Person: Session Tracks Changes on Models automatically.\n[/cyan]")

person.name = "Paul Harris"
book.title = "The End of Faith II"
book.price = 9.99
session.save()

print("\n[cyan]Book & Author Updated[/cyan]")
print("\n")

print("[cyan]3. Session has an in-memory identity map, so you can get the book from the session directly.[/cyan]")

found = session.get(book.key)
assert found == book
assert found is book

print(f"[bold green]Found: {found}, and verified that the book is the same instance...[/bold green]")
print("\n")

print("[cyan]4. You can also query using Session.\n[/cyan]")

found = session.query(Book).where(author=person).first()
assert found == book

print(f"[bold green]Found Book: {found}[/bold green]")
print("\n")

print("[cyan]5. Session with Atom, and Batch for Atomicity and Isolation\n[/cyan]")
try:
    with Atom() as atom: 
        session.delete(book)
        session.delete(person)
        session.save()
except Exception as e:
    print(f"[bold red]Accord Transaction Failed: {e}[/bold red]")


print("\n")
print("[cyan]Verifying Database State [/cyan]")
print(f"[bold green]Number of Books: {Book.objects.count().get()}[/bold green]")
print(f"[bold green]Number of Authors: {Author.objects.count().get()}[/bold green]")
print("\n")


try:
    print("Cleaning up...")
    Schema.destroy(keyspace="Chapter11")
except Exception as e:
    pass 
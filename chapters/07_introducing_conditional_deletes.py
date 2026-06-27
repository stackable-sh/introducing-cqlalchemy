from rich import print

import cqlalchemy
from cqlalchemy.core.models import Model
from cqlalchemy.core.commons import String, Double
from cqlalchemy.connection.table import Schema
from cqlalchemy.connection.functions import when, r


cqlalchemy.configure(keyspace="Chapter07",servers=["localhost",], debug=False)

try:
    Schema.destroy(keyspace="Chapter07")
except Exception as e:
    pass 

print("Chapter 7: Transactions I - Conditional Updates!")


class Book(Model):
    name = String(index=True, required=True)
    publisher = String(index=True)
    price = Double(index=True, required=True)
    currency = String(index=True, required=True)

print("\n")
print("[cyan]1. Creating a Book entity[/cyan]\n")

book = Book.create(
    name="A Tale of Two Cities", 
    publisher="Amazon Kindle", 
    price=100,
    currency="USD"
)

print("Publisher:", book.publisher)
print("Price:", book.price)
print("Currency:", book.currency)
print("\n")


try:
    print("[cyan]2. Conditionally removing book publisher [/cyan]")
    book.remove(
        "publisher", 
        condition=when(
            r("publisher") =="Amazon Kindle",  # This condition will pass.
        )
    )
    book.save()
    print("[bold green]Book['publisher'] column successfully removed.[/bold green]")
except Exception as e:
    print(f"[bold red]Book update failed because: {e}[/bold red]")


print("3. Fetch the original book to show that the book did not change.\n")
instance = Book.read(book.key)

print("Publisher:", instance.publisher)
print("Price:", instance.price)
print("Currency:", instance.currency)
print("\n")

try:
    print("Cleaning up...")
    Schema.destroy(keyspace="Chapter07")
except Exception as e:
    pass 
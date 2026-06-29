from rich import print

import cqlalchemy
from cqlalchemy.connection.cql import Level, Batch
from cqlalchemy.core.models import Model
from cqlalchemy.core.commons import String, Email, Password
from cqlalchemy.connection.table import Schema


cqlalchemy.configure(keyspace="Chapter09",servers=["localhost",], debug=True)

try:
    Schema.destroy(keyspace="Chapter09")
except Exception as e:
    pass 

print("\n")
print("Chapter 8 and 9: Introducing Consistency Levels and Batching!")
salt = b'$2b$12$96KFBLBjPKZTEEOBzmU1cu'


class Account(Model):
    """An Account Entity"""
    email = Email(primary=True)
    name = String(required=True, index=True)
    password = Password(required=True, salt=salt, index=True)


print("[cyan]Creating Account with Level.All[/cyan]")

with Level.All:
    account = Account.create(
        name="Sam Harris", 
        email="reach@samharris.org",
        password="123456",
        unique=True
    )
    assert account.saved()
    print(f"[bold green]Account Created: {account.name}[/bold green]")
    print("\n")


print("[cyan]Creating Multiple Accounts in a Batch, using Consistency Level: Quorum [/cyan]")

data = [
  	("JRR Tolkein", "jrr@tolkein.org", "hobbits and dwarves"),
  	("CS Lewis", "cs@lewis.org", "nannies in narnia"),
  	("Ben Graham", "ben@graham.org", "intelligent investor #1")
]

with Level.Quorum:  						# Set the Consistency Level to Quorum for the entire operation
    with Batch() as batch:  				# Bundle all the changes together 
        for name, email, password in data:
            account = Account(name=name, email=email, password=password)
            account.save()
            print(f"[bold green]Account Created: {account.name}[/bold green]")

print("\n")
print("[cyan]Verifying State [/cyan]")
print(f"[bold green]Found Accounts: {Account.objects.count().get()}[/bold green]")
print("\n")
try:
    print("Cleaning up...")
    Schema.destroy(keyspace="Chapter09")
except Exception as e:
    pass 
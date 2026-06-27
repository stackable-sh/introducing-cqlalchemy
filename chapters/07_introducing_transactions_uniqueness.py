from rich import print

import cqlalchemy
from cqlalchemy.core.models import Model
from cqlalchemy.core.commons import String, Email, Password
from cqlalchemy.connection.table import Schema


cqlalchemy.configure(keyspace="Chapter07",servers=["localhost",], debug=False)

try:
    Schema.destroy(keyspace="Chapter07")
except Exception as e:
    pass 


print("Chapter 7: Transactions I - Uniqueness!")
salt = b'$2b$12$96KFBLBjPKZTEEOBzmU1cu'


class Account(Model):
    """An Account Entity"""
    email = Email(primary=True)
    name = String(required=True, index=True)
    password = Password(required=True, salt=salt, index=True)


print("[cyan]Creating Account[/cyan]")

account = Account.create(
    name="Sam Harris", 
    email="reach@samharris.org",
    password="123456",
    unique=True
)
assert account.saved()

print(f"[bold green]Account Created: {account.name}[/bold green]")
print("\n")

try:
    print("[cyan]Attempting to create another account with the same email[/cyan]")
    Account.create(
        name="Sam Harrison", 
        email="reach@samharris.org",
        password="12345678",
        unique=True
    )
except Exception as e:
    print("[bold red]Account creation failed because of duplicate key!\n[/bold red]")


print("[cyan]Verifying Account State[/cyan]")

found = Account.read(account.email)

print(f"[bold green]Found Account: {found.name}[/bold green]")
print(f"[bold green]Found Email: {found.email}[/bold green]")
print("\n")

try:
    print("Cleaning up...")
    Schema.destroy(keyspace="Chapter07")
except Exception as e:
    pass 
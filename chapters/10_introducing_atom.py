from datetime import datetime
from rich import print

import cqlalchemy
from cqlalchemy.connection.cql import Atom
from cqlalchemy.core.models import Model, UUID
from cqlalchemy.core.commons import String, Email, Password, DateTime, Reference
from cqlalchemy.connection.table import Schema


cqlalchemy.configure(keyspace="Chapter10",servers=["localhost",], debug=True)

try:
    Schema.destroy(keyspace="Chapter10")
except Exception as e:
    pass 

print("\n")
print("Chapter 10: Introducing Atomic Transactions with Accord!")

salt = b'$2b$12$96KFBLBjPKZTEEOBzmU1cu'


class Profile(Model):
    id = UUID(primary=True)
    email = Email(index=True, required=True)
    name = String(required=True, index=True)
    password = Password(required=True, salt=salt, index=True)

class Account(Model):
    email = Email(primary=True)
    created = DateTime(index=True, required=True)
    profile = Reference(Profile, index=True)

print("\n[cyan]Creating an Account & Profile[/cyan]")

profile = Profile.create(
    name="Sam Harris", 
    email="old@samharris.org",
    password="123456"
)

account = Account.create(
    email="old@samharris.org", 
    created=datetime.now(), 
    profile=profile
)

print(f"[bold green]Account Created: {account.email}[/bold green]")
profile = account.profile 
print(f"[bold green]Account Name: {profile.name}[/bold green]")
print(f"[bold green]Account Email: {profile.email}[/bold green]")
print("\n")

print("[cyan]Attempting to atomically change the email address using Accord![/cyan]")
try:
    with Atom() as atom: 
        # 1. Create a transaction variable for storing the current state.
        old =  atom.var(Account.objects.where(email="old@samharris.org"))
        new = atom.var(Account.objects.where(email="new@samharris.org"))
        # 2. Make sure that no one else uses that email address on the system.
        with atom.when(old != None, new == None):
            # 3. Change the email address in atomically within Accord 
            profile = account.profile 
            profile.email = "new@samharris.org"
            profile.save()
            # 4. Create a new Account object pointing to this Preference
            Account.create(email="new@samharris.org", profile=profile, created=datetime.now())
            # 5. Delete the old Account instance
            Account.delete(account)
except Exception as e:
    print(f"[bold red]Accord Transaction Failed: {e}[/bold red]")

print("\n")
print("[cyan]Verifying State [/cyan]")
print(f"[bold green]Number of Accounts: {Account.objects.count().get()}[/bold green]")
print("\n")

# 3. Verify that the account was updated.
account = Account.read("new@samharris.org")
assert account
profile = account.profile 
print(f"[bold green]Account Name: {profile.name}[/bold green]")
print(f"[bold green]Account Email: {profile.email}[/bold green]")
print("\n")

try:
    print("Cleaning up...")
    Schema.destroy(keyspace="Chapter10")
except Exception as e:
    pass 
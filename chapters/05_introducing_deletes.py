from rich import print

import cqlalchemy
from cqlalchemy.core.models import Model, UUID
from cqlalchemy.core.commons import String, Email
from cqlalchemy.connection.table import Schema


cqlalchemy.configure(keyspace="Chapter05",servers=["localhost",], debug=False)

try:
    Schema.destroy(keyspace="Chapter05")
except Exception as e:
    pass 

print("Chapter 5: Deleting Instances of Model from C*")
print("\n")


# Define an Author 
class Author(Model):
    """An Author Entity"""
    id = UUID(primary=True)
    name = String(required=True, index=True)
    email = Email(required=True, index=True)
    publisher = String(required=True, index=True)


print("1. Let's create a few instances of Author")

sam = Author.create(
    name="Sam Harris", 
    email="reach@samharris.org", 
    publisher="Penguin Random House"
)
rowling = Author.create(
    name="JK Rowling", 
    email="reach@jkrowling.org", 
    publisher="Barnes and Noble"
)
tolkien = Author.create(
    name="JRR Tolkien", 
    email="reach@tolkien.org", 
    publisher="Houghton Mifflin Harcourt"
)
chinua = Author.create(
    name="Chinua Achebe", 
    email="reach@achebe.org", 
    publisher="Everyman Library"
)

print("\n")
print(f"Created {sam.name}")
print(f"Created {rowling.name}")
print(f"Created {tolkien.name}")
print(f"Created {chinua.name}")
print("\n")


print("2. You can delete an instance of a Model by passing the instance itself")
print(f"Deleting Sam: {sam}")
Author.delete(sam)
print("\n")


print("3. You can also delete an instance of a Model by passing its Pointer")
print(f"Deleting Tolkien: {tolkien.key}")
Author.delete(tolkien.key)
print("\n")

print("4. You can delete an instance by passing a key part")
print(f"Deleting Rowling: {rowling.id}")
Author.delete(rowling.id)
print("\n")

print("5. Or you can pass a dictionary with all the key columns")
print(f"Deleting Chinua: %s" % {"id" : chinua.id})
Author.delete({"id": chinua.id})
print("\n")


print("Let's verify that all instances have been deleted")
print("Found Authors: %s" % Author.objects.count().get())
print("\n")

try:
    print("Cleaning up...")
    Schema.destroy(keyspace="Chapter05")
except Exception as e:
    pass 
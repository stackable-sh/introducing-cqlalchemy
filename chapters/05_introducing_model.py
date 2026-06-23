import cqlalchemy
from cqlalchemy.core.models import Model, UUID
from cqlalchemy.core.commons import String, URL, Phone, Text, Email
from cqlalchemy.connection.table import Schema


cqlalchemy.configure(keyspace="Chapter05",servers=["localhost",], debug=False)

try:
    Schema.destroy(keyspace="Chapter05")
except Exception as e:
    pass 

print("Chapter 5: Introducing Model!")
print("\n")

# Define a Model for an Author 
class Author(Model):
    """An Author Entity"""
    id = UUID(primary=True)
    name = String(required=True, index=True)
    email = Email(required=True, index=True)
    publisher = String(required=True, index=True)
    address = Text(required=True)
    website = URL(required=True)
    phone = Phone(required=True, index=True)

person = Author.create(
    name="Sam Harris", 
    email="reach@samharris.org",
    publisher="Penguin Random House", 
    address="123 Main St, Sacramento, California, US", 
    website="http://samharris.org", 
    phone="+2348094487105"
)
assert person.saved()

person.publisher = "Barnes & Noble, Inc"
person.save()   

found = Author.read(person.id)

print("Author Details:")
print("===============")
print(f"ID:        {found.id}")
print(f"Name:      {found.name}")
print(f"Address:   {found.address}")
print(f"Phone:     {found.phone}")
print(f"Publisher: {found.publisher}")
print("\n")

try:
    Schema.destroy()
except Exception as e:
    pass 
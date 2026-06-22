import cqlalchemy
from cqlalchemy.core.models import Expando
from cqlalchemy.connection.table import Schema


cqlalchemy.configure(keyspace="Chapter04",servers=["localhost",], debug=False)

try:
    Schema.destroy(keyspace="Chapter04")
except Exception as e:
    pass 

print("Chapter 4: Hello World")
print("\n")

class Author(Expando):
    pass 


person = Author.create(name="Sam Harris", age=49, category="Philosophy")

id = person["id"]
instance = Author.read(id)

assert instance["name"] == "Sam Harris"
assert instance["age"] == 49
assert instance["category"] == "Philosophy"

instance["name"] = "Shakespeare"
instance["address"] = "#10 Downing Street, London"
instance["age"] = 53
instance["publisher"] = "Barnes & Noble, Inc"
instance.save()   

found = Author.read(id)

print("Author:")
print(f"ID:        {found['id']}")
print(f"Name:      {found['name']}")
print(f"Address:   {found['address']}")
print(f"Age:       {found['age']}")
print(f"Publisher: {found['publisher']}")
print("\n")

try:
    Schema.destroy()
except Exception as e:
    pass 
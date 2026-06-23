import cqlalchemy
from cqlalchemy.core.models import SortedSet
from cqlalchemy.connection.table import Schema


cqlalchemy.configure(keyspace="Chapter04",servers=["localhost",], debug=False)

try:
    Schema.destroy(keyspace="Chapter04")
except Exception as e:
    pass 

print("Chapter 4: Hello SortedSet!")
print("\n")

# Define an SortedSet using inheritance. 
class Bag(SortedSet):
    pass

# You can also Define an SortedSet using the functional style
Bag = SortedSet.new("Bag")

# Create a Bag and add some fruits, and persist it to C*
fruits = Bag(data=["Apple", "Banana", "Watermelon", "Grapes"])
fruits.save()

id = fruits["id"] 
fruits = Bag.read(id)

assert len(fruits) == 4

# You can add objects to a SortedSet
others = ["Carrot", "Orange", "Cucumber", "Mango", "Apple", "Banana"]
for name in others:
    fruits.add(name)

# Save Set to C*, in a network efficient way. 
fruits.save()

# Read the Bag from another session, and verify the data you've persisted
fruits = Bag.read(id)
assert len(fruits) == 8

print("Fruit Bag: ")
print("================")
for idx, fruit in enumerate(fruits):
    print(f"{idx} => {fruit}")
    
print("================")
print("\n")

try:
    Schema.destroy()
except Exception as e:
    pass 
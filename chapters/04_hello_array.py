import cqlalchemy
from cqlalchemy.core.models import Array
from cqlalchemy.connection.table import Schema


cqlalchemy.configure(keyspace="Chapter04",servers=["localhost",], debug=False)

try:
    Schema.destroy(keyspace="Chapter04")
except Exception as e:
    pass 

print("Chapter 4: Hello Array!")
print("\n")

# Define an Array using inheritance. 
class Basket(Array):
    pass

# You can also Define an Array using the functional style
Basket = Array.new("Basket")

# Create a Basket and add some fruits, and persist it to C*
fruits = Basket(data=["Apple", "Banana", "Watermelon", "Grapes"])
fruits.save()

id = fruits["id"] 
fruits = Basket.read(id)

assert fruits[0] == "Apple"
assert len(fruits) == 4

# You can prepend, extend, remove, and append objects to an Array
fruits.append("Carrot")
fruits.extend(["Orange", "Cucumber", "Mango"])
fruits.prepend("Guava")
fruits.insert(3, "Plantain")
del fruits[3]     

# Save Array to C*, in a network efficient way. 
fruits.save()

# Read the Basket from another session, and verify the data you've persisted
fruits = Basket.read(id)

print("Fruit Basket: ")
print("==============")
for idx, fruit in enumerate(fruits):
    print(f"{idx} => {fruit}")
    
print("==============")
print("\n")

try:
    Schema.destroy()
except Exception as e:
    pass 
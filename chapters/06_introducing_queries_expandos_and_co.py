from rich import print

import cqlalchemy
from cqlalchemy.core.models import Array, Expando, SortedSet
from cqlalchemy.connection.table import Schema


cqlalchemy.configure(keyspace="Chapter06",servers=["localhost",], debug=False)


try:
    Schema.destroy(keyspace="Chapter06")
except Exception as e:
    pass 


print("Chapter 6: Queries I - Expandos and Co")
print("1 Expando Queries: Creating some entities for usage. \n")

Book = Expando.new("Book")
book = Book.create(name="A Tale of Two Cities", publisher="Penguin Random House", year=1984)

print("1(a) Querying Book object by value")

found = Book.objects.contains(value="A Tale of Two Cities").get()
assert book == found 
assert book["publisher"] == found["publisher"]
print("Found:", found)

print("\n")

print("1(b) Querying Book objects by keys")

found = Book.objects.contains(key="publisher").get()
assert book == found 
assert book["publisher"] == found["publisher"]
print("Found:", found)

print("\n")

print("2. Array Queries: Creating some entities \n")

Basket = Array.new("Basket")
basket = Basket.create(data=["Pear", "Apple", "Mango", "Orange", "Banana"])

print("2(a) Querying Array objects by value")

found = Basket.objects.contains(value="Apple").get()
assert basket == found 
assert "Apple" in found 
print("Found: ", found)


print("\n")

print("3. SortedSet Queries: Creating some entities \n")

Bag = SortedSet.new("Bag")
bag = Bag.create(data={"Pear", "Apple", "Mango", "Orange", "Banana"})

print("3(a) Querying SortedSet objects by value")
found = Bag.objects.contains(value="Apple").get()
assert bag == found 
assert "Apple" in found 
print("Found: ", found)

print("\n")


try:
    print("Cleaning up...")
    Schema.destroy(keyspace="Chapter06")
except Exception as e:
    pass 
from django.shortcuts import render, redirect
from .mongodb import get_fruits
from pymongo import MongoClient
from django.http import Http404
# Create your views here.
from django.conf import settings





# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['fruits']
collection = db['fruitss']

def fruits_view(request):
    # Fetch all documents from the 'fruitss' collection
    fruits = get_fruits() 
    return render(request, 'fruits/fruits.html', {'fruits': fruits})
 # Fetch all fruits from MongoDB



def delete_product_view(request, name):
    if request.method == "POST":
        # Delete the product by name
        collection.delete_one({"name": name})
        return redirect("/")



def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = float(request.POST.get('price'))  # Convert price to a number
        description = request.POST.get('description')
        image = request.POST.get('image')

        # Save product to MongoDB
        collection.insert_one({
            'name': name,
            'price': price,
            'description': description,
            'image': image
        })
        return redirect('/')  # Redirect to the home page

    return render(request, 'fruits/add_product.html')




def product_detail_view(request, name):
    product = collection.find_one({"name": name})
    
    if not product:
        return render(request, "404.html", status=404)

    if request.method == "POST":
        new_name = request.POST.get("name")
        new_price = request.POST.get("price")
        new_description = request.POST.get("description")
        
        # Update the product in the database
        collection.update_one(
            {"name": name},
            {
                "$set": {
                    "name": new_name,
                    "price": float(new_price),
                    "description": new_description,
                }
            }
        )
        return redirect("fruits")  # Redirect to the updated product detail page

    return render(request, "fruits/product_detail.html", {"product": product})
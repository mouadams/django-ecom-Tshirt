from django.shortcuts import render, redirect
from .mongodb import get_tshirts_ecom
from pymongo import MongoClient
from django.http import Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib import messages
from bson import ObjectId





# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['tshirts_ecom']
collection = db['tshirts']




def tshirts_view(request):
    query = request.GET.get("q", "")  # Get the search query from the request
    logged_in = request.session.get("logged_in")
    user = request.session.get("user")

    if query:
        # Search by name or description (case-insensitive)
        tshirts = collection.find({
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                
            ]
        })
    else:
        tshirts = collection.find()  # If no search query, fetch all products

    return render(request, 'tshirts/home.html', {'tshirts': tshirts, 'logged_in': logged_in, 'user': user})






def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = float(request.POST.get('price'))  # Convert price to a number
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if image:
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            image_url = fs.url(filename)
        else:
            image_url = None

        # Save product to MongoDB
        collection.insert_one({
            'name': name,
            'price': price,
            'description': description,
            'image': image_url
        })
        return redirect('/')  # Redirect to the home page

    return render(request, 'tshirts/add_product.html')




def product_detail_view(request, name):
    logged_in = request.session.get("logged_in")
    product = collection.find_one({"name": name, })
    
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
        return redirect("home")  # Redirect to the updated product detail page

    return render(request, "tshirts/product_detail.html", {"product": product, "logged_in": logged_in})


def delete_product_view(request, name):
    if request.method == "POST":
        # Delete the product by name
        collection.delete_one({"name": name})
        return redirect("/")
    




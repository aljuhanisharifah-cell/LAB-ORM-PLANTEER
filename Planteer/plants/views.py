from django.shortcuts import render, redirect
from .models import Plant, Comment
from django.core.paginator import Paginator


def add_plant(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')

       
        if not name:
            return render(request, 'plants/add.html', {
                'error': 'Name is required'
            })

        if not description:
            return render(request, 'plants/add.html', {
                'error': 'Description is required'
            })

        Plant.objects.create(
            name=name,
            description=description,
            image=request.FILES.get('image'),
            category=request.POST.get('category'),
            is_edible=True if request.POST.get('is_edible') else False
        )

        return redirect('all_plants')

    return render(request, 'plants/add.html')


def all_plants(request):
    plants_list = Plant.objects.all()

   
    query = request.GET.get('q')
    if query:
        plants_list = plants_list.filter(name__icontains=query)

    
    paginator = Paginator(plants_list, 6) 

    page_number = request.GET.get('page')
    plants = paginator.get_page(page_number)

    return render(request, 'plants/all.html', {'plants': plants})

  

def plant_detail(request, plant_id):
    plant = Plant.objects.get(id=plant_id)

    if request.method == "POST":
        text = request.POST.get('comment')
        if text:
            Comment.objects.create(plant=plant, text=text)

    related = Plant.objects.filter(category=plant.category).exclude(id=plant.id)

    return render(request, 'plants/detail.html', {
        'plant': plant,
        'related': related
    })
    
def update_plant(request, plant_id):
    plant = Plant.objects.get(id=plant_id)

    

    if request.method == "POST":
        plant.name = request.POST.get('name')
        plant.description = request.POST.get('description')
        plant.category = request.POST.get('category')
        plant.is_edible = True if request.POST.get('is_edible') else False

        if request.FILES.get('image'):
            plant.image = request.FILES.get('image')

        plant.save()
        return redirect('plant_detail', plant_id=plant.id)

    return render(request, 'plants/update.html', {'plant': plant})

def delete_plant(request, plant_id):
    plant = Plant.objects.get(id=plant_id)

    if request.method == "POST":
        plant.delete()
        return redirect('all_plants')

    return render(request, 'plants/delete.html', {'plant': plant})

def search_plants(request):
    plants = Plant.objects.all()

    query = request.GET.get('q')
    if query:
        plants = plants.filter(name__icontains=query)

    category = request.GET.get('category')
    if category:
        plants = plants.filter(category=category)

    is_edible = request.GET.get('edible')
    if is_edible:
        plants = plants.filter(is_edible=True)

    return render(request, 'plants/search.html', {'plants': plants})
from django.shortcuts import render, redirect
from plants.models import Plant
from .models import Contact


def home(request):
    plants = Plant.objects.all()
    return render(request, 'main/home.html', {'plants': plants})


def contact(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # validation
        if first_name and last_name and email and message:
            Contact.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                message=message
            )
            return redirect("contact_messages")

    return render(request, "main/contact.html")


def contact_messages(request):
    messages = Contact.objects.all()
    return render(request, 'main/messages.html', {'messages': messages})
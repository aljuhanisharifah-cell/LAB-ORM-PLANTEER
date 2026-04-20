from django.db import models


class Plant(models.Model):

    CATEGORIES = [
        ('Fruit', 'Fruit'),
        ('Vegetable', 'Vegetable'),
        ('Flower', 'Flower'),
        ('Tree', 'Tree'),
    ]

  
    name = models.CharField(max_length=200)

   
    description = models.TextField()

    image = models.ImageField(upload_to='plants/images', blank=True, null=True)


    category = models.CharField(max_length=100, choices=CATEGORIES, default='Fruit')

  
    is_edible = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)   # ✨ هذا الجديد
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
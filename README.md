<p align="center">
  <img src="https://github.com/user-attachments/assets/f46a7e13-1b3c-43fb-9bde-ed6c88c12120" alt="YS-mobilebanner@2x" />
</p>
<p align="center">
  <strong style="font-size: 8em;">Trees Everywhere - Teste YouShop</strong>
</p>

<p align="center">
  <hr style="width: 50%; border: 2px solid black;"/>
</p>




</br>

# Project Documentation

</br>

## Table of Contents
1. [Project Overview](#project-overview)
2. [Installation and Setup](#installation-and-setup)
3. [Models](#models)
4. [Views](#views)
5. [Forms](#forms)
6. [Serializers](#serializers)
7. [Admin Configuration](#admin-configuration)
8. [Testing](#testing)
9. [API Endpoints](#api-endpoints)
10. [Conclusion](#conclusion)

---

## Project Overview

This project is a Django application that allows users to plant trees and track their planted trees. Users can log in, view their planted trees, and plant new trees. The project also includes a REST API for interacting with the tree planting functionality.

## Installation and Setup

### Prerequisites

- Python 3.10.12
- Django
- Django Rest Framework

### Installation Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/ViniciusRodrigues10/trees-everywhere-projet.git
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply the migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

## Models

The project includes the following models:

### Account

```python
class Account(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, related_name="accounts")

    def __str__(self):
        return self.name
```

### Profile

```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    joined = models.DateTimeField(auto_now_add=True)
```

### Tree

```python
class Tree(models.Model):
    name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)
```

### PlantedTree

```python
class PlantedTree(models.Model):
    planted_at = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
```

## Views

The project includes both function-based views and class-based views for handling different functionalities.

### Function-Based Views

- register_user
- user_login
- planted_trees
- user_logout
- planted_tree_detail
- add_planted_tree
- list_trees_planted_by_user_in_your_accounts

### Class-Based Views

- UserLoginView
- UserPlantedTreesListView

## Forms

The project uses Django forms for handling user input.

### PlantedTreeForm

```python
from django import forms
from .models import PlantedTree

class PlantedTreeForm(forms.ModelForm):
    class Meta:
        model = PlantedTree
        fields = ["tree", "age", "latitude", "longitude", "account"]
```

### UserRegistrationForm

```python
about = forms.CharField(required=False, widget=forms.Textarea)

class Meta:
    model = User
    fields = ("username", "password1", "password2", "about")

def save(self, commit=True):
    user = super().save(commit=False)
    if commit:
        user.save()
        Profile.objects.create(user=user, about=self.cleaned_data["about"])
    return user
```

## Serializers

The project uses Django Rest Framework serializers to handle serialization and deserialization of model instances.

### PlantedTreeSerializer

```python
from rest_framework import serializers
from .models import PlantedTree

class PlantedTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantedTree
        fields = ["id", "tree", "age", "latitude", "longitude", "planted_at", "account"]
```

## Admin Configuration

The project includes custom admin configurations for managing the models.

### AccountAdmin

```python
from django.contrib import admin
from .models import Account, Profile, Tree, PlantedTree

class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "active")

admin.site.register(Account, AccountAdmin)
```

### ProfileAdmin

```python
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "joined")

admin.site.register(Profile, ProfileAdmin)
```

### TreeAdmin
```python
class TreeAdmin(admin.ModelAdmin):
    list_display = ("name", "scientific_name")

admin.site.register(Tree, TreeAdmin)
```

### PlantedTreeAdmin
```python
class PlantedTreeAdmin(admin.ModelAdmin):
    list_display = ("tree", "user", "age", "planted_at", "latitude", "longitude", "account")

admin.site.register(PlantedTree, PlantedTreeAdmin)
```

## Testing

The project includes tests for various functionalities.

### Models Tests
```python
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Account, Profile, Tree, PlantedTree

class TreePlantingTestCase(TestCase):
    def setUp(self):
        """
        Sets up initial data for the test case.
        """
        # Create accounts and users
        # ... (setup code)

    def test_user_can_plant_tree(self):
        """
        Tests that a user can plant a single tree.
        """
        # ... (test code)

    def test_user_can_plant_multiple_trees(self):
        """
        Tests that a user can plant multiple trees.
        """
        # ... (test code)
```

### Views Tests
```python
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from ..models import Account, Profile, Tree, PlantedTree

class TreePlantingTemplateTestCase(TestCase):
    def setUp(self):
        """
        Sets up initial data and client for the test case.
        """
        # ... (setup code)

    def test_list_user_planted_trees(self):
        """
        Tests that the user can list their planted trees.
        """
        # ... (test code)

    def test_list_user_planted_trees_forbidden(self):
        """
        Tests that the user can list planted trees in their accounts.
        """
        # ... (test code)

    def test_list_account_planted_trees(self):
        """
        Tests that the user can list trees planted in their account.
        """
        # ... (test code)

    def test_plant_tree_view(self):
        """
        Tests that the user can plant a tree using the view.
        """
        # ... (test code)
```

## API Endpoints

### Login

**Endpoint:** /api/login

**Method:** POST

**Request:**

~~~json
{
  "username": "user",
  "password": "user123456789"
}
~~~

**Response:**

~~~json
{
  "message": "Successfully logged in.",
  "token": "e30c20d52a6d0d20508ebc4e68a5ef90e59a3008"
}
~~~

### List Planted Trees

**Endpoint:** /api/planted-trees/

**Method:** GET

**Headers:**

~~~bash
Authorization: Token e30c20d52a6d0d20508ebc4e68a5ef90e59a3008
~~~

**Response:**

~~~json
[
  {
    "id": 1,
    "tree": "Tree 1",
    "age": 2,
    "latitude": "12.456",
    "longitude": "13.456",
    "planted_at": "2023-01-01T00:00:00Z",
    "account": "Account 1"
  },
  ...
]
~~~

## Conclusion

This documentation provides an overview of the project structure, models, views, forms, serializers, admin configuration, testing, and API endpoints. Use this as a guide to understand the project.

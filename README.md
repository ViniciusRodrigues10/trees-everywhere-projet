# Trees Everywhere - Teste YouShop

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

- Python 3.x
- Django
- Django Rest Framework

### Installation Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv env
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

## AccountAdmin

```python
from django.contrib import admin
from .models import Account, Profile, Tree, PlantedTree

class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "active")

admin.site.register(Account, AccountAdmin)
```


from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


# Adds a method to the User model to plant a single tree.
User.add_to_class(
    "plant_tree",
    lambda self, tree, latitude, longitude: PlantedTree.objects.create(
        user=self, tree=tree, latitude=Decimal(latitude), longitude=Decimal(longitude)
    ),
)

# Adds a method to the User model to plant multiple trees at different locations.
User.add_to_class(
    "plant_trees",
    lambda self, tree_locations, account: [
        PlantedTree.objects.create(
            user=self,
            tree=tree_location[0],
            latitude=Decimal(tree_location[1][0]),
            longitude=Decimal(tree_location[1][1]),
            account=account,
        )
        for tree_location in tree_locations
    ],
)

# Adds method to the User model to plant a single tree with age and account information.
User.add_to_class(
    "plant_tree",
    lambda self, tree, latitude, longitude, age, account: PlantedTree.objects.create(
        user=self,
        tree=tree,
        latitude=Decimal(latitude),
        longitude=Decimal(longitude),
        age=age,
        account=account,
    ),
)


class Account(models.Model):
    """
    Model representing an account which can have multiple users.
    """

    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, related_name="accounts")

    def __str__(self):
        return self.name


class Profile(models.Model):
    """
    Model representing a user profile with additional information.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    joined = models.DateTimeField(auto_now_add=True)


class Tree(models.Model):
    """
    Model representing a tree species.
    """

    name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)


class PlantedTree(models.Model):
    """
    Model representing a planted tree with its details.
    """

    planted_at = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

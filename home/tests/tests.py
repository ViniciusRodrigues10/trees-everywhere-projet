from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Account, Profile, Tree, PlantedTree


class TreePlantingTestCase(TestCase):
    def setUp(self):
        """
        Sets up initial data for the test case.
        """

        # Create accounts
        self.account1 = Account.objects.create(name="Account 1", active=True)
        self.account2 = Account.objects.create(name="Account 2", active=True)

        # Create users
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.user3 = User.objects.create_user(username="user3", password="password")

        # Associate users with accounts
        self.account1.users.add(self.user1, self.user3)
        self.account2.users.add(self.user2)

        # Create profiles for users
        Profile.objects.create(user=self.user1, about="About user1")
        Profile.objects.create(user=self.user2, about="About user2")
        Profile.objects.create(user=self.user3, about="About user3")

        # Create trees
        self.tree1 = Tree.objects.create(name="Tree 1", scientific_name="Treeus oneus")
        self.tree2 = Tree.objects.create(name="Tree 2", scientific_name="Treeus twous")

        # Plant trees
        self.user1.plant_tree(
            tree=self.tree1,
            latitude="123.456",
            longitude="123.456",
            age=2,
            account=self.account1,
        )
        self.user2.plant_tree(
            tree=self.tree2,
            latitude="654.321",
            longitude="654.321",
            age=3,
            account=self.account2,
        )
        self.user3.plant_tree(
            tree=self.tree1,
            latitude="789.012",
            longitude="789.012",
            age=1,
            account=self.account1,
        )

    def test_user_can_plant_tree(self):
        """
        Tests that a user can plant a single tree.
        """

        user = User.objects.create_user(username="user4", password="password")
        self.account1.users.add(user)

        tree = Tree.objects.create(name="Tree 3", scientific_name="Tree three")
        user.plant_tree(
            tree=tree,
            latitude="345.678",
            longitude="345.678",
            age=1,
            account=self.account1,
        )

        self.assertEqual(PlantedTree.objects.filter(user=user, tree=tree).count(), 1)

    def test_user_can_plant_multiple_trees(self):
        """
        Tests that a user can plant multiple trees.
        """

        user = User.objects.create_user(username="user5", password="password")
        self.account2.users.add(user)

        tree1 = Tree.objects.create(name="Tree 4", scientific_name="Tree four")
        tree2 = Tree.objects.create(name="Tree 5", scientific_name="Tree five")

        user.plant_trees(
            [(tree1, ("11.111", "11.111")), (tree2, ("22.222", "22.222"))],
            self.account2,
        )

        self.assertEqual(PlantedTree.objects.filter(user=user, tree=tree1).count(), 1)
        self.assertEqual(PlantedTree.objects.filter(user=user, tree=tree2).count(), 1)

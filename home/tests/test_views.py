from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Account, Profile, Tree, PlantedTree


class TreePlantingTemplateTestCase(TestCase):

    def setUp(self):
        """
        Sets up initial data and client for the test case.
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
            latitude="12.456",
            longitude="13.456",
            age=2,
            account=self.account1,
        )

        self.user2.plant_tree(
            tree=self.tree2,
            latitude="65.321",
            longitude="64.321",
            age=3,
            account=self.account2,
        )
        self.user3.plant_tree(
            tree=self.tree1,
            latitude="78.012",
            longitude="79.012",
            age=1,
            account=self.account1,
        )

    def test_list_user_planted_trees(self):
        """
        Tests that the user can list their planted trees.
        """

        self.client.login(username="user1", password="password")
        response = self.client.get("/planted-trees/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tree 1")
        self.assertNotContains(response, "Tree 2")

    def test_list_user_planted_trees_forbidden(self):
        """
        Tests that the user can list planted trees in their accounts.
        """

        self.client.login(username="user1", password="password")
        response = self.client.get("/list-planted-tree-in-your-accounts/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tree 1")
        self.assertNotContains(response, "Tree 2")
        self.assertNotContains(response, "Tree 3")

    def test_list_account_planted_trees(self):
        """
        Tests that the user can list trees planted in their account.
        """

        self.client.login(username="user1", password="password")
        response = self.client.get("/list-planted-tree-in-your-accounts/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tree 1")
        self.assertNotContains(response, "Tree 2")

    def test_plant_tree_view(self):
        """
        Tests that the user can plant a tree using the view.
        """

        self.client.login(username="user1", password="password")
        tree = Tree.objects.create(name="Tree 3", scientific_name="Tree three")
        response = self.client.post(
            ("/add-planted-tree/"),
            {
                "tree": tree.id,
                "latitude": "34.128",
                "longitude": "35.678",
                "age": 1,
                "account": self.account1.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            PlantedTree.objects.filter(tree=tree, user=self.user1).count(), 1
        )

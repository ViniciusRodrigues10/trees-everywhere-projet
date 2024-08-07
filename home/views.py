from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import login as django_login
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import PlantedTree
from .forms import PlantedTreeForm, UserRegistrationForm
from .serializers import PlantedTreeSerializer


def register_user(request):
    """
    Handles user registration requests.
    """

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, "register_user.html", {"form": form})


def user_login(request):
    """
    Handles user login. Authenticates and logs in the user if credentials are valid.
    """

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("planted_trees")
        else:
            return render(
                request, "login.html", {"error": "nome de usuário ou senha inválidos."}
            )
    else:
        return render(request, "login.html")


@login_required
def planted_trees(request):
    """
    Displays a list of trees planted by the logged-in user.
    """

    trees = PlantedTree.objects.filter(user=request.user)
    return render(request, "planted_trees.html", {"trees": trees})


def user_logout(request):
    """
    Logs out the user and redirects to the login page.
    """

    logout(request)
    return redirect("/login")


@login_required
def planted_tree_detail(request, tree_id):
    """
    Displays the details of a specific planted tree for the logged-in user.
    """

    tree = get_object_or_404(PlantedTree, id=tree_id, user=request.user)
    return render(request, "planted_tree_detail.html", {"tree": tree})


@login_required
def add_planted_tree(request):
    """
    Handles the addition of a new planted tree by the logged-in user.
    """

    if request.method == "POST":
        form = PlantedTreeForm(request.POST)
        if form.is_valid():
            planted_tree = form.save(commit=False)
            planted_tree.user = request.user
            planted_tree.save()
            return redirect("planted_trees")
    else:
        form = PlantedTreeForm()
    return render(request, "add_planted_tree.html", {"form": form})


@login_required
def list_trees_planted_by_user_in_your_accounts(request):
    """
    Displays a list of trees planted by the logged-in user across all their accounts.
    """

    planted_trees = (
        PlantedTree.objects.filter(user=request.user)
        .select_related("account", "tree")
        .distinct()
    )
    accounts = set()
    for tree in planted_trees:
        accounts.add(tree.account)
    trees_in_acounts = PlantedTree.objects.filter(account__in=accounts).distinct()
    return render(
        request,
        "trees_planted_by_users_in_their_accounts.html",
        {"planted_trees": trees_in_acounts},
    )


class UserLoginView(APIView):
    """
    API view for user login. Returns a token if the credentials are valid.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if username is None or password is None:
            return Response(
                {"error": "Please provide both username and password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"message": "Successfully logged in.", "token": token.key},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class UserPlantedTreesListView(APIView):
    """
    API view to list all trees planted by the authenticated user.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        trees_planted_by_user = PlantedTree.objects.filter(user=user)
        serializer = PlantedTreeSerializer(trees_planted_by_user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

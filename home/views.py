from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import PlantedTree
from .forms import PlantedTreeForm


def user_login(request):
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
    trees = PlantedTree.objects.filter(user=request.user)
    return render(request, "planted_trees.html", {"trees": trees})


@login_required
def planted_tree_detail(request, tree_id):
    tree = get_object_or_404(PlantedTree, id=tree_id, user=request.user)
    return render(request, "planted_tree_detail.html", {"tree": tree})


@login_required
def add_planted_tree(request):
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

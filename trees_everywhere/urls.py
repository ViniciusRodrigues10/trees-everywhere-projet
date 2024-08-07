"""
URL configuration for trees_everywhere project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from home import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="API documentation for the Trees Everywhere project",
        contact=openapi.Contact(email="viniciusgcrodrigues.contato@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register-user/", views.register_user, name="register_user"),
    path("planted-trees/", views.planted_trees, name="planted_trees"),
    path(
        "planted-trees/<int:tree_id>/",
        views.planted_tree_detail,
        name="planted_tree_detail",
    ),
    path("add-planted-tree/", views.add_planted_tree, name="add_planted_tree"),
    path(
        "list-planted-tree-in-your-accounts/",
        views.list_trees_planted_by_user_in_your_accounts,
        name="list_planted_tree_in_your_accounts",
    ),
    path("api/login", views.UserLoginView.as_view(), name="login"),
    path(
        "api/planted-trees/",
        views.UserPlantedTreesListView.as_view(),
        name="planted-trees-list",
    ),
]

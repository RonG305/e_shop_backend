from django.urls import path
from category import views

urlpatterns = [
    path("categories/", views.getCategories, name="categories"),
    path('get-category/<int:pk>/', views.getCategory, name="get-category"),
    path("post-category/", views.postCategory, name="post-category"),
    path("update-category/<int:pk>/", views.updateCategory, name="update-category"),
    path('delete-category/<int:pk>/', views.deleteCategory, name="delete-category")
]
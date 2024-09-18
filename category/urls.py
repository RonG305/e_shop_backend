from django.urls import path
from category import views

urlpatterns = [
    path("categories/", views.getCategories, name="categories"),
     path("sub_categories/", views.getSubCategories, name="sub_categories"),
    path('get-category/<int:pk>/', views.getCategory, name="get-category"),
    path("post-category/", views.postCategory, name="post-category"),
    path("update-category/<int:pk>/", views.updateCategory, name="update-category"),
    path('delete-category/<int:pk>/', views.deleteCategory, name="delete-category"),


  
    path('get-subcategory/<int:pk>/', views.getSubCategory, name="get-subcategory"),
    path("post-subcategory/", views.postSubCategory, name="post-subcategory"),
    path("update-subcategory/<int:pk>/", views.updateSubCategory, name="update-subcategory"),
    path('delete-subcategory/<int:pk>/', views.deleteSubCategory, name="delete-subcategory")
]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 


    path("api/products/", include("product.urls")),
    path("api/category/", include("category.urls")),
    path("api/orders/", include("order.urls")),
    path('api/cart/', include('cart.urls')),
    path('api/payment/', include('payment.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

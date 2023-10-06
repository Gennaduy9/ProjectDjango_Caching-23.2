from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import IndexView, CategoryListView, ProductDetailView, ProductListView, ContactView, \
    ConnectionView, StoreView, PrivacyView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('categorys/', CategoryListView.as_view(), name='categorys'),
    path('<int:pk>/products/', ProductListView.as_view(), name='category_product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('connections/', ConnectionView.as_view(), name='connections'),
    path('store/', StoreView.as_view(), name='store'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
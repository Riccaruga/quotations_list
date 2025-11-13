from django.urls import path
from . import views # Keep this line
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Update the views to use 'views.<ViewName>'
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.QuoteList.as_view(), name='quotes'),
    path('quote/<int:pk>/', views.QuoteDetail.as_view(), name='quote'),
    path('quote-create/', views.QuoteCreate.as_view(), name='quote-create'),
    path('quote-update/<int:pk>/', views.QuoteUpdate.as_view(), name='quote-update'),
    path('quote-delete/<int:pk>/', views.QuoteDelete.as_view(), name='quote-delete'),
    path('quote/<int:pk>/toggle-complete/', views.toggle_complete, name='quote-toggle-complete'),
]
from django.urls import path
from . import views
from .views import QuoteList, QuoteDetail, QuoteCreate, QuoteUpdate, QuoteDelete, CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', QuoteList.as_view(), name='quotes'),
    path('quote/<int:pk>/', QuoteDetail.as_view(), name='quote'),
    path('quote-create/', QuoteCreate.as_view(), name='quote-create'),
    path('quote-update/<int:pk>/', QuoteUpdate.as_view(), name='quote-update'),
    path('quote-delete/<int:pk>/', views.QuoteDelete.as_view(), name='quote-delete'),
    path('quote/<int:pk>/toggle-complete/', views.toggle_complete, name='quote-toggle-complete'),
]

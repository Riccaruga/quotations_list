from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Quote
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('quotes')

class QuoteList(LoginRequiredMixin, ListView):
    model = Quote
    context_object_name = 'quotes'
    
class QuoteDetail(LoginRequiredMixin, DetailView):
    model = Quote
    context_object_name = 'quote'
    template_name = 'base/quote.html'

@require_POST
def toggle_complete(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    quote.completed = not quote.completed
    quote.save()
    messages.success(request, f'Quote #{quote.id} marked as {"completed" if quote.completed else "pending"}')
    return redirect('quotes')

class QuoteCreate(LoginRequiredMixin, CreateView):
    model = Quote
    fields = '__all__'
    success_url = reverse_lazy('quotes')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class QuoteUpdate(LoginRequiredMixin, UpdateView):
    model = Quote
    fields = '__all__'
    success_url = reverse_lazy('quotes')

class QuoteDelete(LoginRequiredMixin, DeleteView):
    model = Quote
    success_url = reverse_lazy('quotes')

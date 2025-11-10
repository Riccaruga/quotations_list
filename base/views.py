from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Quote
from .forms import QuoteForm
from django.urls import reverse_lazy
from django.conf import settings
import os

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
    template_name = 'base/quote_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status', 'all')
        
        if status == 'pending':
            return queryset.filter(completed=False).order_by('-created_at')
        elif status == 'completed':
            return queryset.filter(completed=True).order_by('-created_at')
        else:
            return queryset.order_by('-created_at')
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'all')
        return context
    
class QuoteDetail(LoginRequiredMixin, DetailView):
    model = Quote
    context_object_name = 'quote'
    template_name = 'base/quote.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_attachment'] = bool(self.object.attachment)
        return context

@require_POST
def toggle_complete(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    quote.completed = not quote.completed
    quote.save()
    messages.success(request, f'Quote #{quote.id} marked as {"completed" if quote.completed else "pending"}')
    return redirect('quotes')

class QuoteCreate(LoginRequiredMixin, CreateView):
    model = Quote
    form_class = QuoteForm
    template_name = 'base/quote_form.html'
    success_url = reverse_lazy('quotes')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)
        if 'attachment' in self.request.FILES:
            self.object.attachment = self.request.FILES['attachment']
        self.object.save()
        return super().form_valid(form)
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'data': self.request.POST or None,
            'files': self.request.FILES or None,
        })
        return kwargs

class QuoteUpdate(LoginRequiredMixin, UpdateView):
    model = Quote
    form_class = QuoteForm
    template_name = 'base/quote_form.html'
    success_url = reverse_lazy('quotes')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'data': self.request.POST or None,
            'files': self.request.FILES or None,
        })
        return kwargs
        
    def form_valid(self, form):
        # Save the form with the uploaded file
        self.object = form.save(commit=False)
        if 'attachment-clear' in self.request.POST:
            # If the clear checkbox is checked, delete the file
            self.object.attachment.delete(save=False)
        elif 'attachment' in self.request.FILES:
            # If a new file is uploaded, save it
            self.object.attachment = self.request.FILES['attachment']
        self.object.save()
        return super().form_valid(form)

class QuoteDelete(LoginRequiredMixin, DeleteView):
    model = Quote
    success_url = reverse_lazy('quotes')

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Quote, LaserCuttingSpec, PressBrakeSpec, TubeLaserSpec # <-- ADD SPEC MODELS
from .forms import QuoteForm, LaserCuttingForm, PressBrakeForm, TubeLaserForm # <-- ADD SPEC FORMS
from django.urls import reverse_lazy
from django.conf import settings
import os

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction, models

# --- Utility Mapping ---
SPEC_FORM_MAP = {
    'laser_cutting': {'model': LaserCuttingSpec, 'form': LaserCuttingForm},
    'press_brake': {'model': PressBrakeSpec, 'form': PressBrakeForm},
    'tube_laser': {'model': TubeLaserSpec, 'form': TubeLaserForm},
}

# --- Authentication Views ---

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('quotes')

# --- List View ---

class QuoteList(LoginRequiredMixin, ListView):
    model = Quote
    context_object_name = 'quotes'
    template_name = 'base/quote_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status', 'all')
        search_query = self.request.GET.get('search', '').strip()
        
        # Apply status filter
        if status == 'pending':
            queryset = queryset.filter(completed=False)
        elif status == 'completed':
            queryset = queryset.filter(completed=True)
            
        # Apply search filter if search query exists
        if search_query:
            queryset = queryset.filter(
                models.Q(manager__icontains=search_query) | 
                models.Q(client__icontains=search_query)
            )
            
        return queryset.order_by('-created_at')
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'all')
        context['search_query'] = self.request.GET.get('search', '')
        return context

# --- Detail View (Already fixed) ---

class QuoteDetail(LoginRequiredMixin, DetailView):
    model = Quote
    context_object_name = 'quote'
    template_name = 'base/quote.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quote = self.get_object()
        spec = None
        spec_fields_to_display = []

        # Determine which specification object to fetch
        spec_info = SPEC_FORM_MAP.get(quote.machine_type)
        if spec_info:
            spec_model = spec_info['model']
            try:
                # Dynamically access the related object manager (e.g., quote.lasercuttingspec)
                spec = getattr(quote, spec_model.__name__.lower(), None)
            except spec_model.DoesNotExist:
                spec = None

            if spec:
                # Extract fields manually for display, filtering out 'id' and 'quote'
                for field in spec._meta.fields:
                    if field.name not in ['id', 'quote']:
                        spec_fields_to_display.append(field)

        context['spec'] = spec
        context['spec_fields'] = spec_fields_to_display
        return context

# --- Create View (Refactored for two-form handling) ---

class QuoteCreate(LoginRequiredMixin, CreateView):
    model = Quote
    form_class = QuoteForm
    template_name = 'base/quote_form.html'
    success_url = reverse_lazy('quotes')

    def get_context_data(self, **kwargs):
        # Don't call parent's get_context_data to avoid the object attribute issue
        context = {}
        context['form'] = self.get_form()
        # Pass all unbound spec forms to the template for initial rendering
        context['lc_form'] = LaserCuttingForm()
        context['pb_form'] = PressBrakeForm()
        context['tl_form'] = TubeLaserForm()
        return context

    def post(self, request, *args, **kwargs):
        main_form = self.get_form()
        
        # Get the selected machine type from the POST data
        machine_type = request.POST.get('machine_type')
        
        SpecFormClass = SPEC_FORM_MAP.get(machine_type, {}).get('form')
        
        if SpecFormClass:
            # Instantiate the correct spec form with POST data
            spec_form = SpecFormClass(request.POST)
        else:
            # Fallback for an invalid machine type selection
            spec_form = None
            
        # Check both forms' validity
        if main_form.is_valid() and (spec_form is None or spec_form.is_valid()):
            return self.forms_valid(main_form, spec_form)
        else:
            return self.forms_invalid(main_form, spec_form)

    def forms_valid(self, main_form, spec_form):
        with transaction.atomic():
            # 1. Save main Quote object
            main_form.instance.user = self.request.user
            quote_object = main_form.save(commit=False)
            
            # Handle attachment save logic (copied from your old Update/Create)
            if 'attachment' in self.request.FILES:
                quote_object.attachment = self.request.FILES['attachment']
            quote_object.save()
            
            # 2. Save Spec object
            if spec_form:
                spec_instance = spec_form.save(commit=False)
                spec_instance.quote = quote_object  # Link spec to the saved quote
                spec_instance.save()

        return redirect(self.success_url)

    def forms_invalid(self, main_form, spec_form):
        context = self.get_context_data()
        context['form'] = main_form
        # Pass the bound/invalid spec forms back to the context
        context['lc_form'] = LaserCuttingForm(self.request.POST if main_form.data.get('machine_type') == 'laser_cutting' else None)
        context['pb_form'] = PressBrakeForm(self.request.POST if main_form.data.get('machine_type') == 'press_brake' else None)
        context['tl_form'] = TubeLaserForm(self.request.POST if main_form.data.get('machine_type') == 'tube_laser' else None)
        return self.render_to_response(context)

# --- Update View (Refactored for two-form handling) ---

class QuoteUpdate(LoginRequiredMixin, UpdateView):
    model = Quote
    form_class = QuoteForm
    template_name = 'base/quote_form.html'
    success_url = reverse_lazy('quotes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quote = self.get_object()
        
        # Determine the current spec form/model
        spec_info = SPEC_FORM_MAP.get(quote.machine_type)
        if spec_info:
            SpecModel = spec_info['model']
            SpecForm = spec_info['form']
            
            try:
                # Get the existing spec instance
                spec_instance = getattr(quote, SpecModel.__name__.lower())
            except SpecModel.DoesNotExist:
                spec_instance = None
            
            # Pass the currently active, bound form as 'spec_form'
            spec_form = SpecForm(instance=spec_instance)
            
            # Pass all spec forms, but only the current one is bound to an instance
            context['lc_form'] = SpecForm(instance=spec_instance) if quote.machine_type == 'laser_cutting' else LaserCuttingForm()
            context['pb_form'] = SpecForm(instance=spec_instance) if quote.machine_type == 'press_brake' else PressBrakeForm()
            context['tl_form'] = SpecForm(instance=spec_instance) if quote.machine_type == 'tube_laser' else TubeLaserForm()
        else:
            # Fallback for quotes with no machine_type or an invalid one
            context['lc_form'] = LaserCuttingForm()
            context['pb_form'] = PressBrakeForm()
            context['tl_form'] = TubeLaserForm()

        return context

class QuoteDelete(LoginRequiredMixin, DeleteView):
    model = Quote
    context_object_name = 'quote'
    template_name = 'base/delete_confirm.html'
    success_url = reverse_lazy('quotes')

# --- Other Functionality ---

@require_POST
def toggle_complete(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    # The checkbox value will be 'on' if checked, or absent if unchecked.
    is_completed = 'completed' in request.POST
    quote.completed = is_completed
    quote.save()
    messages.success(request, f"Quote '{quote.title}' status updated.")
    return redirect('quotes')
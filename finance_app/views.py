from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from .models import CashFlow, Status, Type, Category, SubCategory
from .forms import CashFlowForm, DirectoryForm
import logging

# Set up logging
logger = logging.getLogger(__name__)

def index(request):
    """Display and filter cash flow records."""
    cashflows = CashFlow.objects.all()
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    # Apply filters based on GET parameters
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status = request.GET.get('status')
    type_ = request.GET.get('type')
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')

    if date_from:
        cashflows = cashflows.filter(date__gte=date_from)
    if date_to:
        cashflows = cashflows.filter(date__lte=date_to)
    if status:
        cashflows = cashflows.filter(status_id=status)
    if type_:
        cashflows = cashflows.filter(type_id=type_)
    if category:
        cashflows = cashflows.filter(category_id=category)
    if subcategory:
        cashflows = cashflows.filter(subcategory_id=subcategory)

    return render(request, 'index.html', {
        'cashflows': cashflows,
        'statuses': statuses,
        'types': types,
        'categories': categories,
        'subcategories': subcategories,
    })

def cashflow_create(request):
    """Create a new cash flow record."""
    if request.method == 'POST':
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CashFlowForm()
    return render(request, 'cashflow_form.html', {'form': form})

def cashflow_edit(request, pk):
    """Edit an existing cash flow record."""
    cashflow = get_object_or_404(CashFlow, pk=pk)
    if request.method == 'POST':
        form = CashFlowForm(request.POST, instance=cashflow)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CashFlowForm(instance=cashflow)
    return render(request, 'cashflow_form.html', {'form': form})

def cashflow_delete(request, pk):
    """Delete a cash flow record."""
    cashflow = get_object_or_404(CashFlow, pk=pk)
    if request.method == 'POST':
        cashflow.delete()
        return redirect('index')
    return render(request, 'cashflow_delete.html', {'cashflow': cashflow})

def directory(request):
    """Manage directory entries (statuses, types, categories, subcategories)."""
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        logger.debug(f"POST data: {request.POST}")
        if form.is_valid():
            name = form.cleaned_data['name']
            type_ = form.cleaned_data.get('type')
            category = form.cleaned_data.get('category')

            try:
                if 'add_status' in request.POST:
                    Status.objects.create(name=name)
                    messages.success(request, f"Status '{name}' added successfully.")
                elif 'add_type' in request.POST:
                    Type.objects.create(name=name)
                    messages.success(request, f"Type '{name}' added successfully.")
                elif 'add_category' in request.POST and type_:
                    Category.objects.create(name=name, type=type_)
                    messages.success(request, f"Category '{name}' added successfully.")
                elif 'add_subcategory' in request.POST and category:
                    SubCategory.objects.create(name=name, category=category)
                    messages.success(request, f"Subcategory '{name}' added successfully.")
                else:
                    messages.error(request, "Invalid action: Please select an action (add status, type, category, or subcategory).")
                return redirect('directory')
            except Exception as e:
                logger.error(f"Error saving directory entry: {str(e)}")
                messages.error(request, f"Error adding entry: {str(e)}")
        else:
            logger.error(f"Form validation failed: {form.errors}")
            messages.error(request, f"Form validation failed: {form.errors.as_text()}")
    else:
        form = DirectoryForm()

    return render(request, 'directory.html', {
        'form': form,
        'statuses': statuses,
        'types': types,
        'categories': categories,
        'subcategories': subcategories,
    })

def get_categories(request):
    """Return categories for a given type (AJAX)."""
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

def get_subcategories(request):
    """Return subcategories for a given category (AJAX)."""
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def status_edit(request, pk):
    """Edit a status."""
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        if form.is_valid():
            status.name = form.cleaned_data['name']
            try:
                status.save()
                messages.success(request, f"Status '{status.name}' updated successfully.")
                return redirect('directory')
            except Exception as e:
                messages.error(request, f"Error updating status: {str(e)}")
        else:
            messages.error(request, f"Form validation failed: {form.errors.as_text()}")
    else:
        form = DirectoryForm(initial={'name': status.name})
    return render(request, 'directory_edit.html', {'form': form, 'entity': status, 'entity_type': 'Status'})

def type_edit(request, pk):
    """Edit a type."""
    type_ = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        if form.is_valid():
            type_.name = form.cleaned_data['name']
            try:
                type_.save()
                messages.success(request, f"Type '{type_.name}' updated successfully.")
                return redirect('directory')
            except Exception as e:
                messages.error(request, f"Error updating type: {str(e)}")
        else:
            messages.error(request, f"Form validation failed: {form.errors.as_text()}")
    else:
        form = DirectoryForm(initial={'name': type_.name})
    return render(request, 'directory_edit.html', {'form': form, 'entity': type_, 'entity_type': 'Type'})

def category_edit(request, pk):
    """Edit a category."""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        if form.is_valid():
            category.name = form.cleaned_data['name']
            type_ = form.cleaned_data['type']
            if type_:
                category.type = type_
            try:
                category.save()
                messages.success(request, f"Category '{category.name}' updated successfully.")
                return redirect('directory')
            except Exception as e:
                messages.error(request, f"Error updating category: {str(e)}")
        else:
            messages.error(request, f"Form validation failed: {form.errors.as_text()}")
    else:
        form = DirectoryForm(initial={'name': category.name, 'type': category.type})
    return render(request, 'directory_edit.html', {'form': form, 'entity': category, 'entity_type': 'Category'})

def subcategory_edit(request, pk):
    """Edit a subcategory."""
    subcategory = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        if form.is_valid():
            subcategory.name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            if category:
                subcategory.category = category
            try:
                subcategory.save()
                messages.success(request, f"Subcategory '{subcategory.name}' updated successfully.")
                return redirect('directory')
            except Exception as e:
                messages.error(request, f"Error updating subcategory: {str(e)}")
        else:
            messages.error(request, f"Form validation failed: {form.errors.as_text()}")
    else:
        form = DirectoryForm(initial={'name': subcategory.name, 'category': subcategory.category})
    return render(request, 'directory_edit.html', {'form': form, 'entity': subcategory, 'entity_type': 'Subcategory'})

def status_delete(request, pk):
    """Delete a status with dependency check."""
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        if CashFlow.objects.filter(status=status).exists():
            messages.error(request, "Cannot delete status: it is used in cash flow records.")
        else:
            status.delete()
            messages.success(request, f"Status '{status.name}' deleted successfully.")
        return redirect('directory')
    return render(request, 'directory_delete.html', {'entity': status, 'entity_type': 'Status'})

def type_delete(request, pk):
    """Delete a type with dependency check."""
    type_ = get_object_or_404(Type, pk=pk)
    if request.method == 'POST':
        if Category.objects.filter(type=type_).exists():
            messages.error(request, "Cannot delete type: it has associated categories.")
        else:
            type_.delete()
            messages.success(request, f"Type '{type_.name}' deleted successfully.")
        return redirect('directory')
    return render(request, 'directory_delete.html', {'entity': type_, 'entity_type': 'Type'})

def category_delete(request, pk):
    """Delete a category with dependency check."""
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        if SubCategory.objects.filter(category=category).exists():
            messages.error(request, "Cannot delete category: it has associated subcategories.")
        else:
            category.delete()
            messages.success(request, f"Category '{category.name}' deleted successfully.")
        return redirect('directory')
    return render(request, 'directory_delete.html', {'entity': category, 'entity_type': 'Category'})

def subcategory_delete(request, pk):
    """Delete a subcategory with dependency check."""
    subcategory = get_object_or_404(SubCategory, pk=pk)
    if request.method == 'POST':
        if CashFlow.objects.filter(subcategory=subcategory).exists():
            messages.error(request, "Cannot delete subcategory: it is used in cash flow records.")
        else:
            subcategory.delete()
            messages.success(request, f"Subcategory '{subcategory.name}' deleted successfully.")
        return redirect('directory')
    return render(request, 'directory_delete.html', {'entity': subcategory, 'entity_type': 'Subcategory'})
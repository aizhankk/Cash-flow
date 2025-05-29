from django import forms
from .models import CashFlow, Status, Type, Category, SubCategory

class CashFlowForm(forms.ModelForm):
    """Form for creating and editing cash flow records."""
    class Meta:
        model = CashFlow
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize category and subcategory fields as empty
        self.fields['category'].queryset = Category.objects.none()
        self.fields['subcategory'].queryset = SubCategory.objects.none()

        # Populate categories based on selected type
        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['category'].queryset = self.instance.type.categories.all()

        # Populate subcategories based on selected category
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.all()

class DirectoryForm(forms.Form):
    """Form for managing directory entries (statuses, types, categories, subcategories)."""
    name = forms.CharField(max_length=100, label="Name", required=True, strip=True)
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=False, label="Type (for Category)")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label="Category (for Subcategory)")

    def clean_name(self):
        """Validate the name field to ensure it's not empty and check for uniqueness."""
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError("Name cannot be empty.")
        return name

    def clean(self):
        """Validate dependencies based on action."""
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        type_ = cleaned_data.get('type')
        category = cleaned_data.get('category')

        # Check uniqueness for Status
        if 'add_status' in self.data and Status.objects.filter(name=name).exists():
            raise forms.ValidationError(f"Status '{name}' already exists.")
        # Check uniqueness for Type
        if 'add_type' in self.data and Type.objects.filter(name=name).exists():
            raise forms.ValidationError(f"Type '{name}' already exists.")
        # Check uniqueness for Category within Type
        if 'add_category' in self.data and type_ and Category.objects.filter(name=name, type=type_).exists():
            raise forms.ValidationError(f"Category '{name}' already exists for this type.")
        # Check uniqueness for Subcategory within Category
        if 'add_subcategory' in self.data and category and SubCategory.objects.filter(name=name, category=category).exists():
            raise forms.ValidationError(f"Subcategory '{name}' already exists for this category.")
        return cleaned_data
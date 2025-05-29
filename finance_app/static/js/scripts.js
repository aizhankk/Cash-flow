document.addEventListener('DOMContentLoaded', function() {
    const typeSelect = document.querySelector('#id_type');
    const categorySelect = document.querySelector('#id_category');
    const subcategorySelect = document.querySelector('#id_subcategory');

    if (typeSelect && categorySelect) {
        typeSelect.addEventListener('change', function() {
            const typeId = this.value;
            categorySelect.innerHTML = '<option value="">Select Category</option>';
            subcategorySelect.innerHTML = '<option value="">Select Subcategory</option>';

            if (typeId) {
                fetch(`/get_categories/?type_id=${typeId}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(category => {
                            const option = document.createElement('option');
                            option.value = category.id;
                            option.textContent = category.name;
                            categorySelect.appendChild(option);
                        });
                    });
            }
        });
    }

    if (categorySelect && subcategorySelect) {
        categorySelect.addEventListener('change', function() {
            const categoryId = this.value;
            subcategorySelect.innerHTML = '<option value="">Select Subcategory</option>';

            if (categoryId) {
                fetch(`/get_subcategories/?category_id=${categoryId}`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(subcategory => {
                            const option = document.createElement('option');
                            option.value = subcategory.id;
                            option.textContent = subcategory.name;
                            subcategorySelect.appendChild(option);
                        });
                    });
            }
        });
    }
});
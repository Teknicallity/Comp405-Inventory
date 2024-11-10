function toggleEdit() {
    const form = document.getElementById('itemForm');
    const inputs = form.querySelectorAll('input');
    const editButton = document.getElementById('editButton');
    const csrfToken = document.getElementById('csrf_token').value;
    const itemNameHeader = document.getElementById('itemName');
    const itemNameInput = document.getElementById('name');

    if (editButton.textContent === 'Edit') {
        // Enable inputs for editing
        inputs.forEach(input => {
            if (input.id !== 'item_id') input.disabled = false;
        });
        editButton.textContent = 'Save';
    } else {
        // Gather form data and send a PUT request
        const itemData = {};
        inputs.forEach(input => itemData[input.name] = input.value);
        const itemId = document.getElementById('item_id').value;
        console.log(itemData)
        fetch(`/api/items/${itemId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(itemData)
        })
            .then(response => {
                if (response.ok) {
                    // Disable inputs after saving
                    inputs.forEach(input => input.disabled = true);
                    editButton.textContent = 'Edit';
                    itemNameHeader.innerHTML = itemNameInput.value
                    flashResponseText('Item updated successfully.', 'darkgreen').then();
                } else {
                    flashResponseText('Failed to update item.', 'red').then();
                }
            })
            .catch(error => {
                console.error('Error updating item:', error);
                flashResponseText('An error occurred.', 'red').then();
            });
    }
}

async function flashResponseText(text, color) {
    const responseText = document.getElementById('responseText');
    responseText.style.color = color;
    responseText.innerHTML = text;
    setTimeout(() => {
        responseText.style.color = color;
        responseText.innerHTML = '';
    }, 1500)
}
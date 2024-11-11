function toggleEdit(url) {
    const form = document.getElementById('objectForm');
    const inputs = form.querySelectorAll('input');
    const editButton = document.getElementById('editButton');
    const cancelButton = document.getElementById('cancelButton');
    const csrfToken = document.getElementById('csrf_token').value;
    const objectNameHeader = document.getElementById('objectName');
    const objectNameInput = document.getElementById('name');
    const objectIdElement = document.getElementById('objectId');
    const objectIdType = objectIdElement.getAttribute('name');

    if (editButton.textContent.trim() === 'Edit') {
        // Enable inputs for editing
        inputs.forEach(input => {
            if (input.id !== 'objectId') input.disabled = false;
        });
        editButton.textContent = 'Save';
        cancelButton.style.display = 'inline';
    } else {
        // Gather form data and send a PUT request
        const formData = {};
        inputs.forEach(input => {
            if (input.type === 'checkbox') {
                formData[input.name] = input.checked;
            } else { // currently text and hidden
                formData[input.name] = input.value
            }
        });

        const method = (editButton.textContent === 'Save') ? 'PUT' : 'POST';
        console.log(formData)
        fetch(`${url}`, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(formData)
        })
            .then(response => {
                if (response.ok) {
                    if (method === 'PUT') {
                        // Update object
                        inputs.forEach(input => input.disabled = true);
                        editButton.textContent = 'Edit';
                        cancelButton.style.display = 'none';
                        objectNameHeader.innerHTML = objectNameInput.value;

                        response.json().then(data => {
                            inputs.forEach(input => {
                                if (input.name in data) {
                                    input.value = data[input.name];
                                }
                            });
                            flashResponseText('Updated successfully.', 'darkgreen').then();
                        });
                    } else {
                        // Create object
                        inputs.forEach(input => input.value = '');
                        flashResponseText('Created successfully.', 'darkgreen').then();
                    }


                } else if (response.status === 401) {
                    flashResponseText('Unauthorized', 'red').then();
                } else {
                    flashResponseText('Failed to update.', 'red').then();
                }
            })
            .catch(error => {
                console.error('Error updating:', error);
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

function cancelEdit(getObjectFromIdUrl) {
    const form = document.getElementById('objectForm');
    const inputs = form.querySelectorAll('input');
    const editButton = document.getElementById('editButton');
    const cancelButton = document.getElementById('cancelButton');

    inputs.forEach(input => input.disabled = true);

    editButton.textContent = 'Edit';
    cancelButton.style.display = 'none';

    fetch(`${getObjectFromIdUrl}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch original data');
            }
            return response.json();
        })
        .then(data => {
            inputs.forEach(input => {
                if (data.hasOwnProperty(input.name)) {
                    if (input.type === 'checkbox') {
                        input.checked = data[input.name];
                    } else {
                        input.value = data[input.name];
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching original data:', error);
            flashResponseText('Failed to reset changes.', 'red').then();
        });
}

function deleteObject(deleteUrl) {
    const csrfToken = document.getElementById('csrf_token').value
    const deleteButton = document.getElementById('deleteButton');
    const cancelDeleteButton = document.getElementById('cancelDeleteButton');

    if (deleteButton.textContent.trim() !== 'Confirm') {
        deleteButton.textContent = 'Confirm'
        cancelDeleteButton.style.display = 'inline';
    } else {
        fetch(`${deleteUrl}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        }).then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else if (response.status === 404) {
                flashResponseText('Item not found.', 'red').then();
            } else if (response.status === 403 || response.status === 401) {
                flashResponseText('You are not authorized to delete this item.', 'red').then();
            } else {
                flashResponseText('Failed to delete the item.', 'red').then();
            }
        }).catch(error => {
            console.error('Error during deletion:', error);
            flashResponseText('An error occurred while deleting.', 'red').then();
        });
    }
}

function cancelDelete() {
    const deleteButton = document.getElementById('deleteButton');
    const cancelDeleteButton = document.getElementById('cancelDeleteButton');

    deleteButton.textContent = 'Delete'
    cancelDeleteButton.style.display = 'none';
}

function returnCheckout(returnUrl) {
    const csrfToken = document.getElementById('csrf_token').value
    const returnButton = document.getElementById('returnButton')

    fetch(returnUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else if (response.status === 404) {
            flashResponseText('Item not found.', 'red').then();
        } else if (response.status === 403 || response.status === 401) {
            flashResponseText('You are not authorized to return this item.', 'red').then();
        } else {
            flashResponseText('Failed to return the item.', 'red').then();
        }
    })
}
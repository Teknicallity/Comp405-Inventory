function toggleEdit(url) {
    const form = document.getElementById('objectForm');
    const inputs = form.querySelectorAll('input');
    const editButton = document.getElementById('editButton');
    const csrfToken = document.getElementById('csrf_token').value;
    const objectNameHeader = document.getElementById('objectName');
    const objectNameInput = document.getElementById('name');
    const objectIdElement = document.getElementById('objectId');
    const objectIdType = objectIdElement.getAttribute('name');
    console.log('toggle')
    if (editButton.textContent.trim() === 'Edit') {
        // Enable inputs for editing
        inputs.forEach(input => {
            if (input.id !== 'objectId') input.disabled = false;
        });
        editButton.textContent = 'Save';
        console.log('editButton');
    } else {
        console.log('saving')
        // Gather form data and send a PUT request
        const formData = {};
        inputs.forEach(input => formData[input.name] = input.value);

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
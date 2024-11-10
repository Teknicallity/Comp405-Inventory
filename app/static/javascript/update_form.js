function toggleEdit(url) {
    const form = document.getElementById('objectForm');
    const inputs = form.querySelectorAll('input');
    const editButton = document.getElementById('editButton');
    const csrfToken = document.getElementById('csrf_token').value;
    const objectNameHeader = document.getElementById('objectName');
    const objectNameInput = document.getElementById('name');
    console.log('toggle')
    if (editButton.textContent === 'Edit') {
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

        console.log(formData)
        fetch(`${url}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(formData)
        })
            .then(response => {
                if (response.ok) {
                    // Disable inputs after saving
                    inputs.forEach(input => input.disabled = true);
                    editButton.textContent = 'Edit';
                    objectNameHeader.innerHTML = objectNameInput.value
                    flashResponseText('Updated successfully.', 'darkgreen').then();
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
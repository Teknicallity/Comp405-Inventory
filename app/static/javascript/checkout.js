
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
            console.log(response)
            // window.location.href = response.url;
        } else if (response.status === 404) {
            flashResponseText('Item not found.', 'red').then();
        } else if (response.status === 403 || response.status === 401) {
            flashResponseText('You are not authorized to return this item.', 'red').then();
        } else {
            flashResponseText('Failed to return the item.', 'red').then();
        }
    })
}
function returnCheckout(returnUrl, refreshUrl) {
    const csrfToken = document.getElementById('csrf_token').value
    const returnButton = document.getElementById('returnButton')

    let next = false;
    if (refreshUrl) {
        next = refreshUrl;
    }

    fetch(returnUrl, {
        method: 'POST',
        headers: {
            'next': next,
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

function checkout(url, item_id){
    const csrfToken = document.getElementById('csrf_token').value
    console.log(url, item_id);
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({'item_id': item_id})
    }).then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            flashResponseText('Something went wrong', 'red').then();
        }
    })
}
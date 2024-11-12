
async function flashResponseText(text, color) {
    const responseText = document.getElementById('responseText');
    responseText.style.color = color;
    responseText.innerHTML = text;
    setTimeout(() => {
        responseText.style.color = color;
        responseText.innerHTML = '';
    }, 1500)
}
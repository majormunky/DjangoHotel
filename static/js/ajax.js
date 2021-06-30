// Example POST method implementation:
async function postData(url, csrf, data) {
    let formData = new FormData();
    for (let k in data) {
        formData.append(k, data[k])
    }

    const response = await fetch(url, {
        method: 'POST',
        mode: 'same-origin',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            // 'Content-Type': 'application/json'
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrf,
        },
        redirect: 'follow',
        body: formData
    });
    return response.json(); // parses JSON response into native JavaScript objects
}

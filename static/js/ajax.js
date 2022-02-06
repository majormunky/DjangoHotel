// Example POST method implementation:
async function postData(url, csrf, data, options) {
    let formData = new FormData();
    for (let k in data) {
        formData.append(k, data[k])
    }

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: formData
    });

    if (options.returnType == "json") {
        return response.json();
    }

    return response;
}

async function getData(url) {
    const response = await fetch(url, {
        method: 'GET'
    });
    return response.json();
}

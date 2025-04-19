const getAuthHeader = (token) => {
    return new Headers(new Headers({
        'Authorization': "Bearer "+token,
        'Content-Type':'application/x-www-form-urlencoded'
    }))
}

export {getAuthHeader};

const getAuthHeader = (token) => {
    return new Headers(new Headers({
        'Authorization': "Bearer "+token,
    }))
}

export {getAuthHeader};

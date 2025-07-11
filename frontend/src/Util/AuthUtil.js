const getAuthHeader = (token) => {
    return new Headers(new Headers({
        'Authorization': "Bearer "+token,
    }))
}

const getBackendContext = () => {
    return "http://localhost:8000"
}

const getWebsocketContext = () => {
    return "ws://localhost:8000"
}

export {getAuthHeader, getBackendContext, getWebsocketContext};
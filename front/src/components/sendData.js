const getAxiosBody = (method, params) => {
    return {
        "jsonrpc": "2.0",
        "id": 0,
        "method": method,
        "params": {
            ...params
        }
    }
};



export default getAxiosBody;
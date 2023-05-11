const getAxiosBody = (method, params) => {
    if (!params){
        return {
        "id": 0,
        "jsonrpc": "2.0",
        "method": method,
        "params": {}
        }
    }
    return {
        "id": 0,
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            ...params
        }
    }
};



export default getAxiosBody;
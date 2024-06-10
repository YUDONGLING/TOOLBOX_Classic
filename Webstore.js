addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request));
})

async function handleRequest(request) {
    switch (request.method.toUpperCase()) {
        case 'POST':
            break;
        case 'OPTIONS':
            return new Response( null, { status: 200, headers: { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': '*', 'Access-Control-Allow-Headers': '*', 'Server' : 'edge-routine' }});
        default:
            return new Response( JSON.stringify({ 'ErrorCode': -1, 'ErrorMsg': '', 'Data': {} }), { status: 200, headers: { 'Content-Type': 'application/json', 'Server': 'edge-routine' }});
    }

    try {
        var data = await request.json();
        if (data === undefined) { throw new Error() }
    } catch (e) {
        try {
            var data = Object.fromEntries(( await request.formData() ).entries() );
            if (data === undefined) { throw new Error() }
        } catch (e) {
            return new Response( JSON.stringify({ 'ErrorCode': -1, 'ErrorMsg': '', 'Data': {} }), { status: 200, headers: { 'Content-Type': 'application/json', 'Server': 'edge-routine' }});
        }
    }

    try {
        var edgeKv = new EdgeKV({ namespace: data.namespace });
    } catch (e) {
        return new Response( JSON.stringify({ 'ErrorCode': -1, 'ErrorMsg': '', 'Data': {} }), { status: 200, headers: { 'Content-Type': 'application/json', 'Server': 'edge-routine' }});
    }

    switch (data.action.toUpperCase()) {
        case 'GET':
            var promiseList = [];
            for (let i = 0; i < data.key.length && i < 32; i++) {
                promiseList.push(
                    data.key[i].toString().length > 512                   ? { code: 400, value: ''    } :
                        edgeKv.get( data.key[i].toString(), { type: 'text' } )
                             .then( value => { return value !== undefined ? { code:   0, value: value } : { code: 404, value: '' } })
                            .catch( error => { return                       { code: 500, value: ''    } })
                )
            }
            for (let i = 32; i < data.key.length; i++) {
                promiseList.push( { code: 429, value: '' } )
            }
            var resultsList = {};
            await Promise.all(promiseList)
                .then( object => {
                    for (let i = 0; i < data.key.length; i++) {
                        resultsList[data.key[i].toString()] = object[i]
                    }
                }
            )
            return new Response( JSON.stringify({ 'ErrorCode': 0, 'ErrorMsg': '', 'Data': resultsList }), { status: 200, headers: { 'Content-Type': 'application/json', 'Server': 'edge-routine' }});
    
        case 'PUT':
            var promiseList = [];
            for (let i = 0; i < data.key.length && i < 16; i++) {
                promiseList.push(
                    data.key[i].toString().length > 512  ? { code: 400 } :
                        edgeKv.put( data.key[i].toString(), typeof data.value[i] === 'string' ? data.value[i] : typeof data.value[i] === 'number' ? data.value[i].toString() : JSON.stringify(data.value[i]) )
                             .then( value => { return      { code:   0 } })
                            .catch( error => { return      { code: 500 } })
                )
            }
            for (let i = 16; i < data.key.length; i++) {
                promiseList.push( { code: 429 } )
            }
            var resultsList = {};
            await Promise.all(promiseList)
                .then( object => {
                    for (let i = 0; i < data.key.length; i++) {
                        resultsList[data.key[i].toString()] = object[i]
                    }
                }
            )
            return new Response( JSON.stringify({ 'ErrorCode': 0, 'ErrorMsg': '', 'Data': resultsList }), { status: 200, headers: { 'Content-Type': 'application/json', 'Server': 'edge-routine' }});

        case 'DELETE': 
            var promiseList = [];
            for (let i = 0; i < data.key.length && i < 32; i++) {
                promiseList.push(
                    data.key[i].toString().length > 512     ? { code: 400 } :
                        edgeKv.delete( data.key[i].toString() )
                             .then( value => { return value ? { code:   0 } : { code: 404 } })
                            .catch( error => { return         { code: 500 } })
                )
            }
            for (let i = 32; i < data.key.length; i++) {
                promiseList.push( { code: 429 } )
            }
            var resultsList = {};
            await Promise.all(promiseList)
                .then( object => {
                    for (let i = 0; i < data.key.length; i++) {
                        resultsList[data.key[i].toString()] = object[i]
                    }
                }
            )
            return new Response( JSON.stringify({ 'ErrorCode': 0, 'ErrorMsg': '', 'Data': resultsList }), { status: 200, headers: { 'Content-Type': 'application/json', 'Server': 'edge-routine' }});

        default:
            return new Response( JSON.stringify({ 'ErrorCode': -1, 'ErrorMsg': '', 'Data': {} }), { status: 200, headers: { 'Content-Type': 'application/json', 'Server': 'edge-routine' }});
    }
}

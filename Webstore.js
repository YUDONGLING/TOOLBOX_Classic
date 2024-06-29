addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request));
})

function getValue(value) {
    if (value === undefined) {
        return { code: 404, value: '' }
    } else {
        exp    = value.split('|', 1)[0],
        exp_ts = parseInt(exp);
        return (exp_ts === -1 || exp_ts > Date.now() / 1000) ? { code: 0, value: value.slice(exp.length + 1) } : { code: 404, value: '' }
    }
}

function setValue(value, ttl, expire) {
    value  = typeof value  === 'string' ? value  : typeof value === 'number' ? value.toString() : JSON.stringify(value);
    ttl    = typeof ttl    === 'number' ? ttl    : undefined;
    expire = typeof expire === 'number' ? expire : undefined;

    if (expire > 0) {
        return `${expire}|${value}`
    } else {
        if (ttl > 0) {
            return `${Math.floor(Date.now() / 1000 + ttl)}|${value}`
        } else {
            return `${-1}|${value}`
        }
    }
}

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
            // Sample Request Body
            // {
            //     'action'   : 'GET',
            //     'namespace': 'sample-storage',
            //     'key'      : ['key1', 'key2', 'key3', ...]
            // }
            var promiseList = [];
            for (let i = 0; i < data.key.length && i < 32; i++) {
                promiseList.push(
                    data.key[i].toString().length > 512 ? { code: 400, value: '' } :
                        edgeKv.get( data.key[i].toString(), { type: 'text' } )
                             .then( value => { return        getValue( value )     })
                            .catch( error => { return     { code: 500, value: '' } })
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
            // Sample Request Body
            // {
            //     'action'   : 'PUT',
            //     'namespace': 'sample-storage',
            //     'key'      : [
            //         { key: 'key1', value: 'value' },
            //         { key: 'key2', value: 'value', ttl: 0 },
            //         { key: 'key3', value: 'value', expire: 1700000000 },
            //         ...
            //     ]
            // }
            var promiseList = [];
            for (let i = 0; i < data.key.length && i < 16; i++) {
                promiseList.push(
                    data.key[i].toString().length > 512  ? { code: 400 } :
                        edgeKv.put( data.key[i].key.toString(), setValue( data.key[i].value, data.key[i].ttl, data.key[i].expire ) )
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
                        resultsList[data.key[i].key.toString()] = object[i]
                    }
                }
            )
            return new Response( JSON.stringify({ 'ErrorCode': 0, 'ErrorMsg': '', 'Data': resultsList }), { status: 200, headers: { 'Content-Type': 'application/json', 'Server': 'edge-routine' }});

        case 'DELETE':
            // Sample Request Body
            // {
            //     'action'   : 'DELETE',
            //     'namespace': 'sample-storage',
            //     'key'      : ['key1', 'key2', 'key3', ...]
            // }
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

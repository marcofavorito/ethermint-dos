import sys
import requests as r
import json


def makeRequest(endpoint, msg, method, *params):
    print("*"*50)
    print(msg)
    print()
    req = toJsonRpc(method, *params)
    print("Request: \n%s"%req)
    res = r.post(endpoint, data=req).json()
    print("Response: \n%s" % res)
    return res

def toJsonRpc(method, *params):
    global JSON_ID
    jobj = {
        "jsonrpc":"2.0",
        "method":method,
        "params": params,
        "id": JSON_ID
    }
    JSON_ID+=1
    return json.dumps(jobj)

def setup(endpoint):
    global JSON_ID
    JSON_ID=0

    res_accounts = makeRequest(endpoint, "Get Accounts", "eth_accounts")
    addr_1 = res_accounts["result"][0]

    res_newAccount = makeRequest(endpoint, "Create new account:", "personal_newAccount", "1234")
    addr_2 = res_newAccount["result"]

    res_unlockAccount = makeRequest(endpoint, "Unlock account %s:" % addr_1, "personal_unlockAccount", addr_1, "1234", 10000)
    res = res_unlockAccount["result"]
    assert res

    with open("accounts.temp", "w") as f:
        f.write(";".join([addr_1, addr_2]))

    transaction = {'from': addr_1, 'to': addr_2, 'value': "0x1"}
    res_sendTransaction = makeRequest(endpoint, "Send dummy transaction: %s"%transaction, "eth_sendTransaction", transaction)

    print("*"*50)
    print("*" * 50)

if __name__ == '__main__':

    setup(sys.argv[1])

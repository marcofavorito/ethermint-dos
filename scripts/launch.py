import os
import sys

IP = "0.0.0.0"
LHIP = "127.0.0.1"
AA = "tcp://" + IP
LH = "tcp://" + LHIP
BASE_RPC_PORT = 46606
BASE_P2P_PORT = 46607
BASE_APP_PORT = 46608
BASE_RCP_PORT_ETH = 8505
BASE_WS_PORT_ETH = 8506
FLAGS = "--consensus.create_empty_blocks=false --log_level state:info,*:error"
# FLAGS = "--consensus.create_empty_blocks=false --log_level state:info,*:error"

TESTNET_FOLDER = "mytestnet"

ETHERMINT_FOLDER = ".ethermint"
ETHERMINT_FLAGS = "--rpc --rpcaddr=0.0.0.0 --ws --wsaddr=0.0.0.0 --rpcapi eth,net,web3,personal,admin --gasprice \"1\""

TENDERMINT_PATH="./bin/tendermint"
TENDERMINT_EVIL_PATH="./bin/tendermint_evil"


def new_tab(tab_name, delay, command):
    return "--tab --name '{tab_name}' -e 'bash -c \"echo Loading...; echo {command}; {command}; exec $SHELL\"'".format(
        **locals())


def tendermint_command(node_name, home, flags, address_flags):
    return TENDERMINT_PATH + " node --home {home} {flags} {address_flags}".format(**locals())


def tendermint_address_flags(rpc, p2p, seeds, proxy):
    return "--rpc.laddr {rpc} --p2p.laddr {p2p} --p2p.seeds {seeds} --proxy_app {proxy}".format(**locals())


def ethermint_init_command(home):
    return "ethermint --datadir {home} unsafe_reset_all && ethermint --datadir {home} init".format(**locals())


def ethermint_command(home, flags, address_flags):
    return "ethermint --datadir {home} {flags} {address_flags}".format(**locals())


def ethermint_address_flags(abci_addr, tendermint_addr, rpc_port, ws_port):
    return "--abci_laddr {abci_addr} --tendermint_addr {tendermint_addr} --rpcport {rpc_port} --wsport {ws_port}".format(
        **locals())


# def ethermint_init_command(home):
# 	return "init abci-cli"
#
# def ethermint_command(home, flags, address_flags):
# 	return "abci-cli counter {address_flags}".format(**locals())
#
# def ethermint_address_flags(abci_addr, tendermint_addr, rpc_port, ws_port):
# 	return "--addr {abci_addr}".format(**locals())


def main():
    N = int(sys.argv[1])


    RPC_PORTS = [BASE_RPC_PORT + i * 10 for i in range(N)]
    P2P_PORTS = [BASE_P2P_PORT + i * 10 for i in range(N)]
    APP_PORTS = [BASE_APP_PORT + i * 10 for i in range(N)]
    ETH_RCP_PORTS = [BASE_RCP_PORT_ETH + i * 10 for i in range(N)]
    ETH_WS_PORTS  = [BASE_WS_PORT_ETH + i * 10 for i in range(N)]
    SEEDS = ",".join([IP + ":" + str(p2pp) for p2pp in P2P_PORTS])

    TENDERMINT_TABS_COMMAND = " ".join([new_tab(
        "node_%d" % i,
        "Loading node %d..." % i,
        tendermint_command(
            "node_%i" % i,
            TESTNET_FOLDER + "/mach%d" % i,
            FLAGS,
            tendermint_address_flags(
                AA + ":" + str(RPC_PORTS[i]),
                AA + ":" + str(P2P_PORTS[i]),
                SEEDS,
                LH + ":" + str(APP_PORTS[i])
            )
        )) for i in range(N)]
    )

    ETHERMINT_TABS_COMMAND = " ".join([new_tab(
        "node_%d" % i,
        "Loading node %d..." % i,
        ethermint_init_command(ETHERMINT_FOLDER + "%d" % i) + ";" +
        ethermint_command(
            ETHERMINT_FOLDER + "%d" % i,
            ETHERMINT_FLAGS,
            ethermint_address_flags(
                AA + ":" + str(APP_PORTS[i]),
                LH + ":" + str(RPC_PORTS[i]),
                ETH_RCP_PORTS[i],
                ETH_WS_PORTS[i]
            )
        )) for i in range(N)]
    )
    print(TENDERMINT_TABS_COMMAND)
    print(ETHERMINT_TABS_COMMAND)

    os.system("rm -rf %s" % TESTNET_FOLDER)
    os.system("rm -rf %s*" % ETHERMINT_FOLDER)
    os.system(TENDERMINT_PATH + " testnet --dir %s --n %d" % (TESTNET_FOLDER, N))
    os.system("gnome-terminal " + TENDERMINT_TABS_COMMAND)
    os.system("gnome-terminal " + ETHERMINT_TABS_COMMAND)

    os.system("sleep 12")
    os.system("gnome-terminal -e 'bash -c \"./scripts/geth-script-loader.sh http://localhost:%s" % BASE_RCP_PORT_ETH + " ./scripts/geth-transactions.js; exec $SHELL\"'")

if __name__ == '__main__':
    main()

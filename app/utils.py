from app.constants import *

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

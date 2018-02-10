import os

from app.EthermintApp import EthermintApp
from app.TendermintNode import TendermintNode
from app.constants import *
from app.utils import *

def main(args):
    RPC_PORTS = [BASE_RPC_PORT + i * 10 for i in range(args.num_of_nodes)]
    P2P_PORTS = [BASE_P2P_PORT + i * 10 for i in range(args.num_of_nodes)]
    APP_PORTS = [BASE_APP_PORT + i * 10 for i in range(args.num_of_nodes)]
    ETH_RCP_PORTS = [BASE_RCP_PORT_ETH + i * 10 for i in range(args.num_of_nodes)]
    ETH_WS_PORTS = [BASE_WS_PORT_ETH + i * 10 for i in range(args.num_of_nodes)]
    SEEDS = ",".join([IP + ":" + str(p2pp) for p2pp in P2P_PORTS])
    tendermint_nodes = [TendermintNode(i,
                                       TCP_ALL_IPS + ":" + str(RPC_PORTS[i]),
                                       TCP_ALL_IPS + ":" + str(P2P_PORTS[i]),
                                       SEEDS,
                                       TCP_LOCALHOST + ":" + str(APP_PORTS[i]) if not args.dummy else "dummy",
                                       verbosity=args.verbosity,
                                       save_logs=args.save_logs,
                                       create_empty_blocks=args.create_empty_blocks,
                                       is_evil=True if i >= args.num_of_nodes - args.num_of_evils else False,
                                       path=TENDERMINT_PATH if i < args.num_of_nodes - args.num_of_evils else TENDERMINT_EVIL_PATH,
                                       )
                        for i in range(args.num_of_nodes)]


    print("*" * 100)
    print("Tendermint tabs:")
    TENDERMINT_TABS_COMMAND = " ".join([new_tab("node_%d" % i,
                                                tendermint_nodes[i].get_node_command())
                                        for i in range(args.num_of_nodes)])

    print("\n".join(TENDERMINT_TABS_COMMAND.split("--tab")))

    if not args.dummy:
        ethermint_apps = [EthermintApp(i,
                                       TCP_ALL_IPS + ":" + str(APP_PORTS[i]),
                                       TCP_LOCALHOST + ":" + str(RPC_PORTS[i]),
                                       ETH_RCP_PORTS[i],
                                       ETH_WS_PORTS[i],
                                       verbosity=args.verbosity,
                                       save_logs=args.save_logs,
                                       genesis_file_path=args.ethermint_genesis_path,
                                       other_flags=args.ethermint_flags
                                       )
                          for i in range(args.num_of_nodes)]

        ABCI_APP_TABS_COMMAND = " ".join([new_tab("node_%d" % i,
                                                  ethermint_apps[i].get_init_command() + ";" + ethermint_apps[
                                                      i].get_app_command())
                                          for i in range(args.num_of_nodes)])

        print("*" * 100)
        print("Ethermint tabs:")
        print("\n".join(ABCI_APP_TABS_COMMAND.split("--tab")))
        os.system("gnome-terminal " + ABCI_APP_TABS_COMMAND)

    os.system(TENDERMINT_PATH + " testnet --dir %s --n %d" % (TESTNET_FOLDER, args.num_of_nodes))
    os.system("gnome-terminal " + TENDERMINT_TABS_COMMAND)
import os
import sys

import argparse

from app.ABCIExampleApp import ABCIExampleApp
from app.EthermintApp import EthermintApp
from app.TendermintNode import TendermintNode
from app.constants import *
from app.utils import *

parser = argparse.ArgumentParser(description='Run a local private Tendermint/Ethermint network with some byzantine client.')
parser.add_argument('num_of_nodes', type=int, help='The number of nodes in the network')
parser.add_argument('num_of_evils', type=int, nargs='?', default=0, help='The number of evil nodes in the network (default: 0)')
parser.add_argument('--dummy', dest='dummy', action='store_const', const=True, default=False, help="Use the 'dummy' ABCI application")
parser.add_argument('--verbose', dest='verbose', action='store_const', const=True, default=False, help="enable the maximum log volume.")
parser.add_argument('--create_empty_blocks', dest='create_empty_blocks', action='store_const', const=True, default=False, help="Enable creation of empty blocks (works only for --dummy app).")
parser.add_argument('--save_logs', dest='save_logs', action='store_const', const=True, default=False, help="save logs in logs/. NOTICE: with this flag the program to remove old logs.")
parser.add_argument('--stress_test', type=int,  nargs='?', metavar='TX_NUM', default=0, dest='stress_test', help="After the network setup, send TX_NUM transactions to stress the network (default: TX_NUM=1)")

args = parser.parse_args()




def main():

    if args.num_of_nodes < args.num_of_evils:
        print("the number of evil nodes must be lower than the total number of nodes.")
        exit(-1)
    os.system("rm -rf %s" % TESTNET_FOLDER)
    os.system("rm -rf %s*" % ETHERMINT_FOLDER)
    os.system("rm -rf %s" % LOGS_FOLDER)
    if (args.save_logs):
        os.mkdir(LOGS_FOLDER)


    N = int(args.num_of_nodes)


    RPC_PORTS = [BASE_RPC_PORT + i * 10 for i in range(N)]
    P2P_PORTS = [BASE_P2P_PORT + i * 10 for i in range(N)]
    APP_PORTS = [BASE_APP_PORT + i * 10 for i in range(N)]
    ETH_RCP_PORTS = [BASE_RCP_PORT_ETH + i * 10 for i in range(N)]
    ETH_WS_PORTS  = [BASE_WS_PORT_ETH + i * 10 for i in range(N)]
    SEEDS = ",".join([IP + ":" + str(p2pp) for p2pp in P2P_PORTS])

    tendermint_nodes = [TendermintNode(i,
                                       TCP_ALL_IPS + ":" + str(RPC_PORTS[i]),
                                       TCP_ALL_IPS + ":" + str(P2P_PORTS[i]),
                                       SEEDS,
                                       TCP_LOCALHOST + ":" + str(APP_PORTS[i]) if not args.dummy else "dummy",
                                       verbose=args.verbose,
                                       save_logs=args.save_logs,
                                       is_evil=True if i>= N-args.num_of_evils else False
                                       )
                        for i in range(N)]

    TENDERMINT_TABS_COMMAND = " ".join([new_tab("node_%d" % i, "Loading node %d..." % i,
                                                tendermint_nodes[i].get_node_command())
                                        for i in range(N)])
    print(TENDERMINT_TABS_COMMAND)

    if not args.dummy:
        ethermint_apps = [EthermintApp(i,
                                   TCP_ALL_IPS + ":" + str(APP_PORTS[i]),
                                   TCP_LOCALHOST + ":" + str(RPC_PORTS[i]),
                                   ETH_RCP_PORTS[i],
                                   ETH_WS_PORTS[i],
                                   verbose=args.verbose,
                                   save_logs=args.save_logs
                                   )
                      for i in range(N)]

        ABCI_APP_TABS_COMMAND = " ".join([new_tab("node_%d" % i, "Loading node %d..." % i,
                                               ethermint_apps[i].get_init_command() + ";" + ethermint_apps[i].get_app_command())
                                       for i in range(N)])


        print(ABCI_APP_TABS_COMMAND)
        os.system("gnome-terminal " + ABCI_APP_TABS_COMMAND)

    os.system(TENDERMINT_PATH + " testnet --dir %s --n %d" % (TESTNET_FOLDER, N))
    os.system("gnome-terminal " + TENDERMINT_TABS_COMMAND)

    if args.stress_test > 0:
        os.system("echo 'Wait for the network setup'")
        os.system("sleep 12")
        os.system("echo 'Start sending transactions...'")
        os.system("gnome-terminal -e 'bash -c \"./scripts/geth-script-loader.sh " + '.ethermint0' + " " + "./scripts/geth-transactions.js " + str(args.stress_test) + "; exec $SHELL\"'")


if __name__ == '__main__':
    main()

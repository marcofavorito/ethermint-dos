import os
import sys

import argparse

from app.TendermintEvilVersion import TendermintEvilVersion
from app.constants import *

import app.gnome_terminal
import app.dockerized

parser = argparse.ArgumentParser(description='Run a local private Tendermint/Ethermint network with some byzantine client.')
parser.add_argument('num_of_nodes', type=int, help='The number of nodes in the network')
parser.add_argument('num_of_evils', type=int, nargs='?', default=0, help='The number of evil nodes in the network (default: 0)')
parser.add_argument('--no-docker', dest='dockerized', action='store_const', const=False, default=True, help="Do not use Docker but gnome-termninal")
parser.add_argument('--verbosity', type=int, dest='verbosity', nargs='?', metavar='LEVEL', default=0, choices=[0, 1, 2], help="Tune the log level [0=default. 1=info. 2=debug]")
parser.add_argument('--create_empty_blocks', dest='create_empty_blocks', action='store_const', const=True, default=False, help="Enable creation of empty blocks (works only for --dummy app).")
parser.add_argument('--dummy', action='store_const', const=True, default=False, help="Use the 'dummy' ABCI application")
parser.add_argument('--save-logs', dest='save_logs', action='store_const', const=True, default=False, help="save logs in logs/. NOTICE: with this flag the program to remove old logs.")
parser.add_argument('--ethermint_genesis_path', dest='ethermint_genesis_path', default="", help="Specify path folder where to find genesis.json file and keystore folder")
parser.add_argument('--ethermint_flags', dest='ethermint_flags', default="", help="generic Ethermint flags")
parser.add_argument('--tendermint_evil', dest='tendermint_evil', default=TendermintEvilVersion.shy.value, choices=[e.value for e in TendermintEvilVersion], help="Tendermint Evil version (default: 'shy')")
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

    if not args.dockerized:
        app.gnome_terminal.main(args)
    else:
        app.dockerized.main(args)



if __name__ == '__main__':
    main()

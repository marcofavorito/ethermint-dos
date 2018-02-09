import os

from app.EthermintApp import EthermintApp
from app.TendermintNode import TendermintNode
from app.utils import new_tab

DOCKER_NETWORK_NAME = "ethermint_dos_network"
DOCKER_FILE = "./docker/Dockerfile"

DOCKER_IMAGE_TENDERMINT = "marcofavorito/ethermint-dos"

DOCKER_NETWORK_ADDRESS_NET = "172.57"
DOCKER_NETWORK_TENDERMINT_NODES = "172.57.100"
DOCKER_NETWORK_ETHERMINT_NODES = "172.57.101"

DOCKER_ROOT_TESTNET_FOLDER =     "/root/mytestnet"
DOCKER_PATH_TENDERMINT =         "/bin/tendermint"
DOCKER_PATH_TENDERMINT_EVIL =    "/bin/tendermint_evil"
DOCKER_PATH_ETHERMINT =          "/bin/ethermint"

DOCKER_ETHERMINT_DATADIR= "/root/ethermint"

def docker_setup(N):
    os.system("docker network rm  %s" % DOCKER_NETWORK_NAME)
    os.system("docker network create --driver bridge --subnet %s.0.0/16 %s" % (DOCKER_NETWORK_ADDRESS_NET, DOCKER_NETWORK_NAME))
    os.system("docker build -t %s -f %s --build-arg NUM_NODES=%s  ." % (DOCKER_IMAGE_TENDERMINT, DOCKER_FILE, N))


def main(args):
    docker_setup(args.num_of_nodes)

    SEEDS = ["172.57.100.%s:46656" % (i + 100) for i in range(args.num_of_nodes)]
    TENDERMINT_TABS_COMMAND= ""

    # Generate Tendermint Nodes objects
    tendermint_nodes = [TendermintNode(i,
                                           p2p_seeds=",".join(SEEDS),
                                           proxy="dummy" if args.dummy else "tcp://%s.%s:46658" %(DOCKER_NETWORK_ETHERMINT_NODES, 100+i),
                                           verbosity=args.verbosity,
                                           save_logs=args.save_logs,
                                           create_empty_blocks=args.create_empty_blocks,
                                           is_evil=False if i < args.num_of_nodes - args.num_of_evils else True,
                                           testnet_folder=DOCKER_ROOT_TESTNET_FOLDER,
                                           path=DOCKER_PATH_TENDERMINT if i < args.num_of_nodes - args.num_of_evils else DOCKER_PATH_TENDERMINT_EVIL,
                                           )
                            for i in range(args.num_of_nodes)]


    for i, node in enumerate(tendermint_nodes):
        DOCKER_CMD = 'docker run  --net=%s  --ip="%s.%s" --name local_testnet_%s %s' % (DOCKER_NETWORK_NAME, DOCKER_NETWORK_TENDERMINT_NODES, 100+i, i, DOCKER_IMAGE_TENDERMINT)
        TENDERMINT_CMD = node.get_node_command()
        print(DOCKER_CMD + " " + TENDERMINT_CMD)
        # os.system(DOCKER_CMD + " " + TENDERMINT_CMD)
        TENDERMINT_TABS_COMMAND += new_tab("node_%d" % i, DOCKER_CMD + " " + TENDERMINT_CMD) + " "

    os.system("gnome-terminal " + TENDERMINT_TABS_COMMAND)



    # If not "Dummy" mode, generate Ethermint App objects
    if args.dummy:
        return

    ethermint_apps = [EthermintApp(i,
                                   tendermint_addr="tcp://%s.%s:46657" % (DOCKER_NETWORK_TENDERMINT_NODES, 100 + i),
                                   verbosity=args.verbosity,
                                   save_logs=args.save_logs,
                                   path=DOCKER_PATH_ETHERMINT,
                                   datadir=DOCKER_ETHERMINT_DATADIR,
                                   genesis_file_path=DOCKER_ETHERMINT_DATADIR+"/genesis.json"

                                   )
                      for i in range(args.num_of_nodes)]

    ABCI_APP_TABS_COMMAND = ""

    for i, node in enumerate(ethermint_apps):
        DOCKER_CMD = 'docker run  --net=%s  --ip="%s.%s" --name local_testnet_eth_%s %s' % (DOCKER_NETWORK_NAME, DOCKER_NETWORK_ETHERMINT_NODES, 100+i, i, DOCKER_IMAGE_TENDERMINT)
        ETHERMINT_CMD = node.get_app_command()
        print(DOCKER_CMD + " " + ETHERMINT_CMD)
        # os.system(DOCKER_CMD + " " + TENDERMINT_CMD)
        ABCI_APP_TABS_COMMAND += new_tab("node_%d" % i, DOCKER_CMD + " " + ETHERMINT_CMD) + " "

    os.system("gnome-terminal " + ABCI_APP_TABS_COMMAND)


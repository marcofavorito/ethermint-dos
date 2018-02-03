IP = "0.0.0.0"
LOCALHOST_IP = "127.0.0.1"
TCP_ALL_IPS = "tcp://" + IP
TCP_LOCALHOST = "tcp://" + LOCALHOST_IP
BASE_P2P_PORT = 46606
BASE_RPC_PORT = 46607
BASE_APP_PORT = 46608
BASE_RCP_PORT_ETH = 8505
BASE_WS_PORT_ETH = 8506


FLAGS = "--consensus.create_empty_blocks=false --log_level state:info,*:error"

TESTNET_FOLDER = "mytestnet"

ETHERMINT_FOLDER = ".ethermint"
ETHERMINT_FLAGS = "--rpc --rpcaddr=0.0.0.0 --ws --wsaddr=0.0.0.0"

TENDERMINT_PATH="./bin/tendermint"
TENDERMINT_EVIL_PATH="./bin/tendermint_evil"
ETHERMINT_PATH="./bin/ethermint"


LOGS_FOLDER="logs"
from app.constants import *

class TendermintNode(object):


    def __init__(self,
                 id,
                 rpc_laddr,
                 p2p_laddr,
                 p2p_seeds,
                 proxy,
                 create_empty_blocks=False,
                 path=TENDERMINT_PATH,
                 testnet_folder=TESTNET_FOLDER,
                 save_logs=False,
                 verbose=False,
                 is_evil=False
                 ):

        self.id = id
        self.rpc_laddr = rpc_laddr
        self.p2p_laddr = p2p_laddr
        self.p2p_seeds = p2p_seeds
        self.proxy = proxy
        self.create_empty_blocks = 'true' if create_empty_blocks else 'false'
        self.log_level = '*:debug' if verbose else 'state:info,*:error'
        self.path = path
        self.testnet_folder = testnet_folder
        self.save_logs=save_logs
        self.is_evil=is_evil

        self.home=TESTNET_FOLDER+ "/mach" + str(id)



    def get_node_command(self):
        return "%s" % (TENDERMINT_PATH if not self.is_evil else TENDERMINT_EVIL_PATH) + " node --home %s %s %s %s" % \
               (self.home, self.get_flags(), self.get_address_flags(), "2>&1 | tee %s/log-tendermint-node%s.log" % (LOGS_FOLDER, self.id) if self.save_logs else "")

    def get_flags(self):
        return "--consensus.create_empty_blocks={create_empty_blocks} --log_level \"{log_level}\"".format(**self.__dict__)

    def get_address_flags(self):
        return "--rpc.laddr {rpc_laddr} --p2p.laddr {p2p_laddr} --p2p.seeds {p2p_seeds} --proxy_app {proxy}".format(**self.__dict__)

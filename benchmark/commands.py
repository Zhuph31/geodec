from os.path import join

from benchmark.utils import PathMaker


class CommandMaker:

    @staticmethod
    def clean_node_config(i):
        return (f'rm -rf ./node{i}')

    @staticmethod
    def cleanup():
        return (
            f'rm -r .db-* ; rm .*.json ; mkdir -p {PathMaker.results_path()}'
        )

    @staticmethod
    def clean_logs():
        return f'rm -r {PathMaker.logs_path()} ; mkdir -p {PathMaker.logs_path()}'

    @staticmethod
    def compile():
        return 'cargo build --quiet --release --features benchmark'

    @staticmethod
    def generate_key(filename):
        assert isinstance(filename, str)
        return f'./node keys --filename {filename}'
    
    @staticmethod
    def initalizeDelayQDisc(interface):
        return (f'sudo tc qdisc add dev {interface} parent root handle 1:0 htb default 100')
    
    @staticmethod
    def deleteDelayQDisc(interface):
        return (f'sudo tc qdisc del dev {interface} parent root')

    @staticmethod
    def run_node(keys, committee, store, parameters, mechanism, debug=False):
        assert isinstance(keys, str)
        assert isinstance(committee, str)
        assert isinstance(parameters, str)
        assert isinstance(debug, bool)
        v = '-vvv' if debug else '-vv'
        if mechanism == 'hotstuff':
            return (f'./node {v} run --keys {keys} --committee {committee} '
                    f'--store {store} --parameters {parameters}')
        elif mechanism == 'cometbft':
            # incomplete
            return (f'~/cometbft/build/cometbft node --home ~/node i --p2p.persistent_peers="{persistent_peers}" '
                    f'--proxy_app=kvstore --consensus.create_empty_blocks=true')
    
    @staticmethod
    def run_primary(keys, committee, store, parameters, debug=False):
        assert isinstance(keys, str)
        assert isinstance(committee, str)
        assert isinstance(parameters, str)
        assert isinstance(debug, bool)
        v = '-vvv' if debug else '-vv'
        return (f'./node {v} run --keys {keys} --committee {committee} '
                f'--store {store} --parameters {parameters} primary')

    @staticmethod
    def run_worker(keys, committee, store, parameters, id, debug=False):
        assert isinstance(keys, str)
        assert isinstance(committee, str)
        assert isinstance(parameters, str)
        assert isinstance(debug, bool)
        v = '-vvv' if debug else '-vv'
        return (f'./node {v} run --keys {keys} --committee {committee} '
                f'--store {store} --parameters {parameters} worker --id {id}')

    @staticmethod
    def run_client(address, size, rate, mechanism, timeout=None, nodes=[]):
        assert isinstance(address, str)
        assert isinstance(size, int) and size > 0
        assert isinstance(rate, int) and rate >= 0
        assert isinstance(nodes, list)
        assert all(isinstance(x, str) for x in nodes)
        if mechanism == 'hotstuff':
            nodes = f'--nodes {" ".join(nodes)}' if nodes else ''
            return (f'./client {address} --size {size} '
                    f'--rate {rate} --timeout {timeout} {nodes}')
        elif mechanism == 'cometbft':
            return (f'~/cometbft/test/loadtime/build/load -c 1 --size {size} --rate {rate} --time {timeout}'
                    f' --endpoints ws://localhost:26657/websocket -v --broadcast-tx-method sync --expect-peers {len(nodes)} --min-peer-connectivity {len(nodes)}')
                    # f' --endpoints ws://localhost:26657/websocket -v --expect-peers {len(nodes)-1} --min-peer-connectivity {len(nodes)-1}')
        elif mechanism == 'bullshark':
            nodes = f'--nodes {" ".join(nodes)}' if nodes else ''
            return f'./benchmark_client {address} --size {size} --rate {rate} {nodes}'
    
    @staticmethod
    def kill():
        return 'tmux kill-server'

    @staticmethod
    def alias_binaries(origin, repo_name):
        assert isinstance(origin, str)
        if repo_name == 'narwhal':
            node, client = join(origin, 'node'), join(origin, 'benchmark_client')
            return f'rm node ; rm benchmark_client ; ln -s {node} . ; ln -s {client} .'
        else:
            node, client = join(origin, 'node'), join(origin, 'client')
            return f'rm node ; rm client ; ln -s {node} . ; ln -s {client} .'
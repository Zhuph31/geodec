from benchmark.commands import CommandMaker

class HotStuffMechanism:
    def __init__(self, settings):
        self.settings = settings
        self.name = 'hotstuff'
        print("Inside hotstuff")

        self.install_cmd = [
            'sudo apt-get update',
            'sudo apt-get -y upgrade',
            'sudo apt-get -y autoremove',

            # The following dependencies prevent the error: [error: linker `cc` not found].
            'sudo apt-get -y install build-essential',
            'sudo apt-get -y install cmake',

            # Install rust (non-interactive).
            'curl --proto "=https" --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y',
            'source $HOME/.cargo/env',
            'rustup default stable',

            # This is missing from the Rocksdb installer (needed for Rocksdb).
            'sudo apt-get install -y clang',

            # Clone the repo.
            f'(git clone {self.settings.repo_url} || (cd {self.settings.repo_name} ; git pull))'
        ]
        
        # check_repo_cmd = f'[ -d {self.settings.repo_name} ] || git clone {self.settings.repo_url}'
        
        self.update_cmd = [
            # Check if the repo directory exists
            f'[ -d {self.settings.repo_name} ] || git clone {self.settings.repo_url}',
            f'(cd {self.settings.repo_name} && git fetch -f)',
            f'(cd {self.settings.repo_name} && git checkout -f {self.settings.branch})',
            f'(cd {self.settings.repo_name} && git pull origin -f)',
            'source $HOME/.cargo/env',
            f'(cd {self.settings.repo_name}/node && {CommandMaker.compile()})',
            CommandMaker.alias_binaries(
                f'./{self.settings.repo_name}/target/release/', self.settings.repo_name
            )
        ]

    def install(self):
        print('Installing HotStuff ...')
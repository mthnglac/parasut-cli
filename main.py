import subprocess
import argparse

class PhoenixClient:

    def choose_yarn_version(self, version):
        subprocess.run(['/bin/zsh', '-i', '-c', 'yvm use {0}'.format(version)])

    def choose_node_version(self, version):
        subprocess.run(['/bin/zsh', '-i', '-c', 'nvm use {0}'.format(version)])

    def choose_ruby_version(self, version):
        subprocess.run(['/bin/zsh', '-i', '-c', 'rvm use {0}'.format(version)])

    def run_phoenix(self, yarn_version, node_version):
        self.choose_yarn_version(yarn_version)
        self.choose_node_version(node_version)
        subprocess.run(['/bin/zsh', '-i', '-c', 'PROJECT_TARGET=phoenix ember s'])

    def run_trinity(self, yarn_version, node_version):
        self.choose_yarn_version(yarn_version)
        self.choose_node_version(node_version)
        subprocess.run(['/bin/zsh', '-i', '-c', 'ember s --live-reload-port 6510'])

    def run_ui_library(self, yarn_version, node_version):
        self.choose_yarn_version(yarn_version)
        self.choose_node_version(node_version)
        subprocess.run(['/bin/zsh', '-i', '-c', 'PROJECT_TARGET=phoenix ember s --live-reload-port 6500'])

    def run_client(self, yarn_version, node_version):
        self.choose_yarn_version(yarn_version)
        self.choose_node_version(node_version)
        subprocess.run(['/bin/zsh', '-i', '-c', './node_modules/ember-cli/bin/ember s --live-reload-port 6505'])

    def run_server(self, ruby_version):
        self.choose_ruby_version(ruby_version)
        subprocess.run(['/bin/zsh', '-i', '-c', 'rails server'])

    def run_server_sidekiq(self, ruby_version):
        self.choose_ruby_version(ruby_version)
        subprocess.run(['/bin/zsh', '-i', '-c', 'bundle exec sidekiq'])

    def run_billing(self, ruby_version):
        self.choose_ruby_version(ruby_version)
        subprocess.run(['/bin/zsh', '-i', '-c', 'rails server -p 4002'])

    def run_billing_sidekiq(self, ruby_version):
        self.choose_ruby_version(ruby_version)
        subprocess.run(['/bin/zsh', '-i', '-c', 'bundle exec sidekiq'])


if __name__ == "__main__":
    # client = PhoenixClient()
    # client.run_phoenix('1.21.1', '8.16.0')
    # client.run_trinity('1.21.1', '8.16.0')
    # client.run_ui_library('1.21.1', '8.16.0')
    # client.run_client('1.21.1', '0.11.16')
    # client.run_server('2.6.6')
    # client.run_server_sidekiq('2.6.6')
    # client.run_billing('2.4.2')
    # client.run_billing_sidekiq('2.4.2')
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repo', type=str, nargs='*', required=True, help='repo name')
    parser.add_argument('-s', '--sidekiq', type=bool, default=False, required=False, help='activate sidekiq')
    args = parser.parse_args()
    if (args.repo):
        print(args.repo)

import os
import subprocess
from pyngrok import ngrok
import git
try:
    from google.colab import drive
    colab_env = True
except ImportError:
    colab_env = False


class ColabCode:
    def __init__(self, port=10000, password=None, gcloud=False,github_repo=False):
        self.port = port
        self.password = password
        self._mount = gcloud
        self.github_repo = github_repo 
        self._install_code()
        self._start_server()
        self._run_code()

    def _install_code(self):
        subprocess.run(
            ["wget", "https://code-server.dev/install.sh"], stdout=subprocess.PIPE
        )
        subprocess.run(["sh", "install.sh"], stdout=subprocess.PIPE)
    def clone_repo(self):
        '''Clone a Github Repo to the root directory'''
        git.Git("/").clone(self.github_repo)
    def _start_server(self):
        active_tunnels = ngrok.get_tunnels()
        for tunnel in active_tunnels:
            public_url = tunnel.public_url
            ngrok.disconnect(public_url)
        url = ngrok.connect(port=self.port)
        print(f"Code Server can be accessed on: {url}")

    def _run_code(self):
        os.system(f"fuser -n tcp -k {self.port}")
        if self._mount and colab_env:
            drive.mount("/content/drive")
        if self.github_repo:
            self.clone_repo()
        if self.password:
            code_cmd = f"PASSWORD={self.password} code-server --port {self.port} --disable-telemetry"
        else:
            code_cmd = f"code-server --port {self.port} --auth none --disable-telemetry"
        
        with subprocess.Popen(
            [code_cmd],
            shell=True,
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        ) as proc:
            for line in proc.stdout:
                print(line, end="")

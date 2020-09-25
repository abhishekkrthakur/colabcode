import os
import subprocess
from pyngrok import ngrok

try:
    from google.colab import drive

    colab_env = True
except ImportError:
    colab_env = False


EXTENSIONS = ["ms-python.python", "jithurjacob.nbpreviewer", 
              "njpwerner.autodocstring", "ms-python.vscode-pylance", "ms-vscode-remote.remote-wsl", "ms-python.anaconda-extension-pack",
              "donjayamanne.githistory", "bee.git-temporal-vscode", "kiteco.kite", "vscode-icons-team.vscode-icons"] 
              ## "julialang.language-julia"


class ColabCode:
    def __init__(self, port=10000, password=None, mount_drive=False, add_extensions=None):
        self.port = port
        self.password = password
        self._mount = mount_drive
        self._install_code()
        if add_extensions is not None:
            global EXTENSIONS
            if type(add_extensions) == list and type(add_extensions[0]) == str:
                EXTENSIONS += add_extensions
            else: 
                raise TypeError("You need to pass a list of string(s) e.g. ['ms-python.python']")
        self._install_extensions()
        self._start_server()
        self._run_code()

    def _install_code(self):
        subprocess.run(
            ["wget", "https://code-server.dev/install.sh"], stdout=subprocess.PIPE
        )
        subprocess.run(["sh", "install.sh"], stdout=subprocess.PIPE)

    def _install_extensions(self):
        for ext in EXTENSIONS:
            subprocess.run(["code-server", "--install-extension", f"{ext}"])

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

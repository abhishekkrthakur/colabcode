import os
import subprocess
from pyngrok import ngrok
from google.colab import drive


class ColabCode:
    def __init__(self, port=10000, password=None, gcloud=False):
        self.port = port
        self.password = password
        self.gcloud = gcloud
        self._install_code()
        self._start_server()
        self._run_code()
    def _install_code(self):
        subprocess.run(
            ["wget", "https://code-server.dev/install.sh"], stdout=subprocess.PIPE
        )
        subprocess.run(["sh", "install.sh"], stdout=subprocess.PIPE)
    def _start_server(self):
        active_tunnels = ngrok.get_tunnels()
        for tunnel in active_tunnels:
            public_url = tunnel.public_url
            ngrok.disconnect(public_url)
        url = ngrok.connect(port=self.port)
        print(f"Code Server can be accessed on: {url}")
    def _run_code(self):
        os.system(f"fuser -n tcp -k {self.port}")
        if self.gcloud:
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

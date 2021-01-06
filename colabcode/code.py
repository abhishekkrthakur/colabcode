import os
import subprocess
from pyngrok import ngrok

try:
    from google.colab import drive

    colab_env = True
except ImportError:
    colab_env = False


EXTENSIONS = ["ms-python.python", "ms-toolsai.jupyter"]
CODESERVER_VERSION = "3.7.4"


class ColabCode:
    def __init__(self, port=10000, password=None, authtoken=None, mount_drive=False, drive_path=None):
        self.port = port
        self.password = password
        self.authtoken = authtoken
        self._mount = mount_drive
        self._default_path = "/content/drive"       
        self._install_code()
        self._install_extensions()
        self._start_server(drive_path)
        self._run_code()

    def _install_code(self):
        subprocess.run(
            ["wget", "https://code-server.dev/install.sh"], stdout=subprocess.PIPE
        )
        subprocess.run(
            ["sh", "install.sh", "--version", f"{CODESERVER_VERSION}"],
            stdout=subprocess.PIPE,
        )


    def _install_extensions(self):
        for ext in EXTENSIONS:
            subprocess.run(["code-server", "--install-extension", f"{ext}"])



    def _start_server(self, drive_path):
        if self.authtoken:
            ngrok.set_auth_token(self.authtoken)
        active_tunnels = ngrok.get_tunnels()
        for tunnel in active_tunnels:
            public_url = tunnel.public_url
            ngrok.disconnect(public_url)
        url = ngrok.connect(addr=self.port, options={"bind_tls": True})
        print(self._mount_drive(url, drive_path))


    def _mount_drive(self, url, drive_path):
        if self._mount and colab_env:
            if drive_path:
                try :
                    drive.mount(drive_path)
                    self._default_path = drive_path
                except:
                    drive.mount(self._default_path)
            else:
                drive.mount(self._default_path)
            return f"Code server can be accessed on : {url}/?folder={self._default_path}"
        return f"Code server can be accessed on : {url}"

        

    def _run_code(self):
        os.system(f"fuser -n tcp -k {self.port}")
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

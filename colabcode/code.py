import os
import subprocess
import uuid

import nest_asyncio
import uvicorn
from pyngrok import ngrok


try:
    from google.colab import drive

    colab_env = True
except ImportError:
    colab_env = False


EXTENSIONS = ["ms-python.python", "ms-toolsai.jupyter", "mechatroner.rainbow-csv", "vscode-icons-team.vscode-icons",
"julialang.language-julia", "golang.go",
]
CODESERVER_VERSION = "4.13.0"


class ColabCode:
    def __init__(
        self,
        port=10000,
        password=None,
        authtoken=None,
        mount_drive=False,
        code=True,
        lab=False,
        pluto=False
    ):
        self.port = port
        self.password = password
        self.authtoken = authtoken
        self._mount = mount_drive
        self._code = code
        self._lab = lab
        self._pluto = pluto
        self.url = None
        if self._lab:
            self._start_server()
            self._run_lab()
        if self._code:
            self._install_code()
            self._install_go()
            self._install_julia()
            self._install_extensions()
            self._start_server()
            self._run_code()
        
        if self._pluto:
            print("installing julia")
            self._install_julia()
            print("installing pluto")
            self._install_pluto()
            print("starting server")
            self._start_server()
            print("running pluto")
            self._run_pluto()


    @staticmethod
    def _install_code():
        subprocess.run(["wget", "https://code-server.dev/install.sh"], stdout=subprocess.PIPE)
        subprocess.run(
            ["sh", "install.sh", "--version", f"{CODESERVER_VERSION}"],
            stdout=subprocess.PIPE,
        )
    
    @staticmethod
    def _install_go():
        subprocess.run(["wget","https://go.dev/dl/go1.20.4.linux-amd64.tar.gz"],stdout=subprocess.PIPE)
        subprocess.run([ "tar","xvfz","go1.20.4.linux-amd64.tar.gz","--directory","/opt"],stdout=subprocess.PIPE)
        subprocess.run(["ln","-s","/opt/go/bin/go","/usr/bin/go"])
    
    @staticmethod
    def _install_julia():
        subprocess.run(["wget","https://julialang-s3.julialang.org/bin/linux/x64/1.7/julia-1.7.1-linux-x86_64.tar.gz"],stdout=subprocess.PIPE)
        subprocess.run([ "tar","xvfz","julia-1.7.1-linux-x86_64.tar.gz","--directory","/opt"],stdout=subprocess.PIPE)
        subprocess.run(["ln","-s","/opt/julia-1.7.1/bin/julia","/usr/bin/julia"])

    @staticmethod
    def _install_extensions():
        for ext in EXTENSIONS:
            subprocess.run(["code-server", "--install-extension", f"{ext}"])

    def _start_server(self):
        if self.authtoken:
            ngrok.set_auth_token(self.authtoken)
        active_tunnels = ngrok.get_tunnels()
        for tunnel in active_tunnels:
            public_url = tunnel.public_url
            ngrok.disconnect(public_url)
        url = ngrok.connect(addr=self.port, bind_tls=True)
        self.url = url.public_url
        if self._code:
            print(f"Code Server can be accessed on: {url}")
        else:
            print(f"Public URL: {url}")

    def _run_lab(self):
        token = str(uuid.uuid1())
        print(f"Jupyter lab token: {token}")
        base_cmd = "jupyter-lab --ip='localhost' --allow-root --ServerApp.allow_remote_access=True --no-browser"
        os.system(f"fuser -n tcp -k {self.port}")
        if self._mount and colab_env:
            drive.mount("/content/drive")
        if self.password:
            lab_cmd = f" --ServerApp.token='{token}' --ServerApp.password='{self.password}' --port {self.port}"
        else:
            lab_cmd = f" --ServerApp.token='{token}' --ServerApp.password='' --port {self.port}"
        lab_cmd = base_cmd + lab_cmd
        with subprocess.Popen(
            [lab_cmd],
            shell=True,
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        ) as proc:
            for line in proc.stdout:
                print(line, end="")

    @staticmethod   
    def _install_pluto():
        pluto_install_cmd_list = ["julia","-e",'using Pkg;Pkg.add("Pluto")']
        print("installing Pluto")
        print(pluto_install_cmd_list)
        with subprocess.Popen(
            pluto_install_cmd_list,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        ) as proc:
            stdout,stderr = proc.communicate()

            print("error is="+stderr)

    def _run_pluto(self):
        
        os.system(f"fuser -n tcp -k {self.port}")
        if self._mount and colab_env:
            drive.mount("/content/drive")
        pluto_run_cmd_list = ["julia","-e",f'import Pluto;Pluto.run(port={self.port},launch_browser=false)']
        print(pluto_run_cmd_list)
        with subprocess.Popen(
            pluto_run_cmd_list,
            shell=False,
            stdout=subprocess.PIPE,
            stderr = subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
        ) as proc:
            
            for line in proc.stdout:
                if "localhost" in line:
                    
                    print(line.replace(f"http://localhost:{self.port}",self.url),end="")
                    
               






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

    def run_app(self, app, workers=1):
        self._start_server()
        nest_asyncio.apply()
        uvicorn.run(app, host="127.0.0.1", port=self.port, workers=workers)

# ColabCode

Run code server on Google Colab or Kaggle Notebooks

Quickstart:
- install colabcode: `pip install colabcode`
- import colabcode: `from colabcode import ColabCode`
- run: `ColabCode(port=10000, password="abhishek")`
- you can also run it with any password or port :)

Colab starter notebook: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/abhishekkrthakur/colabcode/blob/master/colab_starter.ipynb)

`ColabCode` has the following arguments:
- `port`: the port you want to run code-server on, default 10000
- `password`: password to protect your code server from being accessed by someone else. Note that there is no password by default!
- `mount_drive`: True or False to mount your Google Drive

`ColabCode` comes pre-installed with some VS Code extensions.

See an example in [this video tutorial](https://www.youtube.com/watch?v=7kTbM3D02jU).

Also an article [here](https://ernestowojori.hashnode.dev/vscode-code-server-in-the-cloud-a-simple-classification-example-on-kaggle) by [Ernest Owojori](https://github.com/E-STAT).

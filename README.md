# ColabCode


[![license](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
[![PyPI version](https://badge.fury.io/py/colabcode.svg)](https://badge.fury.io/py/colabcode)
![python version](https://img.shields.io/badge/python-3.6%2C3.7%2C3.8-blue?logo=python)


Run code server on Google Colab or Kaggle Notebooks

## Getting Started


```shell
# install colabcode
$ pip install colabcode

# import colabcode
$ from colabcode import ColabCode

# run colabcode with by deafult options.
$ ColabCode()

# ColabCode has the following arguments:
# - port: the port you want to run code-server on, default 10000
# - password: password to protect your code server from being accessed by someone else. Note that there is no password by default!
# - mount_drive: True or False to mount your Google Drive

$ ColabCode(port=10000, password="abhishek", mount_drive=True)
```
## How to use it?
Colab starter notebook: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/abhishekkrthakur/colabcode/blob/master/colab_starter.ipynb)

`ColabCode` comes pre-installed with some VS Code extensions.

##### See an example in youtube video     [![YouTube Video](https://img.shields.io/youtube/views/7kTbM3D02jU?style=social)](https://youtu.be/7kTbM3D02jU)

## License

[MIT](LICENSE)

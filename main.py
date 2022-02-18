# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:51:36 2019

@author: McLaren
"""

from Web.router import app
import yaml


def read_yaml(yaml_file_path):
    with open(yaml_file_path, 'rb') as f:
        conf_ = yaml.safe_load(f.read())  # yaml.load(f.read())
    return conf_


if __name__ == '__main__':
    conf = read_yaml("Web/Config/flask_config.yaml")
    app.config.update(conf)
    app.run(host=conf.get("HOST", "127.0.0.1"), port=conf.get("PORT", 5000))

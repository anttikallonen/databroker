#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import restserver
import logging


if __name__ =='__main__':
    logging.getLogger().setLevel(logging.INFO)
    restserver.app.run(host="0.0.0.0", port=8080,threaded=True,debug=True)

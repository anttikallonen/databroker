#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import restserver


if __name__ =='__main__':
	restserver.app.run(host="0.0.0.0", port=8080,threaded=True,debug=True)

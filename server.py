#!/bin/bash
# coding: utf-8

from apiapp import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

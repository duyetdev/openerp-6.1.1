#!/bin/bash

PATH=$(pwd)
/usr/bin/sudo su - openerp -s $PATH/openerp-server -- -c $PATH/openerp-server.conf


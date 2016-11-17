#!/bin/bash
set -x
rm deploy_key.enc
chmod 600 deploy_key
mv deploy_key ~/.ssh/id_rsa

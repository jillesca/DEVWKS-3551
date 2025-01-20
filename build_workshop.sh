#!/bin/bash 

# Define color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}# Setting environment variables${NC}"
LAB_DIR=${HOME}/src
NCS_RUN_DIR=${LAB_DIR}/workshop

# echo 'alias ll="ls -al"' >> ${HOME}/.bashrc
echo LAB_DIR=${HOME}/src >> ${HOME}/.bashrc
echo NCS_RUN_DIR=${LAB_DIR}/workshop >> ${HOME}/.bashrc

echo -e "${GREEN}# Sourcing the bashrc${NC}"
source ${HOME}/.bashrc

echo -e "${GREEN}# Creating workshop directory${NC}"
mkdir -p ${LAB_DIR}
mkdir -p ${NCS_RUN_DIR}

echo -e "${GREEN}# Creating up netsim${NC}"
ncs-netsim delete-network --dir ${NCS_RUN_DIR}/netsim
ncs-netsim --dir ${NCS_RUN_DIR}/netsim create-network $NCS_DIR/packages/neds/cisco-ios-cli-3.0 1 dist-rtr
ncs-netsim --dir ${NCS_RUN_DIR}/netsim add-to-network $NCS_DIR/packages/neds/cisco-iosxr-cli-3.5 1 core-rtr
ncs-netsim --dir ${NCS_RUN_DIR}/netsim add-to-network $NCS_DIR/packages/neds/cisco-nx-cli-3.0 1 dist-sw

echo -e "${GREEN}# Configuring netsim devices${NC}"
ncs-setup --dest ${NCS_RUN_DIR} --netsim-dir ${NCS_RUN_DIR}/netsim

echo -e "${GREEN}# Copying the router package${NC}"
# ncs-make-package  --no-java --service-skeleton python-and-template --component-class router.Router --dest ${NCS_RUN_DIR}/packages/router router
# make clean all -C ${NCS_RUN_DIR}/packages/router/src/
# ln -sf ${HOME}/packages/router ${NCS_RUN_DIR}/packages
ln -sf ${LAB_DIR}/DEVWKS-3551/packages/router ${NCS_RUN_DIR}/packages

echo -e "${GREEN}# Starting netsim devices${NC}"
cd ${NCS_RUN_DIR}
ncs-netsim start

echo -e "${GREEN}# Netsim status${NC}"
ncs-netsim status --dir ${NCS_RUN_DIR}/netsim  | grep -iE 'status|device'

echo -e "${GREEN}Starting NCS${NC}"
ncs

echo -e "${GREEN}# NCS status${NC}"
ncs --status | grep -i 'status:'

echo -e "${GREEN}# NCS packages${NC}"
echo "show packages package oper-status" | ncs_cli -C -u admin 

echo -e "${GREEN}# Syncing devices${NC}"
echo "devices sync-from" | ncs_cli -C -u admin

echo -e "${GREEN}# Workshop setup complete${NC}"
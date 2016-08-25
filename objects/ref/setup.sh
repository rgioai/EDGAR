#!/usr/bin/env bash

# Add edgar function to bash profile

edgar() {
        # script to run EDGAR from command line interface

        # MBPro changes file structure
        cd ~/PycharmProjects

        # General script
        fn=$1
        arg1=${2:-0}
        arg2=${3:-0}
        arg3=${4:-0}
        arg4=${5:-0}
        python3 EDGAR/CLI.py $fn $arg1 $arg2 $arg3 $arg4
}


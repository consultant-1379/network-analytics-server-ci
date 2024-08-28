#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

printf "\n\nCLEANING CACHE FOR DASHBOARD DEPENDENCIES:\n\n"
printf "\n\t1. REMOVING DEBIAN PACKAGES"
find $DIR/apt/archives/ ! -path $DIR/apt/archives/ ! -path $DIR/apt/archives/.gitignore -exec rm -rf {} \;

printf "\n\t2. REMOVING BUNDLE GEMS\n"
find $DIR/bundle/ ! -path $DIR/bundle/ ! -path $DIR/bundle/.gitignore -exec rm -rf {} \;
printf "\n\nCACHE CLEANED!\n\n\n"

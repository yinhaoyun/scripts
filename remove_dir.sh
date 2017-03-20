#!/bin/sh
while true; do
    read -p "Do you really want to delete the folder $1?" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

rsync -a --delete `mktemp -d`/ $1
rmdir $1

#!/bin/bash

this_dir=`cd $(dirname "${BASH_SOURCE[0]}") && pwd`

git config --global core.hooksPath "$this_dir/hooks"

rcfile=`echo "$(basename $SHELL)"`
rcfile="$HOME/.${rcfile}rc"

cfgd=`grep $this_dir $rcfile`
if [[ "$cfgd" == "" ]]; then
  echo "adding rc source to $rcfile"
  echo "source $this_dir/git.rc" >> "$rcfile"
fi

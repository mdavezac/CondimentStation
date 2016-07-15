#! /bin/bash
set -e

prefix=$(pwd)
condiment_dir=$prefix/CondimentStation
virtenv=$prefix/build/salt-env
pysaltdir=$virtenv/lib/python2.7/site-packages/salt
mainrepo=git@github.com:mdavezac/CondimentStation

mkdir -p $(pwd)/build

if [ ! -d "$virtenv" ]; then
  # if [[ "$(uname)" -eq "Darwin" ]] ; then
  #   curl -L https://bootstrap.pypa.io/get-pip.py -o build/get-pip.py
  #   sudo python build/get-pip.py
  #   sudo pip install --upgrade pip virtualenv
  # else
  #   sudo apt-get install python-dev python-pip python-virtualenv
  # fi
  python -m virtualenv $virtenv
  . $virtenv/bin/activate
  pip install --upgrade pip salt click GitPython mako pytest
fi

if [[ "$(uname)" -eq "Darwin" ]] && [[ ! -e /usr/local/bin/brew ]]
then
   sudo chown -R $(whoami) /usr/local
   ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

if [[ ! -e "$condiment_dir/bin/pinch.py" ]] ; then
  git clone git@github.com:mdavezac/CondimentStation -b CondimentStation
fi

$virtenv/bin/python $condiment_dir/bin/pinch.py setup server_hierarchy $prefix
$virtenv/bin/python $condiment_dir/bin/pinch.py setup syspath $prefix
$virtenv/bin/python $condiment_dir/bin/pinch.py setup minion $prefix
$virtenv/bin/python $condiment_dir/bin/pinch.py setup pillar $prefix
$virtenv/bin/python $condiment_dir/bin/pinch.py setup sync
$virtenv/bin/python $condiment_dir/bin/pinch.py run salt
$virtenv/bin/python $condiment_dir/bin/pinch.py run condiments

# cat > $pysaltdir/_syspaths.py <<EOF
# ROOT_DIR="$(pwd)/build"
# CONFIG_DIR="$(pwd)/build/etc"
# CACHE_DIR="$(pwd)/build/var/cache/salt"
# SOCK_DIR="$(pwd)/build/var/run/salt"
# SRV_ROOT_DIR="$(pwd)"
# BASE_FILE_ROOTS_DIR="$(pwd)/salt"
# BASE_PILLAR_ROOTS_DIR="$(pwd)/pillar"
# BASE_MASTER_ROOTS_DIR="$(pwd)/build/srv/salt-master"
# LOGS_DIR="$(pwd)/build/var/log/salt"
# PIDFILE_DIR="$(pwd)/build/var/run"
# SPM_FORMULA_PATH="$(pwd)/build/srv/spm/salt"
# SPM_PILLAR_PATH="$(pwd)/build/srv/spm/pillar"
# SPM_REACTOR_PATH="$(pwd)/build/srv/spm/reactor"
# BASE_THORIUM_ROOTS_DIR=None
# EOF
#
# mkdir -p $prefix/build/etc
# cat > $prefix/build/etc/minion <<EOF
# file_client: local
# user: $(whoami)
# sudo_user: $(whoami)
# file_roots:
#   base:
#     - $prefix/
# EOF
# if [[ "$(uname)" -eq "Darwin" ]] ; then
#   cat >> $prefix/build/etc/minion <<EOF
# pkg: brew
# EOF
# fi
#
# [[ ! -e "$prefix/bin/activate" ]] && \
#   cd $prefix/bin && ln -s $virtenv/bin/activate . && \
#   cd $prefix
# mkdir -p $prefix/build/var/log/salt/
# mkdir -p $prefix/build/var/cache/salt/master
#
# cat > $prefix/pillar/condiment.sls << EOF
# user: $(whoami)
# condiment_dir: $(prefix)/CondimentStation
# condiment_build_dir: $(pwd)/build
# EOF
#
# if [[ ! -d "$prefix/pillar" ]] ; then
#   mkdir $prefix/pillar
# fi
# if [[ ! -e "$prefix/pillar/secrets.sls" ]] ; then
#   touch $prefix/pillar/secrets.sls
# fi

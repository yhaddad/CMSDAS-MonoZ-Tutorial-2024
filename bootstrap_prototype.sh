#!/usr/bin/env zsh

cat <<EOF > shell
#!/usr/bin/env zsh

voms-proxy-init -voms cms --valid 192:00 --out \$HOME/x509up_u\$UID

if [[ "\$1" == "" ]]; then
  export COFFEA_IMAGE="coffeateam/coffea-dask-almalinux8:2024.4.1-py3.11"
  # export COFFEA_IMAGE=/cvmfs/unpacked.cern.ch/registry.hub.docker.com/coffeateam/coffea-dask:latest
else
  export COFFEA_IMAGE=/cvmfs/unpacked.cern.ch/registry.hub.docker.com/\$1
fi

export FULL_IMAGE="/cvmfs/unpacked.cern.ch/registry.hub.docker.com/"\$COFFEA_IMAGE

# Needed to setup cluster
export CONDOR_CONFIG=/srv/.condor_config

grep -v '^include' /etc/condor/config.d/01_cmslpc_interactive > .condor_config

export ZDOTDIR=/srv

SINGULARITY_SHELL=\$(which zsh) singularity exec -B \${PWD}:/srv -B /cvmfs -B /uscmst1b_scratch --pwd /srv \\
  \${FULL_IMAGE} $(which zsh)
# Working version... but not self-consistent with zsh?
# SINGULARITY_SHELL=\$(which zsh) singularity exec -B \${PWD}:/srv -B /cvmfs -B /uscmst1b_scratch --pwd /srv \\
#   \${COFFEA_IMAGE} /bin/zsh #source \${ZDOTDIR}/.zshrc
EOF

cat <<EOF > .bashrc
LPCJQ_VERSION="0.3.1"
install_env() {
  set -e
  echo "Installing shallow virtual environment in \$PWD/.env..."
  python -m venv --without-pip --system-site-packages .env
  unlink .env/lib64  # HTCondor can't transfer symlink to directory and it appears optional
  # work around issues copying CVMFS xattr when copying to tmpdir
  export TMPDIR=\$(mktemp -d -p .)
  .env/bin/python -m ipykernel install --user
  rm -rf \$TMPDIR && unset TMPDIR
  .env/bin/python -m pip install -q git+https://github.com/CoffeaTeam/lpcjobqueue.git@v\${LPCJQ_VERSION}
  echo "done."
}

install_kernel() {
  # work around issues copying CVMFS xattr when copying to tmpdir
  export TMPDIR=\$(mktemp -d -p .)
  .env/bin/python -m ipykernel install --user --name monoz --display-name "monoz" --env PYTHONPATH $PYTHONPATH:$PWD --env PYTHONNOUSERSITE 1
  rm -rf \$TMPDIR && unset TMPDIR
}

install_all() {
  install_env
  install_kernel
}

export JUPYTER_PATH=/srv/.jupyter
export JUPYTER_RUNTIME_DIR=/srv/.local/share/jupyter/runtime
export JUPYTER_DATA_DIR=/srv/.local/share/jupyter
export IPYTHONDIR=/srv/.ipython
unset GREP_OPTIONS

[[ -d .env ]] || install_all
source .env/bin/activate
alias pip="python -m pip"
pip show lpcjobqueue 2>/dev/null | grep -q "Version: \${LPCJQ_VERSION}" || pip install -q git+https://github.com/CoffeaTeam/lpcjobqueue.git@v\${LPCJQ_VERSION}
EOF

cat <<EOF > .zshrc

export JUPYTER_PATH=/srv/.jupyter
export JUPYTER_RUNTIME_DIR=/srv/.local/share/jupyter/runtime
export JUPYTER_DATA_DIR=/srv/.local/share/jupyter
export IPYTHONDIR=/srv/.ipython
unset GREP_OPTIONS

# [[ -d .env ]] || install_env
[[ -d .env ]] || install_all
source .env/bin/activate
alias pip="python -m pip"
# pip show lpcjobqueue 2>/dev/null | grep -q "Version: \${LPCJQ_VERSION}" || pip install -q git+https://github.com/CoffeaTeam/lpcjobqueue.git@v\${LPCJQ_VERSION}
# pip show odapt 2>/dev/null | grep -q "Version:" || pip install -q git+https://github.com/zbilodea/odapt.git@\${ODAPT_BRANCH_OR_TAG}
# pip install -q git+https://github.com/dask-contrib/dask-awkward.git@main
# pip install -q cabinetry correctionlib jupyter-resource-usage

EOF

chmod u+x shell .bashrc
echo "Wrote shell and .bashrc to current directory. Run ./shell to start the singularity shell"

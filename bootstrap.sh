#!/usr/bin/env bash

cat <<EOF > shell
#!/usr/bin/env bash
if [[ "\$1" == "" ]]; then
  export COFFEA_IMAGE="coffeateam/coffea-dask-almalinux8:2024.5.0-py3.11"
  # export COFFEA_IMAGE=/cvmfs/unpacked.cern.ch/registry.hub.docker.com/coffeateam/coffea-dask:latest
else
  export COFFEA_IMAGE=/cvmfs/unpacked.cern.ch/registry.hub.docker.com/\$1
fi

export APPTAINER_BINDPATH=/cvmfs,/cvmfs/grid.cern.ch/etc/grid-security:/etc/grid-security,/eos,/etc/pki/ca-trust,/etc/tnsnames.ora,/run/user,/var/run/user

APPTAINER_SHELL=\$(which bash) apptainer exec -B \${PWD}:/srv --pwd /srv \\
  /cvmfs/unpacked.cern.ch/registry.hub.docker.com/\${COFFEA_IMAGE} \\
  /bin/bash --rcfile /srv/.bashrc
EOF

cat <<EOF > .bashrc
# LPCJQ_VERSION="0.3.1"
install_env() {
  set -e
  echo "Installing shallow virtual environment in \$PWD/.env..."
  python -m venv --without-pip --system-site-packages .env
  unlink .env/lib64  # HTCondor can't transfer symlink to directory and it appears optional
  # work around issues copying CVMFS xattr when copying to tmpdir
  export TMPDIR=\$(mktemp -d -p .)
  rm -rf \$TMPDIR && unset TMPDIR
  # .env/bin/python -m pip install --upgrade awkward dask_awkward coffea uproot
  cd processing
  ../.env/bin/python -m pip install -e .
  cd ..
  # .env/bin/python -m pip install -q git+https://github.com/CoffeaTeam/lpcjobqueue.git@v\${LPCJQ_VERSION}
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
voms-proxy-init -voms cms -vomses /etc/grid-security/vomses/ --valid 192:00 --out \$HOME/x509up_u\$UID
# pip show lpcjobqueue 2>/dev/null | grep -q "Version: \${LPCJQ_VERSION}" || pip install -q git+https://github.com/CoffeaTeam/lpcjobqueue.git@v\${LPCJQ_VERSION}
EOF

cat <<EOF > .zshrc

# LPCJQ_VERSION="0.3.1"
install_env() {
  set -e
  echo "Installing shallow virtual environment in \$PWD/.env..."
  python -m venv --without-pip --system-site-packages .env
  unlink .env/lib64  # HTCondor can't transfer symlink to directory and it appears optional
  # work around issues copying CVMFS xattr when copying to tmpdir
  export TMPDIR=\$(mktemp -d -p .)
  rm -rf \$TMPDIR && unset TMPDIR
  # .env/bin/python -m pip install --upgrade awkward dask_awkward coffea uproot
  cd processing
  ../.env/bin/python -m pip install -e .
  cd ..
  # .env/bin/python -m pip install -q git+https://github.com/CoffeaTeam/lpcjobqueue.git@v\${LPCJQ_VERSION}
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
voms-proxy-init -voms cms -vomses /etc/grid-security/vomses/ --valid 192:00 --out \$HOME/x509up_u\$UID
# pip show lpcjobqueue 2>/dev/null | grep -q "Version: \${LPCJQ_VERSION}" || pip install -q git+https://github.com/CoffeaTeam/lpcjobqueue.git@v\${LPCJQ_VERSION}
EOF

chmod u+x shell .bashrc .zshrc
echo "Wrote shell .bashrc and .zshrc to current directory. Run ./shell to start the singularity shell"

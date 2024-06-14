# Setup

## Connecting to lxplus with tunnels
Choose a port such as 8099 and connect to lxplus. This port should be used for jupyter as well
```
ssh -L localhost:8NNN:localhost:8NNN lxplus.cern.ch
```

## Clone and run the setup once
```
git clone git@github.com:yhaddad/CMSDAS-MonoZ-Tutorial-2024.git
cd CMSDAS-MonoZ-Tutorial-2024
sh bootstrap.sh
```

## Starting the environment
Execute the shell command to start up the container. Once inside, start jupyter lab and copy + paste the link into your browser
```
./shell
jupyter lab --no-browser --port 8NNN
```
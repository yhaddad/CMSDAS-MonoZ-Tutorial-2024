# Setup

## Website for the CMSDAS MonoZ

To start, you can follow the directions below. A summmary of the plan for the MonoZ group at the Data Analysis School is can be found in the main website [here](https://submit.mit.edu/~freerc/MonoZ_CMSDAS/index.html).

There, you will also find introduction to the physics, and explanations on each step of the school. 

Finally, 

Welcome to CMS!

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

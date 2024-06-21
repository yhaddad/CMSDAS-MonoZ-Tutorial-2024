Available software
------------------

This section briefly describes several options in which to set up your environment for working on submit. This section is not exhaustive but introduces several tools which can help you set up your code. 

Native system
~~~~~~~~~~~~~

All of the submit machines come with several tools to help you get started with your work. A few examples are shown below:

1. Languages: python, c++, Julia, Java, etc.

2. Tools: XRootd, gfal, etc.

For more complicated workflows, there are several options on how to proceed. Many environments can be set up through CVFMS provided by CERN. If you need more control of the environment, either conda or dockers are commonly used and well supported. For more information see the sections below.

X2GO
~~~~

X2Go is open source remote desktop software for Linux and is available on submit07. You will need to download the x2goclient on your local machine and then start a session to connect to submit07.mit.edu. 

`x2goclient <https://wiki.x2go.org/doku.php/doc:installation:x2goclient>`_

Remember to point to the correct ssh key that you have uploaded to the submit-portal. There is currently a bug in either XFCE or X2Go causing rendering issues with the compositor when using X2Go. To disable the compositor, you can go to Settings > Window Manager Tweaks > Compositor.

VSCode
~~~~~~

Please note: Not all of the following features are supported for all programming languages.

Visual Studio Code (VSCode) is a free, versatile source-code editor that supports a wide range of programming languages, including Python, C/C++, Java, Julia, Fortran, and others. It also supports various markup languages like HTML/CSS, Markdown, reStructuredText, LaTeX, and JSON. Key features of VSCode include:

* **Debugging:** `simplify your troubleshooting process <https://code.visualstudio.com/docs/editor/debugging>`_.

* **Source control:** `manage your code with git/GitHub <https://code.visualstudio.com/docs/sourcecontrol/overview>`_.

* **Integrated file browser:** easily navigate and manage your files within the editor.

One of the capabilities of VSCode is its client-server mode for `remote development <https://code.visualstudio.com/docs/remote/ssh>`_ on subMIT. This functionality allows you to edit, run, and debug code on the subMIT servers directly from your personal computer. This setup provides the ease of a GUI-based development environment on your local machine while executing the code on subMIT's infrastructure.

For `most languages <https://code.visualstudio.com/docs/languages/overview>`_, VScode enhances your coding experience with features like:

* **Edit code:** including code highlighting and easy `code navigation <https://code.visualstudio.com/docs/editor/editingevolved>`_. `More about code basics <https://code.visualstudio.com/docs/editor/codebasics>`_.

* **Advanced debugging:** use breakpoints, inspect variables, stack navigation. `Debugging guide <https://code.visualstudio.com/docs/editor/debugging>`_.

* **IntelliSense:** code completion, parameter info, quick info, and more. `Discover IntelliSense <https://code.visualstudio.com/docs/editor/intellisense>`_.

* **Time-saving features:** benefit from `AI-assisted code development <https://code.visualstudio.com/docs/editor/artificial-intelligence>`_, `user-defined snippets <https://code.visualstudio.com/docs/editor/userdefinedsnippets>`_, and `task automation <https://code.visualstudio.com/docs/editor/tasks>`_.

* **Accessibility features:** `learn about accessibility in VSCode <https://code.visualstudio.com/docs/editor/accessibility>`_.



Getting Started with VSCode on subMIT
.....................................

Microsoft provides some handy `videos <https://code.visualstudio.com/docs/getstarted/introvideos>`_ for getting started with VSCode, as well as detailed information on `remote connection <https://code.visualstudio.com/docs/remote/ssh>`_.

#. **Install VSCode:** `download and install instructions <https://code.visualstudio.com/docs/setup/setup-overview>`_

#. **SSH Configuration:** Follow the `general configuration guide <https://submit.mit.edu/submit-users-guide/starting.html#common-issues-with-keys>`_ in the subMIT User's Guide. Also have a look at the `VSCode configuration guide <https://submit.mit.edu/submit-users-guide/starting.html#connecting-to-submit-through-VSCode>`_ due to a recent VSCode upgrade which removed the compatibility with CentOS 7.

#. **Remote-SSH Extension:** Available in the VSCode Extensions tab or on the `VSCode website <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh>`_.

#. **Connect to subMIT:** Click the green "Open a Remote Window" button in the lower-left of the VSCode window. Select "submit" from the menu (VSCode automatically reads your ssh config file). Then, simply "open" a folder or workspace. Opening a folder is typically more convenient than opening a single code file.  Remember: VSCode is now connected to subMIT, so you are looking at and navigating your files on the subMIT servers, not on your laptop/desktop.

Handy Resources
...............

* `Intro videos <https://code.visualstudio.com/docs/getstarted/introvideos>`_ (external)

* `Keyboard cheat sheet <https://code.visualstudio.com/docs/getstarted/tips-and-tricks#_keyboard-reference-sheets>`_ (external)

* `Local Python environment tutorial <https://submit.mit.edu/submit-users-guide/tutorials/tutorial_1.html#types-of-python-environments>`_ (internal)

* `Activating a Python environment tutorial <https://submit.mit.edu/submit-users-guide/program.html#conda-in-visual-studio-code>`_ (internal) 

CVMFS
~~~~~

The CernVM File System (CVMFS) provides a scalable, reliable and low- maintenance software distribution service. It was developed to assist High Energy Physics (HEP) collaborations to deploy software on the worldwide- distributed computing infrastructure used to run data processing applications. CernVM-FS is implemented as a POSIX read-only file system in user space (a FUSE module). Files and directories are hosted on standard web servers and mounted in the universal namespace ``/cvmfs``.

More documentation on CVMFS can be found here: `CVMFS <https://cernvm.cern.ch/fs/>`_

A couple examples of using CVMFS are shown below:

To set up ROOT:

.. code-block:: sh

     source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc11-opt/setup.sh
     root

To set up GEANT4 (make sure to use one of the AlmaLinux9 machines):

.. code-block:: sh

     source /cvmfs/sft.cern.ch/lcg/releases/gcc/11.3.1/x86_64-centos9/setup.sh
     export GEANT4_DIR=/cvmfs/geant4.cern.ch/geant4/10.7.p01/x86_64-centos7-gcc8-optdeb-MT
     export QT5_HOME=/cvmfs/sft.cern.ch/lcg/releases/LCG_97/qt5/5.12.4/x86_64-centos7-gcc8-opt
     export Qt5_DIR=$QT5_HOME
     export QT_QPA_PLATFORM_PLUGIN_PATH=$QT5_HOME/plugins
     export QT_XKB_CONFIG_ROOT=/usr/share/X11/xkb
     cd ${GEANT4_DIR}/bin
     source ./geant4.sh
     
     # show the geant version:
     ./geant4-config --version

To set up the CMS software (CMSSW) or other cms specific tools:

.. code-block:: sh

      source /cvmfs/cms.cern.ch/cmsset_default.sh

If you want to use ROOT or any other CMSSW specific tools you can also download CMSSW releases and work within a CMS environment. A simple example is shown below:

.. code-block:: sh

      cmsrel CMSSW_10_2_13
      cd CMSSW_10_2_13/src
      cmsenv

Once the CMS environment is set up, the CMS software version specific ROOT release is now available to you as well.

In addition to the typical CMVFS environments, MIT hosts its own version of CVMFS where additional software is placed. One such example is Matlab which is given through MIT. This can be accessed like below:

.. code-block:: sh
       
      /cvmfs/cvmfs.cmsaf.mit.edu/submit/work/submit/submit-software/matlab/Matlab_install/bin/matlab


Conda
~~~~~

Conda is an open source package management system and environment management system. We can use this to set up consistent environments and manage the package dependencies for various applications. Below is an example to set up a python environment for working with `coffea <https://coffeateam.github.io/coffea/>`_ and `dask <https://docs.dask.org/en/stable/>`_. 

Important Note for Using Conda on submit
........................................

Please note that downloading many conda packages takes a large amount of space which can very quickly use up the quota in your home. If you plan to use conda heavily it is suggested to download and configure it in your work directory where there is much more space. Any new conda environment that you install in your ``/home/submit`` or ``/work/submit`` will be installed on your Jupyterhub only after your server is started up again. If your server is already running, you can stop it by File -> Hub Control Panel -> Stop My Server and then restart it by clicking Start Server. 

Installing Conda
................

.. code-block:: sh

      wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
      # Run and follow instructions on screen
      bash Miniforge3-Linux-x86_64.sh

NOTE: always make sure that conda, python, and pip point to local Miniforge installation (``which conda`` etc.). Another thing to keep in mind is that you should avoid installing packages with ``pip`` using ``--user``. The coffea example below shows the correct way to use pip in conjunction with conda. 

See also https://hackmd.io/GkiNxag0TUmHnnCiqdND1Q#Local-or-remote

Quick commands to know
......................

.. code-block:: sh

     conda activate env_name # To activate the environment called env_name
     conda deactivate # To deactivate an environment
     conda info --envs # To list of your environments. You can also use "conda env list"
     conda list # To list the packages of an environment. Use after activating the environment or add "-n env_name"
     conda env export > environment.yml # To export your environment with its packages. Use after activating the environment
     conda remove --name env_name --all # To remove the environment env_name

Example: coffea installation
............................

You can either use the default environment (``base``) or create a new one:

.. code-block:: sh

      # create new environment with python 3.7, e.g. environment of name "coffea"
      conda create --name coffea python=3.7
      # activate environment "coffea"
      conda activate coffea

To check that the right python version is there, run ``python --version``. This should show ``Python 3.7.XX``.

An example of how to install a mix of packages through conda and pip:


.. code-block:: sh

      pip install git+https://github.com/CoffeaTeam/coffea.git #latest published release with `pip install coffea`
      conda install -c conda-forge xrootd
      conda install -c conda-forge ca-certificates
      conda install -c conda-forge ca-policy-lcg
      conda install -c conda-forge dask-jobqueue
      conda install -c anaconda bokeh 
      conda install -c conda-forge 'fsspec>=0.3.3'
      conda install dask
      conda install pytables
      pip install --pre fastjet
      pip install vector

Conda in Visual Studio Code:
............................

**Selecting and activating a conda environment in VSCode:** you need to inform VSCode which conda environment to use for your Python workspace. Look at the bottom-left corner (macOS) or bottom-right corner (Windows) of the VSCode window to find the "Select Python Interpreter" button. Click on it and a list of available Python interpreters will appear. Choose the one that suits your needs (e.g., ``myenv``). You can also select the environment using the Command Palette (``Cmd+Shift+P`` in macOS or ``Ctrl+Shift+P`` in Windows) and searching for "Python: Select Interpreter". Note that it may take some time for VSCode to detect the available conda environments.

Containers
~~~~~~~~~~

Containers are becoming commonplace in scientific workflows. Submit offers access to containers through Singularity images provided through CVMFS. This section will give a short example on how to enter into a singularity container to run your framework. For more information on dockers see the `docker engine site <https://docs.docker.com/engine/reference/commandline/build/>`_.

Podman
......

SubMIT will be using Podman instead of Docker on all upgraded machines. For users who have been using Docker, you can run on Podman images created with Docker. You can run familiar commands, such as ``pull``, ``push``, ``build``, ``commit``, ``tag``, etc. with Podman


Docker (only on CentOS machines)
................................

All SubMIT users have access to build dockers. You can start by finding instructions through your packages dockerhub or by downloading the code and building the docker image.

.. code-block:: sh

     docker build -t local/docker_name .

You can then run the docker like below.

.. code-block:: sh

     docker run --rm -i -t local/docker_name

Dockerhub:
..........

Code can be pulled directly from Dockerhub:  `dockerhub <https://hub.docker.com/>`_.

If there is a container that you would like to use on Dockerhub, you can pull the container directly.

.. code-block:: sh

      docker pull <Dockerhub_container>

After this is done downloading we can then enter into the container:

.. code-block:: sh

      docker run --rm -i -t <Dockerhub_container>


Singularity and Singularity Image Format (SIF)
..............................................

Singularity can build containers in several different file formats. The default is to build a SIF (singularity image format) container. SIF files are compressed and immutable making them the best choice for reproducible, production-grade containers. If you are going to be running your singularity through one of the batch systems provided by submit, it is suggested that you create a SIF file. For Slurm, this SIF file can be accessed through any of your mounted directories, while for HTCondor, the best practice is to make this file avialble through CVMFS. This singularity image could then be accessed through both the T2 and T3 resources via MIT's hosted CVMFS.

While Singularity doesn’t support running Docker images directly, it can pull them from Docker Hub and convert them into a suitable format for running via Singularity. This opens up access to a huge number of existing container images available on Docker Hub and other registries. When you pull a Docker image, Singularity pulls the slices or layers that make up the Docker image and converts them into a single-file Singularity SIF image. An example of this was shown below.

.. code-block:: sh

      singularity build docker_name.sif docker-daemon://local/docker_name:latest

And start the singularity

.. code-block:: sh

      singularity shell docker_name.sif

If you need this available on worker nodes through HTCondor you can add them to a CVMFS space in your work directory. You will then need to email Max (maxi@mit.edu) to create this CVMFs area for you.

.. code-block:: sh

    #Start singularity from your /work area (email Max with pathway EXAMPLE:/work/submit/freerc/cvmfs/):
    singularity shell /cvmfs/cvmfs.cmsaf.mit.edu/submit/work/submit/freerc/cvmfs/docker_name.sif

Singularity container
.....................

For this example, we will use the coffea-base singularity image based on the following `docker coffea image <https://github.com/CoffeaTeam/docker-coffea-base>`_.

Entering into the singularity container. You can simply do the following command:

.. code-block:: sh

     singularity shell -B ${PWD}:/work /cvmfs/unpacked.cern.ch/registry.hub.docker.com/coffeateam/coffea-dask:latest

Now you should be in a singularity environment. To test you try to import a non-native package like coffea in python:

.. code-block:: sh

     python3 -c "import coffea"

The command above naturally binds the PWD and work directory. If you need to specify another area to bind you can do the following:

.. code-block:: sh

     export SINGULARITY_BIND="/mnt"

Now you can run in many different environments that are available in singularity images through CVMFS.


gcc and systemwide systems
~~~~~~~~~~~~~~~~~~~~~~~~~~

SubMIT is a CentOS07 system and as such will have old versions for some compilers and tools. For example, the gcc compiler for CentOS07 is quite old. Rather than trying to install many versions throughout SubMIT it is suggested for users to try and control the versions themselves. The tools listed above can often help with this. A couple of examples of using a newer version of gcc are shown below. 

If newer versions of gcc are needed, they are available through conda `conda gcc <https://anaconda.org/conda-forge/gcc>`_. 

Alternatively, you can also use a gcc version available through CVMFS. An example is shown below:

.. code-block:: sh

     #An example of using a newer version of gcc
     /cvmfs/cms.cern.ch/el8_amd64_gcc12/external/gcc/12.1.1-bf4aef5069fdf6bb6f77f897bcc8a6ae/bin/gcc

For systemwide tools such as gcc, these options should be considered first in order to solve the issues on the user side. If these options still do not work for your needs then please email <submit-help@mit.edu>.

Additional Operating Systems (CMS specific)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For CMS users, there are additional options to operating systems through CMSSW. The following commands will set up CMSSW and then put you into a singularity for Scientific Linux CERN 6 (slc6), CentOS 7(cc7), AlmaLinux 8 (el8) and AlmaLinux 9 (el9). 

.. code-block:: sh

     source /cvmfs/cms.cern.ch/cmsset_default.sh

You can then do any of the following depending on your desired OS.

.. code-block:: sh

     cmssw-slc6
     cmssw-cc7
     cmssw-el8
     cmssw-el9

If you want to check the OS, you caan do the following.

.. code-block:: sh

     cat /etc/os-release

Jupyterhub
~~~~~~~~~~

In addition to the tools above, you have access to Jupyter Notebooks through a `JupyterHub <http://submit.mit.edu/jupyter>`_ set up at submit.

This is set up through the submit machines meaning that you have access to all of your data through jupyter notebooks. You will have access to basic python3 configurations. In addition, if you need a more complex environment, you can run your notebooks in any conda environment that you have set up. You can check the name and location of your environments using the command ``jupyter kernelspec list``. This allows you to create the exact environment you need for your projects. An example on how to set up a conda environment is shown above, and how it is implemented in jupyter is described below.

A few examples of simple Jupyter notebooks can be found in the `Github jupyter examples <https://github.com/mit-submit/submit-examples/tree/main/jupyter>`_. Several other intro notebooks can be found in the link below:
`JupyterHub_examples <https://github.com/CpResearch/PythonDataAnalysisTutorial/tree/main/jupyter>`_

You have access to a few job profiles. Make sure to use the one that fits your needs. Here are some of the available options:

* **Slurm - Submit - 1/2/4 CPU(s), 2 GB/4 GB/8 GB:** spawns a server on the submit slurm partition, requesting 1, 2, or 4 CPU(s) with 2, 4, or 8 GB of memory.

* **Slurm - Submit-GPU - 1 GPU:** spawns a server on a submit-gpu1080 submit slurm partition, requesting 1 GPU.

* **Slurm - Submit-GPU-A30 - 1 GPU:** spawns a server on a submit-gpu-a30 submit slurm partition, requesting 1 GPU.

By default, Jupyterhub shows the files located in ``/home/submit/<username>``. If you store jupyter notebooks in ``/work`` and they are small, consider moving them to your ``/home`` directory. Otherwise, you should be able to access a notebook in ``/work`` by selecting "``File > Open from Path...``" in the top menu of Jupyter, then type the full path to your notebook.

When you are finished using Jupyter, please select ``File -> Hub Control Panel -> Stop My Server`` from the top menu to stop your server.

.. admonition:: If your session repeatedly terminates unexpectedly ... (click here to show/hide)
   :class: dropdown

   A common reason for a session terminating unexpectedly (besides an unstable internet connection) is overruning memory.  If this happens, please apply the following memory best practices first and then if still necessary, use a spawn option with a larger memory allocation.

   Memory best practices: *all* open notebooks/kernels contribute towards your memory budget.  If you have multiple notebooks open only to read (not to run), please set their kernel to "``No Kernel``".  Please close unused notebooks by selecting ``File --> Close and Shutdown Notebook`` from the top menu.  (When you close a tab, the kernel generally remains open, but closing it this way shuts down the kernel as well, freeing memory).

Here is how jupyter interacts with: conda, singularity, GPUs, Slurm, and ROOT.

#. Conda

    * jupyterhub is set up to automatically load all conda and python environments which are found in the following directories
              
    .. code-block:: sh
    
         '/usr/bin/',
        '/home/submit/<username>/miniforge3/',
        '/home/submit/<username>/anaconda3/',
        '/home/submit/<username>/miniconda3/', 
        '/home/submit/<username>/.conda/',
        '/work/submit/<username>/anaconda3/',
        '/work/submit/<username>/miniconda3/', 
        '/work/submit/<username>/miniforge3/',
        '/data/submit/<username>/anaconda3/', 
        '/data/submit/<username>/miniconda3/',
        '/data/submit/<username>/miniforge3/',
        ]
              
    * If you have a different version of conda, or it is located in a different place, or some other problem has come up, please contact us for help.
    * Alternatively, a manual installation can be performed:
    
    
        1. Switch to the python you want to make available
        2. ``pip install --user ipykernel``
        3. ``python -m ipykernel install --user --name <name>``; where ``<name>`` is what you want it to show up as on jupyter
        
     
    * What the manual and automatic installations do is to create a kernel folder in your ``/home/submit/<user>/.local/share/jupyter/kernels/``. These are then found by jupyterhub, and can be used as kernels for notebooks.
    * You can list all currently installed kernels with ``jupyter kernelspec list``. Individual kernels can be removed with ``jupyter kernelspec remove <name>``.
    * N.B.: if relying on the automatic installation, the first time you log in after having created some environment(s), the spawning will be slower than usual, since it has to install them.
     
#. Singularity

    * Because singularity environments are not located in standardized locations like anaconda tends to be, there is no automatic installation for these environments to jupyterhub.
    * However, we can create a kernel environment by hand, which we can then use in jupyter, just like any other python environment:
    
    
        1. ``mkdir /home/submit/$USER/.local/share/jupyter/kernels/<name>/``
        2. ``touch /home/submit/$USER/.local/share/jupyter/kernels/<name>/kernel.json``
        3. And finally, place the following in the json file
    
        .. code-block:: sh
        
             {
               "argv": [
                "singularity",
                "exec",
                "-e",
                "</path/to/singularity/image/>",
                "python",
                "-m",
                "ipykernel_launcher",
                "-f",
                "{connection_file}"
               ],
               "display_name": "test",
               "language": "python",
               "metadata": {
                "debugger": true
               }
              }
        
        4. You can personalize this ``singularity exec`` command, e.g. if you want to bind a directory, you can just add two lines to the ``argv``, "--bind", "<directory>". You can test out this command by something like:
              
              ``singularity exec -e /path/to/image/ -m python``
          
#. GPUs

    * GPUs are available on submit-gpu machines. The GPUs are not used or  reserved by jupyterhub by itself. Rather, just like when you log in those machines through ssh, the GPUs can be used by a notebook or the jupyterhub terminal only if they are available (you can check this with ``nvidia-smi``).
     
#. SlurmSpawner

    * This spawner relies on Slurm to run your server. You can monitor your job just like any other Slurm job, as described in this guide, with commands such as ``squeue``.

#. ROOT on python, on jupyter: pyROOT and jupyROOT

    * If you are trying to use ROOT in an ipython notebook over jupyter, you might have issues, which are related to missing paths, in particular the path to ``x86_64-conda-linux-gnu-c++``.
    * To fix this, try adding to the PATH of your kernel the ``bin`` directory of the environment. i.e. modify  ``~/.local/share/jupyter/kernel/<YOUR ENVIRONMENT>/kernel.json`` to include:
    
    .. code-block:: sh
    
         "env": {
           "PATH": "/work/submit/<USER>/miniforge3/envs/<YOUR ENVIRONMENT>/bin:${PATH}" 
          }
    
    * N.B.: if you have conda installed elsewhere, your path might be different.

#. IJulia: IJulia is a Julia-language backend combined with the Jupyter interactive environment. Once installed, you can open Jupyterhub and select the Julia 1.6.5 kernel. To install it, in a terminal window, type ``julia``, then

     .. code-block:: julia

          ] # this enters pkg mode
          add IJulia # it will take a few minutes to install the required packages

     Now, if you type ``jupyter kernelspec list`` in a terminal window, you will see

     .. code-block:: sh

          julia-1.6     /home/submit/username/.local/share/jupyter/kernels/julia-1.6

     if it doesn't work, in Julia type ``using Pkg``, then ``Pkg.build("IJulia")``. You should now have the Julia kernel for Jupyterhub.


Wolfram Mathematica
~~~~~~~~~~~~~~~~~~~

Mathematica is easily accessible on ``submit00``. In order to use it for the first time, follow these simple steps:

#. ssh into submit00: ``ssh username@submit00.mit.edu``

#. type ``wolfram``. You should be prompted to enter an activation key, which you can get by requesting one from MIT, following the instructions on the MIT website here: `MIT_Wolfram <https://ist.mit.edu/wolfram/mathematica>`_. Once you have entered the activation key, after a few seconds you should see ``In[1]:=`` and be able to use Mathematica.

Then, anytime you want to use Mathematica, make sure to ssh into submit00 and type ``wolfram`` on the command prompt. When you are done, type ``Quit``, ``Quit[]``, ``Exit``, or ``Exit[]``.

You can easily run scripts (files with extension ``.wls`` and ``.m``) by using one of the following commands, directly into the terminal:

.. code-block:: mathematica

     wolfram -script scriptname.wls
     wolfram -run < scriptname.wls
     wolfram < scriptname.wls
     wolfram -noprompt -run "<<scriptname.wls"

When using scripts, you can use ``Print[]`` statements in your file that will directly appear in the terminal, or use ``Export[]`` to generate plots, for example.

slurm for Mathematica
.....................

You can also submit batch jobs via slurm. In your batch file, make sure to include the line ``#SBATCH --nodelist=submit00``.


Jupyterhub for Mathematica
..........................

If you wish to get an interface similar to a Mathematica notebook (.nb file), you can use WolframLanguageforJupyter. To install, follow these steps:

#. Download the most recent paclet available from `WolframLanguageForJupyter <https://github.com/WolframResearch/WolframLanguageForJupyter/releases>`_ in your home directory.

#. Make sure you are on submit00 and type ``wolfram`` on the command prompt, then

     .. code-block:: mathematica

          (* replace x.y.z by the correct values, e.g. 0.9.3 *)
          PacletInstall["WolframLanguageForJupyter-x.y.z.paclet"] 
          Needs["WolframLanguageForJupyter`"]
          ConfigureJupyter["Add"]
          Quit

#. To test that the installation worked, check whether Wolfram has been added to your list of jupyter kernels by typing ``jupyter kernelspec list`` in the command prompt. You should see

.. code-block:: sh

     wolframlanguage13.2    /home/submit/username/.local/share/jupyter/kernels/wolframlanguage13.2

Now that the kernel is installed, you want to use jupyterhub on ``submit00``. Here's how to do this:

Go to the submit website and open jupyterhub. Choose the job profile to "Slurm for Wolfram Mathematica - submit00 - 1 CPU, 500 MB". The server should start. If you get the error message "Spawn failed: Timeout", it means the CPUs are already busy with other jobs and cannot be used at the moment. You can still use the method below.

You can make sure that you are on submit00 by opening a terminal within the webpage, which should show ``username@submit00.mit.edu``. You can now open a jupyter notebook (.ipynb file), make sure you are using the Wolfram kernel (choose the kernel in the top right of the screen), and use Wolfram syntax as you would in a Wolfram notebook. The outputs will even have the Wolfram fonts!

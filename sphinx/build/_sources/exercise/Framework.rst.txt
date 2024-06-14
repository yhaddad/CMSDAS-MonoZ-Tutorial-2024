.. raw:: html

    <style> 
        .red {color:red;} 
        .black {color:black; text-shadow:none;} 
        .gold {color:#fecb2f;}
    </style>

.. role:: red

.. role:: black

.. role:: gold

Framework
---------

This section will guide you through some of the details of the framework.

Install the Mono-Z framework
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install framework:

.. code-block:: sh

   cmsrel CMSSW_10_6_4 
   cd CMSSW_10_6_4/src 
   cmsenv

   mkdir PhysicsTools/ 
   git clone https://github.com/yhaddad/nanoAOD-tools.git PhysicsTools/NanoAODTools 
   git clone git@github.com:yhaddad/MonoZNanoAOD.git PhysicsTools/MonoZ
   cd $CMSSW_BASE/src/PhysicsTools/MonoZ/
   git checkout remotes/origin/CMSDAS_MonoZ

   cd $CMSSW_BASE/src 
   scram b -j 10


List of backgrounds
~~~~~~~~~~~~~~~~~~~

Main backgrounds:

1. ZZ (Irreducible)
2. WZ (Irreducible)
3. top pair production
4. WW
5. Drell-Yan (DY)
6. Triboson

It's important to define control regions to check that our simulation well describes the backgrounds. We use 4 main backgrounds for this analysis

1. 4 lepton control region (Normalization of ZZ)
2. 3 lepton control region (Normalization of WZ)
3. ElectronMuon control region (Normalization for WW and top pair production)
4. Low pTmiss sideband region (Normalization for DY)

Look at Trees introduction
~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the Mono-Z analysis code (Commands above):

NTuples for 2016 are stored the EOS space we can use:

/eos/user/c/cmsdas/long-exercises/MonoZ/

An example of how to look at a sample root file:

.. code-block:: sh

   cmsenv
   root -l /eos/user/c/cmsdas/long-exercises/MonoZ/CMSDAS_NTuples/ZZTo2L2Nu_13TeV_powheg_pythia8_ext1/tree_0.root

This will open a root session where you can look at a sample file quickly in an interactive session:


.. code-block:: sh
   
    new TBrowser

Each root file contains a TTree called "Events". The trees have many branches, that correspond to single physics variables. They may be have:

1. single floats, for example variables characterising the whole event
2. vectors of variables, for example variables related to a particle type, as pT of the electrons. For these cases, also an an integer defining the size of the vector is present for example "nLepton". The variables are then defined as Collection_variable (e.g. Electron_pt[0]) and the indexing is such that the objects are pT ordered (Object_pt[0] > Object_pt[1] > Object_pt[2] > ...)

The general strategy is the following:

1. **events from the data are required to pass the trigger selections described above (with arbitration described in the following**
2. **in the Monte Carlo simulations (MC) the trigger selection is missing, and it is emulated weighing events with coefficients that mimic the trigger efficiency effect. Weights are used also to correct any residual differences observed between data and MC. All the weights used have to be multiplied, to produce a total weighting factor.**

More information about nanoAOD trees can be found at in the documentation in `NanoAOD <https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html>`_

Some variables have been added in the aforementioned post-processing, for example the combined variable "invariant mass of the two leading pT leptons", Z_mass. If you want to learn more and discover how the variables are built, check here : `Producer <https://github.com/yhaddad/MonoZNanoAOD/blob/master/python/MonoZProducer.py>`_

Lets look at some ROOT commands to make some simple histograms.

Lets start by just looking at the pTmiss distribution directly:

.. code-block:: sh

   Events->Draw("met_pt","","")

Does it make sense? Ok, let's add some simple selections. Let's look at the pTmiss but only for events with 2 electrons with pT>20 GeV:

.. code-block:: sh

   Events->Draw("met_pt","nElectron==2 && Electron_pt[0]>20. && Electron_pt[1]>20.","")

Try to look through the ROOT file and do the same thing as above except for muons. Do they look similar? These commands are very simple but they are often a good way to check things quickly! These Trees also contain several variables that we have added specifically for this analysis. These variables are explained in the next section but one of the most important ones is the mass of the Z boson candidate (Z_mass). Find a sample with a leptonically decaying Z boson (ZZ) and look at this variable.

.. code-block:: sh

   Events->Draw("Z_mass","","")

Find a sample that doesn't have a Z (ttbar). What does it look like there?

Another quick and potentially useful command is to look at both the phi and eta at the same time. Let's look at this for the Z boson candidate:

.. code-block:: sh

   Events->Draw("Z_eta:Z_phi","","colz")

Trees content
~~~~~~~~~~~~~

In addition to the standard variables, we pre-compute in the ntuples several combined kinematic variables, that are useful for the analysis. A set of those variables that are used to define the signal region are shown in the table below.

.. list-table:: Variables in NTuple
   :widths: 30 70
   :header-rows: 1

   * - *Name in NTuple*
     - *Description*
   * - Z_pt
     - Transverse momentum of the Z boson candidate
   * - Z_mass
     - Invariant mass of the Z boson candidate
   * - delta_phi_ll
     - :math:`{\Delta\phi}` between the two leading leptons
   * - delta_R_ll
     - :math:`{\Delta R}` between the two leading leptons
   * - sca_balance
     - The ratio of the difference in the missing transverse momentum and the Z boson candidate momentum. Expect small values for recoiling system
   * - delta_phi_ZMet
     - :math:`{\Delta\phi}` between the Z boson candidate and the missing transverse momentum
   * - delta_phi_j_met
     - :math:`{\Delta\phi}` between the jet candidate and the missing transverse momentum
   * - met_pt
     - The magnitude of the missing transverse momentum. This is Type-1 PF Met with NVtx corrections applied.
   * - MT
     - Transverse mass of the candidate made by the two leading leptons and the MET: :math:`{\sqrt{2p_T^{ll}p_{T}^{miss}(1-cos\Delta\phi_{ll,MET})}}`



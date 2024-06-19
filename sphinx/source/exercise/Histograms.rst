.. raw:: html

    <style> .red {color:red} </style>

.. role:: red

Making Histograms
-----------------

.. image:: ../img/histo.png
      :width: 900
      :alt: Alternative text

An integral part of understanding physics, is finding ways to display data in a way that can be easily understood. One of the fundamental tools in a physicists toolbelt is the histogram which allows us toshow binned data a plethora of different ways. This section will walk you through how to create a histogram using the Mono Z framework. 

An Introduction to Making Histograms from Trees
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Starting from the NTuples we have introduced, we will make histograms for our Control and Signal regions. We will do these for each file filled with NTuples. This means we will need to run our code over a large number of files. In order to make this easier we will submit the jobs on HT Condor and place the output in another directory. These files will only contain the histograms that we want to look at and will be much easier to work with.

The file that will make these histograms can be seen here:
`Producer <https://github.com/yhaddad/CMSDAS-MonoZ-Tutorial-2024/blob/main/processing/dasmonoz/monoz.py>`_.


**In general this code can be split into 3 main categories**

1. The definition of selections for the different regions and their associated binning: `bins <https://github.com/yhaddad/CMSDAS-MonoZ-Tutorial-2024/blob/main/processing/dasmonoz/monoz.py#L97-L229>`_.
2. The weights that will be applied in order to create the histograms. These include the Up and Down variations for our systematics: `weights <https://github.com/yhaddad/CMSDAS-MonoZ-Tutorial-2024/blob/main/processing/dasmonoz/monoz.py#L233-L253>`_.
3. Filling the histograms that we have defined with the weight that we have defined: `Fill <https://github.com/yhaddad/CMSDAS-MonoZ-Tutorial-2024/blob/main/processing/dasmonoz/monoz.py#L44-L76>`_.


For this school, you will want to play with the selections and add in the systematics that need to be added. You can run the code with the following:

.. code-block:: sh

     python3 run-process-local.py --datasets data/datasets-test.yaml

This is a test yaml. Run this to make sure everything in the code works smoothly. If it does then you can move to running the full set of datasets. For this we might need morer cores. Let's try with the full 8 cores. 

.. code-block:: sh

     python3 run-process-local.py --datasets data/datasets-full.yaml --ncores 8

This command will run over all of the files included in the datasets yaml. This includes both data and MC as well as signal. This output should be stored in a pickle which can be used directly to produce datacards as described in the next section of this guide. The rest of this section will give a description of the regions and systematics from this code.

Control Regions in the MonoZ analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We use several control regions to determine the normalizations for the background processes in this analysis. Each control region is designed to isolate a certain process that is seen in the signal region. In addition, the control regions are designed to probe phase spaces with similar kinematic distributions to those seen in the signal region. This is done to ensure that the normalizations are not biassed by effects that are seen in one region and not the other (Such as object efficiencies, triggers, etc.).

The MonoZ analysis uses 4 control regions explained below:

.. list-table:: Control Region Descriptions
   :widths: 20 40 25 25
   :header-rows: 1

   * - **Control Region**
     - **Description**
     - **Processes to model**
     - **# of normalization factors**
   * - 4 Lepton
     - We look at 4 lepton decay with 2 Z boson candidates. We combine one lepton pair and MET to create "emulated MET". This emulated MET should model our SR ZZ.
     - ZZ
     - 3 (low, medium and high MET)
   * - 3 Lepton
     - We look at 3 lepton decay with a Z boson candidate and an additional lepton. We combine information from the lepton and the MET to create "emulated MET". This emulated MET should model our SR WZ.
     - WZ
     - 3 (low, medium and high MET)
   * - Electron and Muon
     - We look as Opposite sign opposite flavor (OSOF) lepton pairs. With a tau veto this means we look at events with an electron and a muon that fall within the Z mass window.
     - Top quark processes and WW
     - 1
   * - Low MET Sideband
     - For Drell-Yan (DY) there is no real MET (no neutrinos) so we look in the signal region but with low MET less than 100 GeV. This low MET region remains dominated with DY since the other backgrounds have real MET.
     - Drell-Yan (DY)
     - 1


For more information on the Control regions and the selections see slides 24-28 `preapproval <https://indico.cern.ch/event/832209/contributions/3486920/attachments/1871948/3085482/Preapproval_EXO-19-003.pdf>`_


Weights and their Variations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The various Event weights that are applied in the analysis are summarized below with brief descriptions. For each weight, variations Up and Down are taken to calculate the effect the uncertainty in the correction.

MC and data ntuples have several weights. MC weights are needed first and foremost to normalize the MC sample to the luminosity of the data. Also, event weights are computed to take into account the different scale factors that we use to improve the description of the data.

.. list-table:: Data vs MC Weights
   :widths: 15 55 15 15
   :header-rows: 1

   * - *name*
     - *description*
     - *available in data*
     - *available in MC*
   * - xsecscale
     - If you weight MC events with this weight you will get MC normalized to 1/fb. In order to normalize to the data luminosity (35.9/fb in 2016) you have to weight MC as XSWeight*35.9. Notice that xsecscale takes into account the effect of negative weight events (sometimes present in NLO MC simulations).
     - **NO**
     - **YES**
   * - puWeight
     - This weight is needed to equalize the Pile-Up profile in MC to that in Data. You need to understand that most of the time the simulation is done before, or at least partly before, the data taking, thus the PU profile in the MC is a guess of what will happen with data. This weight is the ratio of the PU profile in data to that guess that was used when producing the MC.
     - **NO**
     - **YES**
   * - EWK
     - This weight is only applied to Diboson samples of ZZ and WZ. This weight takes into account higher order that are not considered in the original generation. There are LO-->NLO EWK and NLO-->NNLO QCD corrections incorporated in this weight.
     - **NO**
     - **YES**
   * - PDF
     - These are the uncertainties associated with the parton distribution functions (PDF) that are used to generate the samples.
     - **NO**
     - **YES**
   * - QCDScale (0,1,2)
     - Uncertainties calculated by modifying both the normalization and factorization scales. 9 combinations of the two scales at (0.5, 1, 2).
     - **NO**
     - **YES**
   * - MuonSF
     - Weights associated with the scale factors used to correct the muons' pT
     - **YES**
     - **YES**
   * - ElectronSF
     - Weights associated with the scale factors used to correct the electrons' ET
     - **YES**
     - **YES**
   * - PrefireWeight
     - There were some issues with prefiring triggers in the ECAL endcap. These weights correct for the effects caused by this prefiring issue
     - **NO**
     - **YES**
   * - nvtxWeight
     - Discrepancies were seen in the MC/Data distributions for the number of vertices in events. These weights correct for this discrepancy and also have an effect on the MET distribution.
     - **NO**
     - **YES**
   * - TriggerSFWeight
     - These weights correct for inefficiencies in the use of triggers. This weight is always close to one for this analysis due to the use of high-pT lepton triggers
     - **NO**
     - **YES**
   * - bTagEventWeight
     - Weights correspond to the efficiency of the b-tagger efficiency
     - **NO**
     - **YES**
   * - ElectronEn
     - These weights modify the scale of the electron energy
     - **YES**
     - **YES**
   * - MuonEn
     - These weights modify the scale of the muon pT
     - **YES**
     - **YES**
   * - jesTotal
     - These weights modify the Jet energy scale
     - **YES**
     - **YES**
   * - jer
     - These weights modify the jet energy resolution
     - **YES**
     - **YES**

Scale factors (SF) are corrections applied to MC samples to fix imperfections in the simulation. These corrections are derived in data in control regions, meaning in regions where the signal is not present.

The origin of the mis-modelling could be from the hard scattering (theory uncertainty), or from the simulation of the response of particles with the detector (Geant4), or due to the conditions evolution in time in data (the MC has only one set of conditions), such as noise and radiation damage effects on the detectors.

**The SF can be:**

1. object based scale factors
2. event based scale factors

**Object based SF are for example:**

1. lepton identification and isolation efficiency. The identification criteria for leptons could be mis-simulated, then a scale factor is applied
2. jet related scale factors, such as b-tag efficiency mis-modelling

**Event based SF are for example:**

1. normalization of a sample. for example if a new NNLO cross section is available, or if a background normalization is found to be mis-modelled in a control region (a background whose theoretical uncertainty is big)
2. trigger efficiency. The trigger could be mis-modelled. We measure the trigger efficiency "per leg" of the triggers considered (single leptons and double leptons) and combine the efficiency to get the per-event one. We do not require the trigger in the simulation, but apply directly the efficiency to MC events

**Theory Nuisances:**

1. scale choice ((LHEScaleWeight [8]', 'LHEScaleWeight[0]))
2. QCD Scale
3. PDF uncertainty
4. higher order corrections (electroweak)

Do a quick test with one of the systematics listed above

Open 3 root file of signal and do a tree->Draw with:

1. nominal
2. scale up
3. scale down

Learning where these systematics come from can be an important part of an analysis. For systematics related to objects, these are often covered by the Physics object groups (POG). They will often give a prescription with how to correctly calcuate various corrections/uncertainties. See below for some twiki examples:

1. `EGamma POG <https://twiki.cern.ch/twiki/bin/view/CMS/EgammaPOG>`_.
2. `Muon POG <https://twiki.cern.ch/twiki/bin/view/CMS/MuonPOG>`_.
3. `JetMET POG <https://twiki.cern.ch/twiki/bin/view/CMS/JetMET>`_.


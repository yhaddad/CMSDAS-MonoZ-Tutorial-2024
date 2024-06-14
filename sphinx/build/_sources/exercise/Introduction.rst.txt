.. raw:: html

    <style> .red {color:red} </style>

.. role:: red
    

Introduction
-------------

Welcome to the Mono Z page for the CMSDAS Long exercises. These pages will walk you through the Mono Z and give you example code on how the analysis is actually performed.  

Introduction on template analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What is a template analysis and difference w.r.t. parametric analysis.

To do:

1. get a signal ttree
2. for example you can calculate the number events you expect in 35.9/fb, Nsig, after you apply the cut "2 electrons with pt > 20 "

.. code-block:: sh

      "(Electron_pt[0]>20. && Electron_pt[1]>20.)"

3. get a background ttree 
4. calculate number events you expect in 35.9/fb, Nbkg
5. from Nsig and Nbkg calculate the expected significance Nsig/sqrt(Nbkg)
6. Given a number of data events measured Ndata, how do you measure the signal cross section?

Suggestions:

1. You can take a quick look at the missing transverse momentum values for a sampling of events:

.. code-block:: sh
      
      Events->Scan("met_pt")

2. Or we can just draw the distribution for this file directly. Does the distribution make sense for this file? Look at another process and see how it differs.

.. code-block:: sh
      
      Events->Draw("met_pt")

3. Number of events we have analysed

.. code-block:: sh
      
      Runs->Scan("genEventSumw")

You should see an output like below:

.. code-block:: sh

      ************************
      *    Row   * genEventS *
      ************************
      *        0 *    895556 *
      ************************

We will learn more about these files and how to use them later but it is good to familiarize yourself with a couple of the processes now. Take some time to look at the MC background, the MC signal and the data separately.

Introduction on Mono-Z analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For this analysis we are going to be looking for indications of dark matter (dm) being produced by the LHC. Since dm particles will not be seen by the CMS detector, this means our events with dm would have large amounts of missing transverse momentum (pTmiss). The MonoZ analysis focuses on events with a leptonically decaying Z boson that is recoiling against large amounts of missing transverse momentum. Therefore, the final state consists in two charged leptons of opposite charge, same flavor and reconstruct a mass near the known Z boson mass. Tau leptons are unstable and decay either leptonically (in that case we still have an isolated electron or muon) or hadronically, hence difficult to reconstruct. Therefore, the analysis looks at the final stated with electrons and muons only. Additionally, the signal we are looking for has a low amount of hadronic activity, we will only look at events with 0 or 1 recontrsucted jets. Jets that have been flagged as originating from b quarks will also be rejected in oder to reduce the background from top processes.

In order to look for dm we must understand the SM processes that may produce the same final state of the signal. To categorize of background exist: the **irreducible background (ZZ)** is due to all the physics processes that generate exactly the same topology of the signal, while the **reducible background** is due to all those processes that mimic the signal because of faults in the reconstruction. This may happen because of several reasons, typically due to the detector behaviour. For example, hadronic jets may be wrongly identified as charged leptons, or real charged leptons or hadronic jets may not be identified, originating fake MET as if they were neutrinos.

This analysis is a cut and count meaning that we will make selections to try and isolate the signal from the SM background and then used the yield in a binned distribution(s) to calculate the sensitivity and set limits. This twiki will follow the recently published results for Run 2 which can be seen on arXiv here:

`arxiv <https://arxiv.org/abs/2008.04735>`_ 

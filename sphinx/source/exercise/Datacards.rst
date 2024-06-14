Making Datacards
----------------

.. image:: ../img/datacard.png
      :width: 900
      :alt: Alternative text

An important part of an analysis before running combine is the creation of datacards describing the rates, uncertainties and normalizations for the various processes used in the analysis. We have a datacard producer that we run through SWAN that we use for this analysis. Unfortunatly, this is a complicated and time-consuming process so we have created the datacards for you directly. This section will give a description of the creation of these datacards and then a description to understand them.

Mono Z Datacards
~~~~~~~~~~~~~~~~


.. code-block:: html

   imax * number of categories
   jmax * number of samples minus one
   kmax * number of nuisance parameters
   ------------------------------
   shapes * * shapes-chBSM2016.root $PROCESS $PROCESS_$SYSTEMATIC
   bin           chBSM2016
   observation      2236.0
   ------------------------------
   ------------------------------
   bin                                 chBSM2016      chBSM2016      chBSM2016      chBSM2016      chBSM2016      chBSM2016      chBSM2016
   process                             Signal         ZZ             WZ             WW             VVV            TOP            DY
   process                             0              1              2              3              4              5              6
   rate                                151.785        470.638        352.725        74.218         2.589          280.862        811.159
   ------------------------------
   CMS_BTag_2016            shape      1.000          1.000          1.000          1.000          1.000          1.000          1.000
   CMS_EFF_e                shape      1.000          1.000          1.000          1.000          1.000          1.000          1.000
   CMS_EFF_m                shape      1.000          1.000          1.000          1.000          1.000          1.000          1.000
   CMS_JER_2016             shape      1.000          1.000          1.000          1.000          1.000          1.000          1.000
   CMS_JES_2016             shape      1.000          1.000          1.000          1.000          1.000          1.000          1.000
   CMS_PU_2016              shape      1.000          1.000          1.000          1.000          1.000          1.000          1.000
   CMS_QCDScaleSignal_2016  shape      1.000            -              -              -              -              -              -
   CMS_QCDScaleTOP_2016     shape        -              -              -              -              -            1.000            -
   CMS_QCDScaleVVV_2016     shape        -              -              -              -            1.000            -              -
   CMS_QCDScaleWW_2016      shape        -              -              -            1.000            -              -              -
   CMS_QCDScaleWZ_2016      shape        -              -            1.000            -              -              -              -
   CMS_QCDScaleZZ_2016      shape        -            1.000            -              -              -              -              -
   CMS_RES_e                  lnN      1.005          1.005          1.005          1.005          1.005          1.005          1.005
   CMS_RES_m                  lnN      1.005          1.005          1.005          1.005          1.005          1.005          1.005
   CMS_Trig_2016            shape      1.000          1.000          1.000          1.000          1.000          1.000          1.000
   CMS_Vx_2016              shape      1.000          1.000          1.000          1.000          1.000          1.000          1.000
   CMS_lumi_2016              lnN      1.025          1.025          1.025          1.025          1.025          1.025          1.025
   CMS_pfire_2016           shape      1.000            -              -              -              -              -              -
   EWKWZ                    shape        -              -            1.000            -              -              -              -
   EWKZZ                    shape        -            1.000            -              -              -              -              -
   PDF_2016                 shape      1.000          1.000          1.000          1.000          1.000          1.000          1.000
   UEPS                       lnN      1.020          1.020          1.020          1.020          1.020          1.020          1.020
   VVnorm_0_                shape        -            1.000          1.000              -            -              -              -
   VVnorm_1_                shape        -            1.000          1.000              -            -              -              -
   VVnorm_2_                shape        -            1.000          1.000              -            -              -              -
   EMnorm_2016 rateParam chBSM* WW 1 [0.1,10]
   DYnorm_2016 rateParam chBSM* DY 1 [0.1,10]
   chBSM2016 autoMCStats 0 0 1
   EMnorm_2016 rateParam chBSM* TOP 1 [0.1,10]


Understanding the datacards
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A counting experiment is a search where we just count the number of events that pass a selection, and compare that number with the event yields expected from the signal and background.

A shape analysis relies not only on the expected event yields for the signals and backgrounds, but also on the distribution of those events in some discriminating variable. This approach is often convenient with respect to a counting experiment, especially when the background cannot be predicted reliably a-priori, since the information from the shape allows a better discrimination between a signal-like and a background-like excess, and provides an in-situ normalization of the background.

The simpler case of shape analysis is the binned one: the observed distribution of the events in data and the expectations from the signal and all backgrounds are provided as histograms, all with the same binning. Mathematically, this is equivalent to just making N counting experiments, one for each bin of the histogram; however, in practice it's much more convenient to provide the the predictions as histograms directly.

For this kind of analysis, all the information needed for the statistical interpretation of the results is encoded in a simple text file. An example was shown above as the datacard for cards-DMSimp_MonoZLL_Pseudo_500_mxd-1/shapes-chBSM2016.dat. Let's go through the various components of this datacard and try to understand it.

Channels:
*********

These lines describe the basics of the datacard: the number of channels, physical processes, and systematical uncertainties Only the first two words (e.g. imax) are interpreted, the rest is a comment.

1. **imax** defines the number of final states analyzed (one in this case, but datacards can also contain multiple channels)
2. **jmax** defines the number of independent physical processes whose yields are provided to the code, minus one (i.e. if you have 2 signal processes and 5 background processes, you should put 6)
3. **kmax** defines the number of independent systematical uncertainties (these can also be set to * or -1 which instruct the code to figure out the number from what's in the datacard)

You'll notice that in this datacard these numbers are not filled. This is because this datacard is written specifically for the signal region. The full datacard is written in combined.dat and will show these numbers (too long to show here).

.. code-block:: html

   imax * number of categories
   jmax * number of samples minus one
   kmax * number of nuisance parameters

Processes and Rates
*******************

These lines describe the number of observed events in each final state. In this case, there's a final state, with label chBSM2016 that contains the events in our signal region. The observation is the number of data events in this channel. You will also se the background then split into the different processes. Does the observation seem to match the background estimation? Check the rates to see if they make sense.

.. code-block:: html

   shapes * * shapes-chBSM2016.root $PROCESS $PROCESS_$SYSTEMATIC
   bin           chBSM2016
   observation      2236.0
   ------------------------------
   ------------------------------
   bin                                 chBSM2016      chBSM2016      chBSM2016      chBSM2016      chBSM2016      chBSM2016      chBSM2016
   process                             Signal         ZZ             WZ             WW             VVV            TOP            DY
   process                             0              1              2              3              4              5              6
   rate                                151.785        470.638        352.725        74.218         2.589          280.862        811.159

Systematic Uncertainties
************************

The next section deals with the uncertainties and normalizations associated with the different yields. The way systematical uncertainties are implemented in the Higgs statistics package is by identifying each *independent source* of uncertainty, and describing the effect it has on the event yields of the different processes. Each source is identified by a name, and in the statistical model it will be associated with a nuisance parameter.

An individual source of uncertainty can have an effect on multiple processes, also across different channels, and all these effects will be correlated (e.g., the uncertainty on the production cross section for DY will affect the expected event yield for this process in all datacards). While not necessarily problematic for this analysis, the size of the effect doesn't have to be the same, e.g., a 1% uncertainty on the muon resolution might have a 2% effect on WW-->
:math:`{2\mu 2\nu}` but a 4% effect on ZZ-->4l. Anti-correlations are also possible (e.g., an increase in b-tagging efficiency will simultaneously and coherently increase the signal yield in final states that require tagged b-jets and decrease the signal yield in final states that require no tagged b-jets).

The use of names for each source of uncertainty allows the code to be able to combine multiple datacards recognizing which uncertainties are in common and which are instead separate.

The most common model used for systematical uncertainties is the `log-normal distribution <http://en.wikipedia.org/wiki/Log-normal_distribution>`_, which is identified by the *lnN* keyword in combine. The distribution is characterized by a parameter 
:math:`{\kappa}` , and affects the expected event yields in a multiplicative way: a positive deviation of +1
:math:`{\sigma}` corresponds to a yield scaled by a factor 
:math:`{\kappa}` compared to the nominal one, while a negative deviation of -1
:math:`{\alpha}` corresponds to a scaling by a factor 1/
:math:`{\kappa}` . For small uncertainties, the log-normal is approximately a Gaussian. If 
:math:`{\delta}` x/x* is the relative uncertainty on the yield, 
:math:`{\kappa}` can be set to 1+
:math:`{\delta}` x/x.

We can also consider systematical uncertainties that affect not just the normalization but also the shape of the expected distribution for a process. You should recognize some of the shape based systematics from the histograms earlier. The datacard helps tell combine what systematics are associated with various processes and how they are correlated. For example, the JES are applied to all processes and the uncertainty is correlated among the different processes, while the EWK corrections are only applied to the WZ and the ZZ and are uncorrelated. Additionally, if you are using the full Run-2 dataset you could set correlations among the different years here as well.


.. code-block:: html

   CMS_BTag_2016            shape      1.000          1.000          1.000          1.000          1.000          1.000          1.000
   CMS_EFF_e                shape      1.000          1.000          1.000          1.000          1.000          1.000          1.000
   CMS_EFF_m                shape      1.000          1.000          1.000          1.000          1.000          1.000          1.000
   CMS_JER_2016             shape      1.000          1.000          1.000          1.000          1.000          1.000          1.000
   CMS_JES_2016             shape      1.000          1.000          1.000          1.000          1.000          1.000          1.000
   CMS_PU_2016              shape      1.000          1.000          1.000          1.000          1.000          1.000          1.000
   CMS_QCDScaleSignal_2016  shape      1.000            -              -              -              -              -              -
   CMS_QCDScaleTOP_2016 shape       -              -              -              -              -            1.000            -
   CMS_QCDScaleVVV_2016 shape        -              -              -              -            1.000            -              -
   CMS_QCDScaleWW_2016  shape        -              -              -            1.000            -              -              -
   CMS_QCDScaleWZ_2016  shape        -              -            1.000            -              -              -              -
   CMS_QCDScaleZZ_2016  shape        -            1.000            -              -              -              -              -
   CMS_RES_e              lnN      1.005         1.005          1.005          1.005          1.005          1.005          1.005
   CMS_RES_m              lnN      1.005         1.005          1.005          1.005          1.005          1.005          1.005
   CMS_Trig_2016        shape      1.000         1.000          1.000          1.000          1.000          1.000          1.000
   CMS_Vx_2016          shape      1.000         1.000          1.000          1.000          1.000          1.000          1.000
   CMS_lumi_2016          lnN      1.025         1.025          1.025          1.025          1.025          1.025          1.025
   CMS_pfire_2016       shape      1.000           -              -              -              -              -              -
   EWKWZ                shape        -              -            1.000            -              -              -              -
   EWKZZ                shape        -            1.000            -              -              -              -              -
   PDF_2016             shape      1.000         1.000          1.000          1.000          1.000          1.000          1.000
   UEPS                   lnN      1.020         1.020          1.020          1.020          1.020          1.020          1.020
   VVnorm_0_            shape        -            1.000          1.000              -            -              -              -
   VVnorm_1_            shape        -            1.000          1.000              -            -              -              -
   VVnorm_2_            shape        -            1.000          1.000              -            -              -              -

Normalizations
**************

The last section handles the single bin normalization factors for the EMU (Top and WW) and the DY region. For this the normalization is allowed to float anywhere between 0.1 and 10.

.. code-block:: html

   EMnorm_2016 rateParam chBSM* WW 1 [0.1,10]
   DYnorm_2016 rateParam chBSM* DY 1 [0.1,10]
   chBSM2016 autoMCStats 0 0 1
   EMnorm_2016 rateParam chBSM* TOP 1 [0.1,10]


Take some time to look through the datacards for the other channels (control regions). Do they make sense to you? Can you follow some of the systematics and see why they are applied to certain processes and not to others. What about the correlations? The next step would be to look at the combined.dat which combines all of the signal and control regions. These are much bigger but contain the same information. Does the combined datacard make sense? We will be using this as input to combine so make sure these are clear to you.


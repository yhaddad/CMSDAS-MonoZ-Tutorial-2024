Results
-------

This last section is about the outputs of combine and how to use them to make a limit plot. This plot will take into account not only the observed and expected limits but also the 1 and 2 sigma bands.

Limits
~~~~~~

We will need to run limits for all of the models we want to look at which in this case is the DM models. For Axial-vector and vector models we published the limits in a 2D plot showing the limits for both the mediator and dm particle mass. This kind of limit plot is complicated to make from the limits attained from combine. For the Scalar and Pseudoscalar models, we can show the limits in a slightly easier way. For these 2 models we will show the signal strengths direcetly as a function of the mediator mass. You will notice that the dm samples are created with several different mass points. What we will do is to find the limit for each of these mass points and then we will interpolate between the limits to get a smooth limit. This is described in the next section.

For more information on how the limits are calulated you can see these `slides <https://indico.cern.ch/event/637941/contributions/2606105/attachments/1510179/2358420/limits_statistics_201708_sonneveld.pdf>`_.

Plotting Limits
~~~~~~~~~~~~~~~
	  
Once we have all the limits for the dark matter samples we can plot the limits as a function of the mediator mass. Lets do this for the scalar and pseudoscalar models. The example code to plot these limits can be found in file limits-DM-CMSDAS.ipynb in the long exercise directory. You can open this in SWAN as well.

Here, we are plotting the mu value directly for each of the different mediator masses that we created samples for. We interpolate between points in order to get a full distribution. This is done for the expected limits (without data and using toys) and for the observed limits (which are the data). Do the expected and observed limits seem to be close to each other? What would it mean if the observed is higher? What about lower?

Can you modify this code to do a similar limit for just the mediator mass of the vector and axial-vector models? There are several samples with a dm particle mass set to 1 GeV. Try with the vector and axial-vector models.

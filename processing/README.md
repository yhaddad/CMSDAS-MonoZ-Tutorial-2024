
The code need to completed, there are missing systematics missing to be completed by the students 

Running the code locally you can do
```bash 
python brew-coffea-local.py
```

Few points to address before releasing the code: 

1. Run over all the data and make a list of the files
2. Run the code with the singularity image, for the moment I run this with the conda env
3. Save the histograms into a pickled file or similar format
4. Run the DCtools to make datacards and run the combine on them

Possible enhancements:
1. running on lxplus HTCondor, maybe dask? to be checked 

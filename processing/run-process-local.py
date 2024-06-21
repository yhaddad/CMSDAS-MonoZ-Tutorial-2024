from coffea.nanoevents import NanoEventsFactory, BaseSchema
from coffea.dataset_tools import (
    apply_to_fileset,
    max_chunks,
    preprocess,
)

import argparse
import copy
import dask
import gzip, pickle, json
import pprint
import warnings
import yaml
from matplotlib.pyplot import hist
from dask.diagnostics import ProgressBar
from dask.distributed import Client
from dasmonoz.monoz import MonoZ
from dasmonoz.sumw import EventSumw

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-jobs' , '--jobs'  , type=int, default=10    , help="")
    parser.add_argument('-era'    , '--era' , type=str, default="2018", help="")
    parser.add_argument('--datasets', type=str, default='./data/datasets.yaml', help='input dataset yaml')
    parser.add_argument('--preprocessed', action='store_true', help='load preprocessed datasets saved in json form (skip preprocessing again): may not catch files that have become inaccessible since preprocessing')
    parser.add_argument('-max_chunks', '--max_chunks', type=int, default=100, help="limit number of chunks per-file to this number at most")
    parser.add_argument('-ncores', '--ncores', type=int, default=1, help="Number of cores to run dask on locally: 1 uses default scheduler, more creates a distributed LocalCluster")
     
    options  = parser.parse_args()
    
    datasets:dict = dict()
    with open(options.datasets, 'r') as f:
        try:
            datasets = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)    
    
    
    datasets_sumw = copy.deepcopy(datasets)
    datasets_simu = copy.deepcopy(datasets)
    datasets_data = copy.deepcopy(datasets)
    
    for dataset in datasets:
        datasets_sumw[dataset]["files"] = {k: "Runs" for k in datasets[dataset]["files"]}
    
    datasets_sumw = {k:v for k,v in datasets_sumw.items() if v["metadata"]["is_mc"]}
    datasets_simu = {k:v for k,v in datasets_simu.items() if v["metadata"]["is_mc"]}
    datasets_data = {k:v for k,v in datasets_data.items() if "Run20" in k}

    print(datasets_data.keys())
    print(datasets_sumw.keys())
    print(datasets_simu.keys())

    weight_syst_list = ["puWeight", "PDF", "MuonSF", "ElecronSF", "EWK", "nvtxWeight", "TriggerSFWeight", "btagEventWeight",
                        "QCDScale0w", "QCDScale1w", "QCDScale2w"]
    shift_syst_list = ["ElectronEn", "MuonEn", "jesTotal", "jer"]
    
    if options.ncores > 1:
        warnings.filterwarnings("ignore")
        client = Client(processes=True, threads_per_worker=1, n_workers=options.ncores, memory_limit='4GB')
        print("Dashboard:", client.dashboard_link)

    
    print("Processing Sumw ... ")
    for i, c in datasets_sumw.items():
        print(i, len(c['files']))
  
    sumw_runnable, _ = preprocess(
            datasets_sumw, 
            align_clusters=False, 
            step_size=100_000, 
            files_per_batch=1,
            skip_bad_files=True, 
            save_form=True,
    )
          
    sumw_compute = apply_to_fileset(
            EventSumw(), max_chunks(sumw_runnable, options.max_chunks),
            schemaclass=BaseSchema,
    )
    (sumw,) = dask.compute(sumw_compute)
     
    print("Processing MC Events ... ")
    for i, c in datasets_simu.items():
        print(i, len(c['files']))
  
    dataset_simu_runnable, _ = preprocess(
        datasets_simu, 
        align_clusters=False, 
        step_size=100_000, 
        files_per_batch=1,
        skip_bad_files=True,
        save_form=True,
    )

    event_simu_compute = apply_to_fileset(
        MonoZ(weight_syst_list=weight_syst_list, shift_syst_list=shift_syst_list),
        max_chunks(dataset_simu_runnable, options.max_chunks),
        schemaclass=BaseSchema,
        #uproot_options={"allow_read_errors_with_report": (OSError,IndexError)}
    )
    (histograms_simu,) = dask.compute(event_simu_compute)
    
    print(histograms_simu)

    print("Processing Data Events ... ")
    for i, c in datasets_data.items():
        print(i, len(c['files']))

    dataset_data_runnable, _ = preprocess(
        datasets_data, 
        align_clusters=False, 
        step_size=100_000, 
        files_per_batch=1,
        skip_bad_files=True,
        save_form=True,
    )

    event_data_compute = apply_to_fileset(
        MonoZ(weight_syst_list=weight_syst_list, shift_syst_list=shift_syst_list),
        max_chunks(dataset_data_runnable, 300),
        schemaclass=BaseSchema,
    )

    (histograms_data,) = dask.compute(event_data_compute)

   
    
    bh_output = {}
    for key, content in histograms_simu.items():
        bh_output[key] = {
            "hist": content,
            "sumw": sumw[key],
        }

    for key, content in histograms_data.items():
        bh_output[key] = {
            "hist": content,
            "sumw": -1.0
        }

    print(bh_output)

    with gzip.open("histograms.pkl.gz", "wb") as f:
        pickle.dump(bh_output, f)

    
    
    

if __name__ == "__main__":
    # This progress bar should work for local dask clusters; for dask.distributed, try the dask.distributed.progress function instead
    ProgressBar().register()
    main()


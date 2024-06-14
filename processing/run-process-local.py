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
import yaml
from matplotlib.pyplot import hist
from dask.diagnostics import ProgressBar
from dask.distributed import Client, progress
dask.config.set({'logging.distributed': 'error'}) # disable warnings about garbage collection when running with multiple cores

from dasmonoz.monoz import MonoZ
from dasmonoz.sumw import EventSumw


def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-jobs' , '--jobs'  , type=int, default=10    , help="")
    parser.add_argument('-era'    , '--era' , type=str, default="2018", help="")
    parser.add_argument('--datasets', type=str, default='./data/datasets.yaml', help='input dataset yaml')
    parser.add_argument('--preprocessed', type=bool, default=False, help='load preprocessed datasets saved in json form (skip preprocessing again): may not catch files that have become inaccessible since preprocessing')
    parser.add_argument('-max_chunks', '--max_chunks', type=int, default=300, help="limit number of chunks per-file to this number at most")
    parser.add_argument('-ncores', '--ncores', type=int, default=1, help="Number of cores to run dask on locally: 1 uses default scheduler, more creates a distributed LocalCluster")
     
    options  = parser.parse_args()

    # uncommment for testing the code using two files
    # basedir = "file://data/"
    # datasets: dict = {
    #     "DM": {
    #         "files": {
    #             f"{basedir}testfile.root": "Events",
    #             f"{basedir}tree_0.root": "Events",
    #         },
    #         'metadata':{
    #             'era': options.era,
    #             'is_mc': True 
    #         }
    #     }
    # }
    # pprint.pprint(datasets)
    
    datasets:dict = dict()
    with open(options.datasets, 'r') as f:
        try:
            datasets = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)    
    # pprint.pprint(datasets[list(datasets.keys())[0]])
    for i, c in datasets.items():
        print(i, len(c['files']))
        
    # Now lets setup to process the sum of weights
    # Here we change from the Event tree to Runs, that contains the SumW
    sumwdatasets = copy.deepcopy(datasets)

    for dataset in datasets:
        sumwdatasets[dataset]["files"] = {k: "Runs" for k in datasets[dataset]["files"]}

    

    weight_syst_list = ["puWeight", "PDF", "MuonSF", "ElecronSF", "EWK", "nvtxWeight", "TriggerSFWeight", "btagEventWeight",
            "QCDScale0w", "QCDScale1w", "QCDScale2w"]
    shift_syst_list = ["ElectronEn", "MuonEn", "jesTotal", "jer"]
    
    # originaldataset = copy.deepcopy(datasets)
    # originalsumwdataset = copy.deepcopy(sumwdatasets)
    # for dataset in originaldataset:
    #     if "DoubleEG_Run2016B_ver2-Nano1June2019_ver2-v1" not in dataset:
    #         continue
    #     datasets = {dataset: originaldataset[dataset]}
    #     sumwdatasets = {dataset: originalsumwdataset[dataset]}
        
    #     print(dataset)

    if options.ncores > 1:
        client = Client(processes=True, threads_per_worker=1, n_workers=options.ncores, memory_limit='4GB')
        print("Dashboard:", client.dashboard_link)

    
    if options.preprocessed:
        print("Loading preprocessed datasets from gzipped json")

        # Events trees
        output_file = "event_compute"
        with gzip.open(f"{output_file}_runnable.json.gz", "rt") as file:
            dataset_runnable = json.load(file)
        with gzip.open(f"{output_file}_all.json.gz", "rt") as file:
            dataset_updated = json.load(file)
        # Runs trees
        output_file = "sumw_compute"
        with gzip.open(f"{output_file}_runnable.json.gz", "rt") as file:
            sumw_runnable = json.load(file)
        with gzip.open(f"{output_file}_all.json.gz", "rt") as file:
            sumw_updated = json.load(file)
    else:
        print("Preprocessing Events Trees")
        dataset_runnable, dataset_updated = preprocess(
            datasets, align_clusters=False, step_size=100_000, files_per_batch=1,
            skip_bad_files=True, save_form=False,
        )
        output_file = "event_compute"
        with gzip.open(f"{output_file}_runnable.json.gz", "wt") as file:
            print(f"Saved runnable fileset chunks to {output_file}_runnable.json.gz")
            json.dump(dataset_runnable, file, indent=2)
        with gzip.open(f"{output_file}_all.json.gz", "wt") as file:
            print(f"Saved all fileset chunks to {output_file}_all.json.gz")
            json.dump(dataset_updated, file, indent=2)

        print("Preprocessing Runs Trees")
        sumw_runnable, dataset_updated = preprocess(
            sumwdatasets, align_clusters=False, step_size=100_000, files_per_batch=1,
            skip_bad_files=True, save_form=True,
        )
        output_file = "sumw_compute"
        with gzip.open(f"{output_file}_runnable.json.gz", "wt") as file:
            print(f"Saved runnable fileset chunks to {output_file}_runnable.json.gz")
            json.dump(dataset_runnable, file, indent=2)
        with gzip.open(f"{output_file}_all.json.gz", "wt") as file:
            print(f"Saved all fileset chunks to {output_file}_all.json.gz")
            json.dump(dataset_updated, file, indent=2)
            
    
    print("Building TaskGraph for Events Trees")
    event_compute, rep_compute = apply_to_fileset(
        MonoZ(weight_syst_list=weight_syst_list, shift_syst_list=shift_syst_list),
        max_chunks(dataset_runnable, options.max_chunks),
        schemaclass=BaseSchema,
        uproot_options={"allow_read_errors_with_report": (OSError,IndexError)}
    )
    

    print("Building TaskGraph for Runs Trees")
    sumw_compute = apply_to_fileset(
        EventSumw(),
        max_chunks(sumw_runnable, options.max_chunks),
        schemaclass=BaseSchema,
    )
        
    print("Processing TaskGraphs")    
    # (histograms, sumw, report) = dask.compute(event_compute, sumw_compute, rep_compute)
    (histograms, report) = dask.compute(event_compute, rep_compute)
    print("Done")

    bh_output = {}
    for key, content in histograms.items():
        bh_output[key] = {
            "hist": content,
            "sumw": sumw[key],
        }

    print(bh_output)

    with gzip.open("histograms.pkl.gz", "wb") as f:
        pickle.dump(bh_output, f)

    
    
    

if __name__ == "__main__":
    # This progress bar should work for local dask clusters; for dask.distributed, try the dask.distributed.progress function instead
    ProgressBar().register()
    main()


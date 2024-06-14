from coffea.nanoevents import NanoEventsFactory, BaseSchema
from coffea.dataset_tools import (
    apply_to_fileset,
    max_chunks,
    preprocess,
)

import argparse
import dask
import gzip, pickle
from matplotlib.pyplot import hist

from dasmonoz.monoz import MonoZ
from dasmonoz.sumw import EventSumw


def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-jobs' , '--jobs'  , type=int, default=10    , help="")
    parser.add_argument('-era'    , '--era' , type=str, default="2018", help="")
    
    options  = parser.parse_args()

    basedir = "file://data/"

    inputfiles: dict = {
        "DM": {
            "files": {
                f"{basedir}testfile.root": "Events",
                f"{basedir}tree_0.root": "Events",
            },
            'metadata':{
                'era': options.era,
                'is_mc': True 
            }
        }
    }

    weight_syst_list = ["puWeight", "PDF", "MuonSF", "ElecronSF", "EWK", "nvtxWeight", "TriggerSFWeight", "btagEventWeight",
            "QCDScale0w", "QCDScale1w", "QCDScale2w"]
    shift_syst_list = ["ElectronEn", "MuonEn", "jesTotal", "jer"]

    dataset_runnable, dataset_updated = preprocess(
        inputfiles, align_clusters=False, step_size=100_000, files_per_batch=1,
        skip_bad_files=True, save_form=False,
    )

    event_compute = apply_to_fileset(
        MonoZ(weight_syst_list=weight_syst_list, shift_syst_list=shift_syst_list),
        max_chunks(dataset_runnable, 300),
        schemaclass=BaseSchema,
    )

    (histograms,) = dask.compute(event_compute)
    
    # Now let process the sum of weights
    # Here we change from the Event tree to Runs, that contains the SumW

    inputfiles["DM"]["files"] = {k: "Runs" for k in inputfiles["DM"]["files"]}

    sumw_runnable, dataset_updated = preprocess(
        inputfiles, align_clusters=False, step_size=100_000, files_per_batch=1,
        skip_bad_files=True, save_form=False,
    )

    sumw_compute = apply_to_fileset(
        EventSumw(),
        max_chunks(sumw_runnable, 300),
        schemaclass=BaseSchema,
    )

    (sumw,) = dask.compute(sumw_compute)

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
    main()


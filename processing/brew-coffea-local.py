from coffea.nanoevents import NanoEventsFactory, BaseSchema
from coffea.dataset_tools import (
    apply_to_fileset,
    max_chunks,
    preprocess,
)

import argparse
import dask

from dasmonoz.monoz import MonoZ

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-jobs' , '--jobs'  , type=int, default=10    , help="")
    parser.add_argument('-era'    , '--era' , type=str, default="2018", help="")
    
    options  = parser.parse_args()

    filename = "file:///Users/yacinehaddad/work/smp/CMSDAS-MonoZ-Tutorial-2024/processing/data/testfile.root"

    fileset = {
        "DM": {
            "files": {
                filename: "Events",
            }
        }
    }
    dataset_runnable, dataset_updated = preprocess(
        fileset, align_clusters=False, step_size=100_000, files_per_batch=1,
        skip_bad_files=True, save_form=False,
    )

    to_compute = apply_to_fileset(
        MonoZ(isMC=True),
        max_chunks(dataset_runnable, 300),
        schemaclass=BaseSchema,
    )
    (out,) = dask.compute(to_compute)
    print(out)

if __name__ == "__main__":
    main()


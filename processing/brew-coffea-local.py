from coffea import processor
from coffea import nanoevents
from ristretto.coffea_vbs import coffea_vbs
import yaml
import argparse
import pickle
import numpy as np

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-jobs' , '--jobs'  , type=int, default=10    , help="")
    parser.add_argument('-era'    , '--era' , type=str, default="2018", help="")
    
    options  = parser.parse_args()

    samples = {}
    with open('./data/input-NanoAOD-2018UL-Mandalorian-test.yaml') as s_file:
        samples = yaml.full_load(s_file)

    cutflow_input = {}
    with open('data/cutflow.yaml') as cutfn:
        cutflow_input = yaml.full_load(cutfn)

    vbs_out = processor.run_uproot_job(
            samples,
            processor_instance=coffea_vbs(
                syst_scales_list=v_syst_list,
                syst_weight_list=w_syst_list,
                selections=cutflow_input,
            ),
            treename='Events',
            executor=processor.futures_executor,
            executor_args={
                "schema": nanoevents.BaseSchema,
                "workers": options.jobs,
            },
    )
    #
    # sumw_out = processor.run_uproot_job(
    #         samples,
    #         treename="Runs",
    #         processor_instance=coffea_sumw(),
    #         executor=processor.futures_executor,
    #         executor_args={
    #             "schema": nanoevents.BaseSchema,
    #             "workers": options.jobs
    #         },
    # )
    
    # append the sumw on the boost histograms
    bh_output = {}

    for key, content in vbs_out.items():
        bh_output[key] = {
            "hist": content,
            #"sumw": sumw_out[key]
    }

    with open("histogram-zz2l2nu-ristretto-test.pkl", "wb") as f:
        pickle.dump(bh_output, f)


if __name__ == "__main__":
    main()


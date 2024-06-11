from coffea import processor
from coffea import nanoevents
from ristretto.coffea_sumw import coffea_sumw
from ristretto.coffea_vbs import coffea_vbs

# Dask Stuff
from dask.distributed import Client
import os
import yaml
import argparse
import pickle
import socket

# turn off the warning messages form TF
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-jobs', '--jobs', type=int, default=10    , help="")
    parser.add_argument('-era' , '--era' , type=str, default="2018", help="")
    
    options  = parser.parse_args()
    client = Client(
            n_workers=options.jobs,
            threads_per_worker=options.jobs
    )

    print('------------------------------------')
    print('dask client based on HTCondorCluster')
    print(client)
    print('Socket  : ', socket.socket)
    print('------------------------------------')


    samples = {}
    with open('data/input-NanoAOD-2018UL-Mandalorian.yaml') as s_file:
        samples = yaml.full_load(s_file)


    executor = processor.DaskExecutor(client=client)
    run = processor.Runner(
            executor=executor,
            schema=nanoevents.BaseSchema,
    )

    # this is the list of systematics used in 2l2nu analysis
    v_syst_list = [
            "ElectronEn", "MuonEn", "jesTotal", "jer"
    ]
    w_syst_list = [
            "puWeight", "PDF", "MuonSF", "ElecronSF", 
            "EWK", "nvtxWeight","TriggerSF", "BTagSF",
            "QCDScale0", "QCDScale1", "QCDScale2"
    ]
        
    cutflow_input = {}
    with open('data/cutflow.yaml') as cutfn:
        cutflow_input = yaml.full_load(cutfn)

    vbs_out = run(
        samples,
        treename="Events",
        processor_instance=coffea_vbs(
            syst_scales_list=v_syst_list,
            syst_weight_list=w_syst_list,
            selections=cutflow_input,
            model_2j='./nn2j-mandalorian.onnx',
            model_3j='./nn3j-mandalorian.onnx'
        ),
        chunksize=10000
    )
        
    # Sumw processor / should be the fastest
    sumw_out = run(
        samples,
        treename="Runs",
        processor_instance=coffea_sumw(),
        chunksize=10000
    )
        
    # append the sumw on the boost histograms
    bh_output = {}

    for key, content in vbs_out.items():
        bh_output[key] = {
            "hist": content,
            "sumw": sumw_out[key]
        }

    with open("histogram-zz2l2nu-ristretto.pkl", "wb") as f:
        pickle.dump(bh_output, f)


if __name__ == "__main__":
    main()


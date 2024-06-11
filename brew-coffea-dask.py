from coffea import processor
from coffea import nanoevents
from ristretto.coffea_sumw import coffea_sumw
from ristretto.coffea_vbs import coffea_vbs
from dask_jobqueue.htcondor import HTCondorCluster
from dask.distributed import Client
import socket
import yaml
import numpy as np
import argparse
import pickle
import gzip

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-jobs' , '--jobs', type=int, default=200   , help="")
    parser.add_argument('-era'  , '--era' , type=str, default="2018", help="")  
    parser.add_argument('-nt'   , '--ntry', type=int, default= 10, help="")
    options = parser.parse_args()
 
    cluster = HTCondorCluster(
        cores=1, # This should be forced to 1 core
        memory='10GB',
        disk='20GB',
        death_timeout = '60',
        nanny = False,
        scheduler_options={
            'port': 8786,
            'host': f"{socket.gethostname()}"
        },
        job_extra={
            'log'   : 'dask_job_output.log',
            'output': 'dask_job_output.out',
            'error' : 'dask_job_output.err',
            'transfer_input_files'   : './data/nn2j-mandalorian.onnx,./data/nn3j-mandalorian.onnx,./data/trigger-sf-table-2018.npy',
            'should_transfer_files'  : 'YES',
            'when_to_transfer_output': 'ON_EXIT',
            '+JobFlavour'            : '"tomorrow"',
        },
        extra = ['--worker-port 10000:10100']
    )

    client = Client(cluster)
    cluster.scale(jobs=options.jobs)

    print('------------------------------------')
    print('dask client based on HTCondorCluster')
    print(client)
    print('Socket  : ', socket.socket)
    print(cluster.job_script())
    print('------------------------------------')

    samples = {}
    with open('./data/input-NanoAOD-2018UL-Mandalorian.yaml') as s_file:
        samples = yaml.full_load(s_file)

    for proc, cont in samples.items():
        print(proc, " --> #files = {}".format(len(cont['files'])) )

    trigger_sf_map = np.load('./data/trigger-sf-table-2018.npy')
    
    print('trigger map')
    print(trigger_sf_map)
    print('-----------')
    
    # this is the list of systematics used in 2l2nu analysis
    v_syst_list = [
            "ElectronEn", "MuonEn", "jesTotal", "jer"
    ]
    w_syst_list = [
        "puWeight", "PDF", "MuonSF", 
        "ElecronSF", "EWK", "nvtxWeight",
        "TriggerSF", "BTagSF",
        "QCDScale0", "QCDScale1", "QCDScale2"
    ]

    cutflow_input = {}
    with open('data/cutflow.yaml') as cutfn:
        cutflow_input = yaml.full_load(cutfn)

    
    import time
    while len(client.ncores()) < 4:
        print('   -- waiting for more cores to spin up: {0} available'.format(len(client.ncores())))
        print('   -- Dask client info ->', client)

        time.sleep(10)

    
    sumw_out = processor.run_uproot_job(
        samples,
        treename="Runs",
        processor_instance=coffea_sumw(),
        executor=processor.dask_executor,
        executor_args={
            "client": client,
            "align_clusters": True,
        },
        chunksize=50000,
    )

    vbs_out = processor.run_uproot_job(
        samples,
        processor_instance=coffea_vbs(
            syst_scales_list=v_syst_list,
            syst_weight_list=w_syst_list,
            selections=cutflow_input,
            model_2j='./nn2j-mandalorian.onnx',
            model_3j='./nn3j-mandalorian.onnx',
            trigger_sf=trigger_sf_map # trigger SF map
        ),
        treename='Events',
        executor=processor.dask_executor,
        executor_args={
            "client": client,
            "schema": nanoevents.BaseSchema,
            'align_clusters': True,
        },
        chunksize=50000,
    )
    # append the sumw on the boost histograms
    bh_output = {}

    for key, content in vbs_out.items():
        bh_output[key] = {
            "hist": content,
            "sumw": sumw_out[key]
    }

    with gzip.open("histogram-vbs-zz-2018.pkl.gz", "wb") as f:
        pickle.dump(bh_output, f)

    print(bh_output)

if __name__ == "__main__":
    main()


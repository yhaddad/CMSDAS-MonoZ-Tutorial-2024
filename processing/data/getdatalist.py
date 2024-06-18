import os
from time import process_time
import yaml
import uproot

def list_files(directory, data_dir):
    process_files = {}
    for root, dirs, files in os.walk(directory):
        print(f" --> {root}")
        for file in files:
            fields = set()
            if file.endswith(".root"):
                process_name = os.path.basename(root)
                
                if process_name not in process_files:
                    process_files[process_name] = {}
                
                file_path = os.path.join(root, file)
                with uproot.open(f"file://{file_path}:Events") as events:
                    fields = set(events.keys())
                    if events.num_entries > 0:
                        if 'Run20' in file_path:
                            process_files[process_name][f"file://{os.path.join(data_dir, process_name, file)}"] = "Events"
                            print(f"file://{os.path.join(data_dir, process_name, file)}")
                        else:
                            process_files[process_name][f"file://{file_path}"] = "Events"
                    else:
                        print(" --> no events !!")

    return process_files

def write_yaml(process_files):
    data = {}
    print("writing the files ... ")
    for process, files in process_files.items():
        data[process] = {
            'files': files,
            'metadata': {
                'is_mc': False if 'Run20' in process else True
            }
        }
        
    with open(f'datasets.yaml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

if __name__ == "__main__":
    directory = "/eos/user/c/cmsdas/long-exercises/MonoZ/CMSDAS_NTuples/"
    data_dir = "/eos/user/c/cmsdas/long-exercises/MonoZ/CMSDAS_NTuples/"
    #data_dir = "/eos/user/c/cmsdas/2024/long-ex-exo-monoz/datasets/"
    process_files = list_files(directory, data_dir)
    write_yaml(process_files)

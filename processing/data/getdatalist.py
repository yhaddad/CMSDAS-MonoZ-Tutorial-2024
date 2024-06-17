import os
import yaml
import uproot

def list_files(directory):
    process_files = {}
    for root, dirs, files in os.walk(directory):
        if 'merged' in root: continue
        print(f" --> {root}")
        for file in files:
            if file.endswith(".root"):
                process_name = os.path.basename(root)
                
                if process_name not in process_files:
                    process_files[process_name] = {}
                
                file_path = os.path.join(root, file)
                # check if the file has events
                process_files[process_name][f"file:/{file_path}"] = "Events"
                #with uproot.open(f"file://{file_path}:Events") as events:
                #    if events.num_entries > 0:
                #    else:
                #        print(f"{file} : {events.num_entries}")
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
    process_files = list_files(directory)
    write_yaml(process_files)

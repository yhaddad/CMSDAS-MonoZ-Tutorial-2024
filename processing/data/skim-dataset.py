import uproot
import uproot.writing
import os
import yaml
import ROOT
import numpy as np

def filter_and_save(input_file, output_file):
    # Open the input ROOT file
    input_f = ROOT.TFile.Open(input_file, "READ")
    input_tree = input_f.Get("Events")
    
    # Create an output ROOT file
    output_f = ROOT.TFile.Open(output_file, "RECREATE")
    
    # Copy all objects except the Events tree
    input_f.cd()
    for key in ROOT.gDirectory.GetListOfKeys():
        key_name = key.GetName()
        if key_name == "Events":
            continue
        obj = key.ReadObj()
        output_f.cd()
        obj.Write(key_name)
    
    # Create a new Events tree in the output file
    output_f.cd()
    output_tree = ROOT.TTree("Events", "Filtered Events Tree")
    
    # Prepare the buffers for the branches to be kept
    branch_buffers = {}
    for branch in input_tree.GetListOfBranches():
        branch_name = branch.GetName()
        if not branch_name.startswith("HLT_"):
            leaf = branch.GetLeaf(branch_name)
            dtype = leaf.GetTypeName()
            if dtype == "Int_t":
                branch_buffers[branch_name] = np.zeros(1, dtype=np.int32)
            elif dtype == "Float_t":
                branch_buffers[branch_name] = np.zeros(1, dtype=np.float32)
            elif dtype == "Double_t":
                branch_buffers[branch_name] = np.zeros(1, dtype=np.float64)
            elif dtype == 'Bool_t':
                branch_buffers[branch_name] = np.zeros(1, dtype=bool)
            else:
                #print(f"Unhandled type: {dtype} for branch {branch_name}")
                continue
            output_tree.Branch(branch_name, branch_buffers[branch_name], f"{branch_name}/{dtype[0]}")

    # Copy the entries from the input tree to the output tree
    for entry in range(input_tree.GetEntries()):
        input_tree.GetEntry(entry)
        for branch_name, buffer in branch_buffers.items():
            leaf = input_tree.GetLeaf(branch_name)
            buffer[0] = leaf.GetValue(0) if leaf.GetLenStatic() == 1 else list(leaf)
        output_tree.Fill()
    
    # Write the new Events tree to the output file
    output_tree.Write()
    
    # Close the files
    output_f.Close()
    input_f.Close()


def list_files(directory, output_dir): 
    process_files = {}
    for root, dirs, files in os.walk(directory):
        if 'merged' in root: continue
        if 'Run20' not in root: continue

        process_name = os.path.basename(root)

        process_output_dir = os.path.join(output_dir, process_name)
        if not os.path.exists(process_output_dir):
            os.makedirs(process_output_dir)
        print('--> process_name : ', process_name)
        for file in files:
            if file.endswith(".root"):
                if process_name not in process_files:
                    process_files[process_name] = {}
                filter_and_save(os.path.join(root, file), os.path.join(process_output_dir, file))
                file_path = os.path.join(process_output_dir, file)
                process_files[process_name][f"file:/{file_path}"] = "Events"
    
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
        
    with open(f'datasets-full.yaml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


if __name__ == "__main__":
    directory = "/eos/user/c/cmsdas/long-exercises/MonoZ/CMSDAS_NTuples/"  
    output_dir = '/eos/user/c/cmsdas/2024/long-ex-exo-monoz/datasets/'

    process_files = list_files(directory, output_dir)
    write_yaml(process_files)

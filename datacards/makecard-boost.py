import yaml
import os
import json
import gzip
import pickle
import argparse
import dctools
import hist
import matplotlib.pyplot as plt
from dctools import plot as plotter
from typing import Any, IO
import numpy as np

class config_input:
    def __init__(self, cfg):
        self._cfg = cfg 
    
    def __getitem__(self, key):
        v = self._cfg[key]
        if isinstance(v, dict):
            return config_input(v)

    def __getattr__(self, k):
        try:
            v = self._cfg[k]
            if isinstance(v, dict):
                return config_input(v)
            return v
        except:
            return None
    def __iter__(self):
        return iter(self._cfg)



class config_loader(yaml.SafeLoader):
    """YAML Loader with `!include` constructor."""
    def __init__(self, stream: IO) -> None:
        """Initialise Loader."""
        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir
        super().__init__(stream)


def construct_include(loader: config_loader, node: yaml.Node) -> Any:
    """Include file referenced at node."""
    filename = os.path.abspath(os.path.join(loader._root, loader.construct_scalar(node)))
    extension = os.path.splitext(filename)[1].lstrip('.')

    with open(filename, 'r') as f:
        if extension in ('yaml', 'yml'):
            return yaml.load(f, config_loader)
        elif extension in ('json', ):
            return json.load(f)
        else:
            return ''.join(f.readlines())

yaml.add_constructor('!include', construct_include, config_loader)

def main():
    parser = argparse.ArgumentParser(description='The Creator of Combinators')
    parser.add_argument("-i"  , "--input"   , type=str , default="./config/input_DAS_2016.yaml")
    parser.add_argument("-v"  , "--variable", type=str , default="nnscore")
    parser.add_argument("-y"  , "--era"     , type=str , default='2018')
    parser.add_argument("-c"  , "--channel" , nargs='+', type=str)
    parser.add_argument("-s"  , "--signal"  , nargs='+', type=str)
    parser.add_argument('-n'  , "--name"    , type=str , default='')
    parser.add_argument('-p'  , "--plot"    , action="store_true")
    parser.add_argument('--rebin', type=int, default=1, help='rebin')
    parser.add_argument("--bins", 
            type=lambda s: [float(item) for item in s.split(',')], 
            help='input a comma separated list. ex: --bins="-1.2,0,1.2"'
    )
    parser.add_argument("--range", type=lambda s: [float(item) for item in s.split(',')], )
    parser.add_argument('--blind', action='store_true', help='blinding the channel')
    parser.add_argument('--checksyst', action='store_true')
    parser.add_argument('--dd', action='store_true')

    options = parser.parse_args()
    config = dctools.read_config(options.input)

    print(f'making: {options.channel} : {options.variable} : {options.era}')
    
    if len(options.channel) == 1:
        options.channel = options.channel[0]
    
    # make datasets per prcess
    datasets = {}
    signal = ""

    if options.name=='':
        options.name == options.channel
        
        
    datasets:Dict = dict()
    for name in config.groups:
        histograms = dict(
            filter(
                lambda _n: _n[0] in config.groups[name].processes,
                config.boosthist.items()
            )
        )

        p = dctools.datagroup(
            histograms = histograms,
            ptype      = config.groups[name].type,
            observable = options.variable,
            name       = name,
            xsections  = config.xsections,
            channel    = options.channel,
            luminosity = config.luminosity.value,
            rebin      = options.rebin,
            binrange   = options.range
        )
        
        datasets[p.name] = p
        if p.ptype == "signal":
            signal = p.name


    if options.plot:
        _plot_channel = plotter.add_process_axis(datasets)
        pred = _plot_channel.project('process','systematic', options.variable)[:hist.loc('data'),:,:]
        data = _plot_channel[{'systematic':'nominal'}].project('process',options.variable)[hist.loc('data'),:] 

        plt.figure(figsize=(6,7))
        ax, bx = plotter.mcplot(
            pred[{'systematic':'nominal'}].stack('process'),
            data=None if options.blind else data, 
            syst=pred.stack('process'),
        )
        
        try:
            sig_ewk = _plot_channel[{'systematic':'nominal'}].project('process', variable)[hist.loc('VBSZZ2l2nu'),:]   
            sig_qcd = _plot_channel[{'systematic':'nominal'}].project('process', variable)[hist.loc('ZZ2l2nu'),:]   
            sig_ewk.plot(ax=ax, histtype='step', color='red')
            sig_qcd.plot(ax=ax, histtype='step', color='purple')
        except:
            pass
    
        ymax = np.max([line.get_ydata().max() for line in ax.lines if line.get_ydata().shape[0]>0])
        ymin = np.min([line.get_ydata().min() for line in ax.lines if line.get_ydata().shape[0]>0])
    
        ax.set_ylim(0.001, 100*ymax)
        ax.set_title(f"channel {options.channel}: {options.era}")

        ax.set_yscale('log')
        plt.savefig(f'plot-{options.channel}-{options.variable}-{options.era}.pdf')


    if options.checksyst:        
        _plot_channel = plotter.add_process_axis(datasets)
        pred = _plot_channel.project('process','systematic', options.variable)[:hist.loc('data'),:,:]
        data = _plot_channel[{'systematic':'nominal'}].project('process',options.variable)[hist.loc('data'),:] 
        plotter.check_systematic(
            pred[{'systematic':'nominal'}].stack('process'),
            syst=pred.stack('process'),
            plot_file_name=f'check-sys-{options.channel}-{options.era}'
        )

    card_name = options.channel+options.era

    card = dctools.datacard(
        name = signal if len(options.name)==0 else options.name,
        channel= card_name
    )
    card.shapes_headers()
    
    data_obs = datasets.get("data").get("nominal")
    
    card.add_observation(data_obs)

    for _, p in datasets.items():
        print(" --> ", p.name)
        if len(p.to_boost().shape) == 0 or p.get("nominal").sum().value == 0:
            print(f"--> histogram for the process {p.name} is empty !")
            continue

        if p.ptype=="data":
            continue
            
        
        if not card.add_nominal(p.name, p.get("nominal"), p.ptype): continue 

        #Flat uncertaintes
        card.add_log_normal(p.name, f"CMS_lumi_{options.era}", config.luminosity.uncer)
        card.add_log_normal(p.name, f"CMS_res_e_{options.era}", 1.005)
        card.add_log_normal(p.name, f"CMS_res_e_{options.era}", 1.005)
        card.add_log_normal(p.name, f"UEPS", 1.20)

        #Shape uncertainties
        #card.add_shape_nuisance(p.name, f"CMS_eff_m_{options.era}", p.get("MuonSF")  , symmetrise=False)
        #card.add_shape_nuisance(p.name, f"CMS_eff_e_{options.era}", p.get("ElectrronSF") , symmetrise=False)
        #card.add_shape_nuisance(p.name, f"CMS_JES_{options.era}"   , p.get(f"jesTotal")    , symmetrise=False) 
        #card.add_shape_nuisance(p.name, f"CMS_JER_{options.era}"   , p.get(f"jer")         , symmetrise=False) 
        #card.add_shape_nuisance(p.name, f"CMS_BTag_{options.era}"   , p.get(f"btagEventWeight")  , symmetrise=False) 
        #card.add_shape_nuisance(p.name, f"CMS_Trig_{options.era}"   , p.get(f"TriggerSFWeight")  , symmetrise=False)             
        #card.add_shape_nuisance(p.name, f"CMS_pfire_{options.era}"   , p.get(f"PrefireWeight")  , symmetrise=False) 
        #card.add_shape_nuisance(p.name, f"PDF_{options.era}"   , p.get(f"PDF")  , symmetrise=False)
        #card.add_shape_nuisance(p.name, f"CMS_Vx_{options.era}"   , p.get(f"nvtxWeight")  , symmetrise=False)
        #card.add_shape_nuisance(p.name, f"CMS_PU_{options.era}"   , p.get(f"puWeight")  , symmetrise=False)

        #Shapes specific to certain backgrounds 
        if 'DY' not in p.name:
            card.add_qcd_scales(
                name, "CMS_QCDScale{p.name}_{options.era}",
                [p.get("QCDScale0"), p.get("QCDScale1"), p.get("QCDScale2")]
            )
        if 'WZ' in p.name:
            card.add_shape_nuisance(p.name, f"EWKWZ"   , p.get(f"vvewkcor")  , symmetrise=True)
        if 'ZZ' in p.name:
            card.add_shape_nuisance(p.name, f"EWKZZ"   , p.get(f"vvewkcor")  , symmetrise=True)
       

        #Add rate params for the various processes
        if p.name  in ["TOP", "WW"]:
            if "catEM" in card_name:
                card.add_rate_param("EMnorm_" + options.era, "catEM*", p.name)
            elif "BSM" in card_name:
                card.add_rate_param("EMnorm_" + options.era, "chBSM*", p.name)
        elif p.name in ["ZZ", "WZ"]:
            if ("cat3L" in card_name) or ("cat4L" in card_name):
                card.add_rate_param("VVnorm_" + options.era, "cat3L*", p.name)
                card.add_rate_param("VVnorm_" + options.era, "cat4L*", p.name)
            elif "BSM" in card_name:
                card.add_rate_param("VVnorm_" + options.era, "chBSM*", p.name)
        elif p.name in ["DY"]:
            if  "BSM" in card_name:
                card.add_rate_param("DYnorm_" + options.era, "chBSM*", p.name)
        # adding statistical uncertainties
        card.add_auto_stat()

    # saving the datacard
    card.dump()

if __name__ == "__main__":
    main()

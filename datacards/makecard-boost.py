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
    parser.add_argument("-i"  , "--input"   , type=str , default="./config/input_UL_2018_timgad-vbs.yaml")
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

        # For the data driven no uncertainty
        if "DY" in p.name and options.dd:
            card.add_log_normal(p.name, f"CMS_lumi_{options.era}", config.luminosity.uncer)
            card.add_log_normal(p.name, f"DY_dd_uncert_{options.era}", 0.1)
            card.add_auto_stat()
            continue

        # luminausity
        card.add_log_normal(p.name, f"CMS_lumi_{options.era}", config.luminosity.uncer)
        
        # scale factors / resolution
        card.add_shape_nuisance(p.name, f"CMS_res_e_{options.era}"  , p.get("ElectronEn"), symmetrise=True)
        card.add_shape_nuisance(p.name, f"CMS_res_m_{options.era}"  , p.get("MuonRoc")   , symmetrise=True)
        card.add_shape_nuisance(p.name, f"CMS_lept_sf_{options.era}", p.get("LeptonSF")  , symmetrise=False)
        card.add_shape_nuisance(p.name, f"CMS_trig_sf_{options.era}", p.get("triggerSF") , symmetrise=False)

        # JES/JES and UEPS 
        #card.add_shape_nuisance(p.name, f"CMS_jes_{options.era}", p.get("JES"), symmetrise=False) 
        year = options.era.replace('APV','')

        card.add_shape_nuisance(p.name, f"JES_Absolute{year}"      , p.get(f"JES_Absolute{year}")      , symmetrise=False) 
        card.add_shape_nuisance(p.name, f"JES_BBEC1{year}"         , p.get(f"JES_BBEC1{year}")         , symmetrise=False) 
        card.add_shape_nuisance(p.name, f"JES_EC2{year}"           , p.get(f"JES_EC2{year}")           , symmetrise=False) 
        card.add_shape_nuisance(p.name, f"JES_HF{year}"            , p.get(f"JES_HF{year}")            , symmetrise=False) 
        card.add_shape_nuisance(p.name, f"JES_RelativeSample{year}", p.get(f"JES_RelativeSample{year}"), symmetrise=False) 

        card.add_shape_nuisance(p.name, f"JES_Absolute"   , p.get("JES_Absolute")   , symmetrise=False) 
        card.add_shape_nuisance(p.name, f"JES_BBEC1"      , p.get("JES_BBEC1")      , symmetrise=False) 
        card.add_shape_nuisance(p.name, f"JES_EC2"        , p.get("JES_EC2")        , symmetrise=False) 
        card.add_shape_nuisance(p.name, f"JES_HF"         , p.get("JES_HF")         , symmetrise=False) 
        card.add_shape_nuisance(p.name, f"JES_RelativeBal", p.get("JES_RelativeBal"), symmetrise=False) 
        card.add_shape_nuisance(p.name, f"JES_FlavorQCD"  , p.get("JES_FlavorQCD")  , symmetrise=False) 

        card.add_shape_nuisance(p.name, f"CMS_jer_{options.era}", p.get("JER"), symmetrise=False)
        card.add_shape_nuisance(p.name, f"CMS_UES_{options.era}", p.get("UES"), symmetrise=False)
        
        # Can maybe ne correlated over era's? 
        card.add_shape_nuisance(p.name, f"PS_FSR_{options.era}", p.get("UEPS_FSR"), symmetrise=False)
        card.add_shape_nuisance(p.name, f"PS_ISR_{options.era}", p.get("UEPS_ISR"), symmetrise=False)
        
        # taus
        # tauIDvse_sf, tauIDvsmu_sf, tauIDvsjet_sf
        card.add_shape_nuisance(p.name, f"tauIDvse_sf{options.era}"  , p.get("tauIDvse_sf"), symmetrise=False)
        card.add_shape_nuisance(p.name, f"tauIDvsmu_sf{options.era}" , p.get("tauIDvsmu_sf"), symmetrise=False)
        card.add_shape_nuisance(p.name, f"tauIDvsjet_sf{options.era}", p.get("tauIDvsjet_sf"), symmetrise=False)
        
        # b-tagging uncertainties
        # btag_sf_bc_2016APV, btag_sf_light_2016APV
        try:
            card.add_shape_nuisance(p.name, f"CMS_btag_sf_uds_{options.era}" , p.get(f"btag_sf_light_{options.era}"), symmetrise=True)
            card.add_shape_nuisance(p.name, f"CMS_btag_sf_bc_{options.era}"  , p.get(f"btag_sf_bc_{options.era}")   , symmetrise=False)
            card.add_shape_nuisance(p.name, f"CMS_btag_df_stat_{options.era}", p.get("btag_sf_stat")            , symmetrise=False)
        except:
            pass
        
        # b-tagging uncertainties correlated over years
        card.add_shape_nuisance(p.name, "CMS_btag_sf_bc"  , p.get("btag_sf_bc_correlated")   , symmetrise=False)
        card.add_shape_nuisance(p.name, "CMS_btag_sf_uds" , p.get("btag_sf_light_correlated"), symmetrise=True)

        # other uncertainties
        card.add_shape_nuisance(p.name, f"CMS_pileup_{options.era}", p.get("pileup_weight"), symmetrise=False)

        #QCD scale, PDF and other theory uncertainty
        if 'gg' not in p.name:
            card.add_qcd_scales(
                    p.name, f"CMS_QCDScale{p.name}", 
                    [p.get("QCDScale0w"), p.get("QCDScale1w"), p.get("QCDScale2w")]
        )
        
        # PDF uncertaintites / not working for the moment
        card.add_shape_nuisance(p.name, f"pdf_{p.name}"   , p.get("PDF_weight"), symmetrise=False)
        card.add_shape_nuisance(p.name, f"alphaS_{p.name}", p.get("aS_weight" ), symmetrise=False)        
        
        # Electroweak Corrections uncertainties
        if 'WZ' in p.name:
            card.add_shape_nuisance(p.name, "ewk_corr_WZ", p.get("kEW"), symmetrise=False)
        if ('ZZ' in p.name) and ('EWK' not in p.name):
            card.add_shape_nuisance(p.name, "ewk_corr_ZZ", p.get("kEW"), symmetrise=False)
            
        # define rates
        if p.name  in ["WW"]:
            if "vbs-EM" in card_name:
                card.add_rate_param(f"NormWW_{options.era}", "vbs-EM*", p.name)
            elif "SR" in card_name:
                card.add_rate_param(f"NormWW_{options.era}", card_name+'*', p.name)
        
        # define rate 3L categoryel 
        elif p.name in ["WZ"]:
            if "vbs-3L" in card_name:
                card.add_rate_param(f"NormWZ_{options.era}", "vbs-3L*", p.name)
            elif "SR" in card_name:
                card.add_rate_param(f"NormWZ_{options.era}", card_name+'*', p.name)
        
        # define rate for DY category
        elif p.name in ["DY"] and not options.dd:
            if "DY" in card_name:
                card.add_rate_param(f"NormDY_{options.era}", "vbs-DY*", p.name)
            elif "SR" in card_name:
                card.add_rate_param(f"NormDY_{options.era}", card_name+'*', p.name)
        
        # define rate for TOP category
        elif p.name in ["Top"]:
            if "EM" in card_name:
                card.add_rate_param(f"NormTOP_{options.era}", "vbs-EM*", p.name)
            elif "SR" in card_name:
                card.add_rate_param(f"NormTOP_{options.era}", card_name+'*', p.name) 
        card.add_auto_stat()

    # saving the datacard
    card.dump()

if __name__ == "__main__":
    main()

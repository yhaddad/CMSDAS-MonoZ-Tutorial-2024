#import mplhep as hep
import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import awkward as ak
import pandas as pd
import pickle
import hist
import yaml

fn = 'histograms.pkl'
yamlfile = '/eos/user/t/taiwoo/RealMonoZ/CMSDAS-MonoZ-Tutorial-2024/datacards/config/xsections_2016.yaml'
with open(fn, 'rb') as f:
    bh_output = pickle.load(f)
    #draw_keys = ['met_pt']
    met_type = ['h1_measMET', 'h2_measMET', 'h_emulMET']
    #mc_keys = ['ZZ','WZ','WW','TT','ST', 'DY', 'WWZ', 'WZZ', 'ZZZ']
    mc_keys = ['TT','ST','WZ','WW','ZZ','WWZ','WZZ','ZZZ']
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    #metbins = np.array([50, 100, 125, 150, 175, 200, 250, 300, 350, 400, 500, 600, 1000])
    #print(bh_output['Data2016']['hist']['h_emulMET'])
    regions = {
        'h1_measMET': ['catSignal-0jet', 'catSignal-1jet', 'catEM'],
        'h2_measMET': ['catNRB', 'catDY'],
        'h_emulMET': ['cat3L', 'cat4L'],
    }
    metbins = {
        'h1_measMET': np.array([50, 100, 125, 150, 175, 200, 250, 300, 350, 400, 500, 600, 1000]),
        'h2_measMET': np.array([50, 60, 70, 80, 90, 100]),
        'h_emulMET': np.array([50, 100, 125, 150, 175, 200, 250, 300, 350, 400, 500, 600, 1000]),
    }

    for h in met_type:
        #draw = 'met_pt'
        for key in regions[h]:
            data_values = bh_output['Data2016']['hist'][h].integrate('channel', key).integrate('systematic', 'nominal').values()
            data_bins = metbins[h]
            
            mc_hists = []
            for mc in mc_keys:
                print(mc)
                check_firstMC = True
                for bkg in bh_output.keys():
                    if 'WWW' in bkg:
                        continue
                    if mc == 'WZ' and ('WWZ' in bkg or 'WZZ' in bkg or 'ZZZ' in bkg):
                        continue
                    if mc == 'WW' and ('WWZ' in bkg or 'WZZ' in bkg or 'ZZZ' in bkg):
                        continue
                    if mc == 'ZZ' and ('WWZ' in bkg or 'WZZ' in bkg or 'ZZZ' in bkg):
                        continue
                    if mc in bkg:
                        print(mc,bkg)
                        ## open yaml file and get xsecs
                        with open(yamlfile) as file:
                            xsections = yaml.load(file, Loader=yaml.FullLoader)
                        xsec = xsections[bkg]['xsec']
                        scalesMC = 1/bh_output[bkg]['sumw']*xsec*35900
                        try:
                            mc_values += bh_output[bkg]['hist'][h].integrate('channel', key).integrate('systematic', 'nominal').values()*scalesMC
                        except:
                            try:
                                #scalesMC = 1/bh_output[bkg]['sumw']
                                mc_values = bh_output[bkg]['hist'][h].integrate('channel', key).integrate('systematic', 'nominal').values()*scalesMC
                                check_firstMC = False
                            except:
                                pass
                try:
                    mc_hists.append(mc_values)
                    del mc_values
                except:
                    pass
            #print(mc_hists)

            plt.style.use(hep.style.CMS)
            fig, (ax1, ax2) = plt.subplots(
                nrows=2,
                ncols=1,
                figsize=(10,10),
                gridspec_kw={"height_ratios": (3, 1)},
                sharex=True
            )
            fig.subplots_adjust(hspace=.07)
            hep.cms.label(ax=ax1, llabel='DAS Mono-Z', rlabel='35.9 fb$^{-1}$ (13 TeV)')
            # make a center bins
            metbins_center = (data_bins[:-1] + data_bins[1:]) / 2
            print(np.sqrt(data_values))
            ax1.errorbar(
                x=metbins_center,
                y=data_values,
                xerr=(data_bins[1:] - data_bins[:-1]) / 2,
                yerr=np.sqrt(data_values),
                fmt='o',
                color='black',
                label='Data',
            )
            print(len(mc_hists), len(data_bins))
            for i, mc in enumerate(mc_hists):
                ax1.hist(
                    metbins_center,
                    bins=data_bins,
                    weights=mc,
                    histtype='step',
                    edgecolor='black',
                    color=colors[i],
                    stacked=True,
                    fill=True,
                    label=mc_keys[i],
                )
            ax1.set_xlim(50, 1000)
            ax2.set_xlabel('$p^{miss}_{T}$ (GeV)')
            ax1.set_ylabel('Events')
            ax1.set_yscale('log')
            ax1.legend(ncol=4)
            fig.savefig(f'{h}_{key}.png')

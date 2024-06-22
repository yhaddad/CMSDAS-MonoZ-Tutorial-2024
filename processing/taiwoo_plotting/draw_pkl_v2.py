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

fn = 'histograms.pkl'
yamlfile = '/eos/user/t/taiwoo/RealMonoZ/CMSDAS-MonoZ-Tutorial-2024/datacards/config/xsections_2016.yaml'
with open(fn, 'rb') as f:
    bh_output = pickle.load(f)
    #draw_keys = ['met_pt']
    met_type = ['h1_measMET', 'h2_measMET', 'h_emulMET']
    #mc_keys = ['ZZ','WZ','WW','TT','ST', 'DY', 'WWZ', 'WZZ', 'ZZZ']
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
    syst_names = ['nominal', 'QCDScale2Down', 'QCDScale1Up', 'pdfUp', 'puweightUp', 'QCDScale1Down', 'QCDScale2Up', 'pdfDown', 'QCDScale0Up', 'puweightDown', 'QCDScale0Down', 'ElectronEnUp', 'ElectronEnDown', 'MuonEnUp', 'MuonEnDown', 'jesTotalUp', 'jesTotalDown', 'jerUp', 'jerDown']
    #mc_keys = ['TT','ST','WZ','WW','ZZ','WWZ','WZZ','ZZZ']
    mc_keys = ['ZZZ','WZZ','WWZ','ZZ','WW','WZ','ST','TT']
    #colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    colors = ['brown','salmon','lightgreen','gold','green','dodgerblue','cyan','blue']
    for h in met_type:
        #draw = 'met_pt'

        data_values = bh_output['Data2016']['hist'][h].project('met_pt')
        #print(data_values)
        for idx, key in enumerate(regions[h]):
            data_values = bh_output['Data2016']['hist'][h].integrate('systematic', 'nominal').values()[idx]
            data_bins = metbins[h]
            mc_hists = []
            for mc in mc_keys:
                #print(mc)
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
                        #if mc == 'WW' and h == 'h1_measMET' and 'catSignal' in key:
                        #    print(bh_output[bkg]['hist'][h].values()[idx][0]*scalesMC)
                        #print(mc,bkg)
                        ## open yaml file and get xsecs
                        with open(yamlfile) as file:
                            xsections = yaml.load(file, Loader=yaml.FullLoader)
                        xsec = xsections[bkg]['xsec']
                        scalesMC = 1/bh_output[bkg]['sumw']*xsec*35900
                        #print(bh_output[bkg]['hist'][h].values()[idx][0])
                        try:
                            mc_values += bh_output[bkg]['hist'][h].values()[idx][0]*scalesMC
                        except:
                            try:
                                mc_values = bh_output[bkg]['hist'][h].values()[idx][0]*scalesMC
                                check_firstMC = False
                            except:
                                pass
                        if mc == 'WW' and h == 'h1_measMET' and 'catSignal' in key:
                            print(mc,h,key,bkg,bh_output[bkg]['hist'][h].values()[idx]*scalesMC)
                            print(scalesMC)

                ## if there is no MC, set 0
                if check_firstMC:
                    print('No MC for', mc, key)
                    mc_values = np.zeros(len(data_values))

                try:
                    mc_hists.append(np.array(mc_values))
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
            #print(np.sqrt(data_values))
            ax1.errorbar(
                x=metbins_center,
                y=data_values,
                xerr=(data_bins[1:] - data_bins[:-1]) / 2,
                yerr=np.sqrt(data_values),
                fmt='o',
                color='black',
                label='Data',
            )
            #print(metbins[h][:-1])
            #print(np.shape(mc_hists), np.shape([metbins[h][:-1]]* len(mc_hists)))
            ax1.hist(
                x = [metbins[h][:-1]]* len(mc_hists),
                bins = metbins[h],
                weights = mc_hists,
                histtype='stepfilled',
                color=colors,
                edgecolor='black',
                label=mc_keys,
                alpha=1.0,
                stacked=True,
            )
            if key == 'catNRB':
                plt.text(x=0.60, y=3., s = "Non-resonant CR", ha='left', va='center', transform=plt.gca().transAxes,fontsize=24, fontweight='bold')
            if key == 'catDY':
                plt.text(x=0.60, y=3., s = "Drell-Yan CR", ha='left', va='center', transform=plt.gca().transAxes,fontsize=24, fontweight='bold')
            if key == 'cat3L':
                plt.text(x=0.60, y=3., s = "$3\ell$ (WZ) CR", ha='left', va='center', transform=plt.gca().transAxes,fontsize=24, fontweight='bold')
            if key == 'cat4L':
                plt.text(x=0.60, y=3., s = "$4\ell$ (ZZ) CR", ha='left', va='center', transform=plt.gca().transAxes,fontsize=24, fontweight='bold')


            ax1.text(x=0.60, y=0.13, s = "$3\ell$ CR", ha='left', va='center', transform=plt.gca().transAxes,fontsize=20, fontweight='bold')
            ax1.set_xlim(min(data_bins), max(data_bins))
            ax1.set_ylim(0.0001, 1e5)
            if h == 'h2_measMET':
                ax1.set_ylim(0.001, 1e7)


            ## ratio plot
            mc_sum = np.sum(mc_hists, axis=0)
            ratio = data_values / mc_sum
            ratio_err = np.sqrt(data_values) / mc_sum
            ax2.errorbar(
                x=metbins_center,
                y=ratio,
                xerr=(data_bins[1:] - data_bins[:-1]) / 2,
                yerr=ratio_err,
                fmt='o',
                color='black',
            )
            ax2.axhline(y=1, color='skyblue', linestyle='--')
            ax2.set_ylim(0, 3)
            ax2.set_ylabel('Data/MC')
            ax2.set_xlabel('$p^{miss}_{T}$ (GeV)')
            ax1.set_ylabel('Events')
            ax1.set_yscale('log')
            ax1.legend(ncol=3,loc='upper center')
            fig.savefig(f'{h}_{key}.png')
            del mc_hists, data_values

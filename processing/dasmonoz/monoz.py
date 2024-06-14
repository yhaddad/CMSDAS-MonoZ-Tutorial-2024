from ast import List
import sys
from coffea.processor import ProcessorABC
from coffea.analysis_tools import Weights

import dask_awkward
import awkward as ak
import dask_awkward.lib
import dask_awkward.lib.core

import hist
import hist.dask as hda

class BaseProducer(ProcessorABC):
    """
    A coffea Processor which produces a workspace.
    This applies selections and produces histograms from kinematics.
    """

    histograms = NotImplemented
    selection = NotImplemented

    def __init__(self, do_syst=True, weight_syst_list: list = [], shift_syst_list: list = []):
        self.do_syst = do_syst
        self.weight_syst_list = weight_syst_list
        self.vshift_syst_list = shift_syst_list
        
        self._accumulator = {
            name: hda.hist.Hist(
                hist.axis.StrCategory([], name="channel"   , growth=True),
                hist.axis.StrCategory([], name="systematic", growth=True), 
                hist.axis.Variable(h["axis"]["bins"], name=h["axis"]["label"]),
                hist.storage.Weight()
            ) for name, h in list(self.histograms.items())
        }

    def process(self, event: dask_awkward.lib.core.Array):
        dataset_name = event.metadata['dataset']
        is_mc = event.metadata.get("is_mc")

        output = self._accumulator
        weights = self.weighting(event)
        
        # let fill the nominal histograms
        for name, histo in list(self.histograms.items()):
            for region in histo['region']:
                selec = self.evaluate_selection(event, histo['target'], region)
                output[name].fill(**{
                    "channel": region, 
                    "systematic": 'nominal', 
                    histo["axis"]["label"]: event[histo['target']][selec],
                    "weight": weights.weight()[selec]
                })
                if not is_mc: continue

                # Let do the weight based systematics
                for syst in list(weights.variations):
                   
                    selec = self.evaluate_selection(event, histo['target'], region, '', '')
                    output[name].fill(**{
                        "channel": region, 
                        "systematic": syst, 
                        histo["axis"]["label"]: event[histo['target']][selec],
                        "weight": weights.weight(modifier=syst)[selec]
                    })

                # let do the systematics
                for syst in self.vshift_syst_list:
                    for direction in ['Up', 'Down']:
                        selec = self.evaluate_selection(event, histo['target'], region, syst, direction)
                        output[name].fill(**{
                            "channel": region, 
                            "systematic": syst + direction, 
                            histo["axis"]["label"]: event[histo['target']][selec],
                            "weight": weights.weight()[selec]
                        })
        return output

        


    def evaluate_selection(self, event:dask_awkward.lib.core.Array, excut: str, cat: str, syst_shift: str='', direction: str=''):
        if syst_shift:
            syst_shift = '' if syst_shift in self.weight_syst_list else syst_shift
            syst_shift = f'_sys_{syst_shift}{direction}' if syst_shift != '' else ''
        
        expression = '&'.join(f"({cut.format(sys=syst_shift)})"  for cut in self.selection[cat] if excut not in cut)
        return eval(expression)

    def weighting(self, event):
        return NotImplemented

    def naming_schema(self, *args):
        return NotImplemented
    
    def postprocess(self, accumulator):
        pass

class MonoZ(BaseProducer):
    histograms = {
        'h1_measMET': {
            'target': 'met_pt',
            'name'  : 'measMET',
            'region': [
                'catSignal-0jet',
                'catEM',
                'catSignal-1jet',
            ],
            'axis': {
                'label': 'met_pt',
                'bins' : [50, 100, 125, 150, 175, 200, 250, 300, 350, 400, 500, 600, 1000]
            }
        },
        'h2_measMET': {
            'target': 'met_pt',
            'name'  : 'measMET',
            'region': [
                'catNRB',
                'catDY'
            ],
            'axis': {
                'label': 'met_pt',
                'bins': [50, 60, 70, 80, 90, 100]
            }
        },
        'h_emulMET' : {
            'target': 'emulatedMET',
            'name'  : 'measMET',
            'region': [
                'cat3L',
                'cat4L',
            ],
            'axis'  : {
                'label': 'met_pt',
                'bins': [50, 100, 125, 150, 175, 200, 250, 300, 350, 400, 500, 600, 1000]
            }
        }
    }
    selection = {
        "signal": [
            "event.Z_pt{sys}        >  60",
            "abs(event.Z_mass{sys} - 91.1876) < 15",
            "event.ngood_jets{sys}  <=  1",
            "event.ngood_bjets{sys} ==  0",
            "event.nhad_taus{sys}   ==  0",
            "event.met_pt{sys}      >  50",
            "abs(event.delta_phi_ZMet{sys} ) > 2.6",
            "abs(1 - event.sca_balance{sys}) < 0.4",
            "abs(event.delta_phi_j_met{sys}) > 0.5",
            "event.delta_R_ll{sys}           < 1.8"
        ],
        "cat3L": [
            "event.Z_pt{sys}        >  60",
            "abs(event.Z_mass{sys} - 91.1876) < 15",
            "event.ngood_jets{sys}  <=  1",
            "event.ngood_bjets{sys} ==  0",
            "event.met_pt{sys}      >  30",
            "event.mass_alllep{sys} > 100",
            "abs(1 -event.emulatedMET{sys}/event.Z_pt{sys}) < 0.4",
            "abs(event.emulatedMET_phi{sys} - event.Z_phi{sys}) > 2.6",
            "(event.lep_category{sys} == 4) | (event.lep_category{sys} == 5)",
        ],
        "cat4L": [
            "event.Z_pt{sys}        >  60",
            "abs(event.Z_mass{sys} - 91.1876) < 35",
            "event.ngood_jets{sys}  <=  1",
            "abs(event.emulatedMET_phi{sys} - event.Z_phi{sys}) > 2.6",
            "(event.lep_category{sys} == 6) | (event.lep_category{sys} == 7)",
        ],
        "catNRB": [
            "event.Z_pt{sys}        >  60",
            "abs(event.Z_mass{sys} - 91.1876) < 15",
            "event.ngood_jets{sys}  <=  1",
            "event.ngood_bjets{sys} ==  0",
            "event.met_pt{sys}      >  30"
        ],
        "catSignal-0jet": [
            "(event.lep_category{sys} == 1) | (event.lep_category{sys} == 3)",
            "event.ngood_jets{sys} == 0",
            "event.Z_pt{sys}        >  60",
            "abs(event.Z_mass{sys} - 91.1876) < 15",
            "event.ngood_bjets{sys} ==  0",
            "event.nhad_taus{sys}   ==  0",
            "event.met_pt{sys}      >  50",
            "abs(event.delta_phi_ZMet{sys} ) > 2.6",
            "abs(1 - event.sca_balance{sys}) < 0.4",
            "abs(event.delta_phi_j_met{sys}) > 0.5",
            "event.delta_R_ll{sys}           < 1.8"
        ],
        "catSignal-1jet": [
            "(event.lep_category{sys} == 1) | (event.lep_category{sys} == 3)",
            "event.ngood_jets{sys} == 1",
            "event.Z_pt{sys}        >  60",
            "abs(event.Z_mass{sys} - 91.1876) < 15",
            "event.ngood_bjets{sys} ==  0",
            "event.nhad_taus{sys}   ==  0",
            "event.met_pt{sys}      >  50",
            "abs(event.delta_phi_ZMet{sys} ) > 2.6",
            "abs(1 - event.sca_balance{sys}) < 0.4",
            "abs(event.delta_phi_j_met{sys}) > 0.5",
            "event.delta_R_ll{sys}           < 1.8"
        ],
        "catDY": [
            "(event.lep_category{sys} == 1) | (event.lep_category{sys} == 3)",
            "(event.ngood_jets{sys} == 0) | (event.ngood_jets{sys} == 1)",
            "event.Z_pt{sys}        >  60",
            "abs(event.Z_mass{sys} - 91.1876) < 15",
            "event.ngood_bjets{sys} ==  0",
            "event.nhad_taus{sys}   ==  0",
            "event.met_pt{sys}      >  50",
            "abs(event.delta_phi_ZMet{sys} ) > 2.6",
            "abs(1 - event.sca_balance{sys}) < 0.4",
            "abs(event.delta_phi_j_met{sys}) > 0.5",
            "event.delta_R_ll{sys}           < 1.8"
        ],
        "catEM": [
            "event.lep_category{sys} == 2",
            "event.Z_pt{sys}        >  60",
            "abs(event.Z_mass{sys} - 91.1876) < 15",
            "event.ngood_jets{sys}  <=  1",
            "event.ngood_bjets{sys} ==  0",
            "event.met_pt{sys}      >  30"
        ],
        "catTOP": [
            "event.lep_category{sys} == 2",
            "event.Z_pt{sys}        >  60" ,
            "abs(event.Z_mass{sys} - 91.1876) < 15",
            "event.ngood_jets{sys}  >   2" ,
            "event.ngood_bjets{sys} >=  1" ,
            "event.met_pt{sys}      >  80"
        ]
    }

    def weighting(self, event: dask_awkward.Array):

        weights = Weights(None, storeIndividual=True)
        # For data we want a nominal weight of 1, and we do an early return from this function
        if not event.metadata["is_mc"]:
            weights.add("data", ak.ones_like(event.event))
            return weights

        # For MonteCarlo, we add mulitple weights, some with systematic variations (4 args)
        weights.add("xsection", event.xsecscale)
        weights.add("puweight", event.puWeight, event.puWeightUp, event.puWeightDown)
        # EWK correction is estimated only for VV processes
        if 'kEW' in event.fields:
            weights.add("vvewkcor", event.kEW, event.kEWUp, event.kEWDown)
            weights.add("nnlocorr", event.kNNLO)

        weights.add("pdf", ak.ones_like(event.pdfw_Up), event.pdfw_Up, event.pdfw_Down)
        weights.add("QCDScale0", ak.ones_like(event.QCDScale0wUp), event.QCDScale0wUp, event.QCDScale0wDown)
        weights.add("QCDScale1", ak.ones_like(event.QCDScale0wUp), event.QCDScale1wUp, event.QCDScale1wDown)
        weights.add("QCDScale2", ak.ones_like(event.QCDScale0wUp), event.QCDScale2wUp, event.QCDScale2wDown)

        # Insert here the complete list of weight-based systematics: 
        # missing are --> MuonSF, ElectronSF, PrefireWeight, nvtxWeight, TriggerSFWeight, btagEventWeight

        return weights

    def naming_schema(self, name, region):
        return f'{name}_{self.sample}_{region}{self.syst_suffix}'


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

    def __init__(
            self, isMC, era=2017, sample="DY", do_syst=False, 
            syst_var='', weight_syst=False, flag=False):
        self._flag = flag
        self.do_syst = do_syst
        self.era = era
        self.isMC = isMC
        self.sample = sample
        self.syst_var, self.syst_suffix = (syst_var, f'_sys_{syst_var}') if do_syst and syst_var else ('', '')
        self.weight_syst = weight_syst
        self._accumulator = {
            name: hda.hist.Hist(
                hist.axis.Variable(axis["bins"], name=axis["label"]),
                hist.storage.Weight()
            ) for name, axis in (
                (self.naming_schema(hist['name'], region), hist['axis']) for _, hist in list(self.histograms.items()) for region in hist['region']
            )
        }

    def process(self, event: dask_awkward.Array):
        output = self._accumulator
        weights = self.weighting(event)

        if self.syst_var in weights.variations:
            weight = weights.weight(modifier=self.syst_var)
        else:
            weight = weights.weight()


        for h, hist in list(self.histograms.items()):
            for region in hist['region']:
                name = self.naming_schema(hist['name'], region)
                selec = self.passbut(event, hist['target'], region)
                output[name].fill(
                    **{
                        hist['axis']['label']: event[hist['target']][selec],
                        'weight': weight[selec],
                    }
                )

        return output

    def passbut(self, event, excut: str, cat: str):
        """Backwards-compatible passbut."""
        return eval('&'.join('(' + cut.format(sys=('' if self.weight_syst else self.syst_suffix)) + ')'
                             for cut in self.selection[cat] if excut not in cut))

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
            "self.passbut(event, excut, 'signal')",
        ],
        "catSignal-1jet": [
            "(event.lep_category{sys} == 1) | (event.lep_category{sys} == 3)",
            "event.ngood_jets{sys} == 1",
            "self.passbut(event, excut, 'signal')",
        ],
        "catDY": [
            "(event.lep_category{sys} == 1) | (event.lep_category{sys} == 3)",
            "(event.ngood_jets{sys} == 0) | (event.ngood_jets{sys} == 1)",
            "self.passbut(event, excut, 'signal')",
        ],
        "catEM": [
            "event.lep_category{sys} == 2",
            "self.passbut(event, excut, 'catNRB')",
        ],
    }

    def weighting(self, event: dask_awkward.Array):

        weights = Weights(None, storeIndividual=True)
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

        # complete the full list here: 
        # missing are --> MuonSF, ElectronSF, PrefireWeight, nvtxWeight, TriggerSFWeight, btagEventWeight

        return weights

    def naming_schema(self, name, region):
        return f'{name}_{self.sample}_{region}{self.syst_suffix}'


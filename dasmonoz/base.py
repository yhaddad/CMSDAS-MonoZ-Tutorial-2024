




from coffea.processor import ProcessorABC, LazyDataFrame, dict_accumulator

class WSProducer(ProcessorABC):
    histograms = NotImplemented
    selection = NotImplemented

    def __init__(self, isMC, era=2017, sample="DY", do_syst=False, syst_var='', weight_syst=False, haddFileName=None, flag=False):
        self._flag = flag
        self.do_syst = do_syst
        self.era = era
        self.isMC = isMC
        self.sample = sample
        self.syst_var, self.syst_suffix = (syst_var, f'_sys_{syst_var}') if do_syst and syst_var else ('', '')
        self.weight_syst = weight_syst
        self._accumulator = dict_accumulator({
            name: Hist('Events', Bin(name=name, **axis))
            for name, axis in ((self.naming_schema(hist['name'], region), hist['axis'])
                               for _, hist in list(self.histograms.items())
                               for region in hist['region'])
        })
        self.outfile = haddFileName

    @property
    def accumulator(self):
        return self._accumulator

    def process(self, df, *args):
        output = self.accumulator.identity()
        weight = self.eventweight(df)

        for h, hist in list(self.histograms.items()):
            for region in hist['region']:
                name = self.naming_schema(hist['name'], region)
                selec = self.passbut(df, hist['target'], region)
                output[name].fill(**{
                    'weight': weight[selec],
                    name: df[hist['target']][selec].flatten()
                })

        return output

    def postprocess(self, accumulator):
        f = recreate(self.outfile)
        for h, hist in accumulator.items():
            f[h] = export1d(hist)
            print(f'wrote {h} to {self.outfile}')
        f.close()
        return accumulator

    def passbut(self, event: LazyDataFrame, excut: str, cat: str):
        """
        Backwards-compatible passbut.
        
        """
        return eval(
            '&'.join(
                '(' + cut.format(sys=('' if self.weight_syst else self.syst_suffix)) + ')'
                for cut in self.selection[cat] if excut not in cut
            )
        )

    def eventweight(self, event: LazyDataFrame):
        return NotImplemented

    def naming_schema(self, *args):
        return NotImplemented



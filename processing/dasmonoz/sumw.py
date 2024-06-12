from coffea import processor
import awkward as ak

class EventSumw(processor.ProcessorABC):
    def __init__(self):
        super().__init__()

    def process(self, event): 
        dataset_name = event.metadata['dataset']
        is_mc = event.metadata.get("is_mc")
        
        print("sumw:dataset_name(isMC) = ", dataset_name, is_mc)
        if is_mc is None:
            is_mc = 'data' not in dataset_name.lower()
        
        sumw = 1.0
        if is_mc:
            sumw = ak.sum(event.genEventSumw)
        else:
            sumw = -1.0
        
        return sumw
    
    def postprocess(self, accumulator):
        return accumulator

from coffea import processor
import awkward as ak

class EventSumw(processor.ProcessorABC):
    def __init__(self):
        super().__init__()

    def process(self, event): 
        dataset_name = event.metadata['dataset']
        is_mc = event.metadata.get("is_mc")
        
        if is_mc is None:
            is_mc = 'data' not in dataset_name.lower()
        
        sumw = 1.0
        if is_mc:
            try:
                sumw = ak.sum(event.genEventSumw)
            except:
                sumw = -1.0
        else:
            sumw = -1.0
        
        return sumw
    
    def postprocess(self, accumulator):
        return accumulator

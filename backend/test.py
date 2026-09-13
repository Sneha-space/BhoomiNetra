from src.ml.pipeline import MlPipeline
import json
if __name__=="__main__":
    pipeline = MlPipeline()
    output = pipeline.process(r"D:\Diagrams\DigiLanDoc\Data\DummyLandRecord.pdf")
    print(output)
    with open("./result.json","w") as f:
        json.dump(output,f)
    
    
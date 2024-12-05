from englisttohindi.englisttohindi import EngtoHindi
def process(topic):
    message = str(topic)
    res = EngtoHindi(message)
    return res.convert
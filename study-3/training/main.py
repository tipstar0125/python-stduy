#%%

import eel
import numpy as np

eel.init("web")
eel.js_function(np.random.rand(4).tolist()) # JSON serializableでないとダメ
eel.start("main.html")


#%%



#%%
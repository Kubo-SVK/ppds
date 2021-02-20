from fei.ppds import Thread, Mutex


class Shared():
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.elms = [0] * self.end
        self.mutex = Mutex()
        
        
"""
Sice je kod spustitelny no nejedna sa o konkurentny kod, kedze
cely vypocet sa vykona v jednom vlakne.
"""     
def computation(obj):
    obj.mutex.lock()
    while True:
        if obj.counter >= obj.end:
            break
        
        obj.elms[obj.counter] += 1
        obj.counter += 1
    obj.mutex.unlock()
            
            
def histogram(array):
    unique = set(array)
    out = {}    
    for item in unique:
        out[item] = array.count(item)
    return out
            

shared = Shared(1000000)

th1 = Thread(computation, shared)
th2 = Thread(computation, shared)

th1.join()
th2.join()

print(histogram(shared.elms))
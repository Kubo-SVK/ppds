from fei.ppds import Thread, Mutex


class Shared():
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.elms = [0] * self.end
        self.mutex = Mutex()
        

"""
Locknutie objektu pocas inkrementacie premennych, sice zabrani
viacnasobnej inkrementacii alebo preskoceniu prvku. Avsak nezabrani
situacii, kde po ukonceni jednoho vlakna sa to druhe pokusi pristupit 
k prvku mimo rozsah pola.
"""
def computation(obj):
    while True:
        if obj.counter >= obj.end:
            break
        
        obj.mutex.lock()
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
class Queue():

    def __init__(self, len):
        self._maxlen=len
        self._curlen=0
        self._head=0
        self._tail=-1
        self._q = [None for i in range(len)]

    #TODO remove after func testing
    #def __repr__(self):
    #    return_string = "[ "
    #    for i in range(self._curlen):
    #        return_string = return_string + str(self._q[(self._head+i)%self._maxlen])+" "
    #    return return_string+"]" 

    def put(self, val):
        return_val = 1
        if(self._curlen==self._maxlen):
            return_val = self.pop()
        self._curlen = self._curlen + 1
        self._tail = (self._tail + 1)%self._maxlen
        self._q[self._tail]=val
        return return_val

    def pop(self):
        if(self._curlen==0):
            return -1
        return_val = None
        self._curlen = self._curlen - 1
        return_val = self._q[self._head]
        self._head = (self._head + 1)%self._maxlen
        return return_val 
    
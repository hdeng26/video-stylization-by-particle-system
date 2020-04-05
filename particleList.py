import particle


class particleList:
    '''double linked list'''
    def __init__(self):
        self.start_node = None
        self.size = 0

    def insert2Last(self, p):
        '''insert particle at last of list'''
        if self.start_node is None:
            self.start_node = p
            self.size += 1
            return
        temp = self.start_node
        while temp.nex is not None:
            temp = temp.nex
        temp.nex = p
        p.prev = temp
        self.size += 1

    def insert_after(self, orig, newP):
        '''insert after a particle'''
        if self.start_node is None:
            print("list is empty")
            return
        else:
            temp = self.start_node
            while temp is not None:
                if temp is orig:
                    break
                temp = temp.nex
            if temp is None:
                print("item not in the list")
            else:
                if temp.nex is not None:
                    temp.nex.prev = newP
                    newP.nex = temp.nex
                temp.nex = newP
                newP.prev = temp
                self.size += 1

    def delete(self, p):
        '''delete a particle from the list'''
        if self.start_node is None:
            print("The list has no element to delete")
            return

        if self.start_node.nex is None:
            if self.start_node is p:
                self.start_node = None
                self.size -= 1
            else:
                print("didn't find")
            return 

        if self.start_node is p:
            self.start_node = self.start_node.nex
            self.start_node.prev = None
            self.size -= 1
            return

        temp = self.start_node
        while temp.nex is not None:
            if temp == p:
               break
            temp = temp.nex
        if temp.nex is not None:
            temp.prev.nex = temp.nex
            temp.nex.prev = temp.prev
            self.size -= 1
        else:
            if temp == p:
                temp.prev.nex = None
                self.size -= 1
            else:
                print("didn't find")
                return
        





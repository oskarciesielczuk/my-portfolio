# Candidate No: 45216

MIN = -1000
MAX = 1000

class CompactList:
    def __init__(self,inlist=[]):
        #Compact list stored in the inlist property.
        self.inlist = []
        if inlist != []:
            inlist.sort()
            self.inlist = [inlist[0]]
            previous = self.inlist[0]
            #If the current element is 1 more than the previous, they are in
            #the same interval; otherwise, we start a new interval.
            for i in range(1, len(inlist)):
                if inlist[i] == previous + 1:
                    previous = inlist[i]
                else:
                    self.inlist.append(previous + 1)
                    self.inlist.append(inlist[i])
                    previous = inlist[i]
            self.inlist.append(previous + 1)
            #If the last element in the compact list exceeds the MAX value, 
            #this means MAX is in the last interval; hence, the
            #compact list will be of odd length.
            if self.inlist[len(self.inlist) - 1] > MAX:
                self.inlist.pop()

    def cardinality(self):
        count = 0
        for i in range(0, len(self.inlist)):
            #If i is a starting point and not the last element, there are
            #self.inlist[i + 1] - self.inlist[i] elements in the current interval.
            if i%2 == 0 and i != len(self.inlist) - 1:
                count += self.inlist[i + 1] - self.inlist[i]
            #If i is a starting point and also the last element, the compact list
            #is of odd length, and hence there are MAX - self.inlist[i] + 1 elements
            #in this interval.
            elif i%2 == 0 and i == len(self.inlist) - 1:
                count += MAX - self.inlist[i] + 1
        return count

    def insert(self,value):
        #To insert value, create a temp compact list containing the single value element,
        #and update the self compact list with its union with the temp compact list.
        insertion = CompactList([value])
        self.inlist = self.union(insertion)
        
    def delete(self,value):
        #To delete value, create a temp compact list containing the single value element,
        #and update the self compact list with its intersection with the temp
        #compact list.
        deletion = CompactList([value])
        self.inlist = self.difference(deletion)


    def contains(self,value):
        #If the compact list corresponding to the singleton set containing value is
        #a subset of the original compact list, then value is contained in it.
        singleton = CompactList([value])
        if singleton.subsetOf(self):
            return True
        else:
            return False
         
    
    def subsetOf(self,cl):
        #If the intersection of cl and self is equal to self, that means self is
        #fully contained within cl.
        if self.intersection(cl) == self.inlist:
            return True
        else:
            return False
    
    def equals(self,cl):
        #If self and cl are subsets of each other, they are equal.
        if self.subsetOf(cl) and cl.subsetOf(self):
            return True
        else:
            return False

    def isEmpty(self):
        if self.inlist == []:
            return True
        else:
            return False

    def complement(self):
        result = []
        #If the the compact list is empty, the complement is the whole domain.
        if self.isEmpty():
            return [MIN]
        #If MIN is not the first element of the compact list, then MIN will be
        #the first element of the complement.
        if self.inlist[0] != MIN:
            result.append(MIN)
        #For a given element of the compact list, if it is a starting point, then
        #it will be the first element not in the complement; if it is an end point,
        #it will be the first element in the complement; hence we can just copy over
        #the elements of the self compact list.
        for i in range(0, len(self.inlist)):
            if self.inlist[i] != MIN:
                result.append(self.inlist[i])

        return result
        
        
    def union(self,cl):
        n_s = len(self.inlist)
        n_c = len(cl.inlist)
        s, c = 0, 0
        result = []
        #If either list is empty, the union will just be the non-empty list
        if n_s == 0:
            return cl.inlist
        if n_c == 0:
            return self.inlist
        #Trick to deal with odd length lists; treat them as even length lists with
        #the last element being MAX.
        if n_s%2 == 1:
            self.inlist.append(MAX)
        if n_c%2 == 1:
            cl.inlist.append(MAX)
        
        while s < n_s and c < n_c:
            if result != []:
                #If the current start point of self is less than the current start
                #point of cl, we want to add the self interval to result. Either the
                #interval overlaps with the last interval in result, or it's the
                #start of a new interval.
                if self.inlist[s] < cl.inlist[c]:
                    #If it's the start of a new interval, we add the start and end
                    #point to result.
                    if self.inlist[s] > result[len(result) - 1]:
                        result.append(self.inlist[s])
                        result.append(self.inlist[s + 1])
                    #Otherwise, we update the endpoint of the last interval in result to
                    #the end point of the self interval, if the endpoint of the self
                    #interval is greater than the endpoint of the result interval.
                    else:
                        if self.inlist[s + 1] > result[len(result) - 1]:
                            result[len(result) - 1] = self.inlist[s + 1]
                    s += 2
                #Symmetric for the case that the start point of cl is less than
                #the start point of self.
                else:
                    if cl.inlist[c] > result[len(result) - 1]:
                        result.append(cl.inlist[c])
                        result.append(cl.inlist[c + 1])
                    else:
                        if cl.inlist[c + 1] > result[len(result) - 1]:
                            result[len(result) - 1] = cl.inlist[c + 1]
                    c += 2
            #If we are in the first iteration, there is no need to compare to the
            #last interval in result, since result is empty.
            else:
                if self.inlist[s] < cl.inlist[c]:
                    result.append(self.inlist[s])
                    result.append(self.inlist[s + 1])
                    s += 2
                else:
                    result.append(cl.inlist[c])
                    result.append(cl.inlist[c + 1])
                    c += 2
        #If self is the list that reached the end first, we want to append the rest
        #of cl.
        if s >= n_s:
            #We want to advance c until we find the first element in cl greater
            #than the last element of result.
            while c < n_c and cl.inlist[c] <= result[len(result) - 1]:
                c += 1
            #If said element is an endpoint, we want to update the endpoint of
            #the last interval in result to this endpoint.
            if c%2 == 1:
                result[len(result) - 1] = cl.inlist[c]
                c += 1
            #Then, we can simply append the rest of cl.
            result += cl.inlist[c:]
        #Symmetric for the case that cl reaches the end first.
        else:
            while s < n_s and self.inlist[s] <= result[len(result) - 1]:
                s += 1
            if s%2 == 1:
                result[len(result) - 1] = self.inlist[s]
                s += 1
            result += self.inlist[s:]
        #Undo the trick used to deal with odd length lists.
        if n_s%2 == 1:
            self.inlist.pop()
        if n_c%2 == 1:
            cl.inlist.pop()
        if n_s%2 == 1 or n_c%2 == 1:
            result.pop()

        return result
                
    def intersection(self,cl):
        #Uses the identity that the intersection of A and B is the complement
        #of the union of the complements of A and B.
        self_comp = CompactList()
        self_comp.inlist = self.complement()

        cl_comp = CompactList()
        cl_comp.inlist = cl.complement()

        union = CompactList()
        union.inlist = self_comp.union(cl_comp)

        return union.complement()

    def difference(self,cl):
        #Uses the identity that the difference of A and B is the intersection of
        #A and the complement of B.
        cl_comp = CompactList()
        cl_comp.inlist = cl.complement()

        return self.intersection(cl_comp)
            
    def __str__(self):
        if self.isEmpty():
            return "empty"
        result = ""
        for i in range(0, len(self.inlist),2):
            #For each start point, the string will start with "[x_i"
            result += "[" + str(self.inlist[i])
            #If we arrive at the end of an odd length list, and the last starting
            #point isn't MAX, then the last interval will look like "[x_n-1, MAX]".
            if i == len(self.inlist) - 1 and self.inlist[i] != MAX:
                result += "," + str(MAX) + "]"
            #If the end of an odd length list is MAX, or the start and end point are
            #one apart, then we will just have the singleton set [x_i].
            elif ((i == len(self.inlist) - 1 and self.inlist[i] == MAX) or
                  (self.inlist[i] == self.inlist[i + 1] - 1)):
                result += "]"
            else:
                result += "," + str(self.inlist[i + 1] - 1) + "]"
            #If we know we are not at the last interval, we add the union sign.
            if i < len(self.inlist) - 2:
                result += " U "
        return result

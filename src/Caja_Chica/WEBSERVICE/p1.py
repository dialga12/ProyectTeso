def FindArray(p_aArray, p_xSearch, p_nCol = 0):
    llFind = False
    i = 0
    for x in p_aArray:
        print x[p_nCol],p_xSearch 
        if x[p_nCol] == p_xSearch:
           llFind = True
           break
        i += 1
    if not llFind:
       return None
    return i


a = [['M', 'MASCULINO'],['F', 'FEMENINO'],['X', 'NO DEFINIDO']]
a = [[1, 'MASCULINO'],[2, 'FEMENINO'],[0, 'NO DEFINIDO']]
print a
i = FindArray(a, 1, 0)
print i
i = FindArray(a, 2)
print i
i = FindArray(a, 9)
print i




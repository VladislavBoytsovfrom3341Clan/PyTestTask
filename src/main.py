from src.modules.associative_array.associative_array import AssociativeArray

if __name__=="__main__":
    a= AssociativeArray(50)
    for i in range(50):
        a.insert(i, i**2)
    for i in range(50):
        assert a.find(i) == i**2
    for i in range(15, 35):
        a.remove(i)
    for i in range(50):
        if 15<=i<35:
            assert a.find(i) is None
        else:
            assert a.find(i) == i**2

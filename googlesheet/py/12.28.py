

@set
def save():
    path = ['a', 'b', 'c', 'd']
    A = []
    B = []
    for i in path:
        if (len(A) < 3):
            A.append(i)
        else:
            B.append(i)
    print(A, B)

def set(func):
    save.
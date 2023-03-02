def fraction_of_3(a):
    if abs(a - int(a)) < 0.0001:
        return f"{int(a)}"
    else:
        # if first decimal is 3, then it's 1/3
        if int(str(a)[2]) == 3:
            return f"{int(a)} 1/3"
        # if first decimal is 6, then it's 2/3
        elif int(str(a)[2]) == 6:
            return f"{int(a)} 2/3"
def sortdict(dct: dict, bykey: bool=False, descend: bool=False) -> list[list]:
    """
    Returns a list of lists containing the content of the dictionary, sorted in ascending order by value.
    Each list represents [key, value].
    :param dct: the dictionary to be sorted (note: all keys/values must be comparable to each other)
    :param bykey: when set to True, sorts by keys instead
    :param descend: when set to True, sorts in descending order
    :return: the sorted dictionary as a list of lists
    """

    dlist = [[key, value] for key, value in dct.items()]

    if len(dlist) <= 1:
        return dlist
    else:
        G = {}
        E = [dlist.pop(0)]
        L = {}
        compare = 1
        if bykey:
            compare = 0

        for item in dlist:
            if item[compare] > E[0][compare]:
                G[item[0]] = item[1]
            elif item[compare] == E[0][compare]:
                E.append(item)
            else:
                L[item[0]] = item[1]

        if descend:
            return sortdict(G, bykey=bykey, descend=True) + E + sortdict(L, bykey=bykey, descend=True)
        else:
            return sortdict(L, bykey=bykey) + E + sortdict(G, bykey=bykey)

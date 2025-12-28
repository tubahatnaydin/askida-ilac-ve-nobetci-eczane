def mergesort(liste, key_index):
    if len(liste) <= 1:
        return liste

    mid = len(liste) // 2
    sol = mergesort(liste[:mid], key_index)
    sag = mergesort(liste[mid:], key_index)

    return merge(sol, sag, key_index)

def merge(sol, sag, key_index):
    sonuc = []
    i = j = 0

    while i < len(sol) and j < len(sag):
        if sol[i][key_index] <= sag[j][key_index]:
            sonuc.append(sol[i])
            i += 1
        else:
            sonuc.append(sag[j])
            j += 1

    sonuc.extend(sol[i:])
    sonuc.extend(sag[j:])
    return sonuc

def binary_search(sorted_list, tc, tc_index=1):
    alt = 0
    ust = len(sorted_list) - 1

    while alt <= ust:
        mid = (alt + ust) // 2
        if sorted_list[mid][tc_index] == tc:
            return sorted_list[mid]
        elif sorted_list[mid][tc_index] < tc:
            alt = mid + 1
        else:
            ust = mid - 1

    return None

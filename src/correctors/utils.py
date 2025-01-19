def damerau_levenstein(s1, s2):
    """Return the Damerau-Levenstein distance between two strings"""
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1
    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,      # deletion
                d[(i, j - 1)] + 1,      # insertion
                d[(i - 1, j - 1)] + cost  # substitution
            )
            # Check for transposition
            if (i > 0 and j > 0 and
                    s1[i] == s2[j - 1] and
                    s1[i - 1] == s2[j] and
                    s1[i] != s1[i - 1]):  # Ensure characters are different
                d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + 1)
    return d[lenstr1 - 1, lenstr2 - 1]

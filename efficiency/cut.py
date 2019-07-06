def presel_cuts(channel):
    cuts = []
    if channel == 'Xiccp':
        cuts.append('(Lc_M>2222)&(Lc_M<3333)')
        cuts.append('(Lc_MM>2222)&(Lc_MM<3333)')
    if channel == 'Xiccpp':
        cuts.append('(Lc_MM<3620)&(Lc_MM>3626)')


    return '&'.join(cuts)

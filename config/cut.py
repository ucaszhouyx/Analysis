def get_mm_cuts(steps):
    mm_cuts = []                                              
    stripping_cuts = ['(Lc_MM>1620) & (Lc_MM<3626)']
    offline_cuts = ['(Lc_M>2220) & (Lc_MM<2326)']
    l0_cuts = ['(Lc_L0HadronDecision_TOS)']
    hlt1_cuts = ['(Lc_Hlt1Phys_TOS)']
    hlt2_cuts = ['(Lc_Hlt2Phys_TOS)']
    bdt_cuts = ['(BDTG_80fs_step1>0.5)']
    mass_cuts = ['(Lc_M>2270) & (Lc_MM<2300)']
    if steps == 'tmp':
        mm_cuts.extend(stripping_cuts)                     #add all stripping selection here
    if steps == 'reco':
        mm_cuts.extend(stripping_cuts)                     #add all stripping selection here
        mm_cuts.extend(offline_cuts)
    if steps == 'l0':
        mm_cuts.extend(stripping_cuts)                     #add all stripping selection here
        mm_cuts.extend(offline_cuts)
        mm_cuts.extend(l0_cuts)
    if steps == 'hlt1':
        mm_cuts.extend(stripping_cuts)                     #add all stripping selection here
        mm_cuts.extend(offline_cuts)
        mm_cuts.extend(l0_cuts)
        mm_cuts.extend(hlt1_cuts)
    if steps == 'hlt2':
        mm_cuts.extend(stripping_cuts)                     #add all stripping selection here
        mm_cuts.extend(offline_cuts)
        mm_cuts.extend(l0_cuts)
        mm_cuts.extend(hlt1_cuts)
        mm_cuts.extend(hlt2_cuts)
    if steps == 'pid':
        mm_cuts.extend(stripping_cuts)                     #add all stripping selection here
        mm_cuts.extend(offline_cuts)
        mm_cuts.extend(l0_cuts)
        mm_cuts.extend(hlt1_cuts)
        mm_cuts.extend(hlt2_cuts)
    if steps == 'bdt':
        mm_cuts.extend(stripping_cuts)                     #add all stripping selection here
        mm_cuts.extend(offline_cuts)
        mm_cuts.extend(l0_cuts)
        mm_cuts.extend(hlt1_cuts)
        mm_cuts.extend(hlt2_cuts)
        mm_cuts.extend(bdt_cuts)
    if steps == 'mass_veto':
        mm_cuts.extend(stripping_cuts)                     #add all stripping selection here
        mm_cuts.extend(offline_cuts)
        mm_cuts.extend(l0_cuts)
        mm_cuts.extend(hlt1_cuts)
        mm_cuts.extend(hlt2_cuts)
        mm_cuts.extend(bdt_cuts)
        mm_cuts.extend(mass_cuts)


    return '&'.join(mm_cuts)

def get_ee_cuts(steps):
    ee_cuts = []
    if steps == 'Xiccp':
        ee_cuts.append('(Lc_MM>1620) & (Lc_MM<3626)')
        ee_cuts.append('(Lc_M>2220) & (Lc_MM<2326)')
    if steps == 'Xiccpp':
        ee_cuts.append('(Lc_MM<3620)&(Lc_MM>3626)')


    return '&'.join(ee_cuts)



mt_triggers = [
   "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1",
   "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1",
   #"HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
   #"HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
   #"HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1",
   #"HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1",
   #"HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
   #"HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
   #"HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr",
   #"HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1",
   #"HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1",
   #"HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
   #"HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
]

tt_triggers = [
   #"HLT_DoubleLooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
   #"HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg",
   #"HLT_DoubleLooseChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
   #"HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg",
   "HLT_DoubleMediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
   "HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg",
   #"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
   #"HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg",
   #"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
   #"HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg",
   #"HLT_DoubleTightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
   #"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg",
]

# 
# categories
# mt: SS, OS
# tt: SS, OS

# include total n events in text
# 
# mt want :
#     for given trigger, show 2d with Cut Based vs MVA
# 

import ROOT
ROOT.gROOT.SetBatch(True)

# return x, y postion for filling
# x = tau1 MVA
# y = tau2 MVA
def getTauTau2D( row, iso ) :
    assert( iso == 'MVA' or iso == 'CmbIso' or iso == 'Mix' ), "Poor isolation choice %s" % iso
    if iso == 'MVA' :
        x = getIsoCodeMVA( row, 't' )
        y = getIsoCodeMVA( row, 't2' )
    elif iso == 'CmbIso' :
        x = getIsoCodeCmbIso( row, 't' )
        y = getIsoCodeCmbIso( row, 't2' )
    elif iso == 'Mix' :
        # For Mixed, only to tau1, this is for mt channel mainly
        x = getIsoCodeMVA( row, 't' )
        y = getIsoCodeCmbIso( row, 't' )
    return [x, y]


# return a value which fills with the tighest iso WP passed
def getIsoCodeMVA( row, lep ) :
    # None = 0, VL = 1, L = 2, M = 3, T = 4, VT = 5, VVT = 6
    if getattr( row, lep+'MVAIsoVLoose' ) == 0 :   return 0
    if getattr( row, lep+'MVAIsoLoose' ) == 0 :    return 1
    if getattr( row, lep+'MVAIsoMedium' ) == 0 :   return 2
    if getattr( row, lep+'MVAIsoTight' ) == 0 :    return 3
    if getattr( row, lep+'MVAIsoVTight' ) == 0 :   return 4
    if getattr( row, lep+'MVAIsoVVTight' ) == 0 :  return 5
    if getattr( row, lep+'MVAIsoVVTight' ) == 1 :      return 6
    else : return 0



# return a value which fills with the tighest iso WP passed
def getIsoCodeCmbIso( row, lep ) :
    # None = 0, L = 1, M = 2, T = 3
    if getattr( row, lep+'IsoCmbLoose' ) == 0 :  return 0
    if getattr( row, lep+'IsoCmbMedium' ) == 0 : return 1
    if getattr( row, lep+'IsoCmbTight' ) == 0 :  return 2
    if getattr( row, lep+'IsoCmbTight' ) == 1 :  return 3
    else : return 0


def passes_basic_mt_cuts( row ) :
    if getattr( row, 'transMass' ) > 30 : return 0
    if getattr( row, 'm_vis' ) < 40 :     return 0
    if getattr( row, 'm_vis' ) > 80 :     return 0
    if getattr( row, 'HLT_IsoMu24_eta2p1' ) < 0.5 : return 0
    return 1


def passes_basic_tt_cuts( row ) :
    if getattr( row, 'tPt' ) < 40 :          return 0
    if getattr( row, 'tTrigMatch' ) < 0.5 :  return 0
    if getattr( row, 't2Pt' ) < 40 :         return 0
    #if getattr( row, 't2TrigMatch' ) < 0.5 : return 0
    return 1


def loop( c, tree, data_set, h_mvas, h_cmbs, h_mixs ) :
    for row in tree :
        mva_vals = getTauTau2D( row, 'MVA' ) 
        cmb_vals = getTauTau2D( row, 'CmbIso' )
        mix_vals = getTauTau2D( row, 'Mix' )
        #print i
        #print " -- %i %i" % (mva_vals[0], mva_vals[1])
        #print " -- %i %i" % (cmb_vals[0], cmb_vals[1])
    
        if data_set == 'mt' :
            if not passes_basic_mt_cuts( row ) : continue
        if data_set == 'tt' :
            if not passes_basic_tt_cuts( row ) : continue
    
        for trig, hist in h_mvas.iteritems() :
            if getattr( row, trig ) > 0.5 :
                hist.Fill( mva_vals[0], mva_vals[1], 1 ) 
                # Map to cmb WPs
                h_cmbs[trig].Fill( cmb_vals[0], cmb_vals[1], 1 ) 
                h_mixs[trig].Fill( mix_vals[0], mix_vals[1], 1 ) 
    
        #h_cmb.Fill( cmb_vals[0], cmb_vals[1], 1 )
    for trig, hist in h_mvas.iteritems() :
        c.Clear()
        if hist.Integral() > 0 :
            hist.Scale( 1. / hist.Integral() )
        hist.Draw('COLZ')
        c.SaveAs('/afs/cern.ch/user/t/truggles/www/HLT_Studies/%s_mva_%s.png' % (data_set, trig) )
    for trig, hist in h_cmbs.iteritems() :
        c.Clear()
        if hist.Integral() > 0 :
            hist.Scale( 1. / hist.Integral() )
        hist.Draw('COLZ')
        c.SaveAs('/afs/cern.ch/user/t/truggles/www/HLT_Studies/%s_cmb_%s.png' % (data_set, trig) )
    for trig, hist in h_mixs.iteritems() :
        c.Clear()
        if hist.Integral() > 0 :
            hist.Scale( 1. / hist.Integral() )
        hist.Draw('COLZ')
        c.SaveAs('/afs/cern.ch/user/t/truggles/www/HLT_Studies/%s_mix_%s.png' % (data_set, trig) )

bin_label_map_mva = {
    1 : 'None',
    2 : 'VLoose',
    3 : 'Loose',
    4 : 'Medium',
    5 : 'Tight',
    6 : 'VTight',
    7 : 'VVTight',
}

bin_label_map_cmb = {
    1 : 'None',
    2 : 'Loose',
    3 : 'Medium',
    4 : 'Tight',
}

def make_mva2d_plot( trigger='' ) :
    h_mva = ROOT.TH2D( 'Tau MVA'+trigger, 'Tau MVA ID/Iso WPs %s;Tau1 MVA WP;Tau2 MVA WP' % trigger, 7,-0.5,6.5,7,-0.5,6.5 )
    for k, v in bin_label_map_mva.iteritems() :
        h_mva.GetXaxis().SetBinLabel( k, v )
        h_mva.GetYaxis().SetBinLabel( k, v )
    h_mva.SetDirectory(0)
    return h_mva

def make_cmb2d_plot( trigger='' ) :
    h_cmb = ROOT.TH2D( 'Tau Cmb'+trigger, 'Tau Cmb ID/Iso WPs %s;Tau1 CutBased WP;Tau2 CutBased WP' % trigger, 4,-0.5,3.5,4,-0.5,3.5 )
    for k, v in bin_label_map_cmb.iteritems() :
        h_cmb.GetXaxis().SetBinLabel( k, v )
        h_cmb.GetYaxis().SetBinLabel( k, v )
    h_cmb.SetDirectory(0)
    return h_cmb

def make_mva_vs_cmb2d_plot( trigger='' ) :
    h_mix = ROOT.TH2D( 'Tau MVA Cmb'+trigger, 'Tau MVA vs Cmb ID/Iso WPs %s;Tau1 MVA WP;Tau1 CutBased WP' % trigger, 7,-0.5,6.5,4,-0.5,3.5 )
    for k, v in bin_label_map_mva.iteritems() :
        h_mix.GetXaxis().SetBinLabel( k, v )
    for k, v in bin_label_map_cmb.iteritems() :
        h_mix.GetYaxis().SetBinLabel( k, v )
    h_mix.SetDirectory(0)
    return h_mix




for channel in ['mt',]:# 'tt'] :

    # Channel specific setup
    if channel == 'mt' :
        triggers = mt_triggers
        f = ROOT.TFile('/data/truggles/hlt_studies_2/miniAOD_muon.root', 'r')
    if channel == 'tt' :
        triggers = tt_triggers
        f = ROOT.TFile('/data/truggles/hlt_studies_2/miniAOD_tau.root', 'r') 
    tree = f.Get('tauMiniAODHLTStudies/tagAndProbe/Ntuple')

    print f
    print tree
    
    c = ROOT.TCanvas( 'c1', 'c1', 600, 600 ) 
    p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
    p.Draw()
    ROOT.gPad.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.5 )
    ROOT.gPad.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
    p.Draw()
    p.cd()
    
    #h_mva = make_mva2d_plot()
    #h_cmb = make_cmb2d_plot()
    h_mvas = {}
    h_cmbs = {}
    h_mixs = {}


    for trig in triggers :
        print trig
        h_mvas[ trig ] = make_mva2d_plot(trig)
        h_cmbs[ trig ] = make_cmb2d_plot(trig)
        h_mixs[ trig ] = make_mva_vs_cmb2d_plot(trig)
    
    
    loop( c, tree, channel, h_mvas, h_cmbs, h_mixs )

    for trig in triggers :
        del h_mvas[ trig ]
        del h_cmbs[ trig ]
        del h_mixs[ trig ]
    del c, p








import FWCore.ParameterSet.Config as cms

hpsTauMiniAODHLTStudies = cms.EDAnalyzer("HPSTauHLTStudiesMiniAODAnalyzer",
    hadronSrc = cms.InputTag("tauGenJetsSelectorAllHadrons"),
    tauElectronSrc = cms.InputTag("tauGenJetsSelectorElectrons"),
    tauMuonSrc = cms.InputTag("tauGenJetsSelectorMuons"),
    puSrc = cms.InputTag("slimmedAddPileupInfo"),
    tauSrc = cms.InputTag("slimmedTaus"),
    muonSrc = cms.InputTag("slimmedMuons"),
    electronSrc = cms.InputTag("slimmedElectrons"),
    jetSrc = cms.InputTag("slimmedJets"),
    metSrc = cms.InputTag("slimmedMETs"),
    pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    triggerSrc = cms.InputTag("TriggerResults","","TAUHLT"),
    triggerObjectsSrc = cms.InputTag("slimmedPatTrigger","","LOCALHPS"),
    stage2TauSrc = cms.InputTag("caloStage2Digis","Tau","RECO"),
    genSrc = cms.InputTag("prunedGenParticles","","PAT"),
    eleMediumIdMap = cms.InputTag("egmGsfElectronIDs:mvaEleID-Spring16-GeneralPurpose-V1-wp90"),
    eleLooseIdMap = cms.InputTag("egmGsfElectronIDs:mvaEleID-Spring16-HZZ-V1-wpLoose"),
)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import copy
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import importlib
import os

import HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.ArtusConfigUtility as ACU

def build_config(nickname, **kwargs):
  btag_eff = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "btag-eff" else False
  etau_fake_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "etau-fake-es" else False
  pipelines = kwargs["pipelines"] if "pipelines" in kwargs else None
  minimal_setup = True if "minimal_setup" in kwargs and kwargs["minimal_setup"] else False

  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("DY.?JetsToLLM(10to50|50)", nickname)
  isWjets = re.search("W.?JetsToLNu", nickname)
  isSignal = re.search("HToTauTau",nickname)
  isGluonFusion = re.search("GluGluHToTauTauM125", nickname)

  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsLooseElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsLooseMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsTauID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsJEC",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsSvfit",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsBTaggedJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsTauES",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsMinimalPlotlevelFilter_tt"
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname, **kwargs)

  # explicit configuration
  config["Channel"] = "TT"
  config["MinNTaus"] = 2

  ### HLT & Trigger Object configuration
  config["HltPaths"] = [
    "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg",
    "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg",
  ]
  config["CheckLepton1TriggerMatch"] = [
    "trg_singleelectron",
    "trg_singlemuon_raw",

    "trg_mutaucross",
    "trg_doubletau",
    "trg_muonelectron_mu23ele12",
    "trg_muonelectron_mu8ele23",
  ]
  config["CheckLepton2TriggerMatch"] = [
    "trg_mutaucross",
    "trg_doubletau",
    "trg_muonelectron_mu23ele12",
    "trg_muonelectron_mu8ele23",
  ]
  config["HLTBranchNames"] = [
    "trg_singleelectron:HLT_Ele25_eta2p1_WPTight_Gsf_v",
    "trg_singlemuon_raw:HLT_IsoMu22_v",
    "trg_singlemuon_raw:HLT_IsoTkMu22_v",
    "trg_singlemuon_raw:HLT_IsoMu22_eta2p1_v",
    "trg_singlemuon_raw:HLT_IsoTkMu22_eta2p1_v",
    "trg_mutaucross:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",
    "trg_mutaucross:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v"
    "trg_doubletau:HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v",
    "trg_doubletau:HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v",
    "trg_muonelectron_mu23ele12:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v",
    "trg_muonelectron_mu23ele12:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v",
    "trg_muonelectron_mu8ele23:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v",
    "trg_muonelectron_mu8ele23:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v",
  ]
  config["DiTauPairLepton1LowerPtCuts"] = [
      "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg:40.0",
      "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg:40.0"
  ]
  config["DiTauPairLepton2LowerPtCuts"] = [
      "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg:40.0",
      "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg:40.0"
  ]
  config["TauTriggerFilterNames"] = [
      "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumIsolationDz02Reg",
      "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumCombinedIsolationDz02Reg"
  ]

  ### Signal pair selection configuration
  config["TauID"] = "TauIDRecommendation13TeV"
  config["TauUseOldDMs"] = True
  config["TauLowerPtCuts"] = ["40.0"]
  config["TauUpperAbsEtaCuts"] = ["2.1"]
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["DiTauPairIsTauIsoMVA"] = True
  config["TauTauRestFrameReco"] = "collinear_approximation"
  config["TriggerObjectLowerPtCut"] = 28.0
  config["InvalidateNonMatchingElectrons"] = False
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  config["DirectIso"] = True
  config["OSChargeLeptons"] = True
  config["AddGenMatchedTaus"] = True
  config["AddGenMatchedTauJets"] = True
  config["BranchGenMatchedTaus"] = True

  ### Efficiencies & weights configuration
  config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
  config["TauTauTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
  config["TauTauTriggerWeightWorkspaceWeightNames"] = [
      "0:triggerWeight",
      "1:triggerWeight"]
  config["TauTauTriggerWeightWorkspaceObjectNames"] = [
      "0:t_genuine_TightIso_tt_ratio,t_fake_TightIso_tt_ratio",
      "1:t_genuine_TightIso_tt_ratio,t_fake_TightIso_tt_ratio"]
  config["TauTauTriggerWeightWorkspaceObjectArguments"] = [
      "0:t_pt,t_dm",
      "1:t_pt,t_dm"]
  config["EventWeight"] = "eventWeight"
  config["TopPtReweightingStrategy"] = "Run1"

  ### Ntuple output quantities configuration
  config["Quantities"] =      importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.syncQuantities").build_list(isMC = (not isData) and (not isEmbedded), nickname = nickname)
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  config["Quantities"].extend([
      "nLooseElectrons",
      "nLooseMuons",
      "nDiTauPairCandidates",
      "nAllDiTauPairCandidates",
      "trg_doubletau",
      "lep1ErrD0",
      "lep1ErrDz",
      "lep2ErrD0",
      "lep2ErrDz",
      "PVnDOF",
      #"PVchi2",
      #"drel0_1",
      #"drel0_2",
      #"drelZ_1",
      #"drelZ_2",
      "flagMETFilter",
      "pt_ttjj"
  ])
  if re.search("HToTauTauM125", nickname):
    config["Quantities"].extend([
      "htxs_stage0cat",
      "htxs_stage1p1cat",
      "htxs_stage1p1finecat"
    ])
  if isGluonFusion:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.ggHNNLOQuantities").build_list())

  ### Processors & consumers configuration
  config["Processors"] = []
  #if not (isEmbedded):           config["Processors"].append( "producer:ElectronCorrectionsProducer")
  config["Processors"].extend((                               "producer:HttValidLooseElectronsProducer",
                                                              "producer:HttValidLooseMuonsProducer",
                                                              "producer:HltProducer",
                                                              "producer:MetSelector"))
  if not (isData): config["Processors"].append( "producer:TauCorrectionsProducer")
  if not isData:                 config["Processors"].append( "producer:HttValidGenTausProducer")
  config["Processors"].extend((                               "producer:ValidTausProducer",
                                                              "filter:ValidTausFilter",
                                                              "producer:TauTriggerMatchingProducer",
                                                              "filter:MinTausCountFilter",
                                                              "producer:ValidElectronsProducer",
                                                              "producer:ValidMuonsProducer",
                                                              "producer:NewValidTTPairCandidatesProducer",
                                                              "filter:ValidDiTauPairCandidatesFilter",
                                                              "producer:Run2DecayChannelProducer"))
  if not (isData or isEmbedded): config["Processors"].append( "producer:TaggedJetCorrectionsProducer")
  config["Processors"].extend((                               "producer:ValidTaggedJetsProducer",
                                                              "producer:ValidBTaggedJetsProducer"))
  if btag_eff: config["ProcessorsBtagEff"] = copy.deepcp(config["Processors"])
  if not (isData or isEmbedded):  config["Processors"].append("producer:MetCorrector")
  config["Processors"].extend((                               "producer:SimpleEleTauFakeRateWeightProducer",
                                                              "producer:SimpleMuTauFakeRateWeightProducer"))
  if isTTbar:                    config["Processors"].append( "producer:TopPtReweightingProducer")
  if isDY or isEmbedded:        config["Processors"].append( "producer:ZPtReweightProducer")
  config["Processors"].extend((                               "producer:TauTauRestFrameSelector",
                                                              "producer:DiLeptonQuantitiesProducer",
                                                              "producer:DiJetQuantitiesProducer",
                                                              "filter:MinimalPlotlevelFilter"))
  if isEmbedded:                 config["Processors"].append( "producer:EmbeddedWeightProducer")
  if isEmbedded:                 config["Processors"].append( "producer:TauDecayModeWeightProducer")
  #if not isData:                 config["Processors"].append( "producer:TauTrigger2017EfficiencyProducer")
  if not isData:                 config["Processors"].append( "producer:TauTauTriggerWeightProducer")
  config["Processors"].append(                                "producer:EventWeightProducer")
  if isGluonFusion:              config["Processors"].append( "producer:SMggHNNLOProducer")
  config["Processors"].append(                                "producer:SvfitProducer")
  config["Consumers"] = ["KappaLambdaNtupleConsumer",
                         "cutflow_histogram"]

  # Subanalyses settings
  if btag_eff:
     config["Processors"] = copy.deepcp(config["ProcessorsBtagEff"])

     btag_eff_unwanted = ["KappaLambdaNtupleConsumer", "CutFlowTreeConsumer", "KappaElectronsConsumer", "KappaTausConsumer", "KappaTaggedJetsConsumer", "RunTimeConsumer", "PrintEventsConsumer"]
     for unwanted in btag_eff_unwanted:
      if unwanted in config["Consumers"]: config["Consumers"].remove(unwanted)

     config["Consumers"].append("BTagEffConsumer")

  # pipelines - systematic shifts
  # needed pipelines: nominal tauESperDM_shifts regionalJECunc_shifts METunc_shifts METrecoil_shifts btagging_shifts
  if pipelines is None:
      raise Exception("pipelines is None in %s" % (__file__))

  return_conf = jsonTools.JsonDict()
  for pipeline in pipelines:
      log.info('Add pipeline: %s' %(pipeline))
      return_conf += ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis." + pipeline).build_config(nickname, **kwargs))
  return return_conf

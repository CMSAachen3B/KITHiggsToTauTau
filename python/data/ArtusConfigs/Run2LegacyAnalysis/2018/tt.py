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
  nmssm = True if ("nmssm" in kwargs and kwargs["nmssm"]) else False

  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("DY.?JetsToLLM(10to50|50)", nickname)
  isWjets = re.search("(W.?Jets|WG)ToLNu", nickname)
  isSignal = re.search("NMSSM|HToTauTau",nickname)
  isNMSSM = re.search("NMSSM",nickname)
  isHWW = re.search("HToWW",nickname)
  isGluonFusion = re.search("(GluGluHToTauTau|ggZHHToTauTauZToQQ).*M125", nickname)
  isVBF = re.search("(VBFHToTauTau.*M125|^W(minus|plus)HToTauTau.*125.*|^ZHToTauTau.*125.*)", nickname)
  isSUSYggH = re.search("SUSYGluGluToH", nickname) or re.search("GluGluHToTauTauM95", nickname)

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
          "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
          "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
          "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg",
          "HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg",
          "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
  ]
  config["DiTauPairLepton1LowerPtCuts"] = [
          "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v:40.0",
          # "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v:45.0",
          # "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v:45.0",
          "HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v:40.0",
  ]
  config["DiTauPairLepton2LowerPtCuts"] = [
          "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v:40.0",
          # "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v:45.0",
          # "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v:45.0",
          "HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v:40.0",
  ]
  config["CheckL1MatchForDiTauPairLepton1"] = True
  config["CheckL1MatchForDiTauPairLepton2"] = True
  config["CheckLepton1TriggerMatch"] = [
      "trg_singlemuon_24",
      "trg_singlemuon_27",
      "trg_singlemuon",
      "trg_singletau_leading",
      "trg_singleelectron_27",
      "trg_singleelectron_32",
      "trg_singleelectron_32_fallback",
      "trg_singleelectron_35",
      "trg_singleelectron",

      "trg_crossmuon_mu20tau27",
      "trg_crossmuon_mu20tau27_hps",
      "trg_mutacross",
      "trg_crossele_ele24tau30",
      "trg_crossele_ele24tau30_hps",
      "trg_etaucross",
      "trg_doubletau_35_tightiso_tightid",
      "trg_doubletau_40_mediso_tightid",
      "trg_doubletau_40_tightiso",
      "trg_doubletau_35_mediso_hps",
      "trg_muonelectron_mu12ele23",
      "trg_muonelectron_mu23ele12",
      "trg_muonelectron_mu8ele23",
  ]
  config["CheckLepton2TriggerMatch"] = [
      "trg_singletau_trailing",

      "trg_crossmuon_mu20tau27",
      "trg_crossmuon_mu20tau27_hps",
      "trg_mutaucross",
      "trg_crossele_ele24tau30",
      "trg_crossele_ele24tau30_hps",
      "trg_etaucross",
      "trg_doubletau_35_tightiso_tightid",
      "trg_doubletau_40_mediso_tightid",
      "trg_doubletau_40_tightiso",
      "trg_doubletau_35_mediso_hps"
      "trg_muonelectron_mu12ele23",
      "trg_muonelectron_mu23ele12",
      "trg_muonelectron_mu8ele23",
  ]
  config["HLTBranchNames"] = [
      "trg_singlemuon_24:HLT_IsoMu24_v",
      "trg_singlemuon_27:HLT_IsoMu27_v",
      "trg_singlemuon:HLT_IsoMu24_v",
      "trg_singlemuon:HLT_IsoMu27_v",
      "trg_crossmuon_mu20tau27:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v",
      "trg_crossmuon_mu20tau27_hps:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v",
      "trg_mutaucross:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v",
      "trg_mutaucross:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v",
      "trg_singleelectron_27:HLT_Ele27_WPTight_Gsf_v",
      "trg_singleelectron_32:HLT_Ele32_WPTight_Gsf_v",
      "trg_singleelectron_32_fallback:HLT_Ele32_WPTight_Gsf_DoubleL1EG_v",
      "trg_singleelectron_35:HLT_Ele35_WPTight_Gsf_v",
      "trg_singleelectron:HLT_Ele27_WPTight_Gsf_v",
      "trg_singleelectron:HLT_Ele32_WPTight_Gsf_v",
      "trg_singleelectron:HLT_Ele35_WPTight_Gsf_v",
      "trg_crossele_ele24tau30:HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v",
      "trg_crossele_ele24tau30_hps:HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v",
      "trg_etaucross:HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v",
      "trg_etaucross:HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v",
      "trg_doubletau_35_tightiso_tightid:HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v",
      "trg_doubletau_40_mediso_tightid:HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v",
      "trg_doubletau_40_tightiso:HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v",
      "trg_doubletau_35_mediso_hps:HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v",
      "trg_singletau_leading:HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v",
      "trg_singletau_trailing:HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v",
      "trg_muonelectron_mu12ele23:HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v",
      "trg_muonelectron_mu23ele12:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v",
      "trg_muonelectron_mu8ele23:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v",
  ]
  if isEmbedded:
    config["TauTriggerFilterNames"] = [
            "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v:hltDoubleL2IsoTau26eta2p2",
            "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v:hltDoubleL2IsoTau26eta2p2",
            "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v:hltDoubleL2IsoTau26eta2p2",
            "HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v:hltDoubleL2IsoTau26eta2p2",
            "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltSingleL2Tau80eta2p2",
    ]
  else:
    config["TauTriggerFilterNames"] = [
            "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v:hltDoublePFTau35TrackPt1TightChargedIsolationAndTightOOSCPhotonsDz02Reg",
            "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v:hltDoublePFTau40TrackPt1MediumChargedIsolationAndTightOOSCPhotonsDz02Reg",
            "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v:hltDoublePFTau40TrackPt1TightChargedIsolationDz02Reg",
            "HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v:hltHpsDoublePFTau35TrackPt1MediumChargedIsolationDz02Reg",
            "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltPFTau180TrackPt50LooseAbsOrRelMediumHighPtRelaxedIsoIso",
            "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltSelectedPFTau180MediumChargedIsolationL1HLTMatched",
    ]
  # TODO: Check if this is still necessary for 2018.
  config["TauTriggerCheckL1Match"] = [
          "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v",
          "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v",
          "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v",
          "HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v",
  ]

  ### Electron scale and smear corrections
  config["ElectronScaleAndSmearUsed"] = False
  config["ElectronScaleAndSmearTag"] = "ecalTrkEnergyPostCorr"

  ### Signal pair selection configuration
  config["TauID"] = "TauIDRecommendation13TeV"
  config["TauUseOldDMs"] = False
  config["TauVeto2ProngDMs"] = True
  config["TauLowerPtCuts"] = ["40.0"]
  config["TauUpperAbsEtaCuts"] = ["2.1"]
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["DeltaRTriggerMatchingTaus"] = 0.5
  config["DiTauPairIsTauIsoMVA"] = True
  config["TauTauRestFrameReco"] = "collinear_approximation"
  config["InvalidateNonMatchingElectrons"] = False
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  config["DirectIso"] = True
  config["OSChargeLeptons"] = True
  config["AddGenMatchedTaus"] = True
  config["AddGenMatchedTauJets"] = True
  config["BranchGenMatchedTaus"] = True

  ### Met correction SF for embedding
  if isEmbedded:
    config["EmbeddingFakeMETCorrectionNumApplies"] = 1
    config["EmbedddingFakeMETCorrection"] = "(x-y)*0.885 + y*(1.+-0.004)"

  ### Efficiencies & weights configuration
  config["TauTriggerInput"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/tauTriggerEfficiencies2018KIT_deeptau.root"
  config["TauTriggerInputKIT"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/tauTriggerEfficiencies2018KIT_deeptau.root"
  config["TauTrigger"] = "ditau"
  config["TauTriggerWorkingPoints"] = [
       "VVVLoose",
       "VVLoose",
       "VLoose",
       "Loose",
       "Medium",
       "Tight",
       "VTight",
       "VVTight",
  ]
  config["TauTriggerIDTypes"] = [
       # "MVAv2",
       "DeepTau",
  ]
  if isEmbedded:
    config["TauTriggerEfficiencyWeightNames"] = [
        "0:crossTriggerDataEfficiencyWeight",
        "0:crossTriggerKITDataEfficiencyWeight",
        "0:crossTriggerEMBEfficiencyWeight",
        "0:crossTriggerMCEfficiencyWeight",
        "1:crossTriggerDataEfficiencyWeight",
        "1:crossTriggerKITDataEfficiencyWeight",
        "1:crossTriggerEMBEfficiencyWeight",
        "1:crossTriggerMCEfficiencyWeight",
    ]
  else:
    config["TauTriggerEfficiencyWeightNames"] = [
        "0:crossTriggerMCEfficiencyWeight",
        "0:crossTriggerDataEfficiencyWeight",
        "1:crossTriggerMCEfficiencyWeight",
        "1:crossTriggerDataEfficiencyWeight",
    ]
  config["TauTriggerSFProviderInput"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/2018_tauTriggerEff_DeepTau2017v2p1.root"
  config["TauTriggerSFProviderWeightNames"] = [
        "0:crossTriggerDataEfficiencyWeight_POG",
        "0:crossTriggerMCEfficiencyWeight_POG",
        "0:crossTriggerSFWeight_POG",
        "1:crossTriggerDataEfficiencyWeight_POG",
        "1:crossTriggerMCEfficiencyWeight_POG",
        "1:crossTriggerSFWeight_POG",
    ]

  # Define weight names to be written out - only store weights that are actually filled
  tauTriggerWeights = []
  for WeightName in config["TauTriggerEfficiencyWeightNames"]:
    for shift in ["","Up","Down"]:
      for IDType in config["TauTriggerIDTypes"]:
        for wp in config["TauTriggerWorkingPoints"]:
          tauTriggerWeights.append(WeightName.split(":")[1]+shift+"_"+wp+"_"+IDType+"_"+str(int(WeightName.split(":")[0])+1))
  for WeightName in config["TauTriggerSFProviderWeightNames"]:
    for shift in ["","Up","Down"]:
        for wp in config["TauTriggerWorkingPoints"]:
          tauTriggerWeights.append(WeightName.split(":")[1]+shift+"_"+wp+"_"+str(int(WeightName.split(":")[0])+1))

  config["SingleTauTriggerInput"] = "$CMSSW_BASE/src/TauAnalysisTools/TauTriggerSFs/data/tauTriggerEfficiencies2018_singletau.root"
  config["SingleTauTriggerWorkingPoints"] = [
       "vvvloose",
       "vvloose",
       "vloose",
       "loose",
       "medium",
       "tight",
       "vtight",
       "vvtight",
  ]
  config["SingleTauTriggerIDTypes"] = [
       # "MVAv2",
       "DeepTau",
  ]
  singleTauTriggerWeights = []
  if not isData:
    config["SingleTauTriggerEfficiencyWeightNames"] = [
        "0:singleTauTriggerMCEfficiencyWeight",
        "0:singleTauTriggerDataEfficiencyWeight",
        "1:singleTauTriggerMCEfficiencyWeight",
        "1:singleTauTriggerDataEfficiencyWeight",
    ]

    # Define weight names to be written out - only store weights that are actually filled
    for WeightName in config["SingleTauTriggerEfficiencyWeightNames"]:
      for shift in ["","Up","Down"]:
          if "MC" in WeightName and shift in ["Up", "Down"]:
              continue
          for IDType in config["SingleTauTriggerIDTypes"]:
            for wp in config["SingleTauTriggerWorkingPoints"]:
              singleTauTriggerWeights.append(WeightName.split(":")[1]+shift+"_"+wp+"_"+IDType+"_"+str(int(WeightName.split(":")[0])+1))

  config["TauIDSFWorkingPoints"] = [
       "VVVLoose",
       "VVLoose",
       "VLoose",
       "Loose",
       "Medium",
       "Tight",
       "VTight",
       "VVTight",
  ]
  config["TauIDSFTypes"] = [
       "DeepTau2017v2p1VSjet",
  ]
  config["TauIDSFWeightNames"] = [
      "0:tauIDScaleFactorWeight",
      "1:tauIDScaleFactorWeight",
  ]
  config["TauIDSFUseEMBSFs"] = isEmbedded
  config["TauIDSFUseTightVSeSFs"] = False
  config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2018.root"
  if isEmbedded:
    config["EmbeddedWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2018.root"
    config["EmbeddedWeightWorkspaceWeightNames"] = [
            "0:muonEffTrgWeight",
            "0:muonEffIDWeight",
            "1:muonEffIDWeight",

            "0:muonEffTrgWeightIC",
            "0:muonEffIDWeightIC",
            "1:muonEffIDWeightIC",

            "0:triggerWeight",
            "1:triggerWeight",
            #"0:triggerdmBinnedWeight",
            #"1:triggerdmBinnedWeight",
            ]
    config["EmbeddedWeightWorkspaceObjectNames"] = [
            "0:m_sel_trg_ratio",
            "0:m_sel_idEmb_ratio",
            "1:m_sel_idEmb_ratio",

            "0:m_sel_trg_ic_ratio",
            "0:m_sel_id_ic_ratio",
            "1:m_sel_id_ic_ratio",

            "0:tt_emb_PFTau35OR40_tight_kit_ratio",
            "1:tt_emb_PFTau35OR40_tight_kit_ratio",
            #"0:tt_emb_PFTau35OR40_tight_dm_binned_kit_ratio",
            #"1:tt_emb_PFTau35OR40_tight_dm_binned_kit_ratio",
            ]
    config["EmbeddedWeightWorkspaceObjectArguments"] = [
            "0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
            "0:gt_pt,gt_eta",
            "1:gt_pt,gt_eta",

            "0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
            "0:gt_pt,gt_eta",
            "1:gt_pt,gt_eta",

            "0:t_pt",
            "1:t_pt",
            #"0:t_pt,t_dm",
            #"1:t_pt,t_dm",
            ]
    config["HighPtTauWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_trimmed_highpttau_tt_2018.root"
    config["HighPtTauWeightWorkspaceWeightNames"] = [
            "0:tauIDScaleFactorWeight_highpt_deeptauid",
            "1:tauIDScaleFactorWeight_highpt_deeptauid",

            "0:tauIDScaleFactorWeight_highpt_deeptauid_100To500Up",
            "0:tauIDScaleFactorWeight_highpt_deeptauid_100To500Down",
            "0:tauIDScaleFactorWeight_highpt_deeptauid_Gt500Up",
            "0:tauIDScaleFactorWeight_highpt_deeptauid_Gt500Down",

            "1:tauIDScaleFactorWeight_highpt_deeptauid_100To500Up",
            "1:tauIDScaleFactorWeight_highpt_deeptauid_100To500Down",
            "1:tauIDScaleFactorWeight_highpt_deeptauid_Gt500Up",
            "1:tauIDScaleFactorWeight_highpt_deeptauid_Gt500Down",

            "0:tautau_triggerweight_ic",

            "0:tautau_triggerweight_ic_singletau_up",
            "0:tautau_triggerweight_ic_singletau_down",

            "0:tautau_triggerweight_ic_lowpt_dm0_up",
            "0:tautau_triggerweight_ic_lowpt_dm0_down",
            "0:tautau_triggerweight_ic_lowpt_dm1_up",
            "0:tautau_triggerweight_ic_lowpt_dm1_down",
            "0:tautau_triggerweight_ic_lowpt_dm10_up",
            "0:tautau_triggerweight_ic_lowpt_dm10_down",
            "0:tautau_triggerweight_ic_lowpt_dm11_up",
            "0:tautau_triggerweight_ic_lowpt_dm11_down",

            "0:tautau_triggerweight_ic_highpt_dm0_up",
            "0:tautau_triggerweight_ic_highpt_dm0_down",
            "0:tautau_triggerweight_ic_highpt_dm1_up",
            "0:tautau_triggerweight_ic_highpt_dm1_down",
            "0:tautau_triggerweight_ic_highpt_dm10_up",
            "0:tautau_triggerweight_ic_highpt_dm10_down",
            "0:tautau_triggerweight_ic_highpt_dm11_up",
            "0:tautau_triggerweight_ic_highpt_dm11_down",
            ]
    config["HighPtTauWeightWorkspaceObjectNames"] = [
            "0:t_deeptauid_highpt_embed",
            "1:t_deeptauid_highpt_embed",

            "0:t_deeptauid_highpt_embed_bin5_up",
            "0:t_deeptauid_highpt_embed_bin5_down",
            "0:t_deeptauid_highpt_embed_bin6_up",
            "0:t_deeptauid_highpt_embed_bin6_down",

            "1:t_deeptauid_highpt_embed_bin5_up",
            "1:t_deeptauid_highpt_embed_bin5_down",
            "1:t_deeptauid_highpt_embed_bin6_up",
            "1:t_deeptauid_highpt_embed_bin6_down",

            "0:t_trg_2d_embed_ratio",

            "0:t_trg_2d_embed_ratio_singletau_up",
            "0:t_trg_2d_embed_ratio_singletau_down",

            "0:t_trg_2d_embed_ratio_lowpt_dm0_up",
            "0:t_trg_2d_embed_ratio_lowpt_dm0_down",
            "0:t_trg_2d_embed_ratio_lowpt_dm1_up",
            "0:t_trg_2d_embed_ratio_lowpt_dm1_down",
            "0:t_trg_2d_embed_ratio_lowpt_dm10_up",
            "0:t_trg_2d_embed_ratio_lowpt_dm10_down",
            "0:t_trg_2d_embed_ratio_lowpt_dm11_up",
            "0:t_trg_2d_embed_ratio_lowpt_dm11_down",

            "0:t_trg_2d_embed_ratio_highpt_dm0_up",
            "0:t_trg_2d_embed_ratio_highpt_dm0_down",
            "0:t_trg_2d_embed_ratio_highpt_dm1_up",
            "0:t_trg_2d_embed_ratio_highpt_dm1_down",
            "0:t_trg_2d_embed_ratio_highpt_dm10_up",
            "0:t_trg_2d_embed_ratio_highpt_dm10_down",
            "0:t_trg_2d_embed_ratio_highpt_dm11_up",
            "0:t_trg_2d_embed_ratio_highpt_dm11_down",
            ]
    config["HighPtTauWeightWorkspaceObjectArguments"] = [
            "0:t_pt",
            "1:t_pt",

            "0:t_pt",
            "0:t_pt",
            "0:t_pt",
            "0:t_pt",

            "1:t_pt",
            "1:t_pt",
            "1:t_pt",
            "1:t_pt",

            "0:t_pt,t_dm,t_pt_2,t_dm_2",  # Zero in front of line necessary to ensure correct readout of pt_1.

            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",

            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",

            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            ]
    config["EmbeddedZpTMassCorrectionFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/embed_zmm_shifts_v2.root"
    config["EmbeddedZpTMassCorrectionHistogram"] = "shifts_2018"
  elif not isData:
    config["HighPtTauWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_trimmed_highpttau_tt_2018.root"
    config["HighPtTauWeightWorkspaceWeightNames"] = [
            "0:tauIDScaleFactorWeight_highpt_deeptauid",
            "1:tauIDScaleFactorWeight_highpt_deeptauid",

            "0:tauIDScaleFactorWeight_highpt_deeptauid_100To500Up",
            "0:tauIDScaleFactorWeight_highpt_deeptauid_100To500Down",
            "0:tauIDScaleFactorWeight_highpt_deeptauid_Gt500Up",
            "0:tauIDScaleFactorWeight_highpt_deeptauid_Gt500Down",

            "1:tauIDScaleFactorWeight_highpt_deeptauid_100To500Up",
            "1:tauIDScaleFactorWeight_highpt_deeptauid_100To500Down",
            "1:tauIDScaleFactorWeight_highpt_deeptauid_Gt500Up",
            "1:tauIDScaleFactorWeight_highpt_deeptauid_Gt500Down",

            "0:tautau_triggerweight_ic",

            "0:tautau_triggerweight_ic_singletau_up",
            "0:tautau_triggerweight_ic_singletau_down",

            "0:tautau_triggerweight_ic_lowpt_dm0_up",
            "0:tautau_triggerweight_ic_lowpt_dm0_down",
            "0:tautau_triggerweight_ic_lowpt_dm1_up",
            "0:tautau_triggerweight_ic_lowpt_dm1_down",
            "0:tautau_triggerweight_ic_lowpt_dm10_up",
            "0:tautau_triggerweight_ic_lowpt_dm10_down",
            "0:tautau_triggerweight_ic_lowpt_dm11_up",
            "0:tautau_triggerweight_ic_lowpt_dm11_down",

            "0:tautau_triggerweight_ic_highpt_dm0_up",
            "0:tautau_triggerweight_ic_highpt_dm0_down",
            "0:tautau_triggerweight_ic_highpt_dm1_up",
            "0:tautau_triggerweight_ic_highpt_dm1_down",
            "0:tautau_triggerweight_ic_highpt_dm10_up",
            "0:tautau_triggerweight_ic_highpt_dm10_down",
            "0:tautau_triggerweight_ic_highpt_dm11_up",
            "0:tautau_triggerweight_ic_highpt_dm11_down",
            ]
    config["HighPtTauWeightWorkspaceObjectNames"] = [
            "0:t_deeptauid_highpt",
            "1:t_deeptauid_highpt",

            "0:t_deeptauid_highpt_bin5_up",
            "0:t_deeptauid_highpt_bin5_down",
            "0:t_deeptauid_highpt_bin6_up",
            "0:t_deeptauid_highpt_bin6_down",

            "1:t_deeptauid_highpt_bin5_up",
            "1:t_deeptauid_highpt_bin5_down",
            "1:t_deeptauid_highpt_bin6_up",
            "1:t_deeptauid_highpt_bin6_down",

            "0:t_trg_2d_ratio",

            "0:t_trg_2d_ratio_singletau_up",
            "0:t_trg_2d_ratio_singletau_down",

            "0:t_trg_2d_ratio_lowpt_dm0_up",
            "0:t_trg_2d_ratio_lowpt_dm0_down",
            "0:t_trg_2d_ratio_lowpt_dm1_up",
            "0:t_trg_2d_ratio_lowpt_dm1_down",
            "0:t_trg_2d_ratio_lowpt_dm10_up",
            "0:t_trg_2d_ratio_lowpt_dm10_down",
            "0:t_trg_2d_ratio_lowpt_dm11_up",
            "0:t_trg_2d_ratio_lowpt_dm11_down",

            "0:t_trg_2d_ratio_highpt_dm0_up",
            "0:t_trg_2d_ratio_highpt_dm0_down",
            "0:t_trg_2d_ratio_highpt_dm1_up",
            "0:t_trg_2d_ratio_highpt_dm1_down",
            "0:t_trg_2d_ratio_highpt_dm10_up",
            "0:t_trg_2d_ratio_highpt_dm10_down",
            "0:t_trg_2d_ratio_highpt_dm11_up",
            "0:t_trg_2d_ratio_highpt_dm11_down",
            ]
    config["HighPtTauWeightWorkspaceObjectArguments"] = [
            "0:t_pt",
            "1:t_pt",

            "0:t_pt",
            "0:t_pt",
            "0:t_pt",
            "0:t_pt",

            "1:t_pt",
            "1:t_pt",
            "1:t_pt",
            "1:t_pt",

            "0:t_pt,t_dm,t_pt_2,t_dm_2",  # Zero in front of line necessary to ensure correct readout of pt_1.

            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",

            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",

            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            "0:t_pt,t_dm,t_pt_2,t_dm_2",
            ]
    # config["TauTauTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2018.root"
    # config["TauTauTriggerWeightWorkspaceWeightNames"] = [
    #     "0:triggerWeight",
    #     "1:triggerWeight"
    # ]
    # config["TauTauTriggerWeightWorkspaceObjectNames"] = [
    #     "0:t_genuine_MediumIso_tt_ratio,t_fake_MediumIso_tt_ratio",
    #     "1:t_genuine_MediumIso_tt_ratio,t_fake_MediumIso_tt_ratio"
    # ]
    # config["TauTauTriggerWeightWorkspaceObjectArguments"] = [
    #     "0:t_pt,t_dm",
    #     "1:t_pt,t_dm"
    # ]
  config["EventWeight"] = "eventWeight"
  config["TopPtReweightingStrategy"] = "Run1"

  ### Ntuple output quantities configuration
  config["Quantities"] =      importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.syncQuantities").build_list(minimal_setup=minimal_setup, isMC = (not isData) and (not isEmbedded), nickname = nickname, nmssm=nmssm)
  if isNMSSM: config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.lheWeights").build_list(nmssm=nmssm))
  # config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.zptQuantities").build_list())
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  config["Quantities"].extend(tauTriggerWeights)
  config["Quantities"].extend(singleTauTriggerWeights)
  config["Quantities"].extend([
      "had_gen_match_pT_1",
      "had_gen_match_pT_2",
      "flagMETFilter",
      "tauIDScaleFactorWeight_highpt_deeptauid_1",
      "tauIDScaleFactorWeight_highpt_deeptauid_2",
      "tauIDScaleFactorWeight_highpt_deeptauid_100To500Up_1", "tauIDScaleFactorWeight_highpt_deeptauid_100To500Down_1",
      "tauIDScaleFactorWeight_highpt_deeptauid_Gt500Up_1", "tauIDScaleFactorWeight_highpt_deeptauid_Gt500Down_1",
      "tauIDScaleFactorWeight_highpt_deeptauid_100To500Up_1", "tauIDScaleFactorWeight_highpt_deeptauid_100To500Down_1",
      "tauIDScaleFactorWeight_highpt_deeptauid_Gt500Up_1", "tauIDScaleFactorWeight_highpt_deeptauid_Gt500Down_1",
      "tauIDScaleFactorWeight_highpt_deeptauid_100To500Up_2", "tauIDScaleFactorWeight_highpt_deeptauid_100To500Down_2",
      "tauIDScaleFactorWeight_highpt_deeptauid_Gt500Up_2", "tauIDScaleFactorWeight_highpt_deeptauid_Gt500Down_2",
      "tauIDScaleFactorWeight_highpt_deeptauid_100To500Up_2", "tauIDScaleFactorWeight_highpt_deeptauid_100To500Down_2",
      "tauIDScaleFactorWeight_highpt_deeptauid_Gt500Up_2", "tauIDScaleFactorWeight_highpt_deeptauid_Gt500Down_2",
      "tautau_triggerweight_ic",
      "tautau_triggerweight_ic_singletau_up", "tautau_triggerweight_ic_singletau_down",
      "tautau_triggerweight_ic_highpt_dm0_up", "tautau_triggerweight_ic_highpt_dm0_down", "tautau_triggerweight_ic_highpt_dm1_up", "tautau_triggerweight_ic_highpt_dm1_down", "tautau_triggerweight_ic_highpt_dm10_up", "tautau_triggerweight_ic_highpt_dm10_down", "tautau_triggerweight_ic_highpt_dm11_up", "tautau_triggerweight_ic_highpt_dm11_down",
      "tautau_triggerweight_ic_lowpt_dm0_up", "tautau_triggerweight_ic_lowpt_dm0_down", "tautau_triggerweight_ic_lowpt_dm1_up", "tautau_triggerweight_ic_lowpt_dm1_down", "tautau_triggerweight_ic_lowpt_dm10_up", "tautau_triggerweight_ic_lowpt_dm10_down", "tautau_triggerweight_ic_lowpt_dm11_up", "tautau_triggerweight_ic_lowpt_dm11_down",
  ])
  if isEmbedded:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.embeddedDecayModeWeightQuantities").build_list())
    config["Quantities"].extend([
          "muonEffTrgWeight", "muonEffIDWeight_1","muonEffIDWeight_2", "crossTriggerEmbeddedWeight_1", "crossTriggerEmbeddedWeight_2", #, "triggerdmBinnedWeight_1", "triggerdmBinnedWeight_2"
          "embedZpTMassWeight",
          ])
  if re.search("HToTauTau.*M125", nickname):
    config["Quantities"].extend([
      "htxs_stage0cat",
      "htxs_stage1p1cat",
      "htxs_stage1p1finecat",
      "htxs_njets30",
      "htxs_higgsPt",
    ])
  if isGluonFusion:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.ggHNNLOQuantities").build_list())
  if isVBF:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.qqHNNLOQuantities").build_list())
  if isNMSSM:
    config["Quantities"].extend(["genBosonMass_h1","genBosonMass_h2","genBosonMass_h3","genBosonPt_h1","genBosonPt_h2","genBosonPt_h3","genBosonEta_h1","genBosonEta_h2","genBosonEta_h3"])
  if isSUSYggH and re.search("powheg", nickname):
    config["Quantities"].extend(["ggh_b_weight_hdamp_up", "ggh_i_weight_hdamp_up", "ggh_t_weight_hdamp_up",
                                 "ggh_b_weight_hdamp_down", "ggh_i_weight_hdamp_down", "ggh_t_weight_hdamp_down",
                                 "ggh_b_weight_scale_up", "ggh_i_weight_scale_up", "ggh_t_weight_scale_up",
                                 "ggh_b_weight_scale_down", "ggh_i_weight_scale_down", "ggh_t_weight_scale_down",
                                 "ggA_b_weight_hdamp_up", "ggA_i_weight_hdamp_up", "ggA_t_weight_hdamp_up",
                                 "ggA_b_weight_hdamp_down", "ggA_i_weight_hdamp_down", "ggA_t_weight_hdamp_down",
                                 "ggA_b_weight_scale_up", "ggA_i_weight_scale_up", "ggA_t_weight_scale_up",
                                 "ggA_b_weight_scale_down", "ggA_i_weight_scale_down", "ggA_t_weight_scale_down",
    ])
  ### Processors & consumers configuration
  config["Processors"] = []
  #if not (isEmbedded):           config["Processors"].append( "producer:ElectronCorrectionsProducer")
  config["Processors"].extend((                               "producer:HttValidLooseElectronsProducer",
                                                              "producer:HttValidLooseMuonsProducer",
                                                              "producer:HltProducer",
                                                              "producer:MetCollector"))
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
  config["Processors"].append(                                "filter:MinimalPlotlevelFilter")
  if btag_eff: config["ProcessorsBtagEff"] = copy.deepcopy(config["Processors"])
  config["Processors"].extend((                               "producer:DiJetQuantitiesProducer",
                                                              "producer:DiBJetQuantitiesProducer",
                                                              "producer:MetCorrector",
                                                              "producer:PuppiMetCorrector",
                                                              "producer:SimpleEleTauFakeRateWeightProducer",
                                                              "producer:SimpleMuTauFakeRateWeightProducer"))
  if isEmbedded:                 config["Processors"].append( "producer:EmbeddingMETCorrector")
  if isTTbar:                    config["Processors"].append( "producer:TopPtReweightingProducer")
  if isDY or isEmbedded:        config["Processors"].append( "producer:ZPtReweightProducer")
  config["Processors"].extend((                               "producer:TauTauRestFrameSelector",
                                                              "producer:DiLeptonQuantitiesProducer"
                                                              ))
  if isNMSSM:                    config["Processors"].append( "producer:NMSSMVariationProducer")
  if isEmbedded:                 config["Processors"].append( "producer:EmbeddedWeightProducer")
  if isEmbedded:                 config["Processors"].append( "producer:TauDecayModeWeightProducer")
  if isEmbedded:                 config["Processors"].append( "producer:EmbeddedZpTMassCorrectionsProducer")
  if not isData:                 config["Processors"].append( "producer:HighPtTauWeightProducer")
  if not isData:                 config["Processors"].append( "producer:TauTriggerEfficiencyProducer")
  if not isData:                 config["Processors"].append( "producer:TauTriggerSFProviderProducer")
  if not isData:                 config["Processors"].append( "producer:SingleTauTriggerEfficiencyProducer")
  if not isData:                 config["Processors"].append( "producer:TauIDScaleFactorProducer")
  config["Processors"].append(                                "producer:EventWeightProducer")
  if isGluonFusion:              config["Processors"].append( "producer:SMggHNNLOProducer")
  if isVBF:                      config["Processors"].append( "producer:SMvbfNNLOProducer")
  if isSUSYggH:                  config["Processors"].append( "producer:NLOreweightingWeightsProducer")
  config["Processors"].append(                                "producer:SvfitProducer")
  config["Consumers"] = ["KappaLambdaNtupleConsumer",
                         "cutflow_histogram"]
  # Subanalyses settings
  if btag_eff:
    config["Processors"] = copy.deepcopy(config["ProcessorsBtagEff"])
    if pipelines != ['nominal']:
        raise Exception("There is no use case for calculating btagging efficiency with systematics shifts: %s" % ' '.join(pipelines))

    return importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.btag_efficiency_subanalysis").build_config(nickname, nominal_config=config, channel='tt', **kwargs)


  # pipelines - systematic shifts
  needed_pipelines = ['nominal', 'tauESperDM_shifts', 'regionalJECunc_shifts', 'METunc_shifts', 'METrecoil_shifts', 'btagging_shifts']
  if isEmbedded:
      needed_pipelines.append('embMETScale_shifts')
  if pipelines is None:
      raise Exception("pipelines is None in %s" % (__file__))
  elif 'auto' in pipelines:
      pipelines = needed_pipelines

  return_conf = jsonTools.JsonDict()
  for pipeline in pipelines:
      if pipeline not in needed_pipelines:
          log.warning("Warning: pipeline NOT in the list of needed pipelines. Still adding it.")
      log.info('Add pipeline: %s' %(pipeline))
      return_conf += ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis." + pipeline).build_config(nickname, **kwargs))
  return return_conf

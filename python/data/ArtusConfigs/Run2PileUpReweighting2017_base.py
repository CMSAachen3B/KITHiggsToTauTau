
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import importlib
import os

def build_config(nickname, **kwargs):
  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  
  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("DY.?JetsToLLM(10to50|50|150)", nickname)
  isWjets = re.search("W.?JetsToLNu", nickname)
  isGluonFusion = re.search("GluGluHToTauTau.*M125", nickname)
  isSUSYggH = re.search("SUSYGluGluToHToTauTau", nickname)
  year = datasetsHelper.base_dict[nickname]["year"]
  
  
  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.settingsKappa"
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  config["SkipEvents"] = 0
  config["EventCount"] = -1
  config["InputIsData"] = False
  BosonPdgIds = {
      "DY.?JetsToLL|EWKZ2Jets|Embedding(2016|MC)" : [
        23
      ],
      "^(GluGlu|GluGluTo|VBF|Wminus|Wplus|Z)(HToTauTau|H2JetsToTauTau)" : [
        25
      ],
      "W.?JetsToLN|EWKW" : [
        24
      ],
      "SUSY(BB|GluGlu|GluGluTo)(BB)?HToTauTau" : [
        25,
        35,
        36
        ]
  }
  config["BosonPdgIds"] = [0]
  for key, pdgids in BosonPdgIds.items():
    if re.search(key, nickname): config["BosonPdgIds"] = pdgids
  
  config["BosonStatuses"] = [62]
  config["TopPtReweightingStrategy"] = "Run1"
  config["OutputPath"] = "output.root"
  if isSUSYggH:
    config["HiggsBosonMass"] = re.search("SUSYGluGluToHToTauTauM(\d+)_", nickname).groups()[0] #extracts generator mass from nickname
    if re.search("SUSYGluGluToHToTauTau.*powheg", nickname):
        if year == 2016:
            config["NLOweightsRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/NLOWeights/higgs_pt_2016_v2.root"
        else:
            config["NLOweightsRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/NLOWeights/higgs_pt_v2.root"
    else:
        config["NLOweightsRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/NLOWeights/higgs_pt_v2_mssm_mode.root" #TODO could be year-dependent?
  
  config["Processors"] = []
  config["Processors"].append(                                    "producer:NicknameProducer")
  config["Processors"].extend((                                   "producer:CrossSectionWeightProducer",
                                                                  "producer:GeneratorWeightProducer",
                                                                  "producer:NumberGeneratedEventsWeightProducer"))
  if isWjets or isDY or isSUSYggH:   config["Processors"].append( "producer:GenBosonFromGenParticlesProducer")
  if isDY or isEmbedded:             config["Processors"].append( "producer:GenDiLeptonDecayModeProducer")
  config["Processors"].extend((                                   "producer:GenParticleProducer",
                                                                  "producer:GenPartonCounterProducer"))
  if isWjets or isDY or isEmbedded:  config["Processors"].append("producer:GenBosonDiLeptonDecayModeProducer")
  if isTTbar:                    config["Processors"].append( "producer:TopPtReweightingProducer")
  if isGluonFusion:              config["Processors"].append( "producer:SMggHNNLOProducer")
  if isSUSYggH:                  config["Processors"].append( "producer:NLOreweightingWeightsProducer")
  config["ggHNNLOweightsRootfile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/NNLOWeights/NNLOPS_reweight.root" # same for all years?
  if "powheg" in nickname:
    config["Generator"] = "powheg"
  elif "amcatnlo" in nickname:
    config["Generator"] = "amcatnlo"

  # pipelines - channels including systematic shifts
  config["Pipelines"] = jsonTools.JsonDict()
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2PileUpReweighting2017.pu").build_config(nickname)

  return config

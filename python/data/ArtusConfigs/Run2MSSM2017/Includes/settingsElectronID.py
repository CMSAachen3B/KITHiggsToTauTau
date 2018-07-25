#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import copy
import Artus.Utility.jsonTools as jsonTools
#import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import importlib
#import os

def build_config(nickname):
  config = jsonTools.JsonDict()
  #datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  
  
  ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  config["ElectronID_documentation"] = "https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2015#Electrons"
  config["ElectronReco"] = "mvanontrig"
  config["ElectronID"] = "user"
  config["ElectronIDType"] = "cutbased2015andlater" # still MVA, using boolean functionality of IsCutBased()
  
  # signal electron ID
  config["ElectronIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp90" # better S/sqrt(B)
  #config["ElectronIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp90" # already has something like a iso cut ---> not good for side-band regions

  config["ElectronIDList"] = [
    "egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp80",
    "egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp90",
    "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp80",
    "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp90",
    "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-veto",
    "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-loose",
    "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-medium",
    "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-tight",
  ]
  
  config["ElectronIsoType"] = "user"
  config["ElectronIso"] = "none"
  config["ElectronIsoSignalConeSize"] = 0.3
  config["ElectronDeltaBetaCorrectionFactor"] = 0.5
  # reference eA values & bins from https://github.com/cms-sw/cmssw/blob/CMSSW_9_4_X/RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_92X.txt
  config["ElectronEtaBinnedEAValues"] = [0.1566, 0.1626, 0.1073, 0.0854, 0.1051, 0.1204, 0.1524]
  config["ElectronEtaBinsForEA"] = [0.0, 1.0, 1.479, 2.0, 2.2, 2.3, 2.4, 5.0]
  config["ElectronTrackDxyCut"] = 0.045
  config["ElectronTrackDzCut"] = 0.2

  return config

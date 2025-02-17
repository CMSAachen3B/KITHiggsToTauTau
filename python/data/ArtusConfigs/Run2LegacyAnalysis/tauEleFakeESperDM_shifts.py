#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import os

def build_config(nickname, **kwargs):

  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))


  # define frequently used conditions
  #isEmbedded = datasetsHelper.isEmbedded(nickname)
  #isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  #isTTbar = re.search("TT(To|_|Jets)", nickname)
  #isDY = re.search("DY.?JetsToLLM(50|150)", nickname)
  #isWjets = re.search("W.?JetsToLNu", nickname)
  year = datasetsHelper.base_dict[nickname]["year"]

  tauEleFakeES_uncertainties = {
    'inclusive_eta': {
      2016 : {
        "TauElectronFakeEnergyCorrectionOneProng" : {"down" : 0.992, "up" : 1.016},
        "TauElectronFakeEnergyCorrectionOneProngPiZeros" : {"down" : 1.015, "up" : 1.048},
      },
      2017: {
        "TauElectronFakeEnergyCorrectionOneProng" : {"down" : 0.993, "up" : 1.012},
        "TauElectronFakeEnergyCorrectionOneProngPiZeros" : {"down" : 1.006, "up" : 1.036},
      },
      2018: {
        "TauElectronFakeEnergyCorrectionOneProng" : {"down" : 1.008, "up" : 1.020},
        "TauElectronFakeEnergyCorrectionOneProngPiZeros" : {"down" : 0.999, "up" : 1.029},
      }
    },
    'split_eta': {
      2016 : {
        "TauElectronFakeEnergyCorrectionOneProngBarrel" : {"down" : 1.0 + (0.679 - 0.982) / 100, "up" : 1.0 + (0.679 + 0.806) / 100},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel" : {"down" : 1.0 + (3.389 - 2.475) / 100, "up" : 1.0 + (3.389 +1.168) / 100},
        "TauElectronFakeEnergyCorrectionOneProngEndcap" : {"down" : 1.0 + (-3.5 - 1.102) / 100, "up" : 1.0 + (-3.5 + 1.808) / 100},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap" : {"down" : 1.0 + (5.0 - 5.694) / 100, "up" : 1.0 + (5.0 +6.57) / 100},
      },
      2017: {
        "TauElectronFakeEnergyCorrectionOneProngBarrel" : {"down" : 1.0 + (0.911 - 0.882) / 100, "up" : 1.0 + (0.911 + 1.343) / 100},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel" : {"down" : 1.0 + (1.154 - 0.973) / 100, "up" : 1.0 + (1.154 + 2.162) / 100},
        "TauElectronFakeEnergyCorrectionOneProngEndcap" : {"down" : 1.0 + (-2.604 - 1.43) / 100, "up" : 1.0 + (-2.604 + 2.249) / 100},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap" : {"down" : 1.0 + (1.5 - 4.969) / 100, "up" : 1.0 + (1.5 + 6.461) / 100},
      },
      2018: {
        "TauElectronFakeEnergyCorrectionOneProngBarrel" : {"down" : 1.0 + (1.362 - 0.474) / 100, "up" : 1.0 + (1.362 + 0.904) / 100},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel" : {"down" : 1.0 + (1.945 - 1.598) / 100, "up" : 1.0 + (1.945 + 1.226) / 100},
        "TauElectronFakeEnergyCorrectionOneProngEndcap" : {"down" : 1.0 + (-3.097 - 1.25) / 100, "up" : 1.0 + (-3.097 + 3.404) / 100},
        "TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap" : {"down" : 1.0 + (-1.5 - 4.309) / 100, "up" : 1.0 + (-1.5 + 5.499) / 100},
      }
    },
  }

 ## fill config:
  # includes
  includes = [
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  log.info("Fake e->tau Energy Correction Uncertainties shifts split in eta")
  tauEleFakeES_uncertainties = tauEleFakeES_uncertainties['split_eta']
  common_shift = True
  # explicit configuration
  if re.search("DY.?JetsToLL|EWKZ", nickname):
    if common_shift:
      config["tauEleFakeEsOneProngCommonUp"] = {
        "JetEnergyCorrectionUncertaintyShift" : [0.0]
      }
      config["tauEleFakeEsOneProngCommonUp"]["TauElectronFakeEnergyCorrectionOneProngBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngBarrel"]["up"]
      config["tauEleFakeEsOneProngCommonUp"]["TauElectronFakeEnergyCorrectionOneProngEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngEndcap"]["up"]

      config["tauEleFakeEsOneProngCommonDown"] = {
        "JetEnergyCorrectionUncertaintyShift" : [0.0]
      }
      config["tauEleFakeEsOneProngCommonDown"]["TauElectronFakeEnergyCorrectionOneProngBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngBarrel"]["down"]
      config["tauEleFakeEsOneProngCommonDown"]["TauElectronFakeEnergyCorrectionOneProngEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngEndcap"]["down"]


      config["tauEleFakeEsOneProngPiZerosCommonUp"] = {
        "JetEnergyCorrectionUncertaintyShift" : [0.0]
      }
      config["tauEleFakeEsOneProngPiZerosCommonUp"]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"]["up"]
      config["tauEleFakeEsOneProngPiZerosCommonUp"]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"]["up"]

      config["tauEleFakeEsOneProngPiZerosCommonDown"] = {
        "JetEnergyCorrectionUncertaintyShift" : [0.0]
      }
      config["tauEleFakeEsOneProngPiZerosCommonDown"]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"]["down"]
      config["tauEleFakeEsOneProngPiZerosCommonDown"]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"]["down"]
    else:
      config["tauEleFakeEsOneProngBarrelUp"] = {
        "JetEnergyCorrectionUncertaintyShift" : [0.0]
      }
      config["tauEleFakeEsOneProngBarrelUp"]["TauElectronFakeEnergyCorrectionOneProngBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngBarrel"]["up"]

      config["tauEleFakeEsOneProngBarrelDown"] = {
        "JetEnergyCorrectionUncertaintyShift" : [0.0]
      }
      config["tauEleFakeEsOneProngBarrelDown"]["TauElectronFakeEnergyCorrectionOneProngBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngBarrel"]["down"]


      config["tauEleFakeEsOneProngPiZerosBarrelUp"] = {
        "JetEnergyCorrectionUncertaintyShift" : [0.0]
      }
      config["tauEleFakeEsOneProngPiZerosBarrelUp"]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"]["up"]

      config["tauEleFakeEsOneProngPiZerosBarrelDown"] = {
        "JetEnergyCorrectionUncertaintyShift" : [0.0]
      }
      config["tauEleFakeEsOneProngPiZerosBarrelDown"]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosBarrel"]["down"]

      config["tauEleFakeEsOneProngEndcapUp"] = {
        "JetEnergyCorrectionUncertaintyShift" : [0.0]
      }
      config["tauEleFakeEsOneProngEndcapUp"]["TauElectronFakeEnergyCorrectionOneProngEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngEndcap"]["up"]

      config["tauEleFakeEsOneProngEndcapDown"] = {
        "JetEnergyCorrectionUncertaintyShift" : [0.0]
      }
      config["tauEleFakeEsOneProngEndcapDown"]["TauElectronFakeEnergyCorrectionOneProngEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngEndcap"]["down"]


      config["tauEleFakeEsOneProngPiZerosEndcapUp"] = {
        "JetEnergyCorrectionUncertaintyShift" : [0.0]
      }
      config["tauEleFakeEsOneProngPiZerosEndcapUp"]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"]["up"]

      config["tauEleFakeEsOneProngPiZerosEndcapDown"] = {
        "JetEnergyCorrectionUncertaintyShift" : [0.0]
      }
      config["tauEleFakeEsOneProngPiZerosEndcapDown"]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZerosEndcap"]["down"]

  #log.info("Fake e->tau Energy Correction Uncertainties shifts inclusive in eta")
  #tauEleFakeES_uncertainties = tauEleFakeES_uncertainties['inclusive_eta']
  # explicit configuration
  #if re.search("DY.?JetsToLL|EWKZ", nickname):
  #  config["tauEleFakeEsOneProngUp"] = {
  #    "JetEnergyCorrectionUncertaintyShift" : [0.0]
  #  }
  #  config["tauEleFakeEsOneProngUp"]["TauElectronFakeEnergyCorrectionOneProng"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProng"]["up"]

  #  config["tauEleFakeEsOneProngDown"] = {
  #    "JetEnergyCorrectionUncertaintyShift" : [0.0]
  #  }
  #  config["tauEleFakeEsOneProngDown"]["TauElectronFakeEnergyCorrectionOneProng"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProng"]["down"]

  #  config["tauEleFakeEsOneProngPiZerosUp"] = {
  #    "JetEnergyCorrectionUncertaintyShift" : [0.0]
  #  }
  #  config["tauEleFakeEsOneProngPiZerosUp"]["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZeros"]["up"]

  #  config["tauEleFakeEsOneProngPiZerosDown"] = {
  #    "JetEnergyCorrectionUncertaintyShift" : [0.0]
  #  }
  #  config["tauEleFakeEsOneProngPiZerosDown"]["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = tauEleFakeES_uncertainties[year]["TauElectronFakeEnergyCorrectionOneProngPiZeros"]["down"]

  return config

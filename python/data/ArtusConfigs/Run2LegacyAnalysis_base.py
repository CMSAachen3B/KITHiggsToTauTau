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
  # extract the known additional parameters --analysis-channels
  analysis_channels = ['all'] if "analysis_channels" not in kwargs else kwargs["analysis_channels"]
  btag_eff = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "btag-eff" else False
  etau_fake_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "etau-fake-es" else False
  mtau_fake_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "mtau-fake-es" else False
  no_svfit = True if "no_svfit" in kwargs and kwargs["no_svfit"] else False
  addlheweights = True if "addlheweights" in kwargs and kwargs["addlheweights"] else False
  nmssm = True if ("nmssm" in kwargs and kwargs["nmssm"]) else False

  log.debug("%s \n %25s %-30r \n %30s %-25s" % ("    Run2LegacyAnalysis_base::", "btag_eff:", btag_eff, "analysis_channels: ", ' '.join(analysis_channels)))
  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("DY.?JetsToLLM(10to50|50)", nickname)
  isWjets = re.search("W.?JetsToLNu", nickname)
  isSUSYggH = re.search("SUSYGluGluToHToTauTau", nickname)
  isSignal = re.search("HToTauTau|NMSSM",nickname)
  isNMSSM = re.search("NMSSM",nickname)
  year = datasetsHelper.base_dict[nickname]["year"]

  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.settingsKappa",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.lheWeightAssignment",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.settingsSampleStitchingWeights"
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  config["SkipEvents"] = 0
  config["EventCount"] = -1
  config["Year"] = year
  config["InputIsData"] = isData

  if isSUSYggH:
    config["HiggsBosonMass"] = re.search("SUSYGluGluToHToTauTauM(\d+)_", nickname).groups()[0] #extracts generator mass from nickname
    if re.search("SUSYGluGluToHToTauTau.*powheg", nickname):
        if year == 2016:
            config["NLOweightsRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/NLOWeights/higgs_pt_2016_v2.root"
        else:
            config["NLOweightsRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/NLOWeights/higgs_pt_v2.root"
        config["NLOweightsWriteUncertainties"] = True
    else:
        config["NLOweightsRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/NLOWeights/higgs_pt_v2_mssm_mode.root" #TODO could be year-dependent?

  if re.search("GluGluHToTauTauM95", nickname):
      config["HiggsBosonMass"] = re.search("GluGluHToTauTauM(\d+)_", nickname).groups()[0] #extracts generator mass from nickname
      if year == 2016:
          config["NLOweightsRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/NLOWeights/higgs_pt_2016_v2.root"
      else:
          config["NLOweightsRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/NLOWeights/higgs_pt_v2.root"
      config["NLOweightsWriteUncertainties"] = True


  BosonPdgIds = {
      "DY.?JetsToLL|EWKZ2Jets|Embedding" : [
        23
      ],
      "^(GluGlu|GluGluTo|VBF|Wminus|Wplus|Z|ggZH)(HToTauTau|H2JetsToTauTau|HToWW)" : [
        25
      ],
      "NMSSM" : [
	35, 45
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
  if isNMSSM:
    config["MatchNMSSMBosons"] = True
  for key, pdgids in BosonPdgIds.items():
    if re.search(key, nickname): config["BosonPdgIds"] = pdgids
  config["BosonStatuses"] = [62]
  if isNMSSM:
    config["BosonStatuses"].append(22)
  config["UseUWGenMatching"] = True

  # MET filters (JetMMET)
  config["MetFilterToFlag"] = [  # suggested for MC and Data
        "Flag_goodVertices",
        "Flag_globalSuperTightHalo2016Filter",
        "Flag_HBHENoiseFilter",
        "Flag_HBHENoiseIsoFilter",
        "Flag_EcalDeadCellTriggerPrimitiveFilter",
        "Flag_BadPFMuonFilter",
        # "Flag_BadChargedCandidateFilter",   # not recommended, under review
  ]
  if year == 2016 and isEmbedded:
    config["MetFilterToFlag"].remove("Flag_BadPFMuonFilter") # as the 2016 embedded samples dont have this filter
  if isData or isEmbedded:
    config["MetFilterToFlag"].extend((
        "Flag_eeBadScFilter",
    ))
  if year in [2017, 2018]:
    config["MetFilterToFlag"].extend((
        "ecalBadCalibReducedMINIAODFilter",
    ))

  config["OutputPath"] = "output.root"

  config["Processors"] = []
  #config["Processors"].append("filter:RunLumiEventFilter")
  if isData or isEmbedded:             config["Processors"].append( "filter:JsonFilter")
  #if isDY or isTTbar:                  config["Processors"].append( "producer:ScaleVariationProducer")
  config["Processors"].append(                                      "producer:NicknameProducer")
  config["Processors"].append(                                      "producer:MetFilterFlagProducer")
  if not isData:

    if not isEmbedded:
      config["Processors"].append( "producer:PUWeightProducer")
      config["Processors"].extend((                                   "producer:CrossSectionWeightProducer",
                                                                    "producer:NumberGeneratedEventsWeightProducer"))
    if isWjets or isDY or isSignal:    config["Processors"].append( "producer:GenBosonFromGenParticlesProducer")
    if isDY or isEmbedded:             config["Processors"].append( "producer:GenDiLeptonDecayModeProducer")
    config["Processors"].extend((                                   "producer:GenParticleProducer",
                                                                    "producer:GenPartonCounterProducer"))
    if isSUSYggH or re.search("GluGluHToTauTauM95", nickname):
        config["Processors"].append(                                "producer:NLOreweightingWeightsProducer")
    if isWjets or isDY or isEmbedded:  config["Processors"].extend(("producer:GenTauDecayProducer",
                                                                    "producer:GenBosonDiLeptonDecayModeProducer"))
    config["Processors"].append(                                    "producer:GeneratorWeightProducer")
    #if isTTbar:                        config["Processors"].append( "producer:TTbarGenDecayModeProducer")

  if isData or isEmbedded:                config["PileupWeightFile"] = "not needed"
  elif year == 2016: config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2016_271036-284044_13TeVMoriond17_23Sep2016ReReco_69p2mbMinBiasXS.root"
  elif year == 2017: config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927-306462_13TeVFall17_31Mar2018ReReco_69p2mbMinBiasXS/%s.root"%nickname
  elif year == 2018: config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2018_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18.root"
  else:
    print "PileupWeightFile not defined"
    exit(1)
  if year == 2017 and isNMSSM:
    config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927-306462_13TeVFall17_31Mar2018ReReco_69p2mbMinBiasXS/VBFHToTauTauM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8_v1.root"

  if year == 2016:   config["ZptRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2016.root"
  elif year == 2017: config["ZptRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2017.root"
  elif year == 2018: config["ZptRooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2018.root"
  config["DoZptUncertainties"] = True

  if year == 2016:   config["MetRecoilCorrectorFile"] = "HTT-utilities/RecoilCorrections/data/Type1_PFMET_2016.root"
  elif year == 2017: config["MetRecoilCorrectorFile"] = "HTT-utilities/RecoilCorrections/data/Type1_PFMET_2017.root"
  elif year == 2018: config["MetRecoilCorrectorFile"] = "HTT-utilities/RecoilCorrections/data/Type1_PFMET_2018.root"
  if year == 2016:   config["MetShiftCorrectorFile"] = "HTT-utilities/RecoilCorrections/data/PFMETSys_2016.root"
  elif year == 2017: config["MetShiftCorrectorFile"] = "HTT-utilities/RecoilCorrections/data/PFMETSys_2017.root"
  elif year == 2018: config["MetShiftCorrectorFile"] = "HTT-utilities/RecoilCorrections/data/PFMETSys_2018.root"

  if year == 2016:   config["PuppiMetRecoilCorrectorFile"] = "HTT-utilities/RecoilCorrections/data/Type1_PuppiMET_2016.root"
  elif year == 2017: config["PuppiMetRecoilCorrectorFile"] = "HTT-utilities/RecoilCorrections/data/Type1_PuppiMET_2017.root"
  elif year == 2018: config["PuppiMetRecoilCorrectorFile"] = "HTT-utilities/RecoilCorrections/data/Type1_PuppiMET_2018.root"
  if year == 2016:   config["PuppiMetShiftCorrectorFile"] = "HTT-utilities/RecoilCorrections/data/PuppiMETSys_2016.root"
  elif year == 2017: config["PuppiMetShiftCorrectorFile"] = "HTT-utilities/RecoilCorrections/data/PuppiMETSys_2017.root"
  elif year == 2018: config["PuppiMetShiftCorrectorFile"] = "HTT-utilities/RecoilCorrections/data/PuppiMETSys_2018.root"

  config["MetCorrectionMethod"] = "none" if (isData  or isEmbedded) else "quantileMappingHist"
  #config["MetCorrectionMethod"] = "none" if (isData  or isEmbedded) else "meanResolution"
  config["UpdateMetWithCorrectedLeptons"] = True
  if nmssm: config["UpdateMetWithBJetRegression"] = True
  config["UpdateMetWithCorrectedLeptonsFromSignalOnly"] = True
  config["ChooseMvaMet"] = False

  if isData or isEmbedded:
    if   year == 2016:      config["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt"]
    elif year == 2017:      config["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt"]
    elif year == 2018:      config["JsonFiles"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/json/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt"]
    else:
      print "Luminosity GOLDEN JSON not defined"
      exit(1)

  if year == 2016:
    config["SimpleMuTauFakeRateWeightLoose"] = [1.25, 0.96, 1.29, 0.92, 5.01]
    config["SimpleMuTauFakeRateWeightTight"] = [1.38, 0.72, 1.34, 1.03, 5.05]
    config["SimpleEleTauFakeRateWeightVLoose"] = [1.38, 1.29]
    config["SimpleEleTauFakeRateWeightTight"] = [1.22, 1.47]
  elif year == 2017:
    config["SimpleMuTauFakeRateWeightLoose"] = [1.12, 0.76, 0.99, 0.75, 4.44]
    config["SimpleMuTauFakeRateWeightTight"] = [0.92, 0.79, 0.67, 1.07, 4.08]
    config["SimpleEleTauFakeRateWeightVLoose"] = [1.11, 1.03]
    config["SimpleEleTauFakeRateWeightTight"] = [1.22, 0.93]
  elif year == 2018:
    config["SimpleMuTauFakeRateWeightLoose"] = [1.00, 1.08, 1.04, 0.95, 5.58]
    config["SimpleMuTauFakeRateWeightTight"] = [0.81, 1.02, 0.92, 0.83, 4.52]
    config["SimpleEleTauFakeRateWeightVLoose"] = [0.91, 0.91]
    config["SimpleEleTauFakeRateWeightTight"] = [1.47, 0.66]

  if re.search("(GluGluHToTauTau|ggZHHToTauTauZToQQ).*M125", nickname):
    config["ggHNNLOweightsRootfile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/NNLOWeights/NNLOPS_reweight.root" # same for all years?
    if "powheg" in nickname:
      config["Generator"] = "powheg"
    elif "amcatnlo" in nickname:
      config["Generator"] = "amcatnlo"


  if isData or isEmbedded:
    if re.search("(DoubleEG|ElectronEmbedding)", nickname):
      allowed_channels = ["ee"]
    elif re.search("(MuonEG|ElMuFinalState)", nickname):
      allowed_channels = ["em"]
    elif re.search("(SingleElectron|EGamma)", nickname):
      allowed_channels = ["ee", "et", "em"]
    elif re.search("ElTauFinalState", nickname):
      allowed_channels = ["ee", "et"]
    elif re.search("(DoubleMuon|MuonEmbedding)", nickname):
      allowed_channels = ["mm"]
    elif re.search("SingleMuon", nickname):
      allowed_channels = ["mm", "mt", "em"]
    elif re.search("MuTauFinalState", nickname):
      allowed_channels = ["mm", "mt"]
    elif re.search("^Tau", nickname):
      allowed_channels = ["et", "mt", "tt"]
    elif re.search("TauTauFinalState", nickname):
      allowed_channels = ["tt"]
    else:
      print "Unknown format of nickname %s for type data or embedded!"
      raise Exception
    if "all" in analysis_channels:
      analysis_channels = allowed_channels
    else:
      analysis_channels=list(set(analysis_channels).intersection(set(allowed_channels)))

  # pipelines - channels including systematic shifts
  config["Pipelines"] = jsonTools.JsonDict()
  if "ee" in analysis_channels: config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.%s.ee"%str(year)).build_config(nickname, **kwargs)
  if "all" in analysis_channels or "em" in analysis_channels: config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.%s.em"%str(year)).build_config(nickname, **kwargs)
  if "all" in analysis_channels or "et" in analysis_channels: config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.%s.et"%str(year)).build_config(nickname, **kwargs)
  if "mm" in analysis_channels: config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.%s.mm"%str(year)).build_config(nickname, **kwargs)
  if "all" in analysis_channels or "mt" in analysis_channels: config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.%s.mt"%str(year)).build_config(nickname, **kwargs)
  if "all" in analysis_channels or "tt" in analysis_channels: config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.%s.tt"%str(year)).build_config(nickname, **kwargs)

  if etau_fake_es or mtau_fake_es:
    isEWKZ2Jets = re.search("EWKZ2Jets", nickname)
    for pipeline_name, pipeline_config in config["Pipelines"].iteritems():
      # Lower the tau pt cut to 20 to be able to perform the FES variation on the plotting step instead of artus.
      # Meaning: the higher cut should be re-applied later on.
      if isDY or isEWKZ2Jets:
        if (pipeline_name.startswith('mt_') or pipeline_name.startswith('et_')) and (pipeline_name.endswith("Shift_0") or pipeline_name.endswith("_nominal")):
          pipeline_config["TauLowerPtCuts"] = ["20.0"]
          pipeline_config["Quantities"].extend(["leadingTauLV"])

      # Ensuring the MinimalPlotLevel filter can be restored during the plotting
      if pipeline_name.startswith('mt_'):
        pipeline_config["Quantities"].extend(["nDiMuonVetoPairsOS", "extraelec_veto", "extramuon_veto"])
      if pipeline_name.startswith('et_'):
        pipeline_config["Quantities"].extend(["nDiElectronVetoPairsOS", "extraelec_veto", "extramuon_veto"])

      pipeline_config["Quantities"] = list(set(pipeline_config["Quantities"]))

    # delete pipelines with shifts&ele smearing if it is not in mother config
    if isDY or isEWKZ2Jets:
      for k in config["Pipelines"].keys():
        if k.startswith('et_') \
           and any([e in k for e in ['eleScaleUp', 'eleScaleDown', 'eleSmearUp', 'eleSmearDown']]) \
           and 'ElectronScaleAndSmearUsed' in config["Pipelines"][k] \
           and not config["Pipelines"][k]["ElectronScaleAndSmearUsed"]:
          config["Pipelines"].pop(k, None)

  if btag_eff or no_svfit or etau_fake_es or mtau_fake_es:  # disable SVFit
    for pipeline_config in config["Pipelines"].values():
      pipeline_config["Quantities"] = list(set(pipeline_config["Quantities"]) - set(["m_sv", "pt_sv", "eta_sv", "phi_sv"]))
      while "producer:SvfitProducer" in pipeline_config["Processors"]:
        pipeline_config["Processors"].remove("producer:SvfitProducer")

  if btag_eff or etau_fake_es or mtau_fake_es:  # disable GeneratorWeightProducer for sub-analyses
    config["Processors"].remove("producer:GeneratorWeightProducer")
  if addlheweights:
    for pipeline_name, pipeline_config in config["Pipelines"].iteritems():
      if 'nominal' in pipeline_name:  # no need to store lhe for shifts
        pipeline_config["Quantities"] = list(set(pipeline_config["Quantities"]) + set(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.lheWeights").build_list()))

  return config

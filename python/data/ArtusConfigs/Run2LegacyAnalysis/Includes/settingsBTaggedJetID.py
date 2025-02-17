#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import os
import six


def build_config(nickname, **kwargs):
    btager = kwargs["btager"]
    btager_wp = kwargs["btager_wp"]
    if not isinstance(btager_wp, six.string_types):
        btager_wp = "medium"

    config = jsonTools.JsonDict()
    datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
    year = datasetsHelper.base_dict[nickname]["year"]
    isEmbedded = datasetsHelper.isEmbedded(nickname)
    # explicit configuration
    config["BTaggedJetID_documentation"] = [
        "https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation"
    ]

    btaggersf_file_type = 'wponly'
    btaggers_collection = {
        "DeepCSV": {
            2016: {
                "BTagScaleFactorFile": {
                    'raw': "$CMSSW_BASE/src/Artus/KappaAnalysis/data/DeepCSV_2016LegacySF_V1.csv",
                    'wponly': "$CMSSW_BASE/src/Artus/KappaAnalysis/data/DeepCSV_2016LegacySF_WP_V1.csv",
                },
                # TODO measure efficiencies for year 2016
                "BTagEfficiencyFile": {
                    "tight": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepCSV_2016_tight_all_proc_DeepCSV_tight_inclusive_inclusive.root",
                    "medium": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepCSV_2016_medium_all_proc_DeepCSV_medium_inclusive_inclusive.root",
                    "loose": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepCSV_2016_loose_all_proc_DeepCSV_loose_inclusive_inclusive.root",
                },
                "BTaggerWorkingPoints": [
                    "tight:0.8953",
                    "medium:0.6321",
                    "loose:0.2217"
                ],
                "BTaggedJetCombinedSecondaryVertexName": "pfDeepCSVJetTagsprobbb+pfDeepCSVJetTagsprobb",
            },
            2017: {
                "BTagScaleFactorFile": {
                    'raw': "$CMSSW_BASE/src/Artus/KappaAnalysis/data/DeepCSV_94XSF_V4_B_F.csv",
                    'wponly': "$CMSSW_BASE/src/Artus/KappaAnalysis/data/DeepCSV_94XSF_WP_V4_B_F.csv",
                },
                "BTagEfficiencyFile": {
                    "tight": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepCSV_2017_tight_all_proc_DeepCSV_tight_inclusive_inclusive.root",
                    "medium": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepCSV_2017_medium_all_proc_DeepCSV_medium_inclusive_inclusive.root",
                    "loose": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/data/Eff_DeepCSV_2017_loose_all_proc_DeepCSV_loose_inclusive_inclusive.root",
                },
                "BTaggerWorkingPoints": [
                    "tight:0.8001",
                    "medium:0.4941",
                    "loose:0.1522"
                ],
                "BTaggedJetCombinedSecondaryVertexName": "pfDeepCSVJetTagsprobbb+pfDeepCSVJetTagsprobb",
            },
            2018: {
                "BTagScaleFactorFile": {
                    'raw': "$CMSSW_BASE/src/Artus/KappaAnalysis/data/DeepCSV_102XSF_V1.csv",
                    'wponly': "$CMSSW_BASE/src/Artus/KappaAnalysis/data/DeepCSV_102XSF_WP_V1.csv",
                },
                #TODO measure efficiencies for year 2018
                "BTagEfficiencyFile": {
                    "tight": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepCSV_2018_tight_all_proc_DeepCSV_tight_inclusive_inclusive.root",
                    "medium": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepCSV_2018_medium_all_proc_DeepCSV_medium_inclusive_inclusive.root",
                    "loose": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepCSV_2018_loose_all_proc_DeepCSV_loose_inclusive_inclusive.root",
                },
                "BTaggerWorkingPoints": [
                    "tight:0.7527",
                    "medium:0.4184",
                    "loose:0.1241"
                ],
                "BTaggedJetCombinedSecondaryVertexName": "pfDeepCSVJetTagsprobbb+pfDeepCSVJetTagsprobb",
            },
        },
        "DeepFlavour": {
            2016: {
                "BTagScaleFactorFile": {
                    'raw': "$CMSSW_BASE/src/Artus/KappaAnalysis/data/DeepJet_2016LegacySF_V1.csv",
                    'wponly': "$CMSSW_BASE/src/Artus/KappaAnalysis/data/DeepJet_2016LegacySF_WP_V1.csv",
                },
                "BTagEfficiencyFile": {
                    "tight": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepFlavour_2016_tight_all_proc_DeepFlavour_tight_inclusive_inclusive.root",
                    "medium": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepFlavour_2016_medium_all_proc_DeepFlavour_medium_inclusive_inclusive.root",
                    "loose": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepFlavour_2016_loose_all_proc_DeepFlavour_loose_inclusive_inclusive.root",
                },
                "BTaggerWorkingPoints": [
                    "tight:0.7221",
                    "medium:0.3093",
                    "loose:0.0614"
                ],
                "BTaggedJetCombinedSecondaryVertexName": "pfDeepFlavourJetTagsprobb+pfDeepFlavourJetTagsprobbb+pfDeepFlavourJetTagsproblepb",
            },
            2017: {
                "BTagScaleFactorFile": {
                    'raw': "$CMSSW_BASE/src/Artus/KappaAnalysis/data/DeepFlavour_94XSF_V2_B_F.csv",
                    'wponly': "$CMSSW_BASE/src/Artus/KappaAnalysis/data/DeepFlavour_94XSF_WP_V3_B_F.csv",
                },
                "BTagEfficiencyFile": {
                    "tight": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepFlavour_2017_loose_all_proc_DeepFlavour_loose_inclusive_inclusive.root",
                    "medium": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepFlavour_2017_medium_all_proc_DeepFlavour_medium_inclusive_inclusive.root",
                    "loose": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepFlavour_2017_tight_all_proc_DeepFlavour_tight_inclusive_inclusive.root",
                },
                "BTaggerWorkingPoints": [
                    "tight:0.7489",
                    "medium:0.3033",
                    "loose:0.0521"
                ],
                "BTaggedJetCombinedSecondaryVertexName": "pfDeepFlavourJetTagsprobb+pfDeepFlavourJetTagsprobbb+pfDeepFlavourJetTagsproblepb",
            },
            2018:
            {
                "BTagScaleFactorFile": {
                    'raw': "$CMSSW_BASE/src/Artus/KappaAnalysis/data/DeepJet_102XSF_V1.csv",
                    'wponly': "$CMSSW_BASE/src/Artus/KappaAnalysis/data/DeepJet_102XSF_WP_V1.csv",
                },
                "BTagEfficiencyFile": {
                    "tight": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepFlavour_2018_loose_all_proc_DeepFlavour_loose_inclusive_inclusive.root",
                    "medium": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepFlavour_2018_medium_all_proc_DeepFlavour_medium_inclusive_inclusive.root",
                    "loose": "$CMSSW_BASE/src/Artus/KappaAnalysis/data/Eff_DeepFlavour_2018_tight_all_proc_DeepFlavour_tight_inclusive_inclusive.root",
                },
                "BTaggerWorkingPoints": [
                    "tight:0.7264",
                    "medium:0.2770",
                    "loose:0.0494"
                ],
                "BTaggedJetCombinedSecondaryVertexName": "pfDeepFlavourJetTagsprobb+pfDeepFlavourJetTagsprobbb+pfDeepFlavourJetTagsproblepb",
            },
        },
    }

    btag = btaggers_collection[btager][year]
    config["BTagWPs"] = [btager_wp]

    config["BTagScaleFactorFile"] = btag["BTagScaleFactorFile"][btaggersf_file_type]
    config["BTagEfficiencyFile"] = btag["BTagEfficiencyFile"][config["BTagWPs"][0]]
    config["BTaggedJetCombinedSecondaryVertexName"] = btag["BTaggedJetCombinedSecondaryVertexName"]
    config["BTaggerWorkingPoints"] = btag["BTaggerWorkingPoints"]

    if year == 2016:            config["BTaggedJetAbsEtaCut"] = 2.4  # 2016 value
    elif year in [2017, 2018]:  config["BTaggedJetAbsEtaCut"] = 2.5  # 2017,2018 value
    config["ApplyBTagSF"] = not isEmbedded
    config["JetTaggerUpperCuts"] = []
    config["BTagSFMethod"] = "PromotionDemotion"
    config["BTagShift"] = 0
    config["BMistagShift"] = 0

    config["ValidTaggedJetsProducerDebug"] = False
    # Further settings taken into account by ValidBTaggedJetsProducer:
    # - Year, written into the 'base' config

    # Further hard-coded settings in the ValidBTaggedJetsProducer:
    # lower pt_cut for the Jet: 20 GeV -> valid for all years
    # upper pt_cut for the Jet: 1000 GeV -> valid for all years
    # parton flavour definition: hadron-based
    # b- and c- jets: combined measurement type, light jets: inclusive measurement type

    return config

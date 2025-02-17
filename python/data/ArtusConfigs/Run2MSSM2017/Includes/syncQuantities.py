#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import importlib
#import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz


def build_list(**kwargs):
    minimal_setup = True if "minimal_setup" in kwargs and kwargs["minimal_setup"] else False

    # quantities that are needed to run the analysis
    quantities = [
        # channels definitions + triggers selection
        "dilepton_veto",
        "eta_1",
        "eta_2",
        "extraelec_veto",
        "extramuon_veto",
        "flagMETFilter",
        "gen_match_1",
        "gen_match_2",
        "genbosonmass",
        "isEmbedded",
        "iso_1",
        "iso_2",
        "jdeta",
        "jeta_1",
        "jeta_2",
        "jphi_1",
        "jphi_2",
        "jpt_1",
        "jpt_2",
        "mjj",
        "mt_1",
        "nbtag",
        "njets",
        "npartons",
        "pZetaMissVis",
        "phi_1",
        "phi_2",
        "pt_1",
        "pt_2",
        "pt_tt",
        "ptvis",
        "q_1",
        "q_2",
    ]

    quantities.extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.weightQuantities").build_list(minimal_setup=minimal_setup))
    quantities.extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.idQuantities").build_list(minimal_setup=minimal_setup))
    quantities.extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.trgQuantities").build_list(minimal_setup=minimal_setup))

    if not minimal_setup:
        quantities.extend([
            # "Flag_HBHENoiseFilter",
            # "Flag_HBHENoiseIsoFilter",
            # "Flag_EcalDeadCellTriggerPrimitiveFilter",
            # "Flag_goodVertices",
            # "Flag_BadPFMuonFilter",
            # "Flag_BadChargedCandidateFilter",
            # "Flag_eeBadScFilter",
            # "Flag_ecalBadCalibFilter",
            # "Flag_globalTightHalo2016Filter",
            "NUP",
            "bcsv_1",
            "bcsv_2",
            "beta_1",
            "beta_2",
            "bmva_1",
            "bmva_2",
            "bpfid_1",
            "bpfid_2",
            "bphi_1",
            "bphi_2",
            "bpt_1",
            "bpt_2",
            "bpuid_1",
            "bpuid_2",
            "brawf_1",
            "brawf_2",
            "chargedIsoPtSum_1",
            "chargedIsoPtSum_2",
            "d0_1",
            "d0_2",
            "dZ_1",
            "dZ_2",
            "decayDistM_1",
            "decayDistM_2",
            "decayDistX_1",
            "decayDistX_2",
            "decayDistY_1",
            "decayDistY_2",
            "decayDistZ_1",
            "decayDistZ_2",
            "decayModeFindingNewDMs_1",
            "decayModeFindingNewDMs_2",
            "decayModeFinding_1",
            "decayModeFinding_2",
            "decayMode_1",
            "decayMode_2",
            "diLepGenMass",
            "diLepMass",
            "diLepMassSmearDown",
            "diLepMassSmearUp",
            "dijetphi",
            "dijetpt",
            "eRatio_1",
            "eRatio_2",
            "e_1",
            "e_2",
            "ecalTrkEnergyPostCorr_1",
            "ecalTrkEnergyPostCorr_2",
            "eta_sv",
            "event",
            "evt",
            "footprintCorrection_1",
            "footprintCorrection_2",
            "genbosoneta",
            "genbosonphi",
            "genbosonpt",
            "hdijetphi",
            "input",
            "isDoubleEG",
            "isDoubleMuon",
            "isFake",
            "isMC",
            "isMuonEG",
            "isSingleElectron",
            "isSingleMuon",
            "isTau",
            "jcsv_1",
            "jcsv_2",
            "jcsv_3",
            "jcsv_4",
            "jdphi",
            "jm_1",
            "jm_2",
            "jmva_1",
            "jmva_2",
            "jpfid_1",
            "jpfid_2",
            "jpuid_1",
            "jpuid_2",
            "jrawf_1",
            "jrawf_2",
            "leadingTrackChi2_1",
            "leadingTrackChi2_2",
            "lumi",
            "m_1",
            "m_2",
            "m_sv",
            "m_vis",
            "met",
            "metcov00",
            "metcov01",
            "metcov10",
            "metcov11",
            "metphi",
            "mt_2",
            "mt_tot",
            "mt_tt",
            "mvacov00",
            "mvacov01",
            "mvacov10",
            "mvacov11",
            "mvamet",
            "mvametphi",
            "nPhoton_1",
            "nPhoton_2",
            "neutralIsoPtSum_1",
            "neutralIsoPtSum_2",
            "nickname",
            "njetingap",
            "njetingap20",
            "njetspt20",
            "njetspt20eta2p4",
            "njetspt30",
            "npu",
            "npv",
            "phi_sv",
            "photonPtSumOutsideSignalCone_1",
            "photonPtSumOutsideSignalCone_2",
            "ptWeightedDetaStrip_1",
            "ptWeightedDetaStrip_2",
            "ptWeightedDphiStrip_1",
            "ptWeightedDphiStrip_2",
            "ptWeightedDrIsolation_1",
            "ptWeightedDrIsolation_2",
            "ptWeightedDrSignal_1",
            "ptWeightedDrSignal_2",
            "pt_sv",
            "puCorrPtSum_1",
            "puCorrPtSum_2",
            "pzetamiss",
            "pzetavis",
            "rho",
            "run",
            "visjeteta",
        ])

    return list(set(quantities))

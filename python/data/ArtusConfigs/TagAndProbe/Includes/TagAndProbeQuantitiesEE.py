#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

def build_list(year):
  if year==2016:
      trigger_flags = ["trg_t_Ele25eta2p1WPTight", "trg_p_Ele25eta2p1WPTight"]
  else:
      trigger_flags = [
          "trg_t_Ele27",
          "trg_p_Ele27",
          "trg_t_Ele32",
          "trg_p_Ele32",
          "trg_t_Ele35",
          "trg_p_Ele35",
          "trg_t_Ele32_fb",
          "trg_p_Ele32_fb"
          ]    
  quantities_list = trigger_flags + [
    "run",
    "lumi",
    "evt",
    "pt_t", "pt_p",
    "eta_t", "eta_p", "sc_eta_p",
    "phi_t", "phi_p",
    "iso_t", "iso_p",
    "m_ll",
    # "sigmaIetaIeta_p",
	# "sigmaIetaIeta_t",
	# "hadronicOverEm_p",
	# "hadronicOverEm_t",
	# "fbrem_p",
	# "fbrem_t",
	# "r9_p",
	# "r9_t",
	# "circularity_p",
	# "circularity_t",
	# "hoe_p",
	# "hoe_t",
	# "kfhits_p",
	# "kfhits_t",
	# "kfchi2_p",
	# "kfchi2_t",
	# "gsfchi2_p",
	# "gsfchi2_t",
	# "gsfhits_p",
	# "gsfhits_t",
	# "expectedMissingInnerHits_p",
	# "expectedMissingInnerHits_t",
	# "eop_p",
	# "eop_t",
	# "eleeopout_p",
	# "eleeopout_t",
	# "oneOverEminusOneOverP_p",
	# "oneOverEminusOneOverP_t",
	# "deta_p",
	# "deta_t",
	# "dphi_p",
	# "dphi_t",
	# "detacalo_p",
	# "detacalo_t",
	# "preShowerOverRaw_p",
	# "preShowerOverRaw_t",
	# "convVtxFitProbability_t",
	# "convVtxFitProbability_p",
    # "rho_t",
	# "rho_p",
	# "dEtaInSeed_p",
	# "dEtaInSeed_t",
	# "scetaseed_t",
	# "scetaseed_p",
	# "id_old_t", 
	# "id_old_p",
    "id_90_t",
	"id_90_p",
    "id_80_t",
	"id_80_p",
	"id_cutbased_t",
	"id_cutbased_p",
	"id_cutbased_sanity_t",
	"id_cutbased_sanity_p",
	"id_cutbased_t_step_0",
	"id_cutbased_t_step_1",
	"id_cutbased_t_step_2",
	"id_cutbased_t_step_3",
	"id_cutbased_t_step_4",
	"id_cutbased_t_step_5",
	"id_cutbased_t_step_6",
	"id_cutbased_t_step_7",
	"id_cutbased_p_step_0",
	"id_cutbased_p_step_1",
	"id_cutbased_p_step_2",
	"id_cutbased_p_step_3",
	"id_cutbased_p_step_4",
	"id_cutbased_p_step_5",
	"id_cutbased_p_step_6",
	"id_cutbased_p_step_7",
    ]

  return quantities_list

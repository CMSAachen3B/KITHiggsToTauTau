
#pragma once

#include <map>
#include <string>

#include "Artus/KappaAnalysis/interface/KappaProduct.h"

#include "Artus/Utility/interface/DefaultValues.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/DiTauPair.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/DiGenTauPair.h"
#include "TVector2.h"
#include "TVector3.h"

class HttProduct : public KappaProduct
{
public:

	/// added by HttValidLooseElectronsProducer
	std::vector<KElectron*> m_validLooseElectrons;
	std::vector<KElectron*> m_invalidLooseElectrons;

	/// added by HttValidVetoElectronsProducer
	std::vector<KElectron*> m_validVetoElectrons;
	std::vector<KElectron*> m_invalidVetoElectrons;

	/// added by HttValidLooseMuonsProducer
	std::vector<KMuon*> m_validLooseMuons;
	std::vector<KMuon*> m_invalidLooseMuons;

	/// added by HttValidVetoMuonsProducer
	std::vector<KMuon*> m_validVetoMuons;
	std::vector<KMuon*> m_invalidVetoMuons;

	/// added by DiTauPairCandidatesProducers
	std::vector<DiTauPair> m_validDiTauPairCandidates;
	std::vector<DiTauPair> m_invalidDiTauPairCandidates;

	/// added by GenDiTauPairCandidatesProducers and GenDiTauPairAcceptanceProducer
	std::vector<DiGenTauPair> m_genDiTauPairCandidates;
	std::vector<DiGenTauPair> m_genDiTauPairInAcceptance;

	// filled by DecayChannelProducer
	bool m_extraElecVeto = false;
	bool m_extraMuonVeto = false;

	// filled by DiLeptonVetoProducers
	int m_nDiElectronVetoPairsOS = 0;
	int m_nDiElectronVetoPairsSS = 0;
	int m_nDiMuonVetoPairsOS = 0;
	int m_nDiMuonVetoPairsSS = 0;

	// filled by TTHTauPairProducer
	std::vector<KTau*> m_validTTHTaus;

	// filled by DecayChannelProducer
	HttEnumTypes::DecayChannel m_decayChannel;

	// TODO: To be set by producers that apply shifts
	HttEnumTypes::SystematicShift m_systematicShift = HttEnumTypes::SystematicShift::CENTRAL;
	float m_systematicShiftSigma = 0.0;

	// filled by DecayChannelProducer
	std::vector<KLepton*> m_ptOrderedLeptons; // highest pt leptons first
	std::vector<KLepton*> m_flavourOrderedLeptons; // according to channel definition
	std::vector<KLepton*> m_chargeOrderedLeptons; // positively charged leptons first

	std::vector<KGenParticle*> m_ptOrderedGenLeptons; // same ordering as reco collection
	std::vector<KGenParticle*> m_flavourOrderedGenLeptons; // same ordering as reco collection
	std::vector<KGenParticle*> m_chargeOrderedGenLeptons; // same ordering as reco collection

	std::vector<RMFLV*> m_ptOrderedGenLeptonVisibleLVs; // same ordering as reco collection
	std::vector<RMFLV*> m_flavourOrderedGenLeptonVisibleLVs; // same ordering as reco collection
	std::vector<RMFLV*> m_chargeOrderedGenLeptonVisibleLVs; // same ordering as reco collection

	// filled by HttTauEnergyCorrectionProducer
	std::map<KTau*, double> m_tauEnergyScaleWeight;

	// filled by HttValid<Leptons>Producer
	std::map<KLepton*, double> m_leptonIsolation;
	std::map<KLepton*, double> m_leptonIsolationOverPt;
	std::map<KElectron*, double> m_electronIsolation;
	std::map<KElectron*, double> m_electronIsolationOverPt;
	std::map<KMuon*, double> m_muonIsolation;
	std::map<KMuon*, double> m_muonIsolationOverPt;
	std::map<KTau*, double> m_tauIsolation;
	std::map<KTau*, double> m_tauIsolationOverPt;

	// individual isolation components needed for embedding studies (also filled by HttValidMuonsProducer)
	std::map<KMuon*, double> m_muonChargedIsolation;
	std::map<KMuon*, double> m_muonNeutralIsolation;
	std::map<KMuon*, double> m_muonPhotonIsolation;
	std::map<KMuon*, double> m_muonDeltaBetaIsolation;

	std::map<KMuon*, double> m_muonChargedIsolationOverPt;
	std::map<KMuon*, double> m_muonNeutralIsolationOverPt;
	std::map<KMuon*, double> m_muonPhotonIsolationOverPt;
	std::map<KMuon*, double> m_muonDeltaBetaIsolationOverPt;

	// filled by the DiLeptonQuantitiesProducer
	RMFLV m_diLeptonSystem;
	RMFLV m_diLeptonPlusMetSystem;
	RMFLV m_diLeptonPlusPuppiMetSystem;
	RMFLV m_diLeptonGenSystem;
	bool m_diLeptonGenSystemFound = false;
	RMFLV m_diTauGenSystem;
	bool m_diTauGenSystemFound = false;
	std::vector<KBasicJet*> m_LeptonJets;

	// filled by the TauSpinnerProducer
	double m_tauSpinnerPolarisation = DefaultValues::UndefinedDouble;

	// filled by the PolarisationQuantitiesProducer
	std::map<KLepton*, double> m_visibleOverFullEnergyHHKinFit; // Keys are only of type KTau*
	std::map<KLepton*, double> m_visibleOverFullEnergySvfit; // Keys are only of type KTau*
	std::map<KLepton*, double> m_visibleToFullAngleHHKinFit; // Keys are only of type KTau*
	std::map<KLepton*, double> m_visibleToFullAngleSvfit; // Keys are only of type KTau*
	std::map<KLepton*, double> m_rhoNeutralChargedAsymmetry; // Keys are only of type KTau*
	std::map<KLepton*, double> m_a1OmegaHHKinFit; // Keys are only of type KTau*
	std::map<KLepton*, double> m_a1OmegaSvfit; // Keys are only of type KTau*

	double m_tauPolarisationDiscriminatorHHKinFit = DefaultValues::UndefinedDouble;
	double m_tauPolarisationDiscriminatorSvfit = DefaultValues::UndefinedDouble;
	double m_tauPolarisationDiscriminatorSimpleFit = DefaultValues::UndefinedDouble;

	// filled by the MetprojectionProducer
	TVector2 m_recoMetOnGenMetProjection;
	TVector2 m_metPull;
	TVector2 m_recoMetOnBoson;
	TVector2 m_recoilOnBoson;
	double m_chiSquare;
	TVector2 m_recoPfMetOnGenMetProjection;
	TVector2 m_pfmetPull;
	TVector2 m_recoPfMetOnBoson;
	TVector2 m_pfrecoilOnBoson;
	double m_chiSquarePf;
	double m_metPlusVisLepsOnGenBosonPtOverGenBosonPt;
	double m_pfmetPlusVisLepsOnGenBosonPtOverGenBosonPt;
	double m_genBosonPt;
	double m_genBosonPhi;

	// filled by the DiLeptonQuantitiesProducer (collinear approximation)
	std::vector<RMFLV> m_flavourOrderedTauMomentaCA;
	RMFLV m_diTauSystemCA;
	bool m_validCollinearApproximation = false;

	double pZetaVis = 0.0;
	double pZetaMiss = 0.0;
	double pZetaMissVis = 0.0;
	double pZetaPuppiMiss = 0.0;
	double pZetaPuppiMissVis = 0.0;
        double deltaR = 0.0;
	double metPerpToZ = 0.0;
	double metParToZ = 0.0;
	double puppimetPerpToZ = 0.0;
	double puppimetParToZ = 0.0;
	double recoilPerpToZ = 0.0;
	double recoilParToZ = 0.0;
	double puppirecoilPerpToZ = 0.0;
	double puppirecoilParToZ = 0.0;

	// filled by the SvfitProducer
	mutable SvfitEventKey m_svfitEventKey;
	mutable SvfitInputs m_svfitInputs;
	mutable SvfitResults m_svfitResults;
	bool m_svfitCalculated = false;

	// filled by the HHKinFitProducer
	std::map<KLepton*, RMFLV> m_hhKinFitTaus;

	// filled by the SimpleFitProducer
	std::map<KLepton*, RMFLV> m_simpleFitTaus;

	// filled by the DiJetQuantitiesProducer
	RMDLV m_diJetSystem;
	bool m_diJetSystemAvailable = false;
	RMDLV m_diBJetSystem;
	bool m_diBJetSystemAvailable = false;
	RMDLV m_diBJetSystem_bReg;
	RMDLV m_JetPlusBJetSystem;
	bool m_JetPlusBJetSystemAvailable = false;
	RMDLV m_JetPlusBJetSystem_bReg;
	RMDLV m_highCSVJetPlusBJetSystem;
	RMDLV m_highCSVJetPlusBJetSystem_bReg;
	int m_highCSVJetIndex = -1;
	bool m_leadJetIsBJet = false;
	int m_nCentralJets20 = 0;
	int m_nCentralJets30 = 0;

	// filled by the DiGenJetQuantitiesProducer
	RMDLV m_diGenJetSystem;
	bool m_diGenJetSystemAvailable = false;

	// filled by TaggedJetUncertaintyShiftProducer
	std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, std::vector<KJet*>> m_correctedJetsBySplitUncertainty;
	std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, std::vector<KJet*>> m_correctedBTaggedJetsBySplitUncertainty;

	KMET* m_metUncorr = 0;
	KMET* m_puppimetUncorr = 0;
	KMET* m_pfmetUncorr = 0;
	KMET* m_mvametUncorr = 0;

	// filled by the MetCorrectors
	std::vector<float> m_mvametCorrections;
	std::vector<float> m_pfmetCorrections;
	std::vector<float> m_puppimetCorrections;        
	KMET m_met;
	KMET m_pfmet;
	KMET m_puppimet;
	KMET m_mvamet;

	// filled by the TauTauRestFrameProducer
	HttEnumTypes::TauTauRestFrameReco m_tauTauRestFrameReco = HttEnumTypes::TauTauRestFrameReco::NONE;
	std::vector<RMFLV> m_flavourOrderedTauMomenta;
	std::vector<ROOT::Math::Boost> m_boostsToTauRestFrames;
	bool m_tauMomentaReconstructed = false;
	RMFLV m_diTauSystem;
	ROOT::Math::Boost m_boostToDiTauRestFrame;
	bool m_diTauSystemReconstructed = false;

	// filled by the BoostRestFrameProducer
	std::map<KLepton*, RMFLV> m_leptonsBoostToDiLeptonSystem;
	std::map<KLepton*, RMFLV> m_leptonsBoostToDiTauSystem;
	std::map<RMFLV*, RMFLV> m_tausBoostToDiTauSystem;
	std::map<KGenTau*, RMFLV> m_genVisTausBoostToGenDiLeptonSystem;
	std::map<KGenTau*, RMFLV> m_genTausBoostToGenDiLeptonSystem;
	std::map<KGenTau*, RMFLV> m_genTausBoostToGenDiTauSystem;


	// filled by RefitVertexSelector
	RMPoint* m_refP1 = 0;
	RMPoint* m_refP2 = 0;
	RMFLV* m_track1p4 = 0;
	RMFLV* m_track2p4 = 0;


	// filled by GenTauCPProducer
	RMPoint* m_genPV = 0;
	double m_genZMinus  = DefaultValues::UndefinedDouble;
	double m_genZPlus  = DefaultValues::UndefinedDouble;
	double m_genZs  = DefaultValues::UndefinedDouble;

	double m_genPhiStarCP  = DefaultValues::UndefinedDouble;
	double m_genPhiStar  = DefaultValues::UndefinedDouble;
	double m_genOStarCP  = DefaultValues::UndefinedDouble;
	double m_genPhiCP  = DefaultValues::UndefinedDouble;
	double m_genPhi  = DefaultValues::UndefinedDouble;
	double m_genOCP  = DefaultValues::UndefinedDouble;
	double m_genPhiCPLab  = DefaultValues::UndefinedDouble;

	double m_genPhiCP_rho  = DefaultValues::UndefinedDouble;
	double m_genPhiStarCP_rho  = DefaultValues::UndefinedDouble;
	double m_genPhi_rho  = DefaultValues::UndefinedDouble;
	double m_genPhiStar_rho  = DefaultValues::UndefinedDouble;
	double m_gen_yTau  = DefaultValues::UndefinedDouble;
	double m_gen_posyTauL  = DefaultValues::UndefinedDouble;
	double m_gen_negyTauL  = DefaultValues::UndefinedDouble;

	std::pair <double,double> m_genChargedProngEnergies = std::make_pair(DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble);
	KGenParticle* m_genOneProngCharged1 = 0;
	KGenParticle* m_genOneProngCharged2 = 0;
	unsigned int m_genTau1ProngsSize = DefaultValues::UndefinedInt;
	unsigned int m_genTau2ProngsSize = DefaultValues::UndefinedInt;
	int m_genTau1DecayMode = DefaultValues::UndefinedInt;
	int m_genTau2DecayMode = DefaultValues::UndefinedInt;


	// filled by GenMatchedTauCPProducer
	RMPoint* m_genSV1 = 0; // vertex of production of tau daughter 1
	RMPoint* m_genSV2 = 0; // vertex of production of tau daughter 2
	TVector3 m_genIP1;
	TVector3 m_genIP2;
	double m_genCosPsiPlus  = DefaultValues::UndefinedDouble;
	double m_genCosPsiMinus = DefaultValues::UndefinedDouble;


	// filled by RecoTauCPProducer
	KVertex* m_thePV = 0;
	KBeamSpot* m_theBS = 0;

	TVector3 m_recoIP1; // IPvec wrt thePV
	TVector3 m_recoIP2; // IPvec wrt thePV
	double m_cosPsiPlus  = DefaultValues::UndefinedDouble;
	double m_cosPsiMinus = DefaultValues::UndefinedDouble;

	std::vector<double> m_errorIP1vec {DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble};
	std::vector<double> m_errorIP2vec {DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble};

	double m_deltaEtaGenRecoIP1  = DefaultValues::UndefinedDouble;
	double m_deltaEtaGenRecoIP2  = DefaultValues::UndefinedDouble;
	double m_deltaPhiGenRecoIP1  = DefaultValues::UndefinedDouble;
	double m_deltaPhiGenRecoIP2  = DefaultValues::UndefinedDouble;
	double m_deltaRGenRecoIP1  = DefaultValues::UndefinedDouble;
	double m_deltaRGenRecoIP2  = DefaultValues::UndefinedDouble;
	double m_deltaGenRecoIP1  = DefaultValues::UndefinedDouble;
	double m_deltaGenRecoIP2  = DefaultValues::UndefinedDouble;

	double m_deltaRrecoIP1s  = DefaultValues::UndefinedDouble;
	double m_deltaRrecoIP2s  = DefaultValues::UndefinedDouble;

	double m_recoPhiStarCP  = DefaultValues::UndefinedDouble;
	double m_recoPhiStarCPrPV  = DefaultValues::UndefinedDouble;
	double m_recoPhiStarCPrPV2  = DefaultValues::UndefinedDouble;
	double m_recoPhiStarCPrPVbs  = DefaultValues::UndefinedDouble;

	double m_recoPhiStarCP_rho  = DefaultValues::UndefinedDouble;
	double m_recoPhiStarCP_rho_merged  = DefaultValues::UndefinedDouble;
	double m_recoPhiStarCPrPV_rho  = DefaultValues::UndefinedDouble;
	double m_recoPhiStarCPrPVbs_rho  = DefaultValues::UndefinedDouble;

	double m_reco_posyTauL = DefaultValues::UndefinedDouble;
	double m_reco_negyTauL = DefaultValues::UndefinedDouble;
	double m_recoPhiStar = DefaultValues::UndefinedDouble;
	double m_recoPhiStar_rho = DefaultValues::UndefinedDouble;


	double m_recoChargedPiPlus_rho_pt = DefaultValues::UndefinedDouble;
	double m_recoChargedPiMinus_pt = DefaultValues::UndefinedDouble;
	double m_recoPiZeroPlus_pt = DefaultValues::UndefinedDouble;
	double m_recoPiZeroMinus_pt = DefaultValues::UndefinedDouble;
	double m_recoChargedPiPlus_eta = DefaultValues::UndefinedDouble;
	double m_recoChargedPiMinus_eta = DefaultValues::UndefinedDouble;
	double m_recoPiZeroPlus_eta = DefaultValues::UndefinedDouble;
	double m_recoPiZeroMinus_eta = DefaultValues::UndefinedDouble;

	KGenParticle* m_recoChargedParticle1 = 0;
	KGenParticle* m_recoChargedParitcle2 = 0;
	std::pair <double,double> m_recoChargedHadronEnergies = std::make_pair(DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble);
	//double m_recoIP1 = DefaultValues::UndefinedDouble;
	//double m_recoIP2 = DefaultValues::UndefinedDouble;
	double m_recoTrackRefError1 = DefaultValues::UndefinedDouble;
	double m_recoTrackRefError2 = DefaultValues::UndefinedDouble;

	// MVA outputs
	std::vector<double> m_antiTtbarDiscriminators;
	std::vector<double> m_tauPolarisationDiscriminators;

	//MVATestMethods
	std::vector<double> m_MVATestMethodsDiscriminators;

	// filled by HttValidGenTausProducer. Naming scheme like for the reco particles
	std::vector<KGenTau*> m_ptOrderedGenTaus;
	std::vector<KGenTau*> m_flavourOrderedGenTaus;
	std::vector<KGenTau*> m_chargeOrderedGenTaus;
	std::vector<KGenTau*> m_validGenTausToElectrons;
	std::vector<KGenTau*> m_validGenTausToMuons;
	std::vector<KGenTau*> m_validGenTausToTaus;

	// filled by TriggerTagAndProbeProducers
	std::vector<std::pair<KElectron*, KElectron*> > m_triggerTagProbeElectronPairs;
	std::vector<std::pair<KMuon*, KMuon*> > m_triggerTagProbeMuonPairs;
	std::vector<std::pair<KMuon*, KTau*> > m_triggerTagProbeMuonTauPairs;
	std::vector<std::pair<KElectron*, KTau*> > m_triggerTagProbeElectronTauPairs;

	std::vector<std::pair<bool, bool> > m_triggerTagProbeElectronMatchedPairs;
	std::vector<std::pair<bool, bool> > m_triggerTagProbeMuonMatchedPairs;
	std::vector<std::pair<bool, bool> > m_triggerTagProbeMuonTauMatchedPairs;
	std::vector<std::pair<bool, bool> > m_triggerTagProbeElectronTauMatchedPairs;

	// filled by MVAInputQuantitiesProducer
// 	int tsValue = 0;
	double m_pVecSum = -1;
	double m_pScalSum = -1;
	double m_MinLLJetEta = 10;
	double m_Lep1Centrality = -1.5;
	double m_Lep2Centrality = -1;
	double m_DiLepCentrality = -1;
	double m_DiLepDiJetDeltaR = -1;
	double m_diLepBoost = -10;
	double m_diLepJet1DeltaR = -10;
	double m_diLepDeltaR = -10;
	double m_diJetDeltaMass = -10;
	double m_diJetSymDeltaEta = -30;
	double m_diJetDeltaR = -1;
	double m_diCJetDeltaMass = -10;
	double m_diCJetSymDeltaEta = -30;
	double m_diCJetDeltaR = -1;
	double m_diCJetAbsDeltaPhi = -1;
	double m_diCJetSymEta1 = -1;
	double m_jccsv1 = -1;
	double m_jccsv2 = -1;
	double m_jccsv3 = -1;
	double m_jccsv4 = -1;
	double m_csv1JetPt = -10;
	double m_csv2JetPt = -10;
	double m_csv1JetMass = -10;
	double m_csv2JetMass = -10;
	double m_diCJetMass = -10;
	double m_pVecSumCSVJets = -1;

	// filled by EmbeddingGlobalQuantitiesProducer
	double m_pfSumHt = 0.;
	RMFLV m_pfSumP4;
	double m_pfSumHtWithoutZMuMu = 0.;
	RMFLV m_pfSumP4WithoutZMuMu;

	//filled by TagAndProbeMuonPairProducer
	std::vector<std::pair<KMuon*,KMuon*>> m_TagAndProbeMuonPairs;
	//filled by TagAndProbeElectronPairProducer
	std::vector<std::pair<KElectron*,KElectron*>> m_TagAndProbeElectronPairs;
	//filled by TagAndProbeGenLeptonProducer
	std::vector<KElectron*> m_TagAndProbeGenElectrons;
	std::vector<KMuon*> m_TagAndProbeGenMuons;
	std::vector<KTau*> m_TagAndProbeGenTaus;

	//filled by TTbarGenDecayModeProducer
	unsigned int m_TTbarGenDecayMode = 0;

        //filled by NLOreweightingWeightsProducer
        double m_ggh_t_weight = 1.0;
        double m_ggh_b_weight = 1.0;
        double m_ggh_i_weight = 1.0;
        double m_ggH_t_weight = 1.0;
        double m_ggH_b_weight = 1.0;
        double m_ggH_i_weight = 1.0;
        double m_ggA_t_weight = 1.0;
        double m_ggA_b_weight = 1.0;
        double m_ggA_i_weight = 1.0;
        std::map<std::string, double> m_nlo_gg_uncertainty_weights;

        //filled by EmbeddedZpTMassCorrectionsProducer
        double m_embed_zpt_mass_weight;

        //filled by ImpactParameterCorrectionsProducer
	double m_DCAcalib[2][2][2]; //[d0/dZ][abs/rel][0/1]

	//filled by MetFilterFlagProducer
	bool m_MetFilter = true;
	bool m_Flag_goodVertices = true;
	bool m_Flag_globalSuperTightHalo2016Filter = true;
	bool m_Flag_HBHENoiseFilter = true;
	bool m_Flag_HBHENoiseIsoFilter = true;
	bool m_Flag_EcalDeadCellTriggerPrimitiveFilter = true;
	bool m_Flag_BadPFMuonFilter = true;
	bool m_Flag_BadChargedCandidateFilter = true;
	bool m_Flag_eeBadScFilter = true;
	bool m_ecalBadCalibReducedMINIAODFilter = true;

        //filled by SMggHNNLOProducer
        double m_ggh_NNLO_weight = 1.0;
        std::vector<double> m_THU_ggH;
        
        //filled by SMvbfNNLOProducer
        std::vector<double> m_THU_qqH;

        //filled by L1TauTriggerMatchingProducers
        std::map<KLepton*, std::map<std::string, bool>* > m_additionalL1TauMatchedLeptons;
        std::map<KTau*, std::map<std::string, bool> > m_additionalL1TauMatchedTaus;
        std::map<KMuon*, std::map<std::string, bool> > m_additionalL1TauMatchedMuons;
        std::map<KElectron*, std::map<std::string, bool> > m_additionalL1TauMatchedElectrons;
        std::map<std::string, std::vector<float> > m_settingsTauTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick;
        std::map<std::string, std::vector<float> > m_settingsTauTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick;
        std::map<std::string, std::vector<float> > m_settingsMuonTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick;
        std::map<std::string, std::vector<float> > m_settingsMuonTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick;
        std::map<std::string, std::vector<float> > m_settingsElectronTriggerCheckAdditionalL1TauMatchLowerPtCutByHltNick;
        std::map<std::string, std::vector<float> > m_settingsElectronTriggerCheckAdditionalL1TauMatchUpperEtaCutByHltNick;
};


#pragma once

#include "Artus/KappaAnalysis/interface/Producers/ValidElectronsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief GlobalProducer, for valid electrons.
   
   Required config tags in addtion to the ones of the base class:
   - ElectronIDType
   - ElectronIDName (default given)
   - ElectronMvaIDCutEB1 (default given)
   - ElectronMvaIDCutEB2 (default given)
   - ElectronMvaIDCutEE (default given)
   - ElectronChargedIsoVetoConeSizeEB (default given)
   - ElectronChargedIsoVetoConeSizeEE (default given)
   - ElectronNeutralIsoVetoConeSize (default given)
   - ElectronPhotonIsoVetoConeSizeEB (default given)
   - ElectronPhotonIsoVetoConeSizeEE (default given)
   - ElectronDeltaBetaIsoVetoConeSize (default given)
   - ElectronChargedIsoPtThreshold (default given)
   - ElectronNeutralIsoPtThreshold (default given)
   - ElectronPhotonIsoPtThreshold (default given)
   - ElectronDeltaBetaIsoPtThreshold (default given)
   - ElectronIsoSignalConeSize
   - ElectronDeltaBetaCorrectionFactor
   - ElectronIsoPtSumOverPtLowerThresholdEB
   - ElectronIsoPtSumOverPtLowerThresholdEE
   - ElectronIsoPtSumOverPtUpperThresholdEB
   - ElectronIsoPtSumOverPtUpperThresholdEE
   - ElectronIDList (default given)
*/

class HttValidElectronsProducer: public ValidElectronsProducer<HttTypes>
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	enum class ElectronIDType : int
	{
		INVALID = -2,
		NONE  = -1,
		SUMMER2013LOOSE = 0,
		SUMMER2013TIGHT = 1,
		SUMMER2013TTHTIGHT = 2,
		SUMMER2013TTHLOOSE = 3,
		CUTBASED2015ANDLATER = 4,
		MVABASED2015ANDLATER = 5,
		CUTBASED2015NOISOANDIPCUTSVETO = 6,
		CUTBASED2015NOISOANDIPCUTSLOOSE = 7,
		CUTBASED2015NOISOANDIPCUTSMEDIUM = 8,
		CUTBASED2015NOISOANDIPCUTSTIGHT = 9,
		CUTBASED2016NOISOCUTSVETO = 10,
		CUTBASED2016NOISOCUTSLOOSE = 11,
		CUTBASED2016NOISOCUTSMEDIUM = 12,
		CUTBASED2016NOISOCUTSTIGHT = 13
	};
	static ElectronIDType ToElectronIDType(std::string const& electronIDType)
	{
		if (electronIDType == "summer2013loose") return ElectronIDType::SUMMER2013LOOSE;
		else if (electronIDType == "summer2013tight") return ElectronIDType::SUMMER2013TIGHT;
		else if (electronIDType == "summer2013tthloose") return ElectronIDType::SUMMER2013TTHLOOSE;
		else if (electronIDType == "summer2013tthtight") return ElectronIDType::SUMMER2013TTHTIGHT;
		else if (electronIDType == "cutbased2015andlater") return ElectronIDType::CUTBASED2015ANDLATER;
		else if (electronIDType == "mvabased2015andlater") return ElectronIDType::MVABASED2015ANDLATER;
		else if (electronIDType == "cutbased2015noisoandipcutsveto") return ElectronIDType::CUTBASED2015NOISOANDIPCUTSVETO;
		else if (electronIDType == "cutbased2015noisoandipcutsloose") return ElectronIDType::CUTBASED2015NOISOANDIPCUTSLOOSE;
		else if (electronIDType == "cutbased2015noisoandipcutsmedium") return ElectronIDType::CUTBASED2015NOISOANDIPCUTSMEDIUM;
		else if (electronIDType == "cutbased2015noisocutstight") return ElectronIDType::CUTBASED2015NOISOANDIPCUTSTIGHT;
		else if (electronIDType == "cutbased2016noisocutsveto") return ElectronIDType::CUTBASED2016NOISOCUTSVETO;
		else if (electronIDType == "cutbased2016noisocutsloose") return ElectronIDType::CUTBASED2016NOISOCUTSLOOSE;
		else if (electronIDType == "cutbased2016noisocutsmedium") return ElectronIDType::CUTBASED2016NOISOCUTSMEDIUM;
		else if (electronIDType == "cutbased2016noisocutstight") return ElectronIDType::CUTBASED2016NOISOCUTSTIGHT;
		else if (electronIDType == "none") return ElectronIDType::NONE;
		else
			LOG(FATAL) << "Could not find ElectronID " << electronIDType << "! If you want the HttValidElectronsProducer to use no special ID, use \"none\" as argument."<< std::endl;
		return ElectronIDType::INVALID;
	}
	
	HttValidElectronsProducer(
			std::vector<KElectron*> product_type::*validElectrons=&product_type::m_validElectrons,
			std::vector<KElectron*> product_type::*invalidElectrons=&product_type::m_invalidElectrons,
			std::string (setting_type::*GetElectronID)(void) const=&setting_type::GetElectronID,
			std::string (setting_type::*GetElectronIDType)(void) const=&setting_type::GetElectronIDType,
			std::string (setting_type::*GetElectronIDName)(void) const=&setting_type::GetElectronIDName,
			float (setting_type::*GetElectronMvaIDCutEB1)(void) const=&setting_type::GetElectronMvaIDCutEB1,
			float (setting_type::*GetElectronMvaIDCutEB2)(void) const=&setting_type::GetElectronMvaIDCutEB2,
			std::vector<float>& (setting_type::*GetElectronEtaBinnedEAValues)(void) const=&setting_type::GetElectronEtaBinnedEAValues,
			std::vector<float>& (setting_type::*GetElectronEtaBinsForEA)(void) const=&setting_type::GetElectronEtaBinsForEA,
			float (setting_type::*GetElectronMvaIDCutEE)(void) const=&setting_type::GetElectronMvaIDCutEE,
			std::string (setting_type::*GetElectronIsoType)(void) const=&setting_type::GetElectronIsoType,
			std::string (setting_type::*GetElectronIso)(void) const=&setting_type::GetElectronIso,
			std::string (setting_type::*GetElectronReco)(void) const=&setting_type::GetElectronReco,
			std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const=&setting_type::GetElectronLowerPtCuts,
			std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const=&setting_type::GetElectronUpperAbsEtaCuts,
			float (setting_type::*GetElectronChargedIsoVetoConeSizeEB)(void) const=&setting_type::GetElectronChargedIsoVetoConeSizeEB,
			float (setting_type::*GetElectronChargedIsoVetoConeSizeEE)(void) const=&setting_type::GetElectronChargedIsoVetoConeSizeEE,
			float (setting_type::*GetElectronNeutralIsoVetoConeSize)(void) const=&setting_type::GetElectronNeutralIsoVetoConeSize,
			float (setting_type::*GetElectronPhotonIsoVetoConeSizeEB)(void) const=&setting_type::GetElectronPhotonIsoVetoConeSizeEB,
			float (setting_type::*GetElectronPhotonIsoVetoConeSizeEE)(void) const=&setting_type::GetElectronPhotonIsoVetoConeSizeEE,
			float (setting_type::*GetElectronDeltaBetaIsoVetoConeSize)(void) const=&setting_type::GetElectronDeltaBetaIsoVetoConeSize,
			float (setting_type::*GetElectronChargedIsoPtThreshold)(void) const=&setting_type::GetElectronChargedIsoPtThreshold,
			float (setting_type::*GetElectronNeutralIsoPtThreshold)(void) const=&setting_type::GetElectronNeutralIsoPtThreshold,
			float (setting_type::*GetElectronPhotonIsoPtThreshold)(void) const=&setting_type::GetElectronPhotonIsoPtThreshold,
			float (setting_type::*GetElectronDeltaBetaIsoPtThreshold)(void) const=&setting_type::GetElectronDeltaBetaIsoPtThreshold,
			float (setting_type::*GetElectronIsoSignalConeSize)(void) const=&setting_type::GetElectronIsoSignalConeSize,
			float (setting_type::*GetElectronDeltaBetaCorrectionFactor)(void) const=&setting_type::GetElectronDeltaBetaCorrectionFactor,
			float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEB)(void) const=&setting_type::GetElectronIsoPtSumOverPtLowerThresholdEB,
			float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEE)(void) const=&setting_type::GetElectronIsoPtSumOverPtLowerThresholdEE,
			float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEB)(void) const=&setting_type::GetElectronIsoPtSumOverPtUpperThresholdEB,
			float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEE)(void) const=&setting_type::GetElectronIsoPtSumOverPtUpperThresholdEE,
			float (setting_type::*GetElectronTrackDxyCut)(void) const=&setting_type::GetElectronTrackDxyCut,
			float (setting_type::*GetElectronTrackDzCut)(void) const=&setting_type::GetElectronTrackDzCut,
			std::vector<std::string>& (setting_type::*GetElectronIDList)(void) const=&setting_type::GetElectronIDList
	);

	virtual void Init(setting_type const& settings) override;


protected:

	// Htautau specific additional definitions
	virtual bool AdditionalCriteria(KElectron* electron, event_type const& event,
	                                product_type& product, setting_type const& settings) const  override;


private:
	std::string (setting_type::*GetElectronIDType)(void) const;
	std::string (setting_type::*GetElectronIDName)(void) const;
	float (setting_type::*GetElectronMvaIDCutEB1)(void) const;
	float (setting_type::*GetElectronMvaIDCutEB2)(void) const;
	std::vector<float>& (setting_type::*GetElectronEtaBinnedEAValues)(void) const;
	std::vector<float>& (setting_type::*GetElectronEtaBinsForEA)(void) const;
	float (setting_type::*GetElectronMvaIDCutEE)(void) const;
	float (setting_type::*GetElectronChargedIsoVetoConeSizeEB)(void) const;
	float (setting_type::*GetElectronChargedIsoVetoConeSizeEE)(void) const;
	float (setting_type::*GetElectronNeutralIsoVetoConeSize)(void) const;
	float (setting_type::*GetElectronPhotonIsoVetoConeSizeEB)(void) const;
	float (setting_type::*GetElectronPhotonIsoVetoConeSizeEE)(void) const;
	float (setting_type::*GetElectronDeltaBetaIsoVetoConeSize)(void) const;
	float (setting_type::*GetElectronChargedIsoPtThreshold)(void) const;
	float (setting_type::*GetElectronNeutralIsoPtThreshold)(void) const;
	float (setting_type::*GetElectronPhotonIsoPtThreshold)(void) const;
	float (setting_type::*GetElectronDeltaBetaIsoPtThreshold)(void) const;
	float (setting_type::*GetElectronIsoSignalConeSize)(void) const;
	float (setting_type::*GetElectronDeltaBetaCorrectionFactor)(void) const;
	float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEB)(void) const;
	float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEE)(void) const;
	float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEB)(void) const;
	float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEE)(void) const;
	float (setting_type::*GetElectronTrackDxyCut)(void) const;
	float (setting_type::*GetElectronTrackDzCut)(void) const;
	std::vector<std::string>& (setting_type::*GetElectronIDList)(void) const;

	ElectronIDType electronIDType;
	
	mutable bool electronIDListInMetadata;
	mutable bool electronIDInMetadata;

	std::string electronIDName;
	std::vector<std::string> electronIDList;

	float electronMvaIDCutEB1;
	float electronMvaIDCutEB2;
	float electronMvaIDCutEE;

	bool IsMVATrigElectronTTHSummer2013(KElectron* electron, event_type const& event, bool tightID) const;
	bool IsMVANonTrigElectronHttSummer2013(KElectron* electron, event_type const& event, bool tightID) const;
	bool IsCutBased(KElectron* electron, event_type const& event, const std::string &idName) const;
	// This function uses the same criteria as the one above with the exception of
	// isolation (and impact parameters for 2015 Id). Cut values are taken from
	// https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2
	bool IsCutBased(KElectron* electron, event_type const& event,
			float full5x5_sigmaIetaIeta, float dEtaIn_Seed, float dPhiIn,
			float hOverE, float invEMinusInvP, int missingHits, int year=2015) const;
	bool IsMVABased(KElectron* electron, event_type const& event, const std::string &idName) const;
	bool CheckElectronMetadata(const KElectronMetadata *meta, std::string idName, bool &checkedAlready) const;
	bool CheckElectronMetadata(const KElectronMetadata *meta, std::vector<std::string> idNames, bool &checkedAlready) const;

        std::vector<float> eaValues = {};
        std::vector<float> etaBins = {};
};


/**
 */
class HttValidLooseElectronsProducer: public HttValidElectronsProducer
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const override {
		return "HttValidLooseElectronsProducer";
	}
	
	virtual void Init(setting_type const& settings) override {
	
		HttValidElectronsProducer::Init(settings);
	
		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nLooseElectrons", [this](event_type const& event, product_type const& product) {
			return product.m_validLooseElectrons.size();
		});
	}
	
	HttValidLooseElectronsProducer(
			std::vector<KElectron*> product_type::*validElectrons=&product_type::m_validLooseElectrons,
			std::vector<KElectron*> product_type::*invalidElectrons=&product_type::m_invalidLooseElectrons,
			std::string (setting_type::*GetElectronID)(void) const=&setting_type::GetLooseElectronID,
			std::string (setting_type::*GetElectronIDType)(void) const=&setting_type::GetLooseElectronIDType,
			std::string (setting_type::*GetElectronIDName)(void) const=&setting_type::GetLooseElectronIDName,
			float (setting_type::*GetElectronMvaIDCutEB1)(void) const=&setting_type::GetLooseElectronMvaIDCutEB1,
			float (setting_type::*GetElectronMvaIDCutEB2)(void) const=&setting_type::GetLooseElectronMvaIDCutEB2,
			std::vector<float>& (setting_type::*GetElectronEtaBinnedEAValues)(void) const=&setting_type::GetElectronEtaBinnedEAValues,
			std::vector<float>& (setting_type::*GetElectronEtaBinsForEA)(void) const=&setting_type::GetElectronEtaBinsForEA,
			float (setting_type::*GetElectronMvaIDCutEE)(void) const=&setting_type::GetLooseElectronMvaIDCutEE,
			std::string (setting_type::*GetElectronIsoType)(void) const=&setting_type::GetLooseElectronIsoType,
			std::string (setting_type::*GetElectronIso)(void) const=&setting_type::GetLooseElectronIso,
			std::string (setting_type::*GetElectronReco)(void) const=&setting_type::GetLooseElectronReco,
			std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const=&setting_type::GetLooseElectronLowerPtCuts,
			std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const=&setting_type::GetLooseElectronUpperAbsEtaCuts,
			float (setting_type::*GetElectronChargedIsoVetoConeSizeEB)(void) const=&setting_type::GetElectronChargedIsoVetoConeSizeEB,
			float (setting_type::*GetElectronChargedIsoVetoConeSizeEE)(void) const=&setting_type::GetElectronChargedIsoVetoConeSizeEE,
			float (setting_type::*GetElectronNeutralIsoVetoConeSize)(void) const=&setting_type::GetElectronNeutralIsoVetoConeSize,
			float (setting_type::*GetElectronPhotonIsoVetoConeSizeEB)(void) const=&setting_type::GetElectronPhotonIsoVetoConeSizeEB,
			float (setting_type::*GetElectronPhotonIsoVetoConeSizeEE)(void) const=&setting_type::GetElectronPhotonIsoVetoConeSizeEE,
			float (setting_type::*GetElectronDeltaBetaIsoVetoConeSize)(void) const=&setting_type::GetElectronDeltaBetaIsoVetoConeSize,
			float (setting_type::*GetElectronChargedIsoPtThreshold)(void) const=&setting_type::GetElectronChargedIsoPtThreshold,
			float (setting_type::*GetElectronNeutralIsoPtThreshold)(void) const=&setting_type::GetElectronNeutralIsoPtThreshold,
			float (setting_type::*GetElectronPhotonIsoPtThreshold)(void) const=&setting_type::GetElectronPhotonIsoPtThreshold,
			float (setting_type::*GetElectronDeltaBetaIsoPtThreshold)(void) const=&setting_type::GetElectronDeltaBetaIsoPtThreshold,
			float (setting_type::*GetElectronIsoSignalConeSize)(void) const=&setting_type::GetElectronIsoSignalConeSize,
			float (setting_type::*GetElectronDeltaBetaCorrectionFactor)(void) const=&setting_type::GetElectronDeltaBetaCorrectionFactor,
			float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEB)(void) const=&setting_type::GetLooseElectronIsoPtSumOverPtLowerThresholdEB,
			float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEE)(void) const=&setting_type::GetLooseElectronIsoPtSumOverPtLowerThresholdEE,
			float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEB)(void) const=&setting_type::GetLooseElectronIsoPtSumOverPtUpperThresholdEB,
			float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEE)(void) const=&setting_type::GetLooseElectronIsoPtSumOverPtUpperThresholdEE,
			float (setting_type::*GetElectronTrackDxyCut)(void) const=&setting_type::GetLooseElectronTrackDxyCut,
			float (setting_type::*GetElectronTrackDzCut)(void) const=&setting_type::GetLooseElectronTrackDzCut
	);

};


/**
 */
class HttValidVetoElectronsProducer: public HttValidElectronsProducer
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const override {
		return "HttValidVetoElectronsProducer";
	}

	virtual void Init(setting_type const& settings) override {
	
		HttValidElectronsProducer::Init(settings);
	
		// add possible quantities for the lambda ntuples consumers
		LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nVetoElectrons", [this](event_type const& event, product_type const& product) {
			return product.m_validVetoElectrons.size();
		});
	}
	
	HttValidVetoElectronsProducer(
			std::vector<KElectron*> product_type::*validElectrons=&product_type::m_validVetoElectrons,
			std::vector<KElectron*> product_type::*invalidElectrons=&product_type::m_invalidVetoElectrons,
			std::string (setting_type::*GetElectronID)(void) const=&setting_type::GetVetoElectronID,
			std::string (setting_type::*GetElectronIDType)(void) const=&setting_type::GetVetoElectronIDType,
			std::string (setting_type::*GetElectronIDName)(void) const=&setting_type::GetVetoElectronIDName,
			float (setting_type::*GetElectronMvaIDCutEB1)(void) const=&setting_type::GetVetoElectronMvaIDCutEB1,
			float (setting_type::*GetElectronMvaIDCutEB2)(void) const=&setting_type::GetVetoElectronMvaIDCutEB2,
			std::vector<float>& (setting_type::*GetElectronEtaBinnedEAValues)(void) const=&setting_type::GetElectronEtaBinnedEAValues,
			std::vector<float>& (setting_type::*GetElectronEtaBinsForEA)(void) const=&setting_type::GetElectronEtaBinsForEA,
			float (setting_type::*GetElectronMvaIDCutEE)(void) const=&setting_type::GetVetoElectronMvaIDCutEE,
			std::string (setting_type::*GetElectronIsoType)(void) const=&setting_type::GetVetoElectronIsoType,
			std::string (setting_type::*GetElectronIso)(void) const=&setting_type::GetVetoElectronIso,
			std::string (setting_type::*GetElectronReco)(void) const=&setting_type::GetVetoElectronReco,
			std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const=&setting_type::GetVetoElectronLowerPtCuts,
			std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const=&setting_type::GetVetoElectronUpperAbsEtaCuts,
			float (setting_type::*GetElectronChargedIsoVetoConeSizeEB)(void) const=&setting_type::GetElectronChargedIsoVetoConeSizeEB,
			float (setting_type::*GetElectronChargedIsoVetoConeSizeEE)(void) const=&setting_type::GetElectronChargedIsoVetoConeSizeEE,
			float (setting_type::*GetElectronNeutralIsoVetoConeSize)(void) const=&setting_type::GetElectronNeutralIsoVetoConeSize,
			float (setting_type::*GetElectronPhotonIsoVetoConeSizeEB)(void) const=&setting_type::GetElectronPhotonIsoVetoConeSizeEB,
			float (setting_type::*GetElectronPhotonIsoVetoConeSizeEE)(void) const=&setting_type::GetElectronPhotonIsoVetoConeSizeEE,
			float (setting_type::*GetElectronDeltaBetaIsoVetoConeSize)(void) const=&setting_type::GetElectronDeltaBetaIsoVetoConeSize,
			float (setting_type::*GetElectronChargedIsoPtThreshold)(void) const=&setting_type::GetElectronChargedIsoPtThreshold,
			float (setting_type::*GetElectronNeutralIsoPtThreshold)(void) const=&setting_type::GetElectronNeutralIsoPtThreshold,
			float (setting_type::*GetElectronPhotonIsoPtThreshold)(void) const=&setting_type::GetElectronPhotonIsoPtThreshold,
			float (setting_type::*GetElectronDeltaBetaIsoPtThreshold)(void) const=&setting_type::GetElectronDeltaBetaIsoPtThreshold,
			float (setting_type::*GetElectronIsoSignalConeSize)(void) const=&setting_type::GetElectronIsoSignalConeSize,
			float (setting_type::*GetElectronDeltaBetaCorrectionFactor)(void) const=&setting_type::GetElectronDeltaBetaCorrectionFactor,
			float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEB)(void) const=&setting_type::GetVetoElectronIsoPtSumOverPtLowerThresholdEB,
			float (setting_type::*GetElectronIsoPtSumOverPtLowerThresholdEE)(void) const=&setting_type::GetVetoElectronIsoPtSumOverPtLowerThresholdEE,
			float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEB)(void) const=&setting_type::GetVetoElectronIsoPtSumOverPtUpperThresholdEB,
			float (setting_type::*GetElectronIsoPtSumOverPtUpperThresholdEE)(void) const=&setting_type::GetVetoElectronIsoPtSumOverPtUpperThresholdEE,
			float (setting_type::*GetElectronTrackDxyCut)(void) const=&setting_type::GetElectronTrackDxyCut,
			float (setting_type::*GetElectronTrackDzCut)(void) const=&setting_type::GetElectronTrackDzCut
	);

};


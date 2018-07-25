
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/ProducerBase.h"

#include <Math/VectorUtil.h>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Abstract Producer for Veto of dileptons
 */
template<class TLepton>
class DiLeptonVetoProducerBase: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	DiLeptonVetoProducerBase(std::vector<TLepton*> product_type::*leptons,
	                         float (setting_type::*GetDiLeptonMinDeltaRCut)(void) const,
	                         int product_type::*nDiLeptonVetoPairsOS,
	                         int product_type::*nDiLeptonVetoPairsSS) :
		ProducerBase<HttTypes>(),
		m_leptons(leptons),
		GetDiLeptonMinDeltaRCut(GetDiLeptonMinDeltaRCut),
		m_nDiLeptonVetoPairsOS(nDiLeptonVetoPairsOS),
		m_nDiLeptonVetoPairsSS(nDiLeptonVetoPairsSS)
	{
	}					
	
	virtual void Init(setting_type const& settings) override
	{
		ProducerBase<HttTypes>::Init(settings);
		
	}

	virtual void Produce(event_type const& event, product_type& product, setting_type const& settings) const override
	{
		(product.*m_nDiLeptonVetoPairsOS) = 0;
		(product.*m_nDiLeptonVetoPairsSS) = 0;
		
		for (typename std::vector<TLepton*>::const_iterator lepton1 = (product.*m_leptons).begin(); lepton1 != (product.*m_leptons).end(); ++lepton1)
		{
			for (typename std::vector<TLepton*>::const_iterator lepton2 = lepton1+1; lepton2 != (product.*m_leptons).end(); ++lepton2)
			{
			
				if (((settings.*GetDiLeptonMinDeltaRCut)() < 0.0f) ||
				    (ROOT::Math::VectorUtil::DeltaR((*lepton1)->p4, (*lepton2)->p4) > (double)(settings.*GetDiLeptonMinDeltaRCut)()))
				{
					if ((*lepton1)->charge() * (*lepton2)->charge() < 0.0)
					{
						(product.*m_nDiLeptonVetoPairsOS) += 1;
                                                LOG(DEBUG) << "Found OS di-lepton veto pair";
                                                LOG(DEBUG) << "\tLepton 1 candidate p4: " << (*lepton1)->p4;
                                                LOG(DEBUG) << "\tLepton 2 candidate p4: " << (*lepton2)->p4;
					}
					else
					{
						(product.*m_nDiLeptonVetoPairsSS) += 1;
					}
				}
			}
		}
	}


private:
	std::vector<TLepton*> product_type::*m_leptons;
	float (setting_type::*GetDiLeptonMinDeltaRCut)(void) const;
	int product_type::*m_nDiLeptonVetoPairsOS;
	int product_type::*m_nDiLeptonVetoPairsSS;

};


/** Producer for Veto of DiVetoElectrons
 *  Required config tag:
 *  - DiVetoElectronMinDeltaRCut
 */
class DiVetoElectronVetoProducer : public DiLeptonVetoProducerBase<KElectron> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	virtual std::string GetProducerId() const override;
	
	DiVetoElectronVetoProducer();
	
	virtual void Init(setting_type const& settings) override;
};


/** Producer for Veto of DiVetoMuons
 *  Required config tag:
 *  - DiVetoMuonMinDeltaRCut
 */
class DiVetoMuonVetoProducer : public DiLeptonVetoProducerBase<KMuon> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	virtual std::string GetProducerId() const override;
	
	DiVetoMuonVetoProducer();
	
	virtual void Init(setting_type const& settings) override;
};



#pragma once

#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include <boost/regex.hpp>
#include <boost/algorithm/string.hpp>

/**
   \brief TopPtReweightingProducer
   Top Pt reweighting as suggested on:
   https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting
   Config tags:
   - TopPtReweightingStrategy: possible values: Run1, Run2. If something else is defined, then Run2 is taken.
     Both weigths are computed.

*/

class TopPtReweightingProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings) override;
	void Produce( event_type const& event,
			product_type & product,
			setting_type const& settings) const override;
private:
	bool m_isTTbar;
	bool m_oldStrategy = false; // old == true: Run1, new == false: Run2
	float ComputeWeight(float top1Pt, float top2Pt, float parameter_a, float parameter_b, float parameter_c, float setconst_threshold) const;
};

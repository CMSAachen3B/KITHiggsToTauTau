
#pragma once

#include <TH2.h>
#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include <boost/regex.hpp>

/**
   \brief NMSSMVariationsProducer

   See https://indico.cern.ch/event/494682/contributions/1172505/attachments/1223578/1800218/mcaod-Feb15-2016.pdf for the motivation. This Producer copies event-by-event renormalization and factorization weights from the Kappa input file to the output. This can be used to calculate the migration of signal events between channels and categories.

*/

class NMSSMVariationProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	std::string GetProducerId() const;

	virtual void Init(setting_type const& settings) override;

	virtual void Produce(event_type const& event, product_type & product, 
	                     setting_type const& settings) const override;

};

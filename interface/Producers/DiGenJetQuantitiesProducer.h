
#pragma once

#include "../HttTypes.h"


class DiGenJetQuantitiesProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const override;
	typedef std::function<double(RMDLV const&)> digenjet_extractor_lambda;
	static double GetDiGenJetQuantity(product_type const& product,
	                               digenjet_extractor_lambda digenjetQuantity);
	virtual void Init(setting_type const& settings) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const override;
};


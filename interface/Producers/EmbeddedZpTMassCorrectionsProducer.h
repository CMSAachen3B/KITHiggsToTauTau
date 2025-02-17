#pragma once

#include "../HttTypes.h"
#include "TH2D.h"


class EmbeddedZpTMassCorrectionsProducer: public ProducerBase<HttTypes> {
public:

    typedef typename HttTypes::event_type event_type;
    typedef typename HttTypes::product_type product_type;
    typedef typename HttTypes::setting_type setting_type;

    virtual std::string GetProducerId() const override {
        return "EmbeddedZpTMassCorrectionsProducer";
    }

    virtual void Init(setting_type const& settings) override;

    virtual void Produce(event_type const& event, product_type& product,
                         setting_type const& settings) const override;

private:
    TH2F* m_input_hist;
};

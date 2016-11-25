
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RefitVertexSelector.h"



void RefitVertexSelectorBase::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	// add possible quantities for the lambda ntuples consumers
	
	// thePV coordinates
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVx", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->position.x();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVy", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->position.y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("thePVz", [](event_type const& event, product_type const& product)
	{
		return (product.m_thePV)->position.z();
	});

	// BS coordinates
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("theBSx", [](event_type const& event, product_type const& product)
	{
		return (product.m_theBS)->x();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("theBSy", [](event_type const& event, product_type const& product)
	{
		return (product.m_theBS)->y();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("theBSz", [](event_type const& event, product_type const& product)
	{
		return (product.m_theBS)->z();
	});

	// refitted PV coordinates
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refitPVx", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPV != 0 ) ? (product.m_refitPV)->position.x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refitPVy", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPV != 0) ? (product.m_refitPV)->position.y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refitPVz", [](event_type const& event, product_type const& product)
	{
		return ((product.m_refitPV != 0) ? (product.m_refitPV)->position.z() : DefaultValues::UndefinedFloat);
	});
	
	// refitted (w/ BS constraint) PV coordinates
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refitBSPVx", [](event_type const& event, product_type const& product)
	{
		return (product.m_refitBSPV ? (product.m_refitBSPV)->position.x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refitBSPVy", [](event_type const& event, product_type const& product)
	{
		return (product.m_refitBSPV ? (product.m_refitBSPV)->position.y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refitBSPVz", [](event_type const& event, product_type const& product)
	{
		return (product.m_refitBSPV ? (product.m_refitBSPV)->position.z(): DefaultValues::UndefinedFloat);
	});

	// track ref point coordinates
	// lepton1
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refP1x", [](event_type const& event, product_type const& product)
	{
		return (product.m_refP1 ? (product.m_refP1)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refP1y", [](event_type const& event, product_type const& product)
	{
		return (product.m_refP1 ? (product.m_refP1)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refP1z", [](event_type const& event, product_type const& product)
	{
		return (product.m_refP1 ? (product.m_refP1)->z() : DefaultValues::UndefinedFloat);
	});
	// lepton2
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refP2x", [](event_type const& event, product_type const& product)
	{
		return (product.m_refP2 ? (product.m_refP2)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refP2y", [](event_type const& event, product_type const& product)
	{
		return (product.m_refP2 ? (product.m_refP2)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("refP2z", [](event_type const& event, product_type const& product)
	{
		return (product.m_refP2 ? (product.m_refP2)->z() : DefaultValues::UndefinedFloat);
	});

	// track momentum coordinates
	// lepton1
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("track1p4x", [](event_type const& event, product_type const& product)
	{
		return (product.m_track1p4 ? (product.m_track1p4)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("track1p4y", [](event_type const& event, product_type const& product)
	{
		return (product.m_track1p4 ? (product.m_track1p4)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("track1p4z", [](event_type const& event, product_type const& product)
	{
		return (product.m_track1p4 ? (product.m_track1p4)->z() : DefaultValues::UndefinedFloat);
	});
	// lepton2
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("track2p4x", [](event_type const& event, product_type const& product)
	{
		return (product.m_track2p4 ? (product.m_track2p4)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("track2p4y", [](event_type const& event, product_type const& product)
	{
		return (product.m_track2p4 ? (product.m_track2p4)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("track2p4z", [](event_type const& event, product_type const& product)
	{
		return (product.m_track2p4 ? (product.m_track2p4)->z() : DefaultValues::UndefinedFloat);
	});
	
}


void RefitVertexSelectorBase::Produce(event_type const& event, product_type& product,
										setting_type const& settings) const
{
	
	//assert(product.m_ptOrderedLeptons.size() > 0);
	assert(product.m_flavourOrderedLeptons.size() > 0);

	// save thePV and the BS
	product.m_thePV = &event.m_vertexSummary->pv;
	product.m_theBS = &event.m_beamSpot->position;

	// create hashes from lepton selection
	std::vector<KLepton*> leptons = product.m_flavourOrderedLeptons;
	std::vector<size_t> hashes;

	// get reference point of the track
	product.m_refP1 = &((leptons[0])->track.ref);
	product.m_refP2 = &((leptons[1])->track.ref);

	// get momentum of the track
	product.m_track1p4 = &((leptons[0])->track.p4);
	product.m_track2p4 = &((leptons[1])->track.p4);


	if (leptons.size() == 2 && event.m_refitVertices && event.m_refitBSVertices){
		
		size_t hash = 0;

		for (auto lepton : leptons){
			boost::hash_combine(hash, lepton->internalId);
		} // for over leptons
		hashes.push_back(hash);

		std::swap(leptons[0], leptons[1]);
		hash = 0;
		for (auto lepton : leptons){
			boost::hash_combine(hash, lepton->internalId);
		}
		hashes.push_back(hash);

	} // if leptons.size==2


	// find the vertex among the refitted vertices
	//bool foundRefitPV = false;

	for (std::vector<KRefitVertex>::iterator vertex = event.m_refitVertices->begin(); vertex != event.m_refitVertices->end(); ++vertex){
		if ( std::find(hashes.begin(), hashes.end(), vertex->leptonSelectionHash) != hashes.end() ){
			product.m_refitPV = &(*vertex);
			//foundRefitPV = true;
			break;
		}
	} // loop over refitted vertices collection


	// find the vertex among the refitted vertices calculated w/ beamspot constraint
	//bool foundRefitBSPV = false;

	for (std::vector<KRefitVertex>::iterator vertex = event.m_refitBSVertices->begin(); vertex != event.m_refitBSVertices->end(); ++vertex){
		if ( std::find(hashes.begin(), hashes.end(), vertex->leptonSelectionHash) != hashes.end() ){
			product.m_refitBSPV = &(*vertex);
			//foundRefitBSPV = true;
			break;
		}

	} // loop over refitted vertices collection



}


std::string RefitVertexSelector::GetProducerId() const
{
	return "RefitVertexSelector";
}


void RefitVertexSelector::Init(setting_type const& settings)
{
	RefitVertexSelectorBase::Init(settings);
}


void RefitVertexSelector::Produce(event_type const& event, product_type& product,
									setting_type const& settings) const
{
	RefitVertexSelectorBase::Produce(event, product, settings);
}

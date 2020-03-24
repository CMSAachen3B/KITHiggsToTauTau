
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/HttObjectsCutFilters.h"

std::string MetLowerPtCutsFilter::GetFilterId() const {
	return "MetLowerPtCutsFilter";
}

void MetLowerPtCutsFilter::Init(HttSettings const& settings) {
	CutRangeFilterBase<HttTypes>::Init(settings);

	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
		[this](HttEvent const& event, HttProduct const& product, HttSettings const& settings) -> double {
			return (product.m_met.p4.Pt());
			},
			CutRange::LowerThresholdCut(settings.GetMetLowerPtCuts())
		));
}


std::string MetUpperPtCutsFilter::GetFilterId() const {
	return "MetUpperPtCutsFilter";
}

void MetUpperPtCutsFilter::Init(HttSettings const& settings) {
	CutRangeFilterBase<HttTypes>::Init(settings);

	this->m_cuts.push_back(std::pair<double_extractor_lambda, CutRange>(
		[this](HttEvent const& event, HttProduct const& product, HttSettings const& settings) -> double {
			return (product.m_met.p4.Pt());
			},
			CutRange::UpperThresholdCut(settings.GetMetUpperPtCuts())
		));
}

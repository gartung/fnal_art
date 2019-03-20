////////////////////////////////////////////////////////////////////////
/// \file AnalysisDrawingOptions_service.cc
///
/// \author  brebel@fnal.gov

// Framework includes

/// LArSoft includes
#include "lareventdisplay/EventDisplay/AnalysisDrawingOptions.h"

#include <iostream>

namespace evd {

  //......................................................................
  AnalysisDrawingOptions::AnalysisDrawingOptions(fhicl::ParameterSet const& pset, 
					 art::ActivityRegistry& /* reg */) 
  : evdb::Reconfigurable{pset}
  {
    this->reconfigure(pset);
  }
  
  //......................................................................
  AnalysisDrawingOptions::~AnalysisDrawingOptions() 
  {
  }

  //......................................................................
  void AnalysisDrawingOptions::reconfigure(fhicl::ParameterSet const& pset)
  {
    fDrawCalorimetry           = pset.get< int >("DrawCalorimetry"        );
    fDrawParticleID    	       = pset.get< int >("DrawParticleID"   	  );
    fDrawShowerCalor           = pset.get< int >("DrawShowerCalor"        );
    fCaloPlane                 = pset.get< int >("CaloPlane"              );
    fCalorimetryLabels         = pset.get< std::vector<std::string> >("CalorimetryModuleLabels" );
    fParticleIDLabels          = pset.get< std::vector<std::string> >("ParticleIDModuleLabels"  );

    fCalorTemplateFileName     = pset.get< std::string >("CalorTemplateFileName"  );
  }
  
}

namespace evd {

  DEFINE_ART_SERVICE(AnalysisDrawingOptions)

} // namespace evd
////////////////////////////////////////////////////////////////////////
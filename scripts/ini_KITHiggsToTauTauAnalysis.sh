#!/bin/bash

# source Artus ini script
source $CMSSW_BASE/src/Artus/Configuration/scripts/ini_ArtusAnalysis.sh

# source Harry ini script
source $CMSSW_BASE/src/Artus/HarryPlotter/scripts/ini_harry_cmssw.sh

# set the environment
export KITHIGGSTOTAUTAUPATH=$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau

# grid-control
export PATH=${CMSSW_BASE}/src/grid-control/:${CMSSW_BASE}/src/grid-control/scripts/:${PATH}

# setup TauSpinner
#cp $KITHIGGSTOTAUTAUPATH/data/tauspinner.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/tauspinner.xml
#scram setup tauspinner


# overwrite artus settings
if [[ `hostname` == *naf* ]]; then
	export ARTUS_WORK_BASE="/nfs/dust/cms/user/${USER}/htautau/artus/"
elif [[ `hostname` == *bms* ]] && [ ${USER} == "wunsch" ]; then
    echo "Hallo stefan auf der bms"
elif [[ `hostname` == *ekp* ]]; then
	STORAGELIST=(b c 8 9) #list of allowed storages ordered by priority (descending)
	for STORAGE in ${STORAGELIST[*]}
		do
			if [ -d /storage/${STORAGE}/${USER} ]; then
				export ARTUS_WORK_BASE="/storage/${STORAGE}/${USER}/htautau/artus/"
				break
			fi
	done
elif [[ `hostname` == *cern* ]]; then
	export ARTUS_WORK_BASE="/afs/cern.ch/work/${USER:0:1}/${USER}/htautau/artus/"
fi

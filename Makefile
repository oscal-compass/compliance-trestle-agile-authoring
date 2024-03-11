# Makefile

# Purpose: create trestle Agile Authoring GIT Repo's

DIR_TMP = /tmp/download/compliance-trestle/scratch-area

DIR_CAT = $(DIR_TMP)/catalog/NIST_SP-800-53_rev5
DIR_PRO = $(DIR_TMP)/profile/NIST_SP-800-53_rev5
DIR_COM = $(DIR_TMP)/component-definition/data

all: fetch create

all-new: clean delete fetch create

info:
	echo "specify: < all | create | delete | fetch | help >"
	
help:
	python python/agau_repo_setup.py --help
	
create: fetch
	python python/agau_repo_setup.py --action create --config agau-repo-setup.yaml

create-debug: fetch
	python python/agau_repo_setup.py --action create --config agau-repo-setup.yaml --debug
	
delete:
	python python/agau_repo_setup.py --action delete --config agau-repo-setup.yaml
	
delete-debug:
	python python/agau_repo_setup.py --action delete --config agau-repo-setup.yaml

fetch: catalog profile component-definition

clean:
	rm -fr $(DIR_CAT); \
	rm -fr $(DIR_PRO); \
	rm -fr $(DIR_COM); \

catalog:
	if [ ! -d "$(DIR_CAT)" ]; then \
		mkdir -p $(DIR_CAT); \
		cd $(DIR_CAT); \
		wget https://raw.githubusercontent.com/usnistgov/oscal-content/release-v1.0.5-update/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json; \
	fi \
	
profile:
	if [ ! -d "$(DIR_PRO)" ]; then \
		mkdir -p $(DIR_PRO); \
		cd $(DIR_PRO); \
		wget https://raw.githubusercontent.com/usnistgov/oscal-content/release-v1.0.5-update/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_HIGH-baseline_profile.json; \
	fi \
	
component-definition:
	if [ ! -d "$(DIR_COM)" ]; then \
		mkdir -p $(DIR_COM); \
		cd $(DIR_COM); \
		wget https://raw.githubusercontent.com/oscal-compass/compliance-trestle-agile-authoring/main/data/acme-component-definition.csv; \
		wget https://raw.githubusercontent.com/oscal-compass/compliance-trestle-agile-authoring/main/data/acme-component-definition.config; \
	fi \

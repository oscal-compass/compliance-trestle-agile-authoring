## compliance-trestle-agile-authoring

Note: This repo is currently a `Work-In-Progress`...

##### 1. Overview: agile authoring for compliance-trestle

Compliance-[trestle](https://github.com/IBM/compliance-trestle)
supports agile authoring of 
[OSCAL](https://pages.nist.gov/OSCAL/) 
artifacts such as 
[catalogs](https://pages.nist.gov/OSCAL/reference/latest/catalog/json-outline/), 
[profiles](https://pages.nist.gov/OSCAL/reference/latest/profile/json-outline/),
[component definitions](https://pages.nist.gov/OSCAL/reference/latest/component-definition/json-outline/),
and
[mapping collections](https://pages.nist.gov/OSCAL/reference/develop/mapping/json-outline/)
which can be managed in a GIT repo with all the associated built-in desirable features including release management, semantic versioning, access control etc.

Beneficially, markdown snippets are automatically supported which facilitates management of large OSCAL documents in more manageable pieces that are understandable by compliance-oriented personnel.
Distribution of modified artifacts to dependent repos is configurable.

##### 2. GIT repo templates

A collection of agile authoring templates are provided, each pre-populated with the scripts and
configurations needed to support agile authoring.

You can create repo(s) to support the artifact(s) you desire by instantiating each from the template type desired and performing some minimal customization.

Tutorials and templates are provided to set up agile authoring for each of the following:

`Template links`

- [catalog](https://github.com/IBM/compliance-trestle-template-catalog)
- profile
- component definition
- mapping collection

Description & Links: TBD

##### 3. GIT repo - one time setup

![onetime-setup](./drawio/onetime-setup.drawio.png)

Description: TBD

##### 3a. GIT repo - catalog

Description: TBD

##### 4. GIT repo - documents lifecycle

Diagram: TBD

Description: TBD

##### 5. References

- [Compliance Automated Standard Solution (COMPASS), Part 3: Artifacts and Personas](https://dzone.com/articles/compliance-automated-standard-solution-compass-part-3-artifacts-and-personas)
- [Trestle: Compliance-as-Code Orchestrator and Automation Workflows](https://csrc.nist.gov/csrc/media/Presentations/2022/oscal-mini-workshop-2-ibm-s-trestle/IBM_Trestle.pdf)
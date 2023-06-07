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

Create repo(s) to support the artifact(s) you desire by instantiating each from the template type desired and performing some minimal customization.

Tutorials and templates are provided to set up agile authoring for each of the following: catalog, profile, component-definition and mapping-collection.

###### Template links

- [catalog](https://github.com/IBM/compliance-trestle-template-catalog)
- profile
- component-definition
- mapping-collection

##### 3. GIT repo - one time setup

![onetime-setup](./drawio/onetime-setup.drawio.png)

Described below is how to create agile authoring repos from templates.
A template repo is use to create a ready-to-configure repo which is then customized.

##### Prerequisites

- A GitHub token with `workflow` checked has been created

Create (or use existing) token. 
Browser navigate [here](https://github.com/settings/tokens).

<details>
<summary>token creation</summary>
<img src="images/token-create.png" width="500" height="600">
</details>

##### GIT repo - catalog

Create your `catalog` repo from the agile authoring template.

Follow the instructions for [creating-a-repository-from-a-template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template) to create a new repository from template.

Use the [compliance-trestle-template-catalog](https://github.com/IBM/compliance-trestle-template-catalog) as your template.

Choose a repo name and description, for example:
- Repository name `trestle-catalog-nist-800-53-rev5`
- Description `trestle-catalog-nist-800-53-rev5`

###### Customize the catalog repo settings

Install token (from prereqs above) in your newly created `trestle-catalog-nist-800-53-rev5` repo.

Navigate to the newly created `trestle-catalog-nist-800-53-rev5` repo, then use path:

*Settings -> Secrets and variables -> Actions -> New repository secret*

Add repository secret name GIT_TOKEN with token value.

*-> Add secret*

<details>
<summary>token add to repo</summary>
<img src="images/token-catalog.png" width="500" height="600">
</details>

###### Add catalog to repo

- Download the NIST 800-53 Rev 5 catalog to your workstation (laptop)

```
$ mkdir -p download/NIST_SP-800-53_rev5
$ cd download/NIST_SP-800-53_rev5
$ wget https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json
$ mv NIST_SP-800-53_rev5_catalog.json catalog.json
```

- Put the NIST 800-53 Rev 5 catalog into your repo by dragging folder `NIST_SP-800-53_rev5/catalog.json` to the repo in the browser.

<details>
<summary>add catalog</summary>
<img src="images/add-catalog.png" width="500" height="600">
</details>

*-> Commit changes*

###### customize the automation scripts

TBD 

###### install the initial OSCAL catalog (in json format)

The catalog repo is now ready for agile authoring!


##### GIT repo - profile

TBD

##### GIT repo - component-definition

TBD

##### GIT repo - mapping-collection

TBD

##### 4. GIT repo - documents lifecycle

Diagram: TBD

Description: TBD

##### 5. References

- [Compliance Automated Standard Solution (COMPASS), Part 3: Artifacts and Personas](https://dzone.com/articles/compliance-automated-standard-solution-compass-part-3-artifacts-and-personas)
- [Trestle: Compliance-as-Code Orchestrator and Automation Workflows](https://csrc.nist.gov/csrc/media/Presentations/2022/oscal-mini-workshop-2-ibm-s-trestle/IBM_Trestle.pdf)
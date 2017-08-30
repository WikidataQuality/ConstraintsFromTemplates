# ConstraintsFromTemplates [![Build Status](https://travis-ci.org/WikidataQuality/ConstraintsFromTemplates.svg?branch=master)](https://travis-ci.org/WikidataQuality/ConstraintsFromTemplates) [![Coverage Status](https://coveralls.io/repos/WikidataQuality/ConstraintsFromTemplates/badge.svg)](https://coveralls.io/r/WikidataQuality/ConstraintsFromTemplates) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/WikidataQuality/ConstraintsFromTemplates/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/WikidataQuality/ConstraintsFromTemplates/?branch=master)
Parses the property talk pages of Wikidata to extract the constraints and initially fill the constraints table for the WikibaseQualityConstraints extension.

## Obsolescence Notice

**This repository is obsolete.**
Since July 2017, constraints are defined in statements on properties,
not in templates on property talk pages
(see [T169647]),
and since August of the same year,
the WikibaseQualityConstraints extension no longer supports constraint definitions
that were formerly imported from templates
(see [T171291]).
The repository is kept for historic interest only.

[T169647]: https://phabricator.wikimedia.org/T169647
[T171291]: https://phabricator.wikimedia.org/T171291

## Installation
```
git clone https://github.com/WikidataQuality/ConstraintsFromTemplates.git
cd ConstraintsFromTemplates
pip install -r requirements.txt
```

## Usage
`python csvScriptBuilder.py`

### Running the tests
```
py.test
```

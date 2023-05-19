# netto

[![Documentation Status](https://readthedocs.org/projects/netto/badge/?version=latest)](https://netto.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://img.shields.io/pypi/v/netto.svg)](https://pypi.python.org/pypi/netto)
[![CI](https://github.com/0-k/netto/actions/workflows/workflow.yml/badge.svg)](https://github.com/0-k/netto/actions/workflows/workflow.yml)
[![codecov](https://codecov.io/gh/0-k/netto/branch/master/graph/badge.svg)](https://codecov.io/gh/0-k/netto)
[![License](https://img.shields.io/pypi/l/netto.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

German income tax (Einkommensteuer) and social security (Sozialabgaben) calculator.

Currently tested against the following assumptions:
* Public health and pension insurance
* West-German pension deduction
* Optional: Church tax
* Optional: Married 
* Supported tax years: 2018-2024

### TODO list

* Calculate support for children (Kindergeld/Kinderfreibetrag)
* Implement correct pension deductible for East Germany

## Sources

* [German tax curve](https://www.bmf-steuerrechner.de/Tarifhistorie_Steuerrechner.pdf?__blob=publicationFile&v=1)
* [Wage tax (Lohnsteuer)](https://www.bmf-steuerrechner.de/bl/bl2022/eingabeformbl2022.xhtml)
* [Social security deductable (Vorsorgepauschale)](https://www.lohn-info.de/vorsorgepauschale.html)
* [Social security rates](https://www.lohn-info.de/sozialversicherungsbeitraege2022.html)
* [Taxable income calculator](https://udo-brechtel.de/mathe/est_gsv/reverse_zve_brutto.htm)
* [Solidarity tax (Solidaritätszuschlag)](https://www.lohn-info.de/solizuschlag.html)

## Credits

Martin Klein, 2023

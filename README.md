# netto

German income tax (Einkommensteuer) and social security (Sozialabgaben) calculator.

Currently tested against the following assumptions:
* Tax class I/IV
* Public health and pension insurance
* West-German pension deduction
* Optional: Church tax
* Supported tax years: 2018-2023

### TODO list

* Implement tax class II & III/V
* Calculate support for children (Kindergeld/Kinderfreibetrag)
* Implement fields for private health insurance
* Implement fields for private pension insurance
* Implement correct pension deductible for East Germany
* Convenience function to calculate church tax (by state)

## Sources

* [German tax curve](https://www.bmf-steuerrechner.de/Tarifhistorie_Steuerrechner.pdf?__blob=publicationFile&v=1)
* [Wage tax (Lohnsteuer)](https://www.bmf-steuerrechner.de/bl/bl2022/eingabeformbl2022.xhtml)
* [Social security deductable (Vorsorgepauschale)](https://www.lohn-info.de/vorsorgepauschale.html)
* [Social security rates](https://www.lohn-info.de/sozialversicherungsbeitraege2022.html)
* [Taxable income calculator](https://udo-brechtel.de/mathe/est_gsv/reverse_zve_brutto.htm)
* [Solidarity tax (Solidaritätszuschlag)](https://www.lohn-info.de/solizuschlag.html)

## Credits

Martin Klein, 2022

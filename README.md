# scoreLattes
Computes scores from Lattes curricula.

# Usage
scoreLattes.py [-h] [-v] [--version] [-p YYYY] [-s YYYY] [-u YYYY]
                      AREA FILE

positional arguments:
  AREA                  specify Qualis Periodicos area
  FILE                  XML file containing a Lattes curriculum

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         explain what is being done
  --version             show program's version number and exit
  -p YYYY, --qualis-periodicos YYYY
                        employ Qualis Periodicos from year YYYY
  -s YYYY, --since-year YYYY
                        consider academic productivity since year YYYY
  -u YYYY, --until-year YYYY
                        consider academic productivity until year YYYY

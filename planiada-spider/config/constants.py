from robobrowser import RoboBrowser
import requests

counties = [ "dolj", "bacau", "harghita", "bistrita-nasaud", "dambovita", "suceava", "botosani",
    "brasov", "bucuresti", "braila", "hunedoara", "teleorman", "covasna", "tulcea", "timis", "buzau", "prahova"
    "ilfov", "neamt", "cluj", "alba", "giurgiu", "arges", "calarasi", "bihor", "iasi", "valcea"
    "vrancea", "arad", "ialomita", "caras-severin", "galati", "gorj", "constanta", "satu-mare", "maramures"
    "mehedinti", "salaj", "vaslui", "mures", "sibiu", "olt" ]

db_cities_path = "databases/db_cities.sqlite"
db_output_path = "databases/db_output.sqlite"
pln_county_url = "https://planiada.ro/destinatii/"
pln_base = "https://planiada.ro"

'''
    Debug 1 -> Foarte sensibil, latra la orice
    Debug 2 -> Mai finut
    Debug 3 -> Rezumat
'''
debug = 3
defaultStream = "console" # console / file

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0'
browser = RoboBrowser(parser="html5lib", session=session)
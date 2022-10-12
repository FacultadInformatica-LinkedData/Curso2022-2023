from model.graph_loader import graph, SCHEMA, XSD, EC, RDFS, TIME, SSN
from rdflib.plugins.sparql import prepareQuery
from datetime import datetime

g = graph
c_building_inf = dict()
c_years = list()
c_months = dict()

def get_buildings_inf():

    global c_building_inf

    buildings = set()
    building_type = set()
    neighborhood = set()
    district = set()


    query = """
        SELECT DISTINCT ?building_id ?building_name ?structure_type ?structure_neighborhood ?structure_district ?latitude ?longitude
        WHERE 
        {
            ?building_id a schema:CivicStructure ;
                rdfs:label ?building_name ;
                schema:geo ?structure_geo ;
                ec:buildingType ?structure_type ;
                ec:district ?structure_district ;
                ec:neighborhood ?structure_neighborhood .
            
            ?structure_geo a schema:GeoCoordinates ;
                schema:latitude ?latitude ;
                schema:longitude ?longitude .
        }
    """
    result = exec_query(query, {"schema": SCHEMA, "xsd": XSD, "ec": EC, "rdfs":RDFS})

    for row in result:
        buildings.add(row.building_name.value)
        building_type.add(row.structure_type.value)
        neighborhood.add(row.structure_neighborhood.value)
        district.add(row.structure_district.value)

        # Building info cache
        c_building_inf[str(row.building_id)] = {
            "location": (row.latitude.value, row.longitude.value),
            "name":row.building_name.value,
            "type": row.structure_type.value,
            "neighborhood": row.structure_neighborhood.value,
            "district": row.structure_district.value
        }

    buildings = list(buildings)
    buildings.sort()

    building_type = list(building_type)
    building_type.sort()

    neighborhood = list(neighborhood)
    neighborhood.sort()

    district = list(district)
    district.sort()

    return buildings, building_type, neighborhood, district

def get_years_months():

    global c_years, c_months
    c_years = list()
    c_months = dict()
    years = set()
    months = dict()

    query = """
        SELECT DISTINCT (year(?date) as ?year) (month(?date) as ?month)
        WHERE 
        {
            ?ob_id a ssn:Observation ;
                time:inXSDDate ?date .
        }
    """

    result = exec_query(query, {"ssn": SSN, "time":TIME})
    for row in result:
        year, month =row.year.value, row.month.value
        date = datetime(year, month, 1)
        years.add(date.strftime("%Y"))
        months[date.strftime("%B")] = month
    
    c_months = {str_:f"{value:01}"for str_, value in months.items()}
    c_years = list(years)
    return list(years), sorted(list(months.keys()), key=lambda x: months[x])

def get_latest_observations():
    year = datetime.now().strftime("%Y") 
    return observation_lookup({"year": year,})

def observation_lookup(conditions: dict) -> list:

    latest_obs = dict()
    query = """
        SELECT DISTINCT ?ob_id ?building_id ?ob_unit_text ?ob_value ?ob_ec_energy_group ?ob_ec_type_of_energy (year(?date) as ?year) (month(?date) as ?month) 
        {
            ?ob_id a ssn:Observation ;
                time:inXSDDate ?date ;
                ssn:featureOfInterest ?building_id ;
                schema:unitText ?ob_unit_text ;
                schema:value ?ob_value .
                OPTIONAL{
                    ?ob_id ec:energyGroup ?ob_ec_energy_group ;
                        ec:typeOfEnergy ?ob_ec_type_of_energy .
                }
            ?building_id a schema:CivicStructure ;
                rdfs:label ?building_name ;
                schema:geo ?structure_geo ;
                ec:buildingType ?structure_type ;
                ec:district ?structure_district ;
                ec:neighborhood ?structure_neighborhood .
                
        """+ build_filters(conditions) +"""
        } ORDER BY DESC(?date) 
    """

    # TODO: Clean the output
    result = exec_query(query, {"ssn": SSN, "time":TIME, "xsd": XSD, "schema": SCHEMA, "xsd": XSD, "ec": EC, "rdfs":RDFS})
    
    for row in result:
        # Get latest observations for each building.
        building_id = str(row.building_id)
        
        if building_id not in latest_obs.keys():
            latest_obs[building_id] = {
                "building": str(row.building_id),
                "year": row.year.value,
                "month": datetime(1998, row.month.value, 1).strftime("%B"),
                "units": row.ob_unit_text.value,
                "value": row.ob_value.value,
                "group": row.ob_ec_energy_group.value if row.ob_ec_energy_group is not None else "Not Defined",
                "type": row.ob_ec_type_of_energy.value if row.ob_ec_type_of_energy is not None else "Not Defined"
            }
    
    return latest_obs

def build_filters(conditions):
    
    filter_pattern = "FILTER(contains(xsd:string({}),xsd:string({}))) .\n"
    filters = []

    if len(c_months)==0:
        get_years_months()

    if "building_name" in conditions:
        filters.append(filter_pattern.format("?building_name", "\""+ conditions["building_name"] + "\""))
        
    if "building_type" in conditions:
        filters.append(filter_pattern.format("?structure_type", "\""+ conditions["building_type"] + "\""))

    if "district" in conditions:
        filters.append(filter_pattern.format("?structure_district", "\"" + conditions["district"] + "\""))

    if "neighborhood" in conditions:
        filters.append(filter_pattern.format("?structure_neighborhood", "\"" + conditions["neighborhood"] + "\""))
    
    if "year"  in conditions and "month" in conditions:
        year = conditions["year"]
        month = c_months[conditions["month"]]
        filters.append("FILTER(?date = {})".format(f"\"{year}-{month}-01\"^^xsd:date"))

    elif "year" in conditions:
        filters.append(filter_pattern.format("year(?date)", conditions["year"] ))

    elif "month" in conditions:
        filters.append(filter_pattern.format("month(?date)", c_months[conditions["month"]]))

    return "\n".join(filters)

def exec_query(query: str, nss: dict) -> list:
    return [res for res in g.query(prepareQuery(query, initNs=nss))]

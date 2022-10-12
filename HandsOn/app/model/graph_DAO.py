
from graph_loader import graph, SCHEMA, XSD, EC, RDFS
from rdflib.plugins.sparql import prepareQuery

g = graph

def get_buildings_inf():
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
    # TODO: Clean the output

    result = exec_query(exec_query)
    buildings = []
    building_type = []
    neighborhood = []
    district = []
    long_lat = {}
    for row in result:
        buildings.append(row.building_name.value)
        long_lat[row.building_id.value] = (row.latitude.value, row.longitude.value)

    print(buildings)
    print(long_lat)
    return None

def get_years_months():
    query = """
        SELECT DISTINCT ?building_name ?structure_type ?structure_neighborhood ?structure_district ?latitude ?longitude
        WHERE 
        {
            ?name a schema:CivicStructure ;
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

def get_latest_observations():
    query = """
        SELECT DISTINCT ?building_name ?structure_type ?structure_neighborhood ?structure_district ?latitude ?longitude
        WHERE 
        {
            ?name a schema:CivicStructure ;
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

def _div_years_months():
    pass

def search_observation(conditions: dict) -> list:

    query = """
        SELECT ?civicStructures ?name
        WHERE 
        {
            ?civicStructures a schema:CivicStructure ;
                rdfs:label ?name ;
                schema:address ?structure_address ;
                schema:geo ?structure_geo ;
                ec:buildingType ?structure_type ;
                ec:district ?structure_district ;
                ec:neighborhood ?structure_neighborhood .
            
            ?structure_geo a schema:GeoCoordinates .
        }
    """
    # TODO: Clean the output
    return exec_query(exec_query)

def exec_query(query: str) -> list:

    q1 = prepareQuery(query, 
                initNs={"schema": SCHEMA, "xsd": XSD, "ec": EC, "rdfs":RDFS}
        )

    res_list = []
    for res in g.query(q1):
        res_list.append(res)

    return res_list


get_buildings_inf()
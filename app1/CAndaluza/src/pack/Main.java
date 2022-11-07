package pack;

import java.io.InputStream;

import org.apache.jena.query.Query;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.QuerySolution;
import org.apache.jena.query.ResultSet;
import org.apache.jena.rdf.model.Literal;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.RDFNode;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.util.FileManager;
import java.util.Scanner;

public class Main {
 public static void main (String []args) {
	 boolean flag = true;	
	 while (flag) {

     	System.out.println(""
     			+ "--------------------------------------------------------------------------"
     			+ "\n|            \r\n"
     			+ "▒█▀▀█ █░░█ █░░ ▀▀█▀▀ █░░█ █▀▀█ █▀▀█ 　 ░█▀▀█ █▀▀▄ █▀▀▄ █▀▀█ █░░ █░░█ ▀▀█ █▀▀█ \r\n"       
     			+ "▒█░░░ █░░█ █░░ ░░█░░ █░░█ █▄▄▀ █▄▄█ 　 ▒█▄▄█ █░░█ █░░█ █▄▄█ █░░ █░░█ ▄▀░ █▄▄█ \r\n"
     			+ "▒█▄▄█ ░▀▀▀ ▀▀▀ ░░▀░░ ░▀▀▀ ▀░▀▀ ▀░░▀ 　 ▒█░▒█ ▀░░▀ ▀▀▀░ ▀░░▀ ▀▀▀ ░▀▀▀ ▀▀▀ ▀░░▀ \r\n"
     			+ "\r\n"
     			+ "▒█▀▀▀█ █▀▀ █▀▄▀█ █▀▀█ █▀▀▄ ▀▀█▀▀ ▀█▀ █▀▀ 　 █░░░█ ▒█▀▀▀ █▀▀▄ \r\n"
     			+ "░▀▀▀▄▄ █▀▀ █░▀░█ █▄▄█ █░░█ ░░█░░ ▒█░ █░░ 　 █▄█▄█ ▒█▀▀▀ █▀▀▄ \r\n"
     			+ "▒█▄▄▄█ ▀▀▀ ▀░░░▀ ▀░░▀ ▀░░▀ ░░▀░░ ▄█▄ ▀▀▀ 　 ░▀░▀░ ▒█▄▄▄ ▀▀▀░                            |"
     			+ "\n|                                                                                      |"
     			+ "\n|    SELECCIONE LA OPCIÓN QUE DESEE VISUALIZAR   :                                     |"
     			+ "\n|                                                                                      |"
     			+ "\n| 0. Salir.                                                                            |"
     			+ "\n| 1. Contáctanos                                                                       |"
     			+ "\n| 2. Ver lista de todos los museos                                                     |"
     			+ "\n| 3. Ver lista de todos los lugares de interés                                         |"
     			+ "\n| 4. Ver Lugares de interes enlazados                                                  |"
     			+ "\n| 5. Ver Direcciones de los museos                                                     |"
     			+ "\n| 6. Query federada				                                       |"
     			+ "\n| 7. Ver museos cuyo número de teléfono empieza por un prefijo indicado                |"
     			+ "\n"
     			+ "--------------------------------------------------------------------------");
	 
     	Scanner sc = new Scanner(System.in);  
    	String opcion = sc.nextLine();
    	Scanner dato = new Scanner(System.in);
    	switch (opcion) {
    	//------------------------SALIR------------------------
    	case "0":
    		flag=false;
    		System.out.println("\n¡¡¡ GRACIAS POR USAR NUESTRA APLICACION !!!");
    		break;
    	case "1":
    		System.out.println("DEVELOPER         --> david.pedraza.caro@alumnos.upm.es");
    		System.out.println("CUSTOMER SUPPORT  --> eduardo.hernandez.paradinas@alumnos.upm.es");
    		System.out.println("-----------------------------------------------------");
    		System.out.println("-----------------------------------------------------");
    		System.out.println("Escuela Técnica Superior de Ingenieros Informaticos");
    		System.out.println("Universidad Politecnica de Madrid");
    		break;
    	//------------------------VER LISTA DE MUSEOS------------------------
    	case "2":
    		String filename = "museos-updated-withlinks.ttl";
    		Model model = ModelFactory.createDefaultModel();
    		InputStream in = FileManager.get().open(filename);
    		if (in == null) throw new IllegalArgumentException("File not found");
    		model.read(in, null, "TTL");
    		//WSQuery queries = new WSQuery();
    		String query = ("prefix dbp: <http://dbpedia.org/property/>" + " SELECT ?FullName WHERE { ?Subject dbp:fullname ?FullName.}");
    		Query queryE = QueryFactory.create(query);
    		QueryExecution qexec = QueryExecutionFactory.create(queryE, model);
    		ResultSet results = qexec.execSelect();
    		System.out.println(results.toString());
    		while (results.hasNext())
    		{
    			QuerySolution binding = results.nextSolution();
    			Literal texto = binding.getLiteral("FullName");
    			System.out.println(texto);
    		}
    		System.out.println("\nFinalizado con exito.");
    		break;
    	//------------------------VER LISTA DE LUGARES DE INTERES ------------------------
    	case "3":
    		String filename1 = "lugares-interes-updated-v2-withlinks.ttl";
    		Model model1 = ModelFactory.createDefaultModel();
    		InputStream in1 = FileManager.get().open(filename1);
    		if (in1 == null) throw new IllegalArgumentException("File not found");
    		model1.read(in1, null, "TTL");
    		//WSQuery queries1 = new WSQuery();
    		String query1 = ("prefix dbp: <http://dbpedia.org/property/>" + " SELECT ?FullName WHERE { ?Subject dbp:fullname ?FullName.}");
    		Query queryE1 = QueryFactory.create(query1);
    		QueryExecution qexec1 = QueryExecutionFactory.create(queryE1, model1);
    		ResultSet results1 = qexec1.execSelect();
    		System.out.println(results1.toString());
    		while (results1.hasNext()){
    			QuerySolution binding = results1.nextSolution();
    			Literal texto = binding.getLiteral("FullName");
    			System.out.println(texto);
    		}
    		System.out.println("\nFinalizado con exito.");
    		break;
    	//------------------------VER LUGARES DE INTERES ENLAZADOS------------------------
    	case "4":
    		String filename2 = "lugares-interes-updated-v2-withlinks.ttl";
    		Model model2 = ModelFactory.createDefaultModel();
    		InputStream in2 = FileManager.get().open(filename2);
    		if (in2 == null) throw new IllegalArgumentException("File not found");
    		model2.read(in2, null, "TTL");
    		//WSQuery queries2 = new WSQuery();
    		String query2 = ("prefix owl: <http://www.w3.org/2002/07/owl#>" + " SELECT ?FullName ?obj WHERE { ?FullName owl:sameAs ?obj.}");
    		Query queryE2 = QueryFactory.create(query2);
    		QueryExecution qexec2 = QueryExecutionFactory.create(queryE2, model2);
    		ResultSet results2 = qexec2.execSelect();
    		System.out.println(results2.toString());
    		while (results2.hasNext())
    		{
    			QuerySolution binding = results2.nextSolution();
    			String sujeto=binding.getResource("FullName").toString();
    			String enlace=binding.getResource("obj").toString();
    			System.out.println(sujeto + "\t"+ enlace);

    		}
    		System.out.println("\nFinalizado con exito.");

    		break;
    	//------------------------VER DIRECCIONES DE LOS MUSEOS------------------------
    	case "5":
    		String filename3 = "museos-updated-withlinks.ttl";
    		Model model3 = ModelFactory.createDefaultModel();
    		InputStream in3 = FileManager.get().open(filename3);
    		if (in3 == null) throw new IllegalArgumentException("File not found");
    		model3.read(in3, null, "TTL");
    		//WSQuery queries3 = new WSQuery();
    		String query3 = ("prefix dbp: <http://dbpedia.org/property/>" + " SELECT ?Fullname ?obj WHERE { ?Fullname dbp:address ?obj }");
    		Query queryE3 = QueryFactory.create(query3);
    		QueryExecution qexec3 = QueryExecutionFactory.create(queryE3, model3);
    		ResultSet results3 = qexec3.execSelect();
    		System.out.println(results3.toString());
    		while (results3.hasNext()){
    			QuerySolution binding = results3.nextSolution();
    			String sujeto=binding.getResource("Fullname").toString();
    			Literal texto = binding.getLiteral("obj");
    			System.out.println(sujeto + "\t"+ texto);
    		}
    		System.out.println("\nFinalizado con exito.");
    		break;
    	//------------------------QUERY FEDERADA PARA OBTENER LAS PROPIEDADES------------------------
    	case "6":
			/*
			 * String filename4 = "museos-updated-withlinks.ttl"; Model model4 =
			 * ModelFactory.createDefaultModel(); InputStream in4 =
			 * FileManager.get().open(filename4); if (in4 == null) throw new
			 * IllegalArgumentException("File not found"); model4.read(in4, null, "TTL");
			 * String query4 =
			 * ("prefix dbp: <http://dbpedia.org/property/>" +
			 * " SELECT ?property ?value WHERE {\r\n" + "  ?sub owl:sameAs ?enlace .\r\n" +
			 * "  SERVICE<https://query.wikidata.org/sparql> {\r\n" +
			 * "    ?enlace ?property ?value .\r\n" + "  }\r\n" + "} "); Query queryE4 =
			 * QueryFactory.create(query4); QueryExecution qexec4 =
			 * QueryExecutionFactory.create(queryE4, model4); ResultSet results4 =
			 * qexec4.execSelect(); System.out.println(results4.toString()); while
			 * (results4.hasNext()){ QuerySolution binding = results4.nextSolution();
			 * Literal texto = binding.getLiteral("obj"); System.out.println(texto); }
			 */
    		System.out.println("\n¡¡LO SENTIMOS!!");
    		System.out.println("\nHa ocurrido algún problema con el Sparql Endpoint.");
    		break;
    	//------------------------VER MUSEOS CUYO TELEFONO TIENE UN PREFIJO CONCRETO------------------------
    	case "7":
    		String filename5 = "museos-updated-withlinks.ttl";
    		Model model5 = ModelFactory.createDefaultModel();
    		InputStream in5 = FileManager.get().open(filename5);
    		if (in5 == null) throw new IllegalArgumentException("File not found");
    		model5.read(in5, null, "TTL");
    		//WSQuery queries5 = new WSQuery();
    		System.out.println("Por favor indique un prefijo de 3 digitos: ");
    		String prefijoindicado = dato.nextLine();
    		String query5 = ("PREFIX dbp: <http://dbpedia.org/property/>\r\n"
    				+ "SELECT ?sub ?obj WHERE {\r\n"
    				+ "  ?sub dbp:phoneNumber ?obj.\r\n"
    				+ "  FILTER(strstarts(str(?obj),"+"'"+ prefijoindicado+"'"+"))\r\n"
    				+ "}");
    		Query queryE5 = QueryFactory.create(query5);
    		QueryExecution qexec5 = QueryExecutionFactory.create(queryE5, model5);
    		ResultSet results5 = qexec5.execSelect();
    		System.out.println(results5.toString());
    		while (results5.hasNext()){
    			QuerySolution binding = results5.nextSolution();
    			String sujeto=binding.getResource("sub").toString();
    			Literal telefono = binding.getLiteral("obj");
    			System.out.println(sujeto + "\t"+ telefono);
    		}
    		System.out.println("\nFinalizado con exito.");
    		break;
    	} 
	 }
   }
}

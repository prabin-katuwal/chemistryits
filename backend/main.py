from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rdflib import Graph
import random


# Initialize FastAPI app
app = FastAPI(title="Basic Periodic Table Learning System")


# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)


ontology_path = "periodic_table_relationship.owl"
g = Graph()
g.parse(ontology_path, format="xml")


@app.get("/elements")
def list_elements():

    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX pt: <http://www.example.org/periodic_table.owl#>

        SELECT ?element ?atomicNumber ?symbol ?atomicMass ?group ?period ?col
        WHERE {
        ?element rdf:type pt:Element .
        OPTIONAL { ?element pt:atomicNumber ?atomicNumber . }
        OPTIONAL { ?element pt:symbol ?symbol . }
        OPTIONAL { ?element pt:atomicMass ?atomicMass . }
        OPTIONAL { ?element pt:group ?group . }
        OPTIONAL { ?element pt:period ?period . }
        OPTIONAL { ?element pt:col ?col . }
        }
    """
    results = g.query(query)
    elements = []
    for element in results:
        elements.append({
            "symbol": element.symbol,
            "atomicNumber": int(element.atomicNumber),
            "group": int(element.group),
            "period": int(element.period),
            "col" : int( element.col),
        })
    return {"elements": elements}




@app.get("/element/{symbol}")
def get_element_by_symbol(symbol: str):
    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX pt: <http://www.example.org/periodic_table.owl#>

        SELECT ?element ?atomicNumber ?symbol ?atomicMass ?group ?period ?col
        WHERE {
        ?element rdf:type pt:Element .
        OPTIONAL { ?element pt:atomicNumber ?atomicNumber . }
        OPTIONAL { ?element pt:symbol ?symbol . }
        OPTIONAL { ?element pt:atomicMass ?atomicMass . }
        OPTIONAL { ?element pt:group ?group . }
        OPTIONAL { ?element pt:period ?period . }
        OPTIONAL { ?element pt:col ?col . }
        }
    """

    result = g.query(query)
    for element in result:
        if str(element.symbol) and str(element.symbol) == symbol:
            return {
                "name": element.element.replace("http://www.example.org/periodic_table.owl#", ""),
                "symbol": element.symbol,
                "atomicNumber": int(element.atomicNumber),
                "atomicMass": float(element.atomicMass),
                "group": int(element.group),
                "period": int(element.period),
            }
        
    raise HTTPException(status_code=404, detail=f"Element with symbol '{symbol}' not found")

@app.get("/quiz")
async def get_random_quiz():
    """
   Generates a random quiz with 10 element symbols and their atomic numbers.
    """
    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX pt: <http://www.example.org/periodic_table.owl#>

        SELECT ?element ?symbol ?atomicNumber
        WHERE {
        ?element rdf:type pt:Element .
        ?element pt:symbol ?symbol .
        OPTIONAL { ?element pt:atomicNumber ?atomicNumber . }
        }
        """

    results = g.query(query)
    elements = [(str(row.symbol), int(row.atomicNumber)) for row in results]

    quiz_questions = []
    for symbol, atomic_number in random.sample(elements, 10):
        correct_answer = atomic_number
        incorrect_answers = [atomic_number - 2, atomic_number + 2]
        random.shuffle(incorrect_answers)
        options = [correct_answer, *incorrect_answers]
        random.shuffle(options)
        quiz_questions.append({
            "symbol": symbol,
            "options": options
        })

    return {"questions": quiz_questions}
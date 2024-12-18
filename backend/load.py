from owlready2 import *

# Create or load the ontology
onto = get_ontology("http://www.example.org/periodic_table.owl")

with onto:
    # Define the Element class
    class Element(Thing):
        pass
    
    # Define the ChemicalBond class
    class ChemicalBond(Thing):
        pass
    
    # Define properties for Element
    class atomicNumber(DataProperty, FunctionalProperty):
        domain = [Element]
        range = [int]

    class symbol(DataProperty, FunctionalProperty):
        domain = [Element]
        range = [str]

    class atomicMass(DataProperty, FunctionalProperty):
        domain = [Element]
        range = [float]

    class group(DataProperty, FunctionalProperty):
        domain = [Element]
        range = [int]

    class period(DataProperty, FunctionalProperty):
        domain = [Element]
        range = [int]
    
    class col(DataProperty, FunctionalProperty):
        domain = [Element]
        range = [int]

    # Define the 'isInSameGroupAs' ObjectProperty
    class isInSameGroupAs(ObjectProperty):
        domain = [Element]
        range = [Element]
        label = "Is in the same group as"

    # Define the 'formsChemicalBondWith' ObjectProperty
    class formsChemicalBondWith(ObjectProperty):
        domain = [ChemicalBond]
        range = [Element]
        label = "Forms Chemical Bond With"

    # Elements data
    elements_data = [
        {"name": "Hydrogen", "symbol": "H", "atomicNumber": 1, "atomicMass": 1.008, "group": 1, "period": 1, "col": 1},
        {"name": "Helium", "symbol": "He", "atomicNumber": 2, "atomicMass": 4.0026, "group": 18, "period": 1, "col": 8},
        {"name": "Lithium", "symbol": "Li", "atomicNumber": 3, "atomicMass": 6.94, "group": 1, "period": 2, "col": 1},
        {"name": "Beryllium", "symbol": "Be", "atomicNumber": 4, "atomicMass": 9.0122, "group": 2, "period": 2, "col": 2},
        {"name": "Boron", "symbol": "B", "atomicNumber": 5, "atomicMass": 10.81, "group": 13, "period": 2, "col": 3},
        {"name": "Carbon", "symbol": "C", "atomicNumber": 6, "atomicMass": 12.011, "group": 14, "period": 2, "col": 4},
        {"name": "Nitrogen", "symbol": "N", "atomicNumber": 7, "atomicMass": 14.007, "group": 15, "period": 2, "col": 5},
        {"name": "Oxygen", "symbol": "O", "atomicNumber": 8, "atomicMass": 15.999, "group": 16, "period": 2, "col": 6},
        {"name": "Fluorine", "symbol": "F", "atomicNumber": 9, "atomicMass": 18.998, "group": 17, "period": 2, "col": 7},
        {"name": "Neon", "symbol": "Ne", "atomicNumber": 10, "atomicMass": 20.180, "group": 18, "period": 2, "col": 8},
        {"name": "Sodium", "symbol": "Na", "atomicNumber": 11, "atomicMass": 22.990, "group": 1, "period": 3, "col": 1},
        {"name": "Magnesium", "symbol": "Mg", "atomicNumber": 12, "atomicMass": 24.305, "group": 2, "period": 3, "col": 2},
        {"name": "Aluminum", "symbol": "Al", "atomicNumber": 13, "atomicMass": 26.982, "group": 13, "period": 3, "col": 3},
        {"name": "Silicon", "symbol": "Si", "atomicNumber": 14, "atomicMass": 28.085, "group": 14, "period": 3, "col": 4},
        {"name": "Phosphorus", "symbol": "P", "atomicNumber": 15, "atomicMass": 30.974, "group": 15, "period": 3, "col": 5},
        {"name": "Sulfur", "symbol": "S", "atomicNumber": 16, "atomicMass": 32.06, "group": 16, "period": 3, "col": 6},
        {"name": "Chlorine", "symbol": "Cl", "atomicNumber": 17, "atomicMass": 35.45, "group": 17, "period": 3, "col": 7},
        {"name": "Argon", "symbol": "Ar", "atomicNumber": 18, "atomicMass": 39.95, "group": 18, "period": 3, "col": 8},
        {"name": "Potassium", "symbol": "K", "atomicNumber": 19, "atomicMass": 39.098, "group": 1, "period": 4, "col": 1},
        {"name": "Calcium", "symbol": "Ca", "atomicNumber": 20, "atomicMass": 40.078, "group": 2, "period": 4, "col": 2},
    ]

    # Create element instances dynamically
    element_instances = {}
    for element in elements_data:
        element_instance = Element(element["name"])  # Create an instance for each element
        element_instance.atomicNumber = element['atomicNumber']
        element_instance.symbol = element["symbol"]
        element_instance.atomicMass = element['atomicMass']
        element_instance.group = element['group']
        element_instance.period = element['period']
        element_instance.col = element['col']
        
        # Save the element instance for later use (if needed)
        element_instances[element["name"]] = element_instance

    # Example: Create a chemical bond between Hydrogen and Oxygen
    hydrogen = element_instances["Hydrogen"]
    oxygen = element_instances["Oxygen"]

    # Create the bond instance
    bond_hydrogen_oxygen = ChemicalBond("Bond_Hydrogen_Oxygen")
    
    # Link the bond to the elements (formsChemicalBondWith)
    bond_hydrogen_oxygen.formsChemicalBondWith = [hydrogen, oxygen]

    # Save the ontology to a file
    onto.save(file="periodic_table_relationship.owl", format="rdfxml")

# Optionally, print out element details and chemical bonds
for element in onto.Element.instances():
    print(f"{element.name}: Atomic Number = {element.atomicNumber}, Symbol = {element.symbol}, Atomic Mass = {element.atomicMass}")

for bond in onto.ChemicalBond.instances():
    print(f"{bond.name} forms chemical bonds with:")
    for related_element in bond.formsChemicalBondWith:
        print(f" - {related_element.name}")

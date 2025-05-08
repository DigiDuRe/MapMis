#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from rdflib import Graph, Namespace, RDF, RDFS, Literal

# Define namespaces (using our own "ex" namespace for our example data)
EX = Namespace("http://example.org/")

# Read the three CSV files (adjust filenames as needed)
# CSV file 1: persons data with columns: "nama orang", "geb/overl.", "id"
df_person = pd.read_csv("/Volumes/Extreme SSD/Python_Projects/NIAA Project/FINAL_PARSED_DATA/bio_data.csv")

# CSV file 2: work records with columns: "organ.", "werkgebied en -soort", "werkperiode", "bijzonderheden", "id"
df_work = pd.read_csv("/Volumes/Extreme SSD/Python_Projects/NIAA Project/FINAL_PARSED_DATA/events_data.csv")

# CSV file 3: spouse data with columns: "spouse", "id"
df_spouse = pd.read_csv("/Volumes/Extreme SSD/Python_Projects/NIAA Project/FINAL_PARSED_DATA/spouse_data.csv")

# Create an RDF graph and bind the example namespace
g = Graph()
g.bind("ex", EX)

# Define our basic classes for our RDF Schema
Person = EX.Person
Work   = EX.Work
Spouse = EX.Spouse

# Declare our classes in the graph (using RDFS)
g.add((Person, RDF.type, RDFS.Class))
g.add((Work, RDF.type, RDFS.Class))
g.add((Spouse, RDF.type, RDFS.Class))

# Define some properties to link our data (you can extend these as needed)
hasName          = EX.hasName
hasGebOverl      = EX.hasGebOverl      # For birth/death info
hasWork          = EX.hasWork          # Links a Person to a Work record
hasOrgan         = EX.hasOrgan
hasWerkgebied    = EX.hasWerkgebied    # For work area and type
hasWerkperiode   = EX.hasWerkperiode
hasBijzonderheden= EX.hasBijzonderheden
hasSpouse        = EX.hasSpouse        # Links a Person to a Spouse record
spouseInfo       = EX.spouseInfo       # Literal info about spouse

# Process the persons CSV: create a URI for each person and add basic properties
for idx, row in df_person.iterrows():
    person_id = row['id']
    person_uri = EX[f"person/{person_id}"]
    g.add((person_uri, RDF.type, Person))
    g.add((person_uri, hasName, Literal(row['nama orang'])))
    g.add((person_uri, hasGebOverl, Literal(row['geb/overl.'])))

# Process the work CSV: create a work resource for each record and link it to the corresponding person via the "id" column.
for idx, row in df_work.iterrows():
    # Construct a unique URI for the work record (combining id and row index in case of multiple records per person)
    work_uri = EX[f"work/{row['id']}_{idx}"]
    g.add((work_uri, RDF.type, Work))
    g.add((work_uri, hasOrgan, Literal(row['organ.'])))
    g.add((work_uri, hasWerkgebied, Literal(row['werkgebied en -soort'])))
    g.add((work_uri, hasWerkperiode, Literal(row['werkperiode'])))
    g.add((work_uri, hasBijzonderheden, Literal(row['bijzonderheden'])))
    
    # Link the work record to the person resource using the same id
    person_uri = EX[f"person/{row['id']}"]
    g.add((person_uri, hasWork, work_uri))

# Process the spouse CSV: create a spouse resource and link it to the person with the matching id.
for idx, row in df_spouse.iterrows():
    spouse_uri = EX[f"spouse/{row['id']}_{idx}"]
    g.add((spouse_uri, RDF.type, Spouse))
    g.add((spouse_uri, spouseInfo, Literal(row['spouse'])))
    
    # Link this spouse record to the corresponding person
    person_uri = EX[f"person/{row['id']}"]
    g.add((person_uri, hasSpouse, spouse_uri))

# Optionally, use matplotlib to plot a simple statistic (e.g., number of work records per person)
work_counts = df_work['id'].value_counts().sort_index()
plt.figure()
work_counts.plot(kind='bar')
plt.xlabel('Person ID')
plt.ylabel('Number of Work Records')
plt.title('Work Records per Person')
plt.tight_layout()
plt.savefig("work_records.png")
plt.close()
print("Plot saved as work_records.png")

# Serialize the RDF graph to a Turtle file
output_file = "/Volumes/Extreme SSD/Python_Projects/NIAA Project/FINAL_PARSED_DATA/output.ttl"
g.serialize(destination=output_file, format="turtle")
print(f"RDF data written to {output_file}")
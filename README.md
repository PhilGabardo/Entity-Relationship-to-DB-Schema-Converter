# Entity-Relationship-to-DB-Schema-Converter



## Summary

This is a script used to convert a tsv respresentation of an Entity-Relationship model to a DB schema. This is intended to be a proof of 
concept, not a general, all-purpose ER-to-DBSchema converter. The motivation for this script was an assignment that I was assigned
in a databases course that I am currently taking. The assignment involved converting a large ER model to a DB schema. This seemed like
a long and tedious task, so I decided to script it as this seemed like a fun way to get the assignment done, and I would learn the 
material inside out.


## Input/Output

The script is run as:

python ERtoSchema.py \<filename\>

where \<filename\> is the tsv representation of the ER model you want to convert. The tsv file must be formatted according to the following conventions:

#### Order
ALL entities must be declared before relations.

#### Entity Declaration
To declare an entity, include the following lines:

Entity(tab)\<ENTITY_NAME\>(tab)\<NUMBER_OF_ENTITY_ATTRIBUTES\>(tab)\<IS_ENTITY_WEAK\>

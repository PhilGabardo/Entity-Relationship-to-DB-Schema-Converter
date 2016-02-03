# Entity-Relationship-to-DB-Schema-Converter



## Summary

This is a script used to convert a tsv respresentation of an Entity-Relationship model to a DB schema. This is intended to be a proof of 
concept, not a general, all-purpose ER-to-DBSchema converter. The motivation for this script was an assignment that I was given
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

NOTE: Any \<IS_*\> fields should either be True or False.

To declare an entity, include the following line:

Entity(tab)\<ENTITY_NAME\>(tab)\<NUMBER_OF_ENTITY_ATTRIBUTES\>(tab)\<IS_ENTITY_WEAK\>


Then you must declare NUMBER_OF_ENTITY_ATTRIBUTES attributes...

##### Attribute Declaration
To declare an attribute, include the following line:
\<ATTRIBUTE_NAME\>(tab)\<IS_ATTRIBUTE_MULTIVALUED\>(tab)\<NUMBER_OF_NESTED_ATTRIBUTES\>(tab)\<IS_ATTRIBUTE_PRIMARY_KEY\>(tab)\<IS_ATTRIBUTE_FOREIGN_KEY\>(tab)\<IS_ATTRIBUTE_DISCRIMINATOR\>

If the attribute contains nested attributes, another line must be included to declare these attributes. The line should include the nested attribute names, separated by tabs.

#### Relation Declaration
To declare a relation, include the following line:

Relation(tab)\<RELATION_NAME\>(tab)\<RELATION_TYPE\>(tab)\<IS_ENTITY_WEAK\>(tab)\<ENTITY_1_NAME\>(tab)\<ENTITY_2_NAME\>(tab)\<NUMBER_OF_RELATION_ATTRIBUTES\>(tab)\<IS_RELATION_IDENTIFYING\>(tab)\<IS_ENTITY_1_TOTAL\>(tab)\<IS_ENTITY_2_TOTAL\>

RELATION_TYPE must be one of {oneToOne, oneToMany, manyToMany, isa}.

If the relation has any attributes, another line must be included to declare these attributes. The line should include the attribute names, separated by tabs.


See ER.tsv for an example of a fully formatted ER file.

### Testing

For a sample test case, run python ERtoSchema.py ER.tsv.


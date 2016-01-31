class Table(object):
	def __init__(self):
		self.name = None
		self.attributes = []

class Attribute(object):
	def __init__(self):
		self.name = None
		self.composite = False
		self.multivalued = False
		self.attributes = []
		self.PK = False
		self.FK = False

class Entity(object):
	def __init__(self):
		self.name = None
		self.PK = None
		self.attributes = []
		self.weak = False
		self.discriminator = None

class RelationshipType:
	oneToOne, oneToMany, manyToMany, isa = range(4)


class Relationship(object):
	def __init__(self):
		self.name = None
		self.type = None
		self.E1 = None
		self.E2 = None
		self.attributes = []


def createTable(entity):
	table = Table()
	table.name = entity.name
	table.PK = entity.PK
	table.attributes = entity.attributes
	return table


def preprocessAttributes(entities):
	# take care of composite/multivalue attributes
        for entity in entities:
                attributes = entity.attributes
                for attribute in attributes:
                        if attribute.multivalued:
                                newEntity = Entity()
                                newEntity.name = entity.name + "_" + attribute.name
                                newEntity.PK = ""
                                for innerAttribute in attribute.attributes:
                                        newEntity.PK += innerAttribute + "_"
                                newEntity.PK = newEntity.PK[:-1]
				if len(attribute.attributes) == 0:
					newAttribute = Attribute()
					newAttribute.name = attribute.name
					newEntity.attributes.append(newAttribute)
				else:
					for innerAttribute in attribute.attributes:
						newAttribute = Attribute()
						newAttribute.name = innerAttribute
						newEntity.attributes.append(newAttribute)
                                FK = Attribute()
                                FK.FK = True
                                FK.name = entity.PK
                                newEntity.attributes.append(FK)
				entities.append(newEntity)
                        elif len(attribute.attributes) > 0:
                                for innerAttribute in attribute.attributes:
                                        newAttribute = Attribute()
                                        newAttribute.name = innerAttribute
                                        entity.attributes.append(newAttribute)
                                entity.attributes.remove(attribute)
	return entities	


def generateTables(entities, relations):

	tables = {}

	for entity in entities:
		eTable = createTable(entity)
		print eTable.name
		tables[entity.name] = eTable

	for rel in relations:
		if rel.type == RelationshipType.oneToOne:
			# Add FK to link tables
			tableE1 = tables[rel.E1.name]
			tableE2 = tables[rel.E2.name]
			FK = Attribute()
			FK.FK = True
			FK.name = tableE2.PK
			tableE1.attributes.append(FK)	
			for attr in rel.attributes:
				tableE1.attributes(attr)			
			

		elif rel.type == RelationshipType.oneToMany:
			# Create one table with attributes for one entity (R1), one table with the attributes 
			# for the other table (R2) and then put the primary key from your origin (R1 one) table to the other table (R2 many) to keep track of
                        # primary key referencing to R1.
			
			tableE1 = tables[rel.E1.name]
			tableE2 = tables[rel.E2.name]
			FK = Attribute()
			FK.FK = True
			FK.name = tableE2.PK
			tableE1.attributes.append(FK)
			for attr in rel.attributes:
				tableE1.attributes.append(attr)
		elif rel.type == RelationshipType.manyToMany:
			# Translate R1 and R2 into separate tables, then create a table to link these two tables
			tableE1 = tables[rel.E1.name]
			tableE2 = tables[rel.E2.name]
			entity = Entity()
			fk1 = Attribute()
			fk1.FK = True
			fk1.name = tableE1.PK
			fk2 = Attribute()
                        fk2.FK = True
                        fk2.name = tableE2.PK	
			entity.attributes.append(fk1)
			entity.attributes.append(fk2)
			for attr in rel.attributes:
				entity.attributes.append(attr)
			entity.name = rel.name
			relation = createTable(entity)
			tables[entity.name] = relation	
		elif rel.type == RelationshipType.isa:
			tableE1 = tables[rel.E1.name]
			tableE2 = tables[rel.E2.name]
			FK = Attribute()
			FK.FK = True
			FK.name = tableE2.PK
			tableE1.attributes.append(FK)
	tableList = []
	for key in tables:
		tableList.append(tables[key])	
	return tableList


def printSchema(tables):
	schema = ""
	for table in tables:
		schema += "TABLE: " + table.name + "\n"
		for attribute in table.attributes:
			schema += "\t\tATTRIBUTE: " + attribute.name
			if attribute.FK:
				schema += "(FK)"
			if attribute.PK:
				schema += "(PK)" 
			schema += "\n"
	print schema	


def displayResults(entities, relations):
	print "-------ER BREAKDOWN-------\n"
	for entity in entities:
		print "ENTITY: " + entity.name
		print "\t ATTRIBUTE NUMBER: " + str(len(entity.attributes))
		for attr in entity.attributes:
			print "\t\t ATTRIBUTE: " + attr.name
			print "\t\t COMPOSITE: " + str(len(attr.attributes)>0)
			print "\t\t MV: " + str(attr.multivalued)
			print "\t\t PK: " + str(attr.PK)
			print "\t\t FK: " + str(attr.FK)
		print "\t WEAK: " + str(entity.weak)

	for relation in relations:
		print "RELATION: " + relation.name
		print "\t TYPE: " + str(relation.type)
		print "\t R1: " + relation.E1.name
		print "\t R2: " + relation.E2.name

	

def parse(file):
	file = open(file, 'r')
	entities = {}
	relations = {}
	line = file.readline().strip()
	while line:
		elements = line.split('\t')
		if elements[0] == "Entity":
			print elements
			entity = Entity()
			entity.name = elements[1]
			for i in range(0, int(elements[2])):
				line = file.readline().strip()
				innerElements = line.split('\t')
				attr = Attribute()
				attr.name = innerElements[0]
				if innerElements[1] == "True":
					attr.multivalued = True
				if int(innerElements[2]) > 0:
					line = file.readline().strip()
					innerInnerElements = line.split('\t')
					for innerAttr in innerInnerElements:
						attr.attributes.append(innerAttr)

				if innerElements[3] == "True":
					attr.PK = True
					entity.PK = attr.name

				if innerElements[4] == "True":
					attr.FK = True
				if innerElements[5] == "True":
					entity.discriminator = attr.name
				entity.attributes.append(attr)
				if entity.PK == None:
					PK = ""
					for attr in entity.attributes:
						PK += attr.name + "_"
					PK = PK[:-1]
					entity.PK = PK
			if elements[3] == "True":
				entity.weak = True
			entities[entity.name] = entity
		elif elements[0] == "Relation":
			print line
			relation = Relationship()
			relation.name = elements[1]
			if elements[2] == "oneToOne":
				relation.type = RelationshipType.oneToOne
			elif elements[2] == "oneToMany":
				relation.type = RelationshipType.oneToMany
			elif elements[2] == "manyToMany":
				relation.type = RelationshipType.manyToMany
			elif elements[2] == "isa":
				relation.type = RelationshipType.isa
			E1 = elements[3]
			E2 = elements[4]

			if int(elements[5]) > 0:
				line = file.readline().strip()
                                innerElements = line.split('\t')
				for i in range(0, len(innerElements)):
					attr = Attribute()
					attr.name = innerElements[i]
					relation.attributes.append(attr)
				

			relation.E1 = entities[E1]
			relation.E2 = entities[E2]
			relations[relation.name + E1 + "_" + E2] = relation
		line = file.readline().strip()
	entityList = []
	relationList = []
	
	for key in entities:
		entityList.append(entities[key])
	for key in relations:
		relationList.append(relations[key])
	print "Parsing done..."
	displayResults(entityList, relationList)
	entityList = preprocessAttributes(entityList)
	print "Preprocessing done..."
	displayResults(entityList, relationList)
	tables = generateTables(entityList, relationList)	
	printSchema(tables)

parse('ER.csv')



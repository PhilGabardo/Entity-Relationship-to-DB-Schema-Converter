import sys

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

class RelationType:
	oneToOne, oneToMany, manyToMany, isa = range(4)


class Relation(object):
	def __init__(self):
		self.name = None
		self.type = None
		self.E1 = None
		self.E2 = None
		self.identifying = False
		self.attributes = []
		self.E1Total = False
		self.E2Total = False

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
				if attribute.composite:
                                	for innerAttribute in attribute.attributes:
                                        	newEntity.PK += innerAttribute + "_"
				else:
					newEntity.PK += attribute.name + "_"
                                newEntity.PK += entity.PK
				
				PK = Attribute()
				PK.PK = True
				PK.name = newEntity.PK
				newEntity.attributes.append(PK)

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
				attribute.name = newEntity.PK
                                attribute.FK = True
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
		tables[entity.name] = eTable

	for rel in relations:
		if rel.type == RelationType.oneToOne:
			if rel.E1Total == False and rel.E2Total == False:
				entity = Entity()
				FK1 = Attribute()
				FK1.FK = True
				FK1.name = E1.PK
				entity.attribute.append(FK1)
                                FK2 = Attribute()
                                FK2.FK = True
                                FK2.name = E2.PK
                                entity.attribute.append(FK2)
				entity.PK = FK1.name + "_" + FK2.name
				entity.name = E1.name + "_" + E2.name
				for attr in rel.attributes:
					entity.attributes.append(attr)
				relation = createTable(entity)
				tables[entity.name] = relation	
				
			else:
				if rel.E1Total == True:
					# Add FK to link tables
					tableE1 = tables[rel.E1.name]
					tableE2 = tables[rel.E2.name]
					FK = Attribute()
					FK.FK = True
					FK.name = tableE2.PK
					tableE1.attributes.append(FK)	
					for attr in rel.attributes:
						tableE1.attributes.append(attr)			
				else:
                                        tableE1 = tables[rel.E1.name]
                                        tableE2 = tables[rel.E2.name]
                                        FK = Attribute()
                                        FK.FK = True
                                        FK.name = tableE1.PK
                                        tableE2.attributes.append(FK)
                                        for attr in rel.attributes:
                                                tableE2.attributes.append(attr)

		elif rel.type == RelationType.oneToMany:
			if rel.E1Total == False and rel.E2Total == False:
				entity = Entity()
                                FK1 = Attribute()
                                FK1.FK = True
                                FK1.name = E1.PK
                                entity.attribute.append(FK1)
                                FK2 = Attribute()
                                FK2.FK = True
                                FK2.name = E2.PK
                                entity.attribute.append(FK2)
                                entity.PK = FK1.name + "_" + FK2.name
                                entity.name = E1.name + "_" + E2.name
                                for attr in rel.attributes:
                                        entity.attributes.append(attr)
                                relation = createTable(entity)
                                tables[entity.name] = relation

			else:
				tableE1 = tables[rel.E1.name]
				tableE2 = tables[rel.E2.name]
				FK = Attribute()
				FK.FK = True
				FK.name = tableE2.PK
				tableE1.attributes.append(FK)
				for attr in rel.attributes:
					tableE1.attributes.append(attr)
		elif rel.type == RelationType.manyToMany:
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
			entity.PK = tableE1.PK + tableE2.PK
			relation = createTable(entity)
			tables[entity.name] = relation	
		elif rel.type == RelationType.isa:
			tableE1 = tables[rel.E1.name]
			tableE2 = tables[rel.E2.name]
			PK = Attribute()
			PK.PK = True
			PK.name = tableE2.PK
			tableE1.attributes.append(PK)
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

	

def parse(filename):
	file = open(filename, 'r')
	entities = {}
	relations = {}
	line = file.readline().strip()
	while line:
		elements = line.split('\t')
		if elements[0] == "Entity":
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
					print attr.name
					entity.discriminator = attr.name
				entity.attributes.append(attr)
				if entity.PK == None and entity.discriminator == None:
					PK = ""
					for attr in entity.attributes:
						PK += attr.name + "_"
					PK = PK[:-1]
					entity.PK = PK
			if elements[3] == "True":
				entity.weak = True
			entities[entity.name] = entity
		elif elements[0] == "Relation":
			relation = Relation()
			relation.name = elements[1]
			if elements[2] == "oneToOne":
				relation.type = RelationType.oneToOne
			elif elements[2] == "oneToMany":
				relation.type = RelationType.oneToMany
			elif elements[2] == "manyToMany":
				relation.type = RelationType.manyToMany
			elif elements[2] == "isa":
				relation.type = RelationType.isa
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
			
			if elements[6] == "True":
                                relation.identifying = True
                                if relation.E1.PK != None:
					print relation.E1.PK
					print relation.E2.name
					PK = Attribute()
					PK.PK = True
					PK.name = relation.E2.discriminator + "_" + relation.E1.PK
					relation.E2.attributes.append(PK)
					relation.E2.PK = PK.name
				elif relation.E2.PK != None:
					print relation.E1.name
					PK = Attribute()
                                        PK.PK = True
                                        PK.name = relation.E1.discriminator + "_" + relation.E2.PK
                                        relation.E1.attributes.append(PK)
                                        relation.E1.PK = PK.name
				else:
					print "Identifying relation \"" + relation.name + "\" malformed. Neither entity has a primary key" 
			
			if elements[7] == "True":
				relation.E1Total = True
			if elements[8] == "True":
                                relation.E2Total = True
			relations[relation.name + E1 + "_" + E2] = relation
		line = file.readline().strip()
	entityList = []
	relationList = []
	
	for key in entities:
		entityList.append(entities[key])
	for key in relations:
		relationList.append(relations[key])
	return [entityList, relationList]


def convert(file):
	(entityList, relationList) = parse(file)
        print "Parsing done:\n\n"
        displayResults(entityList, relationList)
        entityList = preprocessAttributes(entityList)
        print "\n\nPreprocessing done:\n\n"
        displayResults(entityList, relationList)
        print "\n\nFinal schema:\n\n"
        tables = generateTables(entityList, relationList)
	return tables


tables = convert(sys.argv[1])
printSchema(tables)






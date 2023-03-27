import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError

def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def add_departments(db):
    department_list = ['ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3','EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC']
    collection = db["departments"]
    unique_name: bool = False
    unique_abbreviation: bool = False
    unique_chair_name: bool = False
    unique_building: bool = False
    unique_office: bool = False
    unique_description: bool = False
    department_name: str = ''
    abbreviation: str = ''
    chair_name: str = ''
    building: str = ''
    office: int = 0
    check = True
    description: str = ''
    # variables to check length of the user's input
    min_name = 10
    max_name = 50
    max_abbrev = 6
    max_chair = 80
    min_description = 10
    max_description = 80
    control_checkingLen = True
    try:
        while not unique_name or not unique_abbreviation or not unique_chair_name or not unique_building or not unique_office or not unique_description:
            while control_checkingLen:
                department_name = input("Department name--> ")
                if len(department_name) < min_name or len(department_name) > max_name:
                    print("Your department name is less then 10 characters or more then 50!")
                    pass
                else:
                    abbreviation = input("Abbreviation name--> ")
                    if len(abbreviation) > max_abbrev:
                        print("Your  abbreviation is more then 6 charcaters!")
                        pass
                    else:
                        chair_name = input("chair name--> ")
                        if len(chair_name) > max_chair:
                            print("Your chair name is more then 80 characters")
                            pass
                        else:
                            # Checking if building inside the list of permitted building name list
                            building = input("Building name--> ")
                            while check == True:
                                if building in department_list:
                                    check = False
                                    break
                                else:
                                    print("invalid input. try again")
                                    building = input("Building name--> ")
                            
                            # The office number can be any length
                            office = input("office number--> ")
                            description = input("description of departments--> ")
                            if len(description) < min_description or len(description) > max_description:
                                print("Your Descripttion is less then 10 characters or more then 80 characters!")
                                pass
                            else:
                                break
            
            
            # Checking for uniqueness for all attributes. If there are already departments with the same atributes like the one the user is adding


            name_count: int = collection.count_documents({"department_name": department_name, "abbreviation": abbreviation})
            unique_name = name_count == 0
            if not unique_name:
                print("We already have a department by that name.  Try again.")
            if unique_name:
                abbreviation_count = collection.count_documents({"abbreviation": abbreviation})
                unique_abbreviation = abbreviation_count == 0
                if not unique_abbreviation:
                    print("We already have a department with that abbreviation.  Try again.")
                if unique_abbreviation:
                    chair_count = collection.count_documents({"chair_name": chair_name})
                    unique_chair_name = chair_count == 0
                    if not unique_chair_name:
                        print("We already have a department with that chair. Try again")
                    if unique_chair_name:
                        building_count = collection.count_documents({"building": building})
                        unique_building = building_count == 0
                        if not unique_building:
                            print("We already have a department with that building. Try again")
                        if unique_building:
                            office_count = collection.count_documents({"office": office})
                            unique_office = office_count == 0
                            if not unique_office:
                                print("We already have department with office")
                            if unique_office:
                                description_count = collection.count_documents({"description": description})
                                unique_description = description_count == 0
                                if not unique_description:
                                    print("We already have a description in departments")
    

        department = {
            "name": department_name,
            "abbreviation": abbreviation,
            "chair_name": chair_name,
            "building": building,
            "office": office,
            "description": description
        }
        results = collection.insert_one(department)
    except Exception as e:
        print("You are just trying to add a Department with a name that already exists!")




def add_student(db):
    """
    Add a new student, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    students collection.  Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints.  Extra credit anyone?
    :param collection:  The pointer to the students collection.
    :return:            None
    """
    # Create a "pointer" to the students collection within the db database.
    collection = db["students"]
    unique_name: bool = False
    unique_email: bool = False
    lastName: str = ''
    firstName: str = ''
    email: str = ''
    while not unique_name or not unique_email:
        lastName = input("Student last name--> ")
        firstName = input("Student first name--> ")
        email = input("Student e-mail address--> ")
        name_count: int = collection.count_documents({"last_name": lastName, "first_name": firstName})
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a student by that name.  Try again.")
        if unique_name:
            email_count = collection.count_documents({"e_mail": email})
            unique_email = email_count == 0
            if not unique_email:
                print("We already have a student with that e-mail address.  Try again.")
    # Build a new students document preparatory to storing it
    student = {
        "last_name": lastName,
        "first_name": firstName,
        "e_mail": email
    }
    results = collection.insert_one(student)
    

def select_student(db):
    """
    Select a student by the combination of the last and first.
    :param db:      The connection to the database.
    :return:        The selected student as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from 
                    the database.
    """
    # Create a connection to the students collection from this database
    collection = db["students"]
    found: bool = False
    lastName: str = ''
    firstName: str = ''
    while not found:
        lastName = input("Student's last name--> ")
        firstName = input("Student's first name--> ")
        name_count: int = collection.count_documents({"last_name": lastName, "first_name": firstName})
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    found_student = collection.find_one({"last_name": lastName, "first_name": firstName})
    return found_student

def select_department(db):
    """
    Select a student by the combination of the last and first.
    :param db:      The connection to the database.
    :return:        The selected student as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from
                    the database.
    """
    # Create a connection to the students collection from this database
    collection = db["departments"]
    found: bool = False
    name: str = ''
    while not found:
        name = input("Department's name--> ")
        name_count: int = collection.count_documents({"department_name": name})
        found = name_count == 1
        if not found:
            print("No department found by that name.  Try again.")
    found_department = collection.find_one({"department_name": name})
    return found_department


def delete_student(db):
    """
    Delete a student from the database.
    :param db:  The current database connection.
    :return:    None
    """
    # student isn't a Student object (we have no such thing in this application)
    # rather it's a dict with all the content of the selected student, including
    # the MongoDB-supplied _id column which is a built-in surrogate.
    student = select_student(db)
    # Create a "pointer" to the students collection within the db database.
    students = db["students"]
    # student["_id"] returns the _id value from the selected student document.
    deleted = students.delete_one({"_id": student["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} students.")

def delete_department(db):
    """
    Delete a department from the database.
    :param db:  The current database connection.
    :return:    None
    """

    department = select_department(db)
    # Create a "pointer" to the departments collection within the db database.
    departments = db["departments"]
    # department["_id"] returns the _id value from the selected student document.
    deleted = departments.delete_one({"_id": department["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} departments.")


def list_student(db):
    """
    List all of the students, sorted by last name first, then the first name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    # No real point in creating a pointer to the collection, I'm only using it
    # once in here.  The {} inside the find simply tells the find that I have
    # no criteria.  Essentially this is analogous to a SQL find * from students.
    # Each tuple in the sort specification has the name of the field, followed
    # by the specification of ascending versus descending.
    students = db["students"].find({}).sort([("last_name", pymongo.ASCENDING),
                                             ("first_name", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for student in students:
        pprint(student)

def list_department(db):


    departments = db["departments"].find({}).sort([("department_name", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for department in departments:
        pprint(department)


if __name__ == '__main__':
    password: str = getpass.getpass('Mongo DB password -->')
    username: str = input('Database username [CECS-323-Spring-2023-user] -->') or \
                    "CECS-323-Spring-2023-user"
    project: str = input('Mongo project name [cecs-323-spring-2023] -->') or \
                   "CECS-323-Spring-2023"
    hash_name: str = input('7-character database hash [puxnikb] -->') or "puxnikb"

    cluster = f"mongodb+srv://bryantineoccasani:5IE2sBx0f97yhnCv@cecs-323-spring-2023.fivtmqe.mongodb.net/?retryWrites=true&w=majority"
    print(f"Cluster: mongodb+srv://bryantineoccasani:********@cecs-323-spring-2023.fivtmqe.mongodb.net/?retryWrites=true&w=majority")
    client = MongoClient(cluster)
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.
    db = client["Demonstration"]
    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())
    # student is our students collection within this database.
    # Merely referencing this collection will create it, although it won't show up in Atlas until
    # we insert our first document into this collection.
    students = db["students"]
    student_count = students.count_documents({})
    print(f"Students in the collection so far: {student_count}")

    # /////////////Department//////////////
    departments = db["departments"]
    department_count = departments.count_documents({})
    print(f"Departments in the collection so far: {department_count}")

    # ************************** Set up the students collection
    students_indexes = students.index_information()
    if 'students_last_and_first_names' in students_indexes.keys():
        print("first and last name index present.")
    else:
        # Create a single UNIQUE index on BOTH the last name and the first name.
        students.create_index([('last_name', pymongo.ASCENDING), ('first_name', pymongo.ASCENDING)],
                              unique=True,
                              name="students_last_and_first_names")
    if 'students_e_mail' in students_indexes.keys():
        print("e-mail address index present.")
    else:
        # Create a UNIQUE index on just the e-mail address
        students.create_index([('e_mail', pymongo.ASCENDING)], unique=True, name='students_e_mail')


    # ************************** Set up the departments collection
    departments_indexes = departments.index_information()
    if 'departments_abbreviation' in departments_indexes.keys():
        print("abbreviation index present.")
    else:
        # Create a UNIQUE index on just the abbreviation
        departments.create_index([('abbreviation', pymongo.ASCENDING)], unique=True, name='department_abbreviation')

    if 'departments_chair_name' in departments_indexes.keys():
        print("chair name index present.")
    else:
        # Create a UNIQUE index on just the chair name
        departments.create_index([('chair_name', pymongo.ASCENDING)], unique=True, name='department_chair_name')

    if 'departments_building_and_office' in departments_indexes.keys():
        print("building and office index present.")
    else:
        # Create a single UNIQUE index on BOTH the building and office.
        departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)],
                              unique=True,
                              name="departments_building_and_office")
    if 'departments_name' in departments_indexes.keys():
        print("name index present.")
    else:
        # Create a UNIQUE index on just the name
        departments.create_index([('name', pymongo.ASCENDING)], unique=True, name='department_name')

    pprint(departments.index_information())
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)



#Updated my Assignment 1 Solution

# To working with date and time
import datetime

# base class representing a project
class Project:
    def __init__(self, name, category, year_started, location, funding, total_cost):

        # Project name, category, year, location ,etc.

        self.name = name
        self.category = category
        self.year_started = int(year_started)
        self.location = location
        self.funding = float(funding)
        self.total_cost = float(total_cost)

#to print all project details 

    def display(self):
        print(f"Name: {self.name}\nCategory: {self.category}\nYear Started: {self.year_started}\nLocation: {self.location}\nFunding: ${self.funding:.2f}\nTotal Cost: ${self.total_cost:.2f}\n")

 # This will calculate and return the duration project started

    def duration(self):
        return datetime.datetime.now().year - self.year_started

#I have selected SA1 Biomethane Upgrading Project from Arena
#subclass for biomethane projects

class BiomethaneProject(Project):
    def __init__(self, name, category, year_started, location, funding, total_cost, co2_output=None):
        super().__init__(name, category, year_started, location, funding, total_cost)           #it wil call base class constructor
        self.co2_output = co2_output  

    def display(self):

# Call parent display method
        super().display()
        if self.co2_output:
            print(f"Biogenic CO2 Output: {self.co2_output}\n")

#for managing a list of projects and provide related operation

class ProjectManager:
    def __init__(self):

        # an empty list to store objects
        self.projects = []

    def load_from_file(self, filename):
        try:
     # Open the file for reading

            with open(filename, 'r') as file:
        # Read all lines into a list
                lines = file.readlines()

         # temporary dictionary to hold  project data

            project_data = {}
            for line in lines:
                line = line.strip()    # Remove whitespace and newline
                if not line or line.startswith("Project info"):
                    continue  # skip empty line

                if ':' in line:
                    key, value = line.split(':', 1) # Split the line
                    key = key.strip()
                    value = value.strip().rstrip(',')  # remove trailing comma
                    project_data[key] = value   # Store in dictionary
                
                # When we have all 6 required fields

                if len(project_data) == 6:  
                    project = Project(
                        name=project_data['Name'],
                        category=project_data['Category'],
                        year_started=project_data['Year Started'],
                        location=project_data['Location'],
                        funding=project_data['Funding'],
                        total_cost=project_data['Total Cost']
                    )
                    self.projects.append(project)
                    project_data = {}  # reset for the next project

            print("Projects loaded successfully.\n")
        except Exception as e:
    # Handle any file  error
            print(f"Error loading file: {e}")  

    def display_all(self):
        if not self.projects:
            print("No projects to display.\n")
        for project in self.projects:
     # for calling each project display method ,
            project.display()

# collect user input for each project field

    def add_project(self):
        try:
            name = input("Enter project name: ")
            category = input("Enter project category: ")
            year = int(input("Enter year started: "))
            location = input("Enter location: ")
            funding = float(input("Enter funding amount: "))
            cost = float(input("Enter total cost: "))
            project = Project(name, category, year, location, funding, cost)   # Create a new project add it to list
            self.projects.append(project)
            print("Project added successfully.\n")

        # if incorrect input types
        except ValueError:
            print("Invalid input. Please try again.\n")

    # Get all project that match s category

    def search_by_category(self, category):
        found = [p for p in self.projects if p.category.lower() == category.lower()]
        for p in found:
            p.display()
        #Incase something wrong

        if not found:
            print("No projects found in that category.\n")

    # Get all project that match s location

    def search_by_location(self, location):
        found = [p for p in self.projects if p.location.lower() == location.lower()]
        for p in found:
            p.display()

    #If any error
        if not found:
            print("No projects found in that location.\n")

    def export_report(self, filename, projects):
        try:
            with open(filename, 'w') as file:
            # report file in CSV-like format
                for p in projects:
                    file.write(f"Name: {p.name}, Category: {p.category}, Year Started: {p.year_started}, Location: {p.location}, Funding: {p.funding}, Total Cost: {p.total_cost}\n")
            print(f"Report saved to {filename}\n")
        # handle file errors
        except Exception as e:
            print(f"Failed to write report: {e}")

# Main menu loop

def main():
    manager = ProjectManager()
# Load projects from file
    manager.load_from_file("ARENA_projects.txt")

 # Display menu option
    while True:
        print("""
##### ARENA Project Management System #####\n
1. Display All Imported Projects
2. Add New Project
3. Search Projects by Category
4. Search Projects by Location
5. Export Report by Category
6. Export Report by Location
7. Exit
""")
    #User input
        choice = input("Enter your choice: ")

        if choice == '1':
            manager.display_all()
        elif choice == '2':
            manager.add_project()
        elif choice == '3':
            category = input("Enter category to search: ")
            manager.search_by_category(category)
        elif choice == '4':
            location = input("Enter location to search: ")
            manager.search_by_location(location)
        elif choice == '5':
            category = input("Enter category to export: ")
            filtered = [p for p in manager.projects if p.category.lower() == category.lower()]
            manager.export_report(f"ARENA_report_{category}.txt", filtered)
        elif choice == '6':
            location = input("Enter location to export: ")
            filtered = [p for p in manager.projects if p.location.lower() == location.lower()]
            manager.export_report(f"ARENA_report_{location}.txt", filtered)
        elif choice == '7':
            print("Goodbye! Have a great day.")
        # Exit the loop and end the program
            break
        else:
            print("Invalid choice. Try again.\n")

# Main point of program

if __name__ == '__main__':
    main()
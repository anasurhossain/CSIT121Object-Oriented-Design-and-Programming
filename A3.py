import os
 #to interact with the operating system 
import json     #json module
import re       # is for regular expressions
from datetime import datetime   # for date
import matplotlib.pyplot as plt     #to create charts

# These regex pattern is used to validate user inputs for states, money and periods.
STATE_REGEX = re.compile(r'^[A-Za-z ]+$')    # Only letters and spaces
MONEY_REGEX = re.compile(r'^\$\d+\.\d{2}m$')    ## Format
PERIOD_REGEX = re.compile(r'^\d{2}/\d{2}/\d{4}\s[–-]\s\d{2}/\d{2}/\d{4}$')

#Main Project Class
class Project:
   # Base class for ARENA projects.
    def __init__(self, name, category, state, location, funding, total_cost, period):
        self.name = name
        self.category = category
        self.state = state
        self.location = location
        self.funding = funding       
        self.total_cost = total_cost 
        self.period = period        

    def to_dict(self): #Serialize the project to a dictionary for JSON export.
        return {
            'type': self.__class__.__name__,
            'Name': self.name,
            'Category': self.category,
            'State': self.state,
            'Location': self.location,
            'Funding': self.funding,
            'Total Cost': self.total_cost,
            'Period': self.period
        }
    
    @staticmethod
    
    def from_dict(d):
    # I use BiomethaneProject as a subclass of Project
        if d.get('type', 'Project') == 'BiomethaneProject':
            return BiomethaneProject(
            d['Name'], d['Category'], d['State'], d['Location'],
            d['Funding'], d['Total Cost'], d['Period'],
            co2_output=d.get('CO2 Output')
        )
        else:
            return Project(
            d['Name'], d['Category'], d['State'], d['Location'],
            d['Funding'], d['Total Cost'], d['Period']
        )

    def display(self):  # Display project attributes in a readable format for the user
        print(f"Name: {self.name}\n"
              f"Category: {self.category}\n"
              f"State: {self.state}\n"
              f"Location: {self.location}\n"
              f"Funding: {self.funding}\n"
              f"Total Cost: {self.total_cost}\n"
              f"Period: {self.period}\n")

    def funding_value(self):    # Convert funding string to a float
        return float(self.funding.strip('$m'))

# Subclass for Polymorphism 
class BiomethaneProject(Project):
    def __init__(self, name, category, state, location, funding, total_cost, period, co2_output=None):
        super().__init__(name, category, state, location, funding, total_cost, period)
        self.co2_output = co2_output  # Optional

    def to_dict(self):
        d = super().to_dict()
        d['CO2 Output'] = self.co2_output
        return d

# -Project Manager Design Pattern
class ProjectManager:
    """
    Singleton class to manage arena projects.
    """
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'projects'):
            self.projects = []
            self.txt_file = 'ARENA_projects.txt'    # Path for project text file
            self.json_file = 'ARENA_projects.JSON'  ## Path for JSON file

    def load_data(self):  #Loads data from JSON or TXT  
        if os.path.exists(self.json_file):
            self.load_json()
        elif os.path.exists(self.txt_file):
            self.load_txt()
        else:
            print("No data file found.")

    def load_txt(self):  #Imports projects from the .txt format
        with open(self.txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        entries = [e.strip() for e in content.split('Project info:') if e.strip()]
        for entry in entries:
            lines = [ln.strip() for ln in entry.splitlines() if ln.strip()]
            data = {}
            for line in lines:
                if ':' in line:
                    key, val = line.split(':', 1)
                    data[key.strip()] = val.strip().rstrip(',')
            try:
                # raw funding & cost (int), convert to $Xm format
                raw_funding = float(data['Funding'])
                raw_cost = float(data['Total Cost'])
                funding_str = f"${raw_funding/1e6:.2f}m"
                cost_str = f"${raw_cost/1e6:.2f}m"
                # Default period based on Year Started
                year = data['Year Started']
                period = f"01/01/{year} – 31/12/{year}"

                proj = Project(
                    name=data['Name'],
                    category=data['Category'],
                    state=data['Location'].split(',')[-1].strip(),
                    location=data['Location'],
                    funding=funding_str,
                    total_cost=cost_str,
                    period=period
                )
                self.projects.append(proj)
            except KeyError:
                continue

    def save_txt(self): # Saves all projects to the .txt file
        with open(self.txt_file, 'w', encoding='utf-8') as f:
            for p in self.projects:
                f.write('Project info:\n')
                f.write(f"Name: {p.name},\n")
                f.write(f"Category: {p.category},\n")
                # Infer year from period
                try:
                    year = p.period.split('–')[0].strip().split('/')[-1]
                except Exception:
                    year = "Unknown"
                f.write(f"Year Started: {year},\n")
                f.write(f"Location: {p.location},\n")
                # Funding back to int value in txt for compatibility
                try:
                    fund_val = int(float(p.funding.strip('$m'))*1_000_000)
                except Exception:
                    fund_val = 0
                try:
                    cost_val = int(float(p.total_cost.strip('$m'))*1_000_000)
                except Exception:
                    cost_val = 0
                f.write(f"Funding: {fund_val},\n")
                f.write(f"Total Cost: {cost_val}\n\n")

    def load_json(self): #Loads projects from a JSON file
        with open(self.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data:
            self.projects.append(Project.from_dict(item))

    def save_json(self):    # Saves all projects to JSON file
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump([p.to_dict() for p in self.projects], f, indent=4)

    def add_project(self, proj):    #Adds a new project to the project list.
        self.projects.append(proj)

    def modify_project(self, index, proj):      # Replaces an existing project at the given index.
        self.projects[index] = proj

    def find_by_state(self, state):
        return [p for p in self.projects if p.state.lower() == state.lower()]

    def find_by_category(self, category): # Finds all projects matching the given category
        return [p for p in self.projects if p.category.lower() == category.lower()]

#  Validation Functions 
def input_with_validation(prompt, validation_func):
    """
   Repeatedly prompt user for input until a valid value is entered.
    """
    while True:
        try:
            val = input(prompt)
            return validation_func(val)
        except Exception as e:
            print(f"Invalid input: {e}")

def validate_state(s):
    if not STATE_REGEX.match(s):
        raise ValueError("State must contain only letters and spaces.")
    return s

def validate_money(m):
    if not MONEY_REGEX.match(m):
        raise ValueError("Money must be in format '$X.XXm'.")
    return m

def validate_period(p):
    if not PERIOD_REGEX.match(p):
        raise ValueError("Period must be 'DD/MM/YYYY – DD/MM/YYYY'.")
    start_str, end_str = [d.strip() for d in re.split('[–-]', p)]
    start = datetime.strptime(start_str, '%d/%m/%Y')
    end = datetime.strptime(end_str, '%d/%m/%Y')
    if start > end:
        raise ValueError("Start date must precede end date.")
    return p

#Collecting New Project Attributes
def create_project():
    """
    Collect project attributes from user with validation.
    """
    print("\n-- Enter New Project Details --")
    name = input_with_validation("Project Name: ", lambda x: x.strip() or ValueError("Name required."))
    category = input_with_validation("Category: ", lambda x: x.strip() or ValueError("Category required."))
    state = input_with_validation("State (New South Wales): ", validate_state)
    location = input_with_validation("Location (City, State): ", lambda x: x.strip() or ValueError("Location required."))
    funding = input_with_validation("Funding (e.g. $0.30m): ", validate_money)
    total_cost = input_with_validation("Total Cost (e.g. $0.50m): ", validate_money)
    period = input_with_validation("Period (DD/MM/YYYY – DD/MM/YYYY): ", validate_period)
    # can add more fields or subclass logic if needed
    return Project(name, category, state, location, funding, total_cost, period)

# Generating Textual Reports and Figures
def generate_report(projs, filename):
    """
    Save textual report as JSON lines.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for p in projs:
            f.write(json.dumps(p.to_dict()) + '\n')
    print(f"Report saved to {filename}.")

def visualize_projects(projs, prefix):
    """
    three visualization types (bar, pie, line).
    """
    if not projs:
        print("No projects to visualize.")
        return

    # Bar: count per state
    states = [p.state for p in projs]

    counts = {s: states.count(s) for s in set(states)}
    plt.figure()
    plt.bar(counts.keys(), counts.values())
    plt.title('Projects per State')
    plt.xlabel('State')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(f"{prefix}_bar.png")
    plt.close()

    # Pie: distribution by category
    cats = [p.category for p in projs]
    cat_counts = {c: cats.count(c) for c in set(cats)}
    plt.figure()

    plt.pie(cat_counts.values(), labels=cat_counts.keys(), autopct='%1.1f%%')
    plt.title('Category Distribution')
    plt.tight_layout()
    plt.savefig(f"{prefix}_pie.png")
    plt.close()

    # Line: funding over years
    try:
        years = sorted(set([int(p.period[-4:]) for p in projs]))
        year_funds = []
        for y in years:
            total = sum(p.funding_value() for p in projs if int(p.period[-4:]) == y)
            year_funds.append(total)
        plt.figure()
        plt.plot(years, year_funds, marker='o')
        plt.title('Total Funding per Year')
        plt.xlabel('Year')
        plt.ylabel('Funding (million $)')
        plt.tight_layout()
        plt.savefig(f"{prefix}_line.png")
        plt.close()
    except Exception:
        pass

    print("Image saved.")

# Main Program Menu Loop
def main():
    mgr = ProjectManager()   # Singleton instance
    mgr.load_data()

    while True:
        print("\nMenu:")
        print("1) Display All Projects")
        print("2) Add New Project")
        print("3) Update Project")
        print("4) Search by State")
        print("5) Search by Category")
        print("6) Export Report")
        print("7) Exit")
        choice = input("Select an option: ").strip().upper()

        if choice == '1':   ## Display all projects
            if not mgr.projects:
                print("No projects found.")
            for p in mgr.projects:
                p.display()

        elif choice == '2': # Create a new project
            p = create_project()
            mgr.add_project(p)
            mgr.save_txt()
            mgr.save_json()
            print("Project added and updated.")

        elif choice == '3': # Modify an existing project
            for idx, p in enumerate(mgr.projects): print(f"[{idx}] {p.name}")
            try:
                i = int(input("Enter number to modify: "))
                if 0 <= i < len(mgr.projects):
                    mgr.modify_project(i, create_project())
                    mgr.save_txt()
                    mgr.save_json()
                    print("Project modified and files updated.")
                else:
                    print("Invalid index.")
            except Exception:
                print("Invalid input.")

        elif choice == '4':  # Search projects by state and visualize results
            st = input_with_validation("Enter state to search: ", validate_state)
            res = mgr.find_by_state(st)
            for p in res: p.display()
            if res:
                visualize_projects(res, f'state_report_{st.replace(" ","_")}')

        elif choice == '5':
            cat = input_with_validation("Enter category to search: ", lambda x: x.strip())
            res = mgr.find_by_category(cat)
            for p in res: p.display()
            if res:
                visualize_projects(res, f'category_report_{cat.replace(" ","_")}')

        elif choice == '6':
            mode = input("Report by (S)tate or (C)ategory? ").strip().upper()
            key = input("Enter key: ")
            if mode == 'S':
                res = mgr.find_by_state(validate_state(key))
                prefix = 'state'
            else:
                res = mgr.find_by_category(key)
                prefix = 'category'
            if res:
                fname = f"report_{prefix}_{key.replace(' ', '_')}.txt"
                generate_report(res, fname)
                visualize_projects(res, f"report_{prefix}_{key.replace(' ', '_')}")
            else:
                print("No matching projects.")

        elif choice in ('X', '7', 'EXIT'):  # Save and exit the program
            mgr.save_txt()
            mgr.save_json()
            print("Data saved. Thank You .")
            break

        else:
            print("Invalid Input. Please try again.")

if __name__ == '__main__':
    main()

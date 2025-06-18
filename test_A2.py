# Importing Python's unittest module

import unittest

# Importing my own classes from the main assignment script
from A2 import Project, ProjectManager

# Creating a test case for the Project class

class TestProject(unittest.TestCase):
# This test to check if project is created with correct data
    def test_project_initialization(self):
# Creating a sample project to check name,category, year, location etc. to check

        p = Project("Test Project", "Solar", 2020, "NSW", 300000, 500000)
        self.assertEqual(p.name, "Test Project")
        self.assertEqual(p.category, "Solar")
        self.assertEqual(p.year_started, 2020)
        self.assertEqual(p.location, "NSW")
        self.assertEqual(p.funding, 300000)
        self.assertEqual(p.total_cost, 500000)

     # Test for checking duration
    def test_duration(self):
        p = Project("Old Project", "Wind", 2015, "VIC", 800000, 2000000)
        current_year = 2025  
        self.assertEqual(p.duration(), current_year - 2015)

# Creating a test for Project manager
class TestProjectManager(unittest.TestCase):
    def setUp(self):
        # Create a new ProjectManager object
        self.manager = ProjectManager()
        self.manager.projects = [
            Project("Solar Boost", "Solar", 2022, "NSW", 500000, 1500000),
            Project("Wind Future", "Wind", 2021, "VIC", 700000, 2000000)
        ]
# Testing search by category

    def test_search_by_category(self):
        # Manually search
        results = [p for p in self.manager.projects if p.category.lower() == "solar"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Solar Boost")

# Test searching by location
    def test_search_by_location(self):
        results = [p for p in self.manager.projects if p.location.lower() == "vic"]
        self.assertEqual(len(results), 1)  # Only one project in VIC
        self.assertEqual(results[0].name, "Wind Future")
    
# Test the report export function
    def test_export_report(self):
        # Name of the file to save the report
        output_file = "test_my_reports.txt"
        self.manager.export_report(output_file, self.manager.projects)
        # Open the file 
        with open(output_file, "r") as f:
            lines = f.readlines()        # Read lines from the file
            self.assertEqual(len(lines), 2)

# It will run all the tests defined above
if __name__ == '__main__':
    unittest.main()
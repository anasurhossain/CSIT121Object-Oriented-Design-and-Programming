import unittest
import os

import json

from A3 import Project, BiomethaneProject, ProjectManager

class TestProjectSerialization(unittest.TestCase):
     # setUp and tearDown used to prepare clean test data for each test case.
    def setUp(self):
        # Set up some example projects
        self.proj1 = Project(
            "Solar Demo", "Solar", "New South Wales", "Sydney, NSW",
            "$2.25m", "$5.55m", "01/01/2023 – 31/12/2024"
        )
        self.proj2 = BiomethaneProject(
            "BioGas Future", "Biomethane", "Victoria", "Melbourne, VIC",
            "$2.09m", "$4.58m", "01/06/2022 – 30/06/2025", co2_output="1500t"
        )
     # These files are used for temporary testing only
        self.test_json = "test_projects.JSON"
        self.test_txt = "test_projects.txt"

    def tearDown(self):
        # Remove test files after each test
        if os.path.exists(self.test_json):
            os.remove(self.test_json)
        if os.path.exists(self.test_txt):
            os.remove(self.test_txt)

    def test_to_dict_and_from_dict(self):
       # Ensures serialization and polymorphic deserialization both work.
        d = self.proj1.to_dict()
        p2 = Project.from_dict(d)
        self.assertEqual(p2.name, self.proj1.name)
        self.assertEqual(p2.funding, self.proj1.funding)

        d2 = self.proj2.to_dict()
        p3 = BiomethaneProject.from_dict(d2)
        self.assertEqual(p3.name, self.proj2.name)
        self.assertEqual(p3.co2_output, self.proj2.co2_output)

    def test_serialization_to_json(self):
        """
        Test saving a list of projects to a JSON file and loading them back.
        Ensures that list serialization deserialization works correctly.
        """
        projects = [self.proj1, self.proj2]
        # Save the projects to a test JSON file
        with open(self.test_json, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in projects], f, indent=4)
     # Load them back from the file
        with open(self.test_json, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        loaded_projects = [Project.from_dict(d) for d in loaded]
        self.assertEqual(len(loaded_projects), 2)
        self.assertEqual(loaded_projects[0].name, self.proj1.name)
        self.assertEqual(loaded_projects[1].name, self.proj2.name)

    def test_project_manager_singleton(self):
      #Test ProjectManager enforces the Singleton pattern
        mgr1 = ProjectManager()
        mgr2 = ProjectManager()
        self.assertIs(mgr1, mgr2)

    def test_add_and_modify_project(self):
     #Test adding and modifying a project in ProjectManager
        mgr = ProjectManager()
        mgr.projects = []
        mgr.add_project(self.proj1)
        self.assertEqual(len(mgr.projects), 1)
        new_proj = Project(
            "Solar Demo2", "Solar", "Victoria", "Geelong, VIC",
            "$3.00m", "$4.50m", "01/01/2025 – 31/12/2026"
        )
        mgr.modify_project(0, new_proj)
        self.assertEqual(mgr.projects[0].name, "Solar Demo2")

    def test_find_by_state_and_category(self):
        #Test the searching/filtering by state and by category
        mgr = ProjectManager()
        mgr.projects = [self.proj1, self.proj2]
        res_state = mgr.find_by_state("New South Wales")
        self.assertEqual(len(res_state), 1)
        self.assertEqual(res_state[0].state, "New South Wales")
        res_cat = mgr.find_by_category("Biomethane")
        self.assertEqual(len(res_cat), 1)
        self.assertEqual(res_cat[0].category, "Biomethane")

    def test_txt_file_io(self):
 #Test saving and loading projects from the TXT file
        mgr = ProjectManager()
        mgr.projects = [self.proj1]
        mgr.txt_file = self.test_txt
        mgr.save_txt()
        self.assertTrue(os.path.exists(self.test_txt))
      # Now clear reload from txt
        mgr.projects = []
        mgr.load_txt()
        self.assertEqual(len(mgr.projects), 1)
        self.assertEqual(mgr.projects[0].name, self.proj1.name)

    def test_json_file_io(self):
          #Test saving and loading projectsfrom the json
        mgr = ProjectManager()
        mgr.projects = [self.proj1, self.proj2]
        mgr.json_file = self.test_json
        mgr.save_json()
        self.assertTrue(os.path.exists(self.test_json))
    # Clear projects reload from JSON
        mgr.projects = []
        mgr.load_json()
# Should load both 
        self.assertEqual(len(mgr.projects), 2)
        self.assertEqual(mgr.projects[1].name, self.proj2.name)

if __name__ == "__main__":
    unittest.main()

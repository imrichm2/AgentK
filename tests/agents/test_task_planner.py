import unittest

from agents.task_planner import task_planner

class TestTaskPlanner(unittest.TestCase):
    def test_task_planner(self):
        self.assertTrue(callable(task_planner))
        
        result = task_planner("Organize a small conference")
        self.assertIsInstance(result, str)
        self.assertIn("TASK BREAKDOWN COMPLETE", result)
        self.assertGreater(len(result.split('\n')), 3)  # Ensure multiple subtasks are generated

if __name__ == '__main__':
    unittest.main()
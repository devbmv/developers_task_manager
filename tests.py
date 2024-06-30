import unittest
from run import add_task, delete_task, modify_task, tasks


class OrderedTestLoader(unittest.TestLoader):
    def getTestCaseNames(self, testCaseClass):
        try:
            # Initialize the test case class if it hasn't been initialized
            testCaseClass.setUpClass()
        except AttributeError:
            pass
        return testCaseClass.orderedTestNames


class TestTaskManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.orderedTestNames = [
            'test_add_task',
            'test_delete_task',
            'test_modify_task'
        ]

    def test_add_task(self):
        add_task("Test task")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["Task"], "Test task")

    def test_delete_task(self):
        add_task("Test task")
        delete_task(1)  # Task IDs start from
        self.assertEqual(len(tasks), 1)

    def test_modify_task(self):
        add_task("Test task")
        modify_task(1, "Modified task")  # Task IDs start from 1
        self.assertEqual(tasks[1]["Task"], "Modified task")


if __name__ == '__main__':
    tasks.clear()
    suite = unittest.TestSuite()
    loader = OrderedTestLoader()
    suite.addTests(loader.loadTestsFromTestCase(TestTaskManager))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

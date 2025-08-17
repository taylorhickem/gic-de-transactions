"""unit tests to verify working as expected
"""
import unittest
from crash import drive


class CrashTests(unittest.TestCase):

    def test_add_positive_numbers(self):
        self.assertEqual(drive.add(2, 3), 5)

    def test_grid_create_fail_empty(self):
        expected = -1
        response_actual = drive.grid_create()
        actual = response_actual.get('success')
        self.assertEqual(expected, actual)

    def test_grid_create_fail_non_integer(self):
        expected = -1
        response_actual = drive.grid_create(h='h', w=3)
        actual = response_actual.get('success')
        self.assertEqual(expected, actual)

    def test_grid_create_fail_negative_integer(self):
        expected = -1
        response_actual = drive.grid_create(h=-1, w=3)
        actual = response_actual.get('success')
        self.assertEqual(expected, actual)

    def test_grid_create_success(self):
        expected = 1
        response_actual = drive.grid_create(h=1, w=3)
        actual = response_actual.get('success')
        self.assertEqual(expected, actual)

    def test_car_add_and_run(self):
        drive.state_refresh()
        drive.grid_create(h=5, w=5)
        car_a = {
            'name': 'A',
            'position': {'x': 1, 'y': 1},
            'direction': 'N',
            'moves': 'FF'
        }
        car_b = {
            'name': 'B',
            'position': {'x': 2, 'y': 2},
            'direction': 'E',
            'moves': 'FF'
        }
        response_a = drive.car_add(**car_a)
        response_b = drive.car_add(**car_b)
        self.assertEqual(1, response_a.get('success'))
        self.assertEqual(1, response_b.get('success'))
        run_response = drive.run()
        self.assertEqual(1, run_response.get('success'))

    def test_car_collission(self):
        drive.state_refresh()
        drive.grid_create(h=10, w=10)
        car_a = {
            'name': 'A',
            'position': {'x': 1, 'y': 3},
            'direction': 'N',
            'moves': 'FFFFFF'
        }
        car_b = {
            'name': 'B',
            'position': {'x': 1, 'y': 7},
            'direction': 'S',
            'moves': 'FFFFF'
        }
        response_a = drive.car_add(**car_a)
        response_b = drive.car_add(**car_b)
        self.assertEqual(1, response_a.get('success'))
        self.assertEqual(1, response_b.get('success'))
        run_response = drive.run()
        print(run_response)
        has_collission = 'collide' in run_response.get('msg', '')
        self.assertEqual(True, has_collission)


if __name__ == '__main__':
    unittest.main()

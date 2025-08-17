"""Crash program car simulation module
"""
# dependencies ---------------------------------------------------------------------
from . import state
from typing import Dict, List, Tuple
import numpy as np

# constants ------------------------------------------------------------------------
DIRECTION_LEFT = {
    "N": "W",
    "W": "S",
    "S": "E",
    "E": "N"
}

DIRECTION_RIGHT = {
    "N": "E",
    "E": "S",
    "S": "W",
    "W": "N"
}

VECTOR_MOVE = {
    "N": np.array([1, 0]),
    "E": np.array([0, 1]),

    "S": np.array([-1, 0]),
    "W": np.array([0, -1])
}


# classes --------------------------------------------------------------------------
class Grid(object):
    height = 0
    width = 0
    board = []
    status = 1
    error = ''
    def __init__(self, height:int, width:int, board=[]):
        self.height = height
        self.width = width
        if self.valid():
            if board:
                self.board = board
            else:
                self._board_create()
        else:
            self._exception_handle(ex_type='invalid', params={'h': height, 'w': width})

    def to_dict(self):
        params = {
            'height': self.height,
            'width': self.width,
            'board': self.board
        }
        return params

    def __repr__(self):
        return f'Grid({self.height}, {self.width})'

    def _board_create(self):
        self.board = [[0 for j in range(self.width)] for i in range(self.height)]

    def dim(self):
        return {'height':self.height, 'width': self.width}

    def valid(self):
        board_valid = True
        coord_valid = self.height > 0 and self.width > 0
        if coord_valid:
            if self.board:
                board_valid = False
                try:
                    h_valid = len(self.board) == self.height
                    w_valid = len(self.board[0]) == self.width
                    board_valid = h_valid and w_valid
                except Exception as e:
                    self._exception_handle(ex_type='invalid_board', params={'msg': str(e)})
        return coord_valid and board_valid

    def valid_coordinates(self, i, j):
        h_valid = i >= 0 and i <= (self.height-1)
        w_valid = j >= 0 and j <= (self.width-1)
        coord_valid = h_valid and w_valid
        return coord_valid

    def car_add(self, car_id, i, j):        
        if self.valid_coordinates(i, j):
            if self.slot_available(i, j):
                self.board[i][j] = car_id
                return 1
            else:
                self._exception_handle(
                    ex_type='slot_unavailable', 
                    params={'h': i, 'w': j, 'car_id': car_id},
                    status=1
                )
                return -1
        else:
            self._exception_handle(
                ex_type='out_of_bounds', 
                params={'h': i, 'w': j},
                status=1
            )
            return -1

    def _car_remove(self, i, j):
        self.board[i][j] = 0

    def car_move(self, car_id, pos_start, pos_new):
        i = pos_new[0]
        j = pos_new[1]
        if self.valid_coordinates(i, j):
            if self.slot_available(i, j):
                self._car_remove(pos_start[0], pos_start[1])            
                return self.car_add(car_id, i, j)
            else:
                occupied_id = self.get_slot_index(i, j)
                self._exception_handle(
                    ex_type='slot_unavailable', 
                    params={'h': i, 'w': j, 'car_id': occupied_id},
                    status=1
                )
                return -1
        else:
            self._exception_handle(
                ex_type='out_of_bounds', 
                params={'h': i, 'w': j},
                status=1
            )
            return -1

    def slot_available(self, i, j):
        if self.valid_coordinates(i, j):
            slot_index = self.get_slot_index(i, j)
            is_available = slot_index == 0
            return is_available
        else:
            self._exception_handle(
                ex_type='out_of_bounds',
                params={'h': i, 'w': j},
                status=1
            )

    def get_slot_index(self, i, j):
        slot_index = self.board[i][j]
        return slot_index

    def status_reset(self):
        self.status = 1

    def _exception_message(self, ex_type='', params={}):
        error = ''
        if ex_type == 'out_of_bounds':
            h = params.get('h', None)
            w = params.get('w', None)
            error = f'ERROR. coordinates [{h}, {w}] outside of grid boundary {self.dim()}.'
        elif ex_type == 'slot_unavailable':
            h = params.get('h', None)
            w = params.get('w', None)
            car_id = params.get('car_id', None)
            error = f'ERROR. coordinate [{h}, {w}] is currently occupied by car:{car_id}.'
        elif ex_type == 'invalid':
            h = params.get('h', None)
            w = params.get('w', None)
            error = f'ERROR. grid [{h}, {w}] is not valid. [h, w] must be positive integers.'
        elif ex_type == 'invalid_board':
            msg = params.get('msg', '')
            error = f'ERROR. board invalid. {msg}'
        return error

    def _exception_handle(self, ex_type='', params={}, status=-1):
        error = self._exception_message(ex_type=ex_type, params=params)
        self.status = status
        self.error = error


class Car(object):
    name = ''
    position = []
    direction = 'N'
    next_moves = ''
    _state = 1
    result = ''
    status = 1
    error = ''
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.direction = kwargs.get('direction', '')
        self.next_moves = kwargs.get('moves', '')
        pos_coord = kwargs.get('position', {})
        if pos_coord:
            pos_x = int(pos_coord.get('x', None)) if pos_coord.get('x', None) else None
            pos_y = int(pos_coord.get('y', None)) if pos_coord.get('y', None) else None
            self.position = [pos_x, pos_y]

        valid_response = self.valid_check()
        self.status = valid_response.get('success', -1)
        if self.status == -1:
            self.error = valid_response.get('error', '')

    def to_dict(self):
        params = {
            'name': self.name,
            'position': self.position,
            'direction': self.direction,
            'moves': self.next_moves
        }
        return params

    def valid(self):
        valid_response = self.valid_check()
        return valid_response.get('success', -1) == 1

    def valid_check(self, property=''):
        error = ''
        if property == '':
            properties = [
                'name',
                'position',
                'direction',
                'moves'
            ]
            props_success = []
            props_errors = []
            for p in properties:
                prop_response = self.valid_check(property=p)
                prop_success = prop_response.get('success', -1)
                props_success.append(prop_success)
                if prop_success != 1:
                    prop_error = prop_response.get('error', '')
                    props_errors.append({p: f'ERROR. invalid property {prop_error}'})
            success = 1 if all([s == 1 for s in props_success]) else -1
            error = str(props_errors)                    
        else:
            if property == 'name':
                success = 1 if self.name else -1
                if success == -1:
                    error = 'blank name'
            elif property == 'position':
                if (isinstance(self.position, list) and
                    len(self.position) == 2 and
                    all(isinstance(v, int) and v >= 0 for v in self.position)):
                    success = 1
                    error = ''
                else:
                    success = -1
                    error = f'position must be two positive integers. got {self.position}'
            elif property == 'direction':
                if self.direction in ['N', 'E', 'S', 'W']:
                    success = 1
                    error = ''
                else:
                    success = -1
                    error = f"direction must be one of [N, E, S, W]. got '{self.direction}'"
            elif property == 'moves':
                valid_moves = set('LRF')
                if all(c in valid_moves for c in self.next_moves):
                    success = 1
                    error = ''
                else:
                    success = -1
                    error = f"moves must only contain L, R, F. got '{self.next_moves}'"
            else:
                success = -1
                error = f'invalid property name {property}'

        valid_response = {
            'success': success,
            'error': error
        }
        return valid_response

    def status_reset(self):
        self.status = 1

    def __repr__(self):
        return f'Car({self.name})'


class Case(object):
    grid = Grid
    cars = Dict[int, Car]
    status = int
    error = str
    def __init__(self, grid:Grid, cars={}):
        self.grid = grid
        self.cars = cars
        self.status = 1
        self.error = ''

    def to_dict(self):
        grid_dict = self.grid.to_dict()
        cars_dict = {k: v.to_dict() for k,v in self.cars.items()} if self.cars else {}
        params = {
            'grid': grid_dict,
            'cars': cars_dict,
        }
        return params

    def get_car(self, car_id):
        if car_id in self.cars:
            return self.cars[car_id]
        else:
            raise ValueError(f'ERROR. car with id {car_id} does not exist.')

    def car_add(self, car:Car):
        success = -1
        error = ''
        car_names = [c.name for c in self.cars.values()]
        max_id = max(self.cars.keys()) if self.cars else 0
        if car.valid():
            if car.name not in car_names:
                pos_h = car.position[0]
                pos_w = car.position[1]
                car_id = max_id + 1
                if self.grid.valid():
                    if self.grid.valid_coordinates(pos_h, pos_w):
                        if self.grid.slot_available(pos_h, pos_w):
                            success = self.grid.car_add(car_id, pos_h, pos_w)
                            if success == 1:
                                self.cars[car_id] = car
                            else:
                                error = self.grid.error
                        else:
                            success = -1                        
                            occupied_id = self.grid.get_slot_index(pos_h, pos_w)
                            car_name = self.get_car(occupied_id).name
                            error = self.grid._exception_message(ex_type='slot_unavailable', params={'h': pos_h, 'w': pos_w, 'car_id': car_name})
                    else:
                        success = -1                        
                        error = self.grid._exception_message(ex_type='out_of_bounds', params={'h': pos_h, 'w': pos_w})
                else:
                    success = -1
                    error = f'ERROR. problem with the grid. {self.grid.error}'

            else:
                success = -1
                error = f'ERROR. failed to add car {car.name}. name already exists'
        else:
            success = -1
            invalid_response = car.valid_check()
            invalid_error = invalid_response.get('error', '')
            error = f'ERROR. failed to add car. car specification is invalid. {invalid_error}'

        response = {
            'success': success,
            'error': error
        }
        return response                

    def valid(self):
        grid_valid = self.grid.valid() if self.grid is not None else False
        cars_valid = all([c.valid() for c in self.cars.values()]) if self.cars else False
        return grid_valid and cars_valid


def case_from_dict(params):
    grid_params = params.get('grid', {})
    cars_dict = params.get('cars', {})
    if grid_params:
        grid = grid_from_dict(grid_params)
        if grid.valid():
            if cars_dict:
                cars = cars_from_dict(cars_dict)
                return Case(grid, cars=cars)
            else:
                return Case(grid)            
        else:
            raise ValueError(f"not a valid grid. {grid.error}. args passed {grid_params}")
    else:
        raise ValueError(f"case must contain a 'grid'. {params}")


def cars_from_dict(params):
    return {k:car_from_dict(v) for k,v in params.items()}


def car_from_dict(params):
    name = params.get('name', '')
    position = params.get('position', [])
    direction = params.get('direction', '')
    moves = params.get('moves', '')
    if name and position and direction and moves:
        car = Car(**params)
        if car.valid():
            return car
        else:
            invalid_response = car.valid_check()
            invalid_error = invalid_response.get('error', '')
            ex_msg = f'ERROR. invalid car specification. {invalid_error}'
            raise ValueError(ex_msg)
    else:
        raise ValueError(f"car must contain 'name' 'position', 'direction' and 'moves' keys. dictionary missing required parameters. {params}")


def case_to_matrix(case: Case) -> Tuple[List[int], np.ndarray, List[str], List[str], List[int]]:
    car_ids = sorted(case.cars.keys())
    A = np.array([[case.cars[i].position[0] for i in car_ids],
                  [case.cars[i].position[1] for i in car_ids]])
    directions = [case.cars[i].direction for i in car_ids]
    moves = [case.cars[i].next_moves for i in car_ids]
    states = [case.cars[i]._state for i in car_ids]
    return car_ids, A, directions, moves, states


def matrix_to_case(case: Case, car_ids: List[int], A: np.ndarray, directions: List[str], moves: List[str], states: List[int]):
    for idx, cid in enumerate(car_ids):
        car = case.cars[cid]
        car.position = [int(A[0, idx]), int(A[1, idx])]
        car.direction = directions[idx]
        car.next_moves = moves[idx]
        car._state = states[idx]


def linear_step(case: Case) -> List[Tuple[str, str, Tuple[int, int]]]:
    car_ids, A, directions, moves, states = case_to_matrix(case)
    collisions = []
    for idx, cid in enumerate(car_ids):
        if states[idx] != 1:
            continue
        if not moves[idx]:
            states[idx] = 0
            continue
        cmd = moves[idx][0]
        moves[idx] = moves[idx][1:]
        if cmd == 'L':
            directions[idx] = DIRECTION_LEFT[directions[idx]]
        elif cmd == 'R':
            directions[idx] = DIRECTION_RIGHT[directions[idx]]
        elif cmd == 'F':
            t = VECTOR_MOVE[directions[idx]]
            new_pos = A[:, idx] + t
            new_i, new_j = int(new_pos[0]), int(new_pos[1])
            if case.grid.valid_coordinates(new_i, new_j):
                occupant = case.grid.get_slot_index(new_i, new_j)
                if occupant != 0:
                    other_idx = car_ids.index(occupant)
                    states[idx] = 2
                    states[other_idx] = 2
                    collisions.append((case.cars[cid].name, case.cars[occupant].name, (new_i, new_j)))
                else:
                    case.grid.car_move(cid, [int(A[0, idx]), int(A[1, idx])], [new_i, new_j])
                    A[:, idx] = new_pos
            # ignore move if boundary violation
    matrix_to_case(case, car_ids, A, directions, moves, states)
    state_save()
    return collisions


def grid_from_dict(params):
    height = params.get('height', None)
    width = params.get('width', None)
    board = params.get('board', [])
    if height and width:
        if board:
            return Grid(height, width, board=board)
        else:
            return Grid(height, width)
    else:
        raise ValueError(f"grid must contain 'height' and 'width' keys. dictionary missing required parameters. {params}")


# module variables -----------------------------------------------------------------
case_main = None


# main -----------------------------------------------------------------------------
def state_refresh():
    state.refresh()


def state_load():
    global case_main
    state.load()

    # 01 load Case
    case_dict = state.sim_state.copy()
    if case_dict:
        case_main = case_from_dict(case_dict)


def state_save():
    # 01 save Case
    if case_main:
        case_dict = case_main.to_dict()
        state.sim_state = case_dict
    state.save()


def setup():
    print('Simulation setup: ## UNDER CONSTRUCTIONS##')
    response = {
        'success': 1
    }
    return response


def run():
    global case_main
    if not case_main:
        state_load()
    success = -1
    error = ''
    msg = ''
    if not case_main or not case_main.grid or not case_main.cars:
        error = 'ERROR. simulation not properly setup.'
    else:
        step = 0
        collisions_all = []
        while True:
            active = [c for c in case_main.cars.values() if c._state == 1 and c.next_moves]
            if not active:
                break
            step += 1
            collisions = linear_step(case_main)
            for c1, c2, pos in collisions:
                collisions_all.append((c1, c2, step, pos))
        success = 1
        if collisions_all:
            lines = [f"- {c1}, collides with {c2} at ({pos[0]},{pos[1]}) at step {st}" for c1, c2, st, pos in collisions_all]
            msg = 'After simulation, the result is:\n' + '\n'.join(lines)
        else:
            lines = [f"- {car.name}, ({car.position[0]},{car.position[1]}) {car.direction}" for car in case_main.cars.values()]
            msg = 'After simulation, the result is:\n' + '\n'.join(lines)
    response = {
        'success': success,
        'error': error,
        'msg': msg
    }
    return response


def grid_create(**kwargs):
    global case_main
    create_success = -1
    error = ''
    grid_height_str = kwargs.get('h', None)
    grid_width_str = kwargs.get('w', None)
    if grid_height_str and grid_width_str:
        try:
            grid_height_int = int(grid_height_str)
            grid_width_int = int(grid_width_str)
            grid = Grid(grid_height_int, grid_width_int)
        except Exception as e:
            create_success = -1
            error = f"ERROR. failed to create grid from height {grid_height_str} and width {grid_width_str}.{e}"
        else:
            if grid.valid():
                case_main = Case(grid)
                state_save()
                create_success = 1
            else:
                create_success = -1
                error = f"ERROR. failed to create grid from height {grid_height_str} and width {grid_width_str}.{grid.error}"
    else:
        create_success = -1
        error = f"ERROR. input must have a height 'h' and width 'w'. passed {kwargs}"

    response = {
        'success': create_success,
        'params': kwargs,
        'error': error
    }
    return response


def car_add(**kwargs):
    success = -1
    error = ''
    try:
        car = car_from_dict(kwargs)
    except Exception as e:
        error = f'ERROR. failed to add car. invalid specifications: {kwargs}. {e}'
        response = {
            'success': success,
            'params': kwargs,
            'error': error
        }
    else:
        response = case_main.car_add(car)
        if response['success'] == 1:
            state_save()
        response['params'] = kwargs        

    return response


def add(a, b):
    return a + b
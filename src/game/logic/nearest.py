from typing import Optional, Tuple, List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import clamp
from random import randint
from math import log2

# constants
MAX_INT: int = float("inf")

# Naive Shortest Distance
# Util Functions
# TODO: return manhattan distance of two points with position as parameters
def count_pos_dist(p1: Position, p2: Position) -> int:
  return abs(p2.x - p1.x) + abs(p2.y - p1.y)

# TODO: get minimum distance between two points while considering the distance from portal
def get_minimum_dist(curr: Position, dest: Position, teleport_list: List[GameObject], board_width: int, board_height: int) -> Tuple[int, Position, bool]:
  # count distance without portal
  curr_dist: int = count_pos_dist(curr, dest)
  init_curr_dist = curr_dist
  curr_target: Position = dest
  use_portal: bool = False

  # check edge cases
  # consider y-axis
  if (curr.x <= teleport_list[0].position.x <= dest.x or curr.x >= teleport_list[0].position.x >= dest.x) and (curr.x <= teleport_list[1].position.x <= dest.x or curr.x >= teleport_list[1].position.x >= dest.x):
    if curr.y == dest.y:
      if teleport_list[0].position.y == dest.y:
        if teleport_list[1].position.y == teleport_list[0].position.y:
          curr_dist += 2
        elif teleport_list[1].position.y == teleport_list[0].position.y - 1:
          if curr.y + 1 < board_height:
            curr_dist += 2
          else:
            curr_dist += 4
            if teleport_list[1].position.x == dest.x:
              curr_dist += 2
        elif teleport_list[1].position.y == teleport_list[0].position.y + 1:
          if curr.y - 1 >= 0:
            curr_dist += 2
          else:
            curr_dist += 4
            if teleport_list[1].position.x == dest.x:
              curr_dist += 2        
      elif teleport_list[1].position.y == dest.y:
        if teleport_list[1].position.y == teleport_list[0].position.y:
          curr_dist += 2
        elif teleport_list[1].position.y - 1 == teleport_list[0].position.y:
          if curr.y + 1 < board_height:
            curr_dist += 2
          else:
            curr_dist += 4
            if teleport_list[0].position.x == dest.x:
              curr_dist += 2
        elif teleport_list[1].position.y + 1 == teleport_list[0].position.y:
          if curr.y - 1 >= 0:
            curr_dist += 2
          else:
            curr_dist += 4  
            if teleport_list[0].position.x == dest.x:
              curr_dist += 2          
    elif curr.y == dest.y - 1:
      if curr.y == teleport_list[0].position.y and dest.y == teleport_list[1].position.y:
        curr_dist += 3
        if dest.y + 1 >= board_height and teleport_list[0].position.x == dest.x:
          curr_dist += 2
      elif curr.y == teleport_list[1].position.y and dest.y == teleport_list[0].position.y:
        curr_dist += 3
        if dest.y + 1 >= board_height and teleport_list[1].position.x == dest.x:
          curr_dist += 2
    elif curr.y == dest.y + 1:
      if curr.y == teleport_list[0].position.y and dest.y == teleport_list[1].position.y:
        curr_dist += 3
        if dest.y - 1 < 0 and teleport_list[0].position.x == dest.x:
          curr_dist += 2
      elif curr.y == teleport_list[1].position.y and dest.y == teleport_list[0].position.y:
        curr_dist += 3
        if dest.y - 1 < 0 and teleport_list[1].position.x == dest.x:
          curr_dist += 2

  # consider x-axis
  if (curr.y <= teleport_list[0].position.y <= dest.y or curr.y >= teleport_list[0].position.y >= dest.y) and (curr.y <= teleport_list[1].position.y <= dest.y or curr.y >= teleport_list[1].position.y >= dest.y) and curr_dist == init_curr_dist:
    if curr.x == dest.x:
      # consider the first teleport
      if teleport_list[0].position.x == dest.x:
        if teleport_list[1].position.x == teleport_list[0].position.x:
          curr_dist += 2
        elif teleport_list[1].position.x == teleport_list[0].position.x - 1:
          if curr.x + 1 < board_width:
            curr_dist += 2
          else:
            curr_dist += 4
            if teleport_list[1].position.y == dest.y:
              curr_dist += 2
        elif teleport_list[1].position.x == teleport_list[0].position.x + 1:
          if curr.x - 1 >= 0:
            curr_dist += 2
          else:
            curr_dist += 4
            if teleport_list[1].position.y == dest.y:
              curr_dist += 2
      # consider the second teleport
      elif teleport_list[1].position.x == dest.x:
        if teleport_list[1].position.x == teleport_list[0].position.x:
          curr_dist += 2
        elif teleport_list[1].position.x - 1 == teleport_list[0].position.x:
          if curr.x + 1 < board_width:
            curr_dist += 2
          else:
            curr_dist += 4
            if teleport_list[0].position.y == dest.y:
              curr_dist += 2
        elif teleport_list[1].position.x + 1 == teleport_list[0].position.x:
          if curr.x - 1 >= 0:
            curr_dist += 2
          else:
            curr_dist += 4  
            if teleport_list[0].position.y == dest.y:
              curr_dist += 2
    elif curr.x == dest.x - 1:
      if curr.x == teleport_list[0].position.x and dest.x == teleport_list[1].position.x:
        curr_dist += 3
        if dest.x + 1 >= board_width and teleport_list[0].position.y == dest.y:
          curr_dist += 2
      elif curr.x == teleport_list[1].position.x and dest.x == teleport_list[0].position.x:
        curr_dist += 3
        if dest.x + 1 >= board_width and teleport_list[1].position.y == dest.y:
          curr_dist += 2
    elif curr.x == dest.x + 1:
      if curr.x == teleport_list[0].position.x and dest.x == teleport_list[1].position.x:
        curr_dist += 3
        if dest.x - 1 < 0 and teleport_list[0].position.y == dest.y:
          curr_dist += 2
      elif curr.x == teleport_list[1].position.x and dest.x == teleport_list[0].position.x:
        curr_dist += 3
        if dest.x - 1 < 0 and teleport_list[1].position.y == dest.y:
          curr_dist += 2     

  # count distance by using portal
  for i in range(2):
    dist = count_pos_dist(curr, teleport_list[i].position) + count_pos_dist(dest, teleport_list[1 - i].position)
    if dist < curr_dist:
      use_portal = True
      curr_dist = dist
      curr_target = teleport_list[i].position
  return curr_dist, curr_target, use_portal

# TODO: randomize delta_x and delta_y for determining next position
def randomize_position(delta_x: int, delta_y: int) -> Tuple[int, int]:
  random_number = randint(0, 1)
  if random_number == 0:
    return (0, delta_y)
  else:
    return (delta_x, 0)

# TODO: get direction while considering teleport location
def get_direction_position(curr: Position, dest: Position, teleport_list: List[GameObject], avoid: bool, width: int, height: int):
  delta_x = clamp(dest.x - curr.x, -1, 1)
  delta_y = clamp(dest.y - curr.y, -1, 1)
  tel1_pos = teleport_list[0].position
  tel2_pos = teleport_list[1].position

  if delta_x == 0 and delta_y == 0:
    return get_random_move(curr, width, height)

  if delta_y == 0 and avoid:
    if (tel1_pos.y == curr.y and tel1_pos.x == curr.x + delta_x) or (tel2_pos.y == curr.y and tel2_pos.x == curr.x + delta_x):
      if curr.y + 1 < height:
        delta_x = 0
        delta_y = 1
      else:
        delta_x = 0
        delta_y = -1
  elif delta_x == 0 and avoid:
    if (tel1_pos.x == curr.x and tel1_pos.y == curr.y + delta_y) or (tel2_pos.x == curr.x and tel2_pos.y == curr.y + delta_y):
      if curr.x + 1 < width:
        delta_y = 0
        delta_x = 1
      else:
        delta_y = 0
        delta_x = -1
  elif delta_y != 0 and delta_x != 0:
    if avoid:
      if curr.x + delta_x == tel1_pos.x and tel1_pos.x == dest.x and (curr.y < tel1_pos.y < dest.y or curr.y > tel1_pos.y > dest.y): 
        delta_x = 0
      elif curr.x + delta_x == tel2_pos.x and tel2_pos.x == dest.x and (curr.y < tel2_pos.y < dest.y or curr.y > tel2_pos.y > dest.y): 
        delta_x = 0
      elif curr.y + delta_y == tel1_pos.y and tel1_pos.y == dest.y and (curr.x < tel1_pos.x < dest.x or curr.x > tel1_pos.x > dest.x): 
        delta_y = 0
      elif curr.y + delta_y == tel2_pos.y and tel2_pos.y == dest.y and (curr.x < tel2_pos.x < dest.x or curr.x > tel2_pos.x > dest.x): 
        delta_y = 0  
      elif curr.x + delta_x == tel1_pos.x and curr.y == tel1_pos.y:
        delta_x = 0
      elif curr.x + delta_x == tel2_pos.x and curr.y == tel2_pos.y:
        delta_x = 0
      elif curr.x == tel1_pos.x and curr.y + delta_y == tel1_pos.y:
        delta_y = 0
      elif curr.x == tel2_pos.x and curr.y + delta_y == tel2_pos.y:
        delta_y = 0   
      else:
        # give random effect to movement
        delta_x, delta_y = randomize_position(delta_x, delta_y)
    else: 
      # give random effect to movement
      delta_x, delta_y = randomize_position(delta_x, delta_y)
  return delta_x, delta_y

# TODO: get all shortest diamond distance with its base distance
def get_all_diamonds_dist(diamonds: List[GameObject], teleports: List[GameObject], base: Position,width: int, height: int) -> List[List[int]]:
  n: int = len(diamonds)
  if n == 0:
    return []
  res = [[MAX_INT, MAX_INT, 0] for _ in range(n)]
  for i in range(n):
    base_dist, _, _ = get_minimum_dist(diamonds[i].position, base, teleports, width, height)
    res[i][1] = base_dist
    for j in range(i + 1, n):
      dist, _, _ = get_minimum_dist(diamonds[i].position, diamonds[j].position, teleports, width, height) 
      if dist < res[i][0]:
        res[i][0] = dist
        res[i][2] = j
      if dist < res[j][0]:
        res[j][0] = dist
        res[j][2] = i
  return res

# TODO: check is two positions are equal
def is_position_equal(p1: Position, p2: Position) -> bool:
  return p1.x == p2.x and p1.y == p2.y

def is_position_in_area(base: Position, dest: Position, query_obj: Position) -> bool:
  if base.x == query_obj.x and base.y == query_obj.y:
    return False
  check_x = base.x <= query_obj.x <= dest.x or base.x >= query_obj.x >= dest.x
  check_y = base.y <= query_obj.y <= dest.y or base.y >= query_obj.y >= dest.y
  return check_x and check_y

# TODO: pick optimal diamond
def pick_optimal_diamond(curr_pos: Position, diamond_list: List[GameObject], teleport_list: List[GameObject], diamond_dist_list: List[List[int]], num_of_diamond_needed: int, width: int, height: int) -> Tuple[Position, bool]:
  min_score = MAX_INT
  is_portal_used = False
  selected_diamond = None
  diamond_len = len(diamond_list)

  for i in range(diamond_len):
    # skip if diamond point is greater than number of needed diamond
    if diamond_list[i].properties.points > num_of_diamond_needed:
      continue
    # get current distance to diamond
    curr_dist, curr_target, curr_is_portal_used = get_minimum_dist(curr_pos, diamond_list[i].position, teleport_list, width, height)
    # calculate current score based on number of diamond needed
    d_needed = num_of_diamond_needed - diamond_list[i].properties.points
    base_dist = diamond_dist_list[i][1]
    if num_of_diamond_needed == 1:
      curr_score = curr_dist + base_dist
    elif num_of_diamond_needed == 2:
      if d_needed != 0 and diamond_len > 1:
        curr_score = curr_dist + diamond_dist_list[i][0] + diamond_dist_list[diamond_dist_list[i][2]][1]
      else:
        curr_score = curr_dist + base_dist
    else:
      curr_score = curr_dist
    if curr_score < min_score:
      min_score = curr_score
      selected_diamond = curr_target
      is_portal_used = curr_is_portal_used

  return selected_diamond, is_portal_used

# TODO: get random move from current position
def get_random_move(curr_pos: Position, width: int, height: int):
  if curr_pos.x + 1 < width:
    return 1, 0
  elif curr_pos.x - 1 >= 0:
    return -1, 0
  elif curr_pos.y + 1 < height:
    return 0, 1
  else:
    return 0, -1

# TODO: take the nearest diamond with some considerations
class MeowNearestDiamond(BaseLogic):
  def __init__(self) -> None:
    self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    self.goal_position: Optional[Tuple[int, int]] = None
    self.current_direction = 0
  
  def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int]:
    props = board_bot.properties
    # initialize variables needed
    curr_pos: Position = board_bot.position
    curr_points: int = props.diamonds
    width: int = board.width
    height: int = board.height
    base_pos: Position = board_bot.properties.base
    remaining_time: int = props.milliseconds_left // 1000
    inventory_size: int = props.inventory_size

    # initialize object lists
    teleport_list: List[GameObject] = []
    diamond_list: List[GameObject] = []
    red_button: GameObject = None

    # get all object list
    for obj in board.game_objects:
      if obj.type == "TeleportGameObject":
        teleport_list.append(obj)
      elif obj.type == "DiamondGameObject":
        diamond_list.append(obj)
      elif obj.type == "DiamondButtonGameObject":
        red_button = obj
    
    diamond_dist_list = get_all_diamonds_dist(diamond_list, teleport_list, base_pos, width, height)
    base_dist, base_target, base_use_portal = get_minimum_dist(curr_pos, base_pos, teleport_list, width, height)
    diamond_picked, is_portal_used = pick_optimal_diamond(curr_pos, diamond_list, teleport_list, diamond_dist_list, inventory_size - curr_points, width, height)
    if remaining_time < base_dist + 2:
      # if current points is not equal to zero, go to the base
      if (curr_points != 0):
        if (0 < curr_points < inventory_size and diamond_picked != None and not is_portal_used and is_position_in_area(curr_pos, base_target, diamond_picked)):
          return get_direction_position(curr_pos, diamond_picked, teleport_list, True, width, height)
        elif (is_position_in_area(curr_pos, base_target, red_button.position)):
          return get_direction_position(curr_pos, red_button.position, teleport_list, True, width, height)
        else:
          return get_direction_position(curr_pos, base_target, teleport_list, not base_use_portal, width, height)
      else:
        # will be updated
        # attack other player if possible
        return get_direction_position(curr_pos, diamond_picked, teleport_list, not is_portal_used, width, height)
    else:
      if (curr_points < inventory_size):
        if diamond_picked != None:
          # check if base is in the area
          if is_position_in_area(curr_pos, diamond_picked, base_pos):
            return get_direction_position(curr_pos, base_pos, teleport_list, True, width, height)
          # check if red button is in the area
          elif is_position_in_area(curr_pos, diamond_picked, red_button.position):
            return get_direction_position(curr_pos, red_button.position, teleport_list, True, width, height)
          else:
            return get_direction_position(curr_pos, diamond_picked, teleport_list, not is_portal_used, width, height)
        else:
          return get_direction_position(curr_pos, base_target, teleport_list, not base_use_portal, width, height)
      else:
        return get_direction_position(curr_pos, base_target, teleport_list, not base_use_portal, width, height)
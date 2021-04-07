import pygame
import math
import sys
import datetime

clock = pygame.time.Clock()
name = input("what is file name")
try:
	maze = pygame.image.load(name)
except:
	print("There was an error with the file or file name.")
	sys.exit()
mazelist =[]
size = maze.get_size()
for x in range(size[0]):
	row = []
	for y in range(size[1]):
		if maze.get_at((x,y)) == (255,0,0):
			start = (x,y)
		elif maze.get_at((x,y)) == (0,0,255):
			goal = (x,y)
		if maze.get_at((x, y)) == (0, 0, 0):
			row.append(1)
		else:
			row.append(0)
	mazelist.append(row)

boxsize = 700 // size[0], 700 // size[1]
screen = pygame.display.set_mode((boxsize[0]*size[0],boxsize[1]*size[1]))
pygame.display.set_caption("a*")
pygame.init()
# screen = pygame.display.set_mode((boxsize[0]*size[0],boxsize[1]*size[1]))
# pygame.display.set_caption("a*")


def handleInput():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()


def pathconstruct(node, grid):
	path = []
	x = node
	while True:
		if (grid[x[0]][x[1]].camefrom) != 0:
			path.append(grid[x[0]][x[1]].camefrom)
			x = grid[x[0]][x[1]].camefrom
		else:
			return path


def drawones(grid, start, goal, openset, closeset, win, scren = 0):
	if scren != 0:
		screen = scren
	path = pathconstruct(win, grid)
	for x in range(len(grid)):
		for y in range(len(grid[0])):
			if (x, y) == start:
				pygame.draw.rect(screen, (255, 0, 255), (((boxsize[0]) * x, (boxsize[1]) * y), boxsize))
			elif (x, y) == goal:
				pygame.draw.rect(screen, (255, 255, 0), (((boxsize[0]) * x, (boxsize[1]) * y), boxsize))
			elif (x, y) in path:
				pygame.draw.rect(screen, (0, 0, 255), (((boxsize[0]) * x, (boxsize[1]) * y), boxsize))
			elif (x, y) in openset:
				pygame.draw.rect(screen, (0, 255, 0), (((boxsize[0]) * x, (boxsize[1]) * y), boxsize))
			elif (x, y) in closeset:
				pygame.draw.rect(screen, (255, 0, 0), (((boxsize[0]) * x, (boxsize[1]) * y), boxsize))
			elif grid[x][y].wall:
				pygame.draw.rect(screen, (0, 0, 0), (((boxsize[0]) * x, (boxsize[1]) * y), boxsize))
			else:
				pygame.draw.rect(screen, (255, 255, 255), (((boxsize[0]) * x, (boxsize[1]) * y), boxsize))
	return path

def draw(grid,openset,closeset,win,screen,lastpath):
	path = pathconstruct(win, grid)
	for x in closeset:
		pygame.draw.rect(screen,(255,0,0),(((boxsize[0]) * x[0], (boxsize[1]) * x[1]), boxsize))
	for x in openset:
		pygame.draw.rect(screen,(0,255,0),(((boxsize[0]) * x[0], (boxsize[1]) * x[1]), boxsize))
	for x in lastpath:
		pygame.draw.rect(screen,(255,0,0),(((boxsize[0]) * x[0], (boxsize[1]) * x[1]), boxsize))
	for x in path:
		pygame.draw.rect(screen,(0,0,255),(((boxsize[0]) * x[0], (boxsize[1]) * x[1]), boxsize))
	return path

def herostic(node, end):
	return ((((end[0] - node[0]) ** 2) + ((end[1] - node[1]) ** 2)) ** 0.5)


class spot:
	def __init__(self, i, j, grid, start, goal, wall):
		self.wall = wall
		self.i = i
		self.j = j
		if not wall:
			if start[0] == i and start[1] == j:
				self.f = herostic(start, goal)
				self.g = 0
			else:
				self.f = math.inf
				self.g = math.inf
			self.neighbor = 0
			self.camefrom = 0

	def neighborfind(self, grid):
		neighbor = []
		if self.i > 0:
			if not grid[self.i - 1][self.j].wall:
				neighbor.append((self.i - 1, self.j))
			if self.i < len(grid) - 1:
				if not grid[self.i + 1][self.j].wall:
					neighbor.append((self.i + 1, self.j))
		else:
			if not grid[self.i + 1][self.j].wall:
				neighbor.append((self.i + 1, self.j))

		if self.j > 0:
			if not grid[self.i][self.j - 1].wall:
				neighbor.append((self.i, self.j - 1))
			if self.j < len(grid[0]) - 1:
				if not grid[self.i][self.j + 1].wall:
					neighbor.append((self.i, self.j + 1))
		else:
			if not grid[self.i][self.j + 1].wall:
				neighbor.append((self.i, self.j + 1))

		return neighbor

def astar(start, goal):
	openset = []
	closeset = []
	grid = []
	for x in range(size[0]):
		row = []
		for y in range(size[1]):
			row.append(spot(x, y, size, start, goal, mazelist[x][y]))
		grid.append(list(row))

	for x in range(size[0]):
		for y in range(size[1]):
			grid[x][y].neighbor = grid[x][y].neighborfind(grid)

	openset.append(start)
	win = start
	over = False
	print('wait')
	lastpath = drawones(grid, start, goal, openset, closeset, win, screen)
	closeset2 = []
	openset2 = []
	while True:
		handleInput()
		lastpath = draw(grid,openset2,closeset2,win,screen,lastpath)
		closeset.extend(closeset2)
		openset.extend(openset2)
		closeset2 = []
		openset2 = []
		if len(openset) < 1 and not over:
			over = True
			print("There is no path")
		pygame.display.flip()
		if not over:
			win = openset[0]
			for x in openset:
				if grid[x[0]][x[1]].f < grid[win[0]][win[1]].f:
					win = x
			if win == goal:
				lastpath = draw(grid,openset2, closeset2, win, screen,lastpath)
				closeset.extend(closeset2)
				openset.extend(openset2)
				pygame.display.flip()
				pygame.image.save(screen, str(datetime.datetime.now().strftime("%d %m %Y %H %M %S") + ".png"))
				over = True

			openset.remove(win)
			closeset2.append(win)
			for neighbor in grid[win[0]][win[1]].neighbor:
				tentative_gScore = grid[win[0]][win[1]].g + 1
				if tentative_gScore < grid[neighbor[0]][neighbor[1]].g:
					grid[neighbor[0]][neighbor[1]].camefrom = win
					grid[neighbor[0]][neighbor[1]].g = tentative_gScore
					grid[neighbor[0]][neighbor[1]].f = grid[neighbor[0]][neighbor[1]].g + herostic(neighbor, goal)
					if neighbor not in openset:
						openset2.append(neighbor)
						if neighbor in closeset:
							closeset.remove(neighbor)


astar(start, goal)

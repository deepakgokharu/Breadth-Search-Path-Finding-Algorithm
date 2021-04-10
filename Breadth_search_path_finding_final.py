import pygame
from queue import Queue

pygame.init()

#global variables
white = (255,255,255)
color = [(0,0,0),(128,128,128)]
black = (0,0,0)
red = (255,0,0)
grey = (128,128,128)
green = (0,255,0)
light_grey = (220,220,220)
cells = (20,40)
cell_width,cell_height = 20,20
font_size = 26
option_height = 30
edge_width = 5
white_line_height = 3
screen_dim = (cells[1]*cell_width+(cells[1]+1)*edge_width,option_height+white_line_height+cells[0]*cell_height+(cells[0]+1)*edge_width)
white_line = (0,option_height,screen_dim[0],white_line_height)
matrix = [[-1 for i in range(cells[1])] for j in range(cells[0])]
keyboard_codes_nums = [pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]
run = True
start_pos = (3*cell_width-5,0,50,option_height-10)
mousepushed = False
visualise = True

#global functions
def next_cell(i,j,x,y):
	if (i+cell_width+edge_width)>=screen_dim[0]:
		return edge_width,j+cell_height+edge_width,x+1,0
	return i+cell_width+edge_width,j,x,y+1

def create_cell(i,j,color):
	pygame.draw.rect(screen,color,(i,j,cell_width,cell_height))

def draw_grid():
	screen.fill(white)
	#creating button
	start = font.render('Start',True,black,None)
	pygame.draw.rect(screen,light_grey,(3*cell_width-5,0,50,option_height-10))
	screen.blit(start,(3*cell_width,(option_height-font_size)/2))
	#done
	pygame.draw.rect(screen,black,white_line)
	x,y,i,j = edge_width,edge_width+option_height+white_line_height,0,0
	while x<screen_dim[0] and y<screen_dim[1]:
		create_cell(x,y,color[matrix[i][j]])
		#pygame.display.flip()
		#pygame.time.delay(100)
		x,y,i,j = next_cell(x,y,i,j)

def get_cell_coordinates(h,w):
	return edge_width+w*(cell_width+edge_width),option_height+white_line_height+edge_width+h*(cell_height+edge_width)
	

def solve():
	q = Queue()
	#print(matrix)
	matrix[0][0]=1
	q.put([0,0])
	while(not q.empty()):
		top_i,top_j = q.get()
		x,y = get_cell_coordinates(top_i,top_j)
		rect = (x,y,cell_width,cell_height)
		pygame.draw.rect(screen,green,rect)
		pygame.display.update(rect)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		if visualise:
			pygame.time.delay(10)
		if top_i == (cells[0]-1) and top_j == (cells[1]-1):
			break
		dis = matrix[top_i][top_j]
		#right direction
		temp_i,temp_j = top_i,top_j+1
		if 0<=temp_i<cells[0] and 0<=temp_j<cells[1] and matrix[temp_i][temp_j] == -1:
				q.put([temp_i,temp_j])
				matrix[temp_i][temp_j]=dis+1
		#down direction
		temp_i,temp_j = top_i+1,top_j
		if 0<=temp_i<cells[0] and 0<=temp_j<cells[1] and matrix[temp_i][temp_j] == -1:
				q.put([temp_i,temp_j])
				matrix[temp_i][temp_j]=dis+1
		#left direction
		temp_i,temp_j = top_i,top_j-1
		if 0<=temp_i<cells[0] and 0<=temp_j<cells[1] and matrix[temp_i][temp_j] == -1:
				q.put([temp_i,temp_j])
				matrix[temp_i][temp_j]=dis+1
		#up direction
		temp_i,temp_j = top_i-1,top_j
		if 0<=temp_i<cells[0] and 0<=temp_j<cells[1] and matrix[temp_i][temp_j] == -1:
				q.put([temp_i,temp_j])
				matrix[temp_i][temp_j]=dis+1


def show_path(i,j):
	x,y = get_cell_coordinates(i,j)
	rect = (x,y,cell_width,cell_height)
	pygame.draw.rect(screen,red,rect)
	pygame.display.update(rect)
	pygame.time.delay(30)
	if i==0 and j==0:
		return
	dis = matrix[i][j]-1
	if i>0 and matrix[i-1][j]==dis:
		show_path(i-1,j)
	elif j>0 and matrix[i][j-1] == dis:
		show_path(i,j-1)
	elif i<(cells[0]-1) and matrix[i+1][j] == dis:
		show_path(i+1,j)
	elif j<(cells[1]-1) and matrix[i][j+1] == dis:
		show_path(i,j+1)



#screen initialiser
screen = pygame.display.set_mode(screen_dim)
pygame.display.set_caption('Breadth Search Path Finding Algorithm (from first cell to last cell)')
screen.fill(light_grey)
font = pygame.font.Font(None,font_size)
draw_grid()
pygame.display.flip()

while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			if start_pos[0]<=pos[0]<(start_pos[0]+start_pos[2]) and start_pos[1]<=pos[1]<(start_pos[1]+start_pos[3]):
				solve()
				show_path(cells[0]-1,cells[1]-1)
				temp = True
				while temp:
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							temp=False
				run = False
			if pos[1]>(option_height+white_line_height):
				mousepushed = True
		elif event.type == pygame.MOUSEBUTTONUP:
			mousepushed = False
		pos = pygame.mouse.get_pos()
		i,j = (pos[0]-edge_width)//(cell_width+edge_width),(pos[1]-option_height-white_line_height-edge_width)//(cell_height+edge_width)
		if i>=0 and j>=0 and mousepushed:
			matrix[j][i]=0
	draw_grid()
	pygame.display.flip()

pygame.quit()
import numpy as np
import itertools

def read_in(fname):

	with open(fname, 'r') as f:
		return np.array([list(l.strip()) for l in f.readlines()])

def init_space(input_grid, ndim=3):
    NLAYERS = 20
    midl = NLAYERS // 2
    CELLS_PER_LAYER = len(input_grid) + 2*6
    iac = np.where(input_grid == '#')
    initial_active_coords = (iac[0] + 6, iac[1] + 6)

    if ndim == 3:
    	space = np.full((NLAYERS, CELLS_PER_LAYER, CELLS_PER_LAYER), '.')
	    space[midl][initial_active_coords] = '#'
	else:
		space = np.full((NLAYERS, NLAYERS, CELLS_PER_LAYER, CELLS_PER_LAYER), '.')
		space[midl, midl][initial_active_coords] = '#'

    return space

def get_neighbor_coords(xcoords, ndim=3):
    diffs = np.array(list(itertools.product([0,-1,1], repeat=ndim)))
    return diffs[1:] + xcoords

def one_cycle3d(space):
    next_space = space.copy()
    
    for i in range(space.shape[0]):
        for j in range(space.shape[1]):
            for k in range(space.shape[2]):
                curcube = space[i,j,k]
                neigh_coords = get_neighbor_coords([i,j,k])
                neighbor_values = [space[tuple(ncc)] for ncc in neigh_coords
                                   if (all(ncc > -1) and all(ncc < np.array(space.shape)))]
                
                
                nactive = np.where(np.array(neighbor_values) == '#')[0].size
    
                if curcube == '#' and nactive not in [2,3]:
                    next_space[i,j,k] = '.'
                elif curcube == '.' and nactive == 3:
                    next_space[i,j,k] = '#'
        
    return next_space
                    

def run_cycles3d(space):
    
    next_space = space
    
    for _ in range(6):
        next_space = one_cycle3d(next_space)
    
    nactive = np.where(next_space == '#')[0].size
    
    return nactive, next_space

input_grid = read_in('17.txt')
samp = read_in('17sample1.txt')
space3d = init_space(input_grid)    
nactive, res_space = run_cycles3d(space3d)
print('P1: ', nactive)
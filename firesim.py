import random

## class representation for each cell
class Cell:
    def __init__(self, x, y, time, veg_inten, wind_direc, wind_inten, fire_inten):
        self.x = x
        self.y = y
        self.time = time
        self.veg_inten = veg_inten # vegetation intensity (assuming the most intense, the more flammable; 0 means it can no longer catch on fire)
        self.wind_direc = wind_direc # wind direction
        self.wind_inten = wind_inten # wind intensity
        self.fire_inten = fire_inten # if there is a fire in the cell, how intensly is it burning
        
        
class AreaSimulation:
    def __init__(self, L):
        self.grid = {}
        self.hood = ((-1,-1), (-1,0), (-1,1),
                (0,-1),          (0, 1),
                (1,-1),  (1,0),  (1,1))
        self.L = L
    
    ## rewrite this
    def initialize(self):
        for x in range(self.L):
            for y in range(self.L):
                self.grid[(x,y)] = Cell(
                    x= x,
                    y= y,
                    time= 0,
                    veg_inten= random.random() + 0.1,
                    wind_direc= "right", ### not using this for now
                    wind_inten= random.random(),
                    fire_inten= 0.00    
                )
        ### now I'm going to "start" a fire in the upper left corner
        self.grid[(1,2)].fire_inten = .55
        self.grid[(1,1)].fire_inten = .60
        self.grid[(2,1)].fire_inten = .31
        
        return self.grid
    
    def gnew(self):
        newgrid = {}
        # iterate through all the cells
        for x in range(self.L):
            for y in range(self.L): 
                if self.grid[(x,y)].veg_inten == 0: # no fire is possible here
                    newgrid[(x,y)] = self.grid[(x,y)] ## need to update time
                elif self.grid[(x,y)].fire_inten > 0: # cell is burning
                    new_fire_inten = min(1, self.grid[(x,y)].fire_inten + .1)
                    newgrid[(x,y)] = Cell(
                        x= x,
                        y= y,
                        time= self.grid[(x,y)].time+1,
                        veg_inten= max(0,self.grid[(x,y)].veg_inten -.1), ## figure out a better way to decay
                        wind_direc= self.grid[(x,y)].wind_direc,
                        wind_inten= self.grid[(x,y)].wind_inten,
                        # some previous intensity and a combination of surrounding intensities 
                        fire_inten= round(new_fire_inten,2)   
                   )
                elif self.grid[(x,y)].fire_inten == 0: # cell is not burning but can catch (assuming cells don't randomly catch fire)
                    ## need to take into account the conditions of surrounding cells
                    total_inten = 0
                    for dx,dy in self.hood:
                        if (x+dx,y+dy) in self.grid:
                            total_inten += self.grid[(x+dx,y+dy)].fire_inten # will somehow need to handle the surrounding fire  
                    new_fire_inten = total_inten/8 * self.grid[(x,y)].veg_inten # to do: take into account wind somehow
                    newgrid[(x,y)] = Cell(
                        x= x,
                        y= y,
                        time= self.grid[(x,y)].time+1,
                        veg_inten= self.grid[(x,y)].veg_inten,
                        wind_direc= self.grid[(x,y)].wind_direc,
                        wind_inten= self.grid[(x,y)].wind_inten,
                        fire_inten= round(new_fire_inten,2)     
                   )
        self.grid = newgrid
        return newgrid

    ## printing functions
    def gprint(self):
        txt = '\n'.join(' * '.join(str(self.grid[(x,y)].fire_inten) for x in range(self.L))
                         for y in range(self.L))
        print(txt)
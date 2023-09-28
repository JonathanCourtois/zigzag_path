import numpy as np
import matplotlib.pyplot as plt

class area():
    def __init__(self, pcb_dim:tuple=(10.,10.), space_ant_dim:tuple=(0.,0.), space_ant_pos:tuple=(0.,0.), draw_dim:tuple=(0.,0.), draw_pos:tuple=(0.,0.),
                 margin:tuple=(0.,0.), align_to_pcb_diag:bool=False) -> None:
        """Generate all the area parameters
           All dim are tuple like (width,height) and pos like (x,y)
        """
        
        ### New Version
        # Get pcb parameters
        (self.pcb_w, self.pcb_h) = pcb_dim
        
        # Get space antenna parameters
        if space_ant_dim == (0,0):
            (self.space_ant_w,self.space_ant_h) = pcb_dim
        else:
            (self.space_ant_w,self.space_ant_h) = space_ant_dim
        
        # get margin options if needed
        (self.margin_x, self.margin_y) = margin
        
        # Get Draw area (the area where the computation will be done)
        if draw_dim == (0,0):
            (self.draw_w,self.draw_h) = space_ant_dim
        else:
            (self.draw_w,self.draw_h) = draw_dim
        
        # logic check : draw inside space ant inside pcb :
        self.maternel_rectangle_fit_exercice()
        
        # Set if the draw area diagonal must be parallel the pcb diagonal
        self.align_to_pcb_diag = align_to_pcb_diag
        if self.align_to_pcb_diag :
            pass
        
        #### OLD VERSION
        self.width  = self.draw_w
        self.height = self.draw_h
        self.diag   = np.sqrt(self.height**2 + self.width**2)
        # Diagonale angle (low_left angle of the rectangle) in °
        self.d_angle = np.rad2deg(np.arccos(self.width / self.diag))
        # angle, in °, of line from ordonate axis to abscisse axis -> link to director factor a of ax+b
        self.attack_angle = self.d_angle - np.rad2deg(np.pi/2)
            
        
    def maternel_rectangle_fit_exercice(self):
        # now logic draw area must be inside space antenna parameters, with boundaries. and they need to be inside pcb
        # start from outside - space_ant inside pcb
        if self.space_ant_w > self.pcb_w :
            self.space_ant_w = self.pcb_w
        if self.space_ant_h > self.pcb_h :
            self.space_ant_h = self.pcb_h
        # then draw area inside space_ant+boundaries
        if self.draw_w > self.space_ant_w - self.margin_x :
            self.draw_w = self.space_ant_w - self.margin_x               
        if self.draw_h > self.space_ant_h - self.margin_y :
            self.draw_h = self.space_ant_h - self.margin_y      

    def print(self):
        print(f"H : {self.height} | W : {self.width}")
        print(f"Diagonal length : {self.diag} | Diagonal angle elevation : {self.d_angle}°")
        print(f"Attack angle : {self.attack_angle}°")

class vertical_builder():
    def __init__(self, draw_area, nb_brin:int=1 , base_brin_length:int=3) -> None:
        self.base_brin_length   = base_brin_length
        self.draw_area          = draw_area
        self.nb_brin            = nb_brin

        self.a                  = 0
        self.b_init             = 0
        self.marge              = 0
        
        self.vertical_lines_factors     = list()
        # compute first line
        self.vertical_start_line()
        # compute middle lines
        if nb_brin > 1 :
            self.vertical_mid_lines()
        else:
            # search for last line
            self.vertical_end_line()

    def vertical_start_line(self):
        a =  np.tan(np.deg2rad(self.draw_area.attack_angle)) 

        b_init = (self.base_brin_length)*(np.cos(np.deg2rad(self.draw_area.attack_angle)))

        marge = np.sin(np.deg2rad(self.draw_area.attack_angle) + (np.pi/2)) * b_init

        self.marge = marge
        self.a      = a
        self.b_init = b_init
        self.vertical_lines_factors.append([a,b_init])

    def nb_brin_2_list_distance(self):
        # define empty list
        d_list = list()
        # variables
        D       = self.draw_area.diag
        D_p2    = D - (2*self.marge)

        vertical_length = D_p2 / self.nb_brin

        for i in range(self.nb_brin):
            d_origin    =   self.marge + ((i+1) * vertical_length)
            d_list.append(d_origin)

        return d_list 

    def vertical_mid_lines(self):
        brin_f_list = list()
        d_list = self.nb_brin_2_list_distance()

        for d_origin in d_list:
            brin_f_list.append([self.a,(d_origin * self.b_init) / self.marge])

        self.vertical_lines_factors = self.vertical_lines_factors + brin_f_list

    def vertical_end_line(self):
        max_length = (self.draw_area.diag - self.marge)
        # from thales th
        b_p = (max_length * self.b_init) / self.marge
        self.vertical_lines_factors.append([self.a,b_p])

class horizontal_builder():
    def __init__(self, draw_area, vert_builder, start_pos_top:bool = True) -> None:
        self.vert_builder       = vert_builder
        self.base_brin_length   = vert_builder.base_brin_length
        self.draw_area          = draw_area
        self.nb_brin            = vert_builder.nb_brin
        self.start_pos_top      = start_pos_top

        self.a                  = np.tan(np.deg2rad(self.draw_area.d_angle))         
        self.b_init             = vert_builder.b_init
        
        self.horizontal_lines_factors   = list()
        
        # compute horizontal lines
        self.horizontal_lines()

    def horizontal_lines(self):
        connect_f_list = list()
        a = self.a
        
        pos = self.start_pos_top
        for i in range(len(self.vert_builder.vertical_lines_factors)-1):
            [va,vb] = self.vert_builder.vertical_lines_factors[i]
            
            # check limit on space antena area
            if pos :    # pos = true -> top
                if vb > self.draw_area.space_ant_h:
                    [va,vb] = self.vert_builder.vertical_lines_factors[i+1]
                    vb = self.draw_area.space_ant_h - (a * ((self.draw_area.space_ant_h-vb) / va) )

                [nva,nvb] = self.vert_builder.vertical_lines_factors[i+1]
                if nvb > self.draw_area.space_ant_h:
                    xh = (self.draw_area.space_ant_h - nvb) / nva
                    tmp_b = self.draw_area.space_ant_h - a * xh
                    # intersect de va,vb and a,b -> x<0
                    x_i = (tmp_b-vb) / (va-a)
                    if x_i >= 0:
                        vb = tmp_b

                b = vb

                pos = not(pos)

            else:       # pos = false -> bottom
                x0      = -vb / va
                y_w     = 0

                # check right out bound
                if x0 > self.draw_area.space_ant_w:
                    [va,vb] = self.vert_builder.vertical_lines_factors[i+1]
                    x_w = self.draw_area.space_ant_w
                    x0  = x_w
                    y_w = va * x_w + vb

                tmp_b = -1 * np.tan(np.deg2rad(self.draw_area.d_angle)) * x0
                tmp_y = a * self.draw_area.space_ant_w + tmp_b
                [nva,nvb] = self.vert_builder.vertical_lines_factors[i+1]
                n_y   = nva * self.draw_area.space_ant_w + nvb

                if n_y > tmp_y:
                    y_w = n_y - tmp_y
                    
                b   = -1 * (np.tan(np.deg2rad(self.draw_area.d_angle)) * x0) + y_w
                
                pos = not(pos)

            connect_f_list.append([a, b])

        self.horizontal_lines_factors = self.horizontal_lines_factors + connect_f_list
    
class path_builder():
    def __init__(self, draw_area, nb_brin:int=1 , base_brin_length:int=3, start_pos_top:bool = True) -> None:
        # path builder must be based on space antenna area
        self.vertical_builder   = vertical_builder(draw_area, nb_brin=nb_brin , base_brin_length=base_brin_length)
        self.horizontal_builder = horizontal_builder(draw_area, self.vertical_builder, start_pos_top=start_pos_top)
        self.start_pos_top      = start_pos_top
        self.draw_area          = draw_area
        self.path_list          = None
        self.lines_2_path()

    def get_v_h_lines_factors(self):
        return [self.vertical_builder.vertical_lines_factors, self.horizontal_builder.horizontal_lines_factors]
    
    def debug_lines_factors(self, show:bool=True):
        [v_l_fs, h_l_fs] = self.get_v_h_lines_factors()
        x = np.arange(0,self.draw_area.space_ant_w+1)
        for [a,b] in v_l_fs:
            y = a*x+b
            plt.plot(y)
        for [a,b] in h_l_fs:
            y = a*x+b
            plt.plot(y)
        # plot diag
        diag = np.tan(np.deg2rad(self.draw_area.d_angle))*x
        plt.plot(diag, color='gray', alpha=0.5)
        # plot option
        title = f"space_ant_h:{self.draw_area.space_ant_h} | space_ant_w:{self.draw_area.space_ant_w} |"
        title = f"{title} b_length:{self.vertical_builder.base_brin_length} |"
        title = f"{title} nb_brin:{self.vertical_builder.nb_brin} | start_top:{self.start_pos_top}"
        plt.title(title)
        plt.grid()
        plt.xlim([0, self.draw_area.space_ant_w])
        plt.ylim([0, self.draw_area.space_ant_h])
        if show:
            plt.show()

    def draw_path(self, show:bool=True):
        # diplay must be based on the all pcb
        x = np.arange(0,self.draw_area.pcb_w+1)
        # Path point drawing
        for [a,b] in self.path_list:
            plt.scatter(a, b)  
            
        # Path segment drawing
        for i in range(len(self.path_list)-1):
            [x0,y0] = self.path_list[i]
            [x1,y1] = self.path_list[i+1]

            x_vs = [x0,x1]
            y_vs = [y0,y1]
            plt.plot(x_vs, y_vs, 'bo', linestyle="--")

        # plot diag
        diag = np.tan(np.deg2rad(self.draw_area.d_angle))*x
        plt.plot(diag, color='gray', alpha=0.5)
        # plot option
        title = f"space_ant_h:{self.draw_area.space_ant_h} | space_ant_w:{self.draw_area.space_ant_w} |"
        title = f"{title} b_length:{self.vertical_builder.base_brin_length} |"
        title = f"{title} nb_brin:{self.vertical_builder.nb_brin} | start_top:{self.start_pos_top}"
        plt.title(title)
        plt.grid()
        plt.xlim([0, self.draw_area.pcb_w])
        plt.ylim([0, self.draw_area.pcb_h])
        if show:
            plt.show()
    
    def lines_2_path(self):
        path = list()
        [v_lines_f, h_lines_f] = self.get_v_h_lines_factors()
        pos = self.start_pos_top # true if top, false if bottom

        # first point
        vline0 = v_lines_f[0] # a0,b0
        if pos:
            x0  = -vline0[1] / vline0[0] # x0 = 0-b / a
            path.append([x0,0])
        else:
            y0  = vline0[1]
            path.append([0,y0])

        # loop
        for i in range(len(h_lines_f)):
            [a0,b0] = h_lines_f[i]
            [a1,b1] = v_lines_f[i]
            [a2,b2] = v_lines_f[i+1]
            # h_n and v_n intersect
            x_n = (b1-b0)/(a0-a1)
            y_n = a0*x_n + b0
            # h_n and v_(n+1) intersect
            x_n1 = (b2-b0)/(a0-a2)
            y_n1 = a0*x_n1 + b0
            path = path + [[x_n,y_n],[x_n1,y_n1]]
            pos = not(pos)
        # last point
        vlinef = v_lines_f[-1] # a0,b0
        if pos:
            yf     = self.draw_area.space_ant_h
            xf     = (yf-vlinef[1]) / vlinef[0]
        else:
            xf     = self.draw_area.space_ant_w
            yf     = vlinef[0] * xf + vlinef[1]
        path.append([xf,yf])
        
        # now path is a list of coordinate in space antenna area
        # we must transpose them in the pcb area
        for i in range(len(path)):
            path[i] = [path[i][0] + self.draw_area.pcb_w - self.draw_area.space_ant_w, 
                       path[i][1] + self.draw_area.pcb_h - self.draw_area.space_ant_h]

        self.path_list = path
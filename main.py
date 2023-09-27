###############################################################################################
#####   drawing_zigzag library by Jonathan COURTOIS                                        ####
#####   contact : jonathan.courtois@univ-cotedazur.fr                                      ####
#####   demo file                                                                          ####
###############################################################################################

import matplotlib.pyplot as plt
import numpy as np
import drawings_zigzag 

def test_configs(dims, base_brin_lengths, nb_brins, start_pos_tops):
    for [h,w] in dims:
        for bbl in base_brin_lengths:
            for nb_brin in nb_brins:
                for start_pos_top in start_pos_tops:
                    x = np.arange(0,w+1)
                    da = drawings_zigzag.area(h,w)
                    path_builder = drawings_zigzag.path_builder(da, nb_brin=nb_brin, base_brin_length=bbl, start_pos_top=start_pos_top)
                    
                    # path_builder.debug_lines_factors(show=True)
                    path_builder.draw_path()
                    

def unitary_test(h, w, nb_brin, base_brin_length:float=5, start_pos_top:bool=True):
    #### How to use it - get path list
    da = drawings_zigzag.area(h,w)

    path_builder = drawings_zigzag.path_builder(da, nb_brin=nb_brin, base_brin_length=base_brin_length, start_pos_top=start_pos_top)
    ### end
    # to get path list use :
    path = path_builder.path_list

    # path_builder.debug_lines_factors(show=False)
    path_builder.draw_path()


def main():
    unitary_test(40, 20, 3, start_pos_top=True)
    unitary_test(40, 20, 6, start_pos_top=False)

    dims                = [[20,20],[20,40],[40,20]]
    base_brin_lengths   = [5.0]
    nb_brins            = [1,4,5,8,9,58]
    start_pos_tops      = [True,False]  
    test_configs(dims, base_brin_lengths, nb_brins, start_pos_tops)

if __name__ == '__main__':
    main()
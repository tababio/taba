# coding=utf-8
def read_PDB_return_coord_and_lines(pdb_in):
    """Function to read atomic coordinates from a PDB file"""
    
    # Import libraries
    import sys
    import numpy as np
    
    # Setup empty lists
    x = []
    y = []
    z = []
    my_lines = []
    # Try to open PDB file
    try:
        my_PDB_fo = open(pdb_in,"r")
    except IOError:
        sys.exit("\nI can't file "+pdb_in+" file!")
    
    # Looping through PDB file
    cont = 0
    for line in my_PDB_fo:
        if line[0:6].strip() == "HETATM" or line[0:6].strip() == "ATOM":
            if line[13:14].strip() != "H": # por que nao posso usar a posicao 77:78 (ou 76:78 3 letras)?
                x.append(float(line[30:38].strip()))
                y.append(float(line[38:46].strip()))
                z.append(float(line[46:54].strip()))
                my_lines.append(line)
                cont = cont+1
 
    # Convert list to array
    x_coord = np.array(x)
    y_coord = np.array(y)
    z_coord = np.array(z)
    #fecha arquivo
    my_PDB_fo.close()
    # Return arrays
    return x_coord, y_coord, z_coord, my_lines

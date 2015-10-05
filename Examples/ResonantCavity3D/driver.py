"""
Solve the resonant cavity problem with Whitney forms.

References:
    Douglas N. Arnold and Richard S. Falk and Ragnar Winther
    "Finite element exterior calculus: from Hodge theory to numerical
    stability"
    Bull. Amer. Math. Soc. (N.S.), vol. 47, No. 2, pp. 281--354
    DOI : 10.1090/S0273-0979-10-01278-4

"""
from pydec import simplicial_complex, d, delta, whitney_innerproduct, simplex_quivers
from numpy import loadtxt
from scipy import real, zeros
from scipy.linalg import eig
from matplotlib.pylab import quiver, figure, triplot, show

# Read in mesh data from files and construct complex
vertices = loadtxt('vertices.txt', dtype=float)
triangles = loadtxt('triangles.txt', dtype=int)
sc = simplicial_complex((vertices,triangles))

# Construct stiffness and mass matrices 
K = sc[1].d.T * whitney_innerproduct(sc,2) * sc[1].d
M = whitney_innerproduct(sc,1)

# Eliminate Boundaries from matrices
boundary_edges = sc.boundary()
non_boundary_edges = set(sc[1].simplex_to_index.keys()) - set(boundary_edges)
non_boundary_indices = [sc[1].simplex_to_index[e] for e in non_boundary_edges]

# Eliminate boundary conditions
K = K[non_boundary_indices,:][:,non_boundary_indices]
M = M[non_boundary_indices,:][:,non_boundary_indices]

# Compute eigenvalues and eigenvectors
# (could use sparse eigenvalue solver instead)
eigenvalues, eigenvectors = eig(K.todense(), M.todense())

# Plot eigenvalues
NUM_EIGS = 50 # Number of eigenvalues to plot
values = sorted([x for x in real(eigenvalues) if x > 1e-10])[0:NUM_EIGS]
ax = figure().gca()
ax.set_title('First ' + str(len(values)) + ' Eigenvalues\n\n')
ax.hold(True)
ax.plot(values,'ko')

# Plot the eigenvector 1-cochain as a vector field
N = 3 # Which non-zero eigenvector to plot?
non_zero_values = real(eigenvectors[:,list(eigenvalues).index(values[N])])
all_values = zeros((sc[1].num_simplices,))
all_values[non_boundary_indices] = non_zero_values
bases, arrows = simplex_quivers(sc,all_values)
#print bases
#print arrows

point14 = open("point_data.txt", "wb")
point14.write("\n")
point14.write('POINT_DATA 64')
point14.write("\n")
point14.write('VECTORS bases float\n')

i = 0
for base in bases:
	i = i + 1
	if (i > 64): break
	point14.write(' ' + str(base[0])+' '+str(base[1])+' '+str(base[2])+'\n')

#point14.write("\n")

point14.write('VECTORS arrows float\n')

i=0
for arrow in arrows:
	i = i + 1
	if (i > 64): break 
        point14.write( ' ' + str(float(arrow[0]).__format__('.8f'))+' '+str(float(arrow[1]).__format__('.8f'))+' '+str(float(arrow[2]).__format__('.8f'))+'\n')

point14.close()

ax = figure().gca()
ax.set_title('Mode #' + str(N+1))
ax.quiver(bases[:,0],bases[:,1],arrows[:,0],arrows[:,1])

ax.plot(sc.vertices[:,0], sc.vertices[:,1], 'o')
for j, p in enumerate(sc.vertices): 
    ax.text(p[0]-0.03, p[1]+0.03, j, ha='right') # label the points
for j, s in enumerate(sc.simplices): 
    p = sc.vertices[s].mean(axis=0) 
    ax.text(p[0], p[1], '#%d' % j, ha='center') # label triangles
ax.triplot(sc.vertices[:,0], sc.vertices[:,1], sc[-2].simplices)
ax.axis('equal')

show()


"""
Solve the resonant cavity problem with Whitney forms.

References:
    Douglas N. Arnold and Richard S. Falk and Ragnar Winther
    "Finite element exterior calculus: from Hodge theory to numerical
    stability"
    Bull. Amer. Math. Soc. (N.S.), vol. 47, No. 2, pp. 281--354
    DOI : 10.1090/S0273-0979-10-01278-4

"""
from pydec import simplicial_complex, d, delta, whitney_innerproduct, \
     simplex_quivers
from numpy import loadtxt
from scipy import real, zeros
from scipy.linalg import eig
from matplotlib.pylab import quiver, figure, triplot, show
from pydec import kd_tree, flatten, triplot, read_array
#from pydec.dec.rips_complex import rips_complex
from matplotlib import tri
from scipy.spatial import Delaunay
import numpy as np
import matplotlib.pyplot as plt

# Read in mesh data from files and construct complex
vertices = loadtxt('vertices.txt', dtype=float)
triangles = loadtxt('triangles.txt', dtype=int)
sc = simplicial_complex((vertices,triangles))

#pts = read_array('300pts.mtx')  # 300 random points in 2D
#rc = rips_complex( pts, 0.15 )

#sc = rc.chain_complex()
#si1 = rc.simplices[1]
#si2 = rc.simplices[2]
#b1 = sc[1].astype(float)  # edge boundary operator
#b2 = sc[2].astype(float)  # face boundary operator

# Construct stiffness and mass matrices 
K = sc[1].d.T * whitney_innerproduct(sc,2) * sc[1].d
#print rc.simplices[-1]
#exit(0)
#K = b2.T * whitney_innerproduct(rc,2) * b2
M = whitney_innerproduct(sc,1)

# Eliminate Boundaries from matrices
boundary_edges = sc.boundary()
non_boundary_edges = set(sc[1].simplex_to_index.keys()) - set(boundary_edges)
non_boundary_indices = [sc[1].simplex_to_index[e] for e in non_boundary_edges]
#non_boundary_edges = set(sc[2].simplex_to_index.keys()) - set(b2)
#non_boundary_indices = [sc[2].simplex_to_index[e] for e in non_boundary_edges]


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
print bases
print arrows


ax = figure().gca()
#ax = figure(figsize=(10,10))
ax.set_title('Mode #' + str(N+1))
ax.quiver(bases[:,0],bases[:,1],arrows[:,0],arrows[:,1])
tri = Delaunay(sc.vertices)
#np.unique(tri.simplices.ravel())
plt.triplot(sc.vertices[:,0], sc.vertices[:,1],  tri.simplices.ravel().copy(), 'bo-')
#print tri.simplices.ravel()

ax.plot(sc.vertices[:,0], sc.vertices[:,1], 'o')
for j, p in enumerate(sc.vertices): 
    ax.text(p[0]-0.03, p[1]+0.03, j, ha='right') # label the points
for j, s in enumerate(sc.simplices): 
    p = sc.vertices[s].mean(axis=0) 
    ax.text(p[0], p[1], '#%d' % j, ha='center') # label triangles
#ax.xlim(-0.5, 1.5); ax.ylim(-0.5, 1.5)
#ax.triplot(sc.vertices[:,0], sc.vertices[:,1], sc[-1].simplices)
ax.axis('equal')

show()


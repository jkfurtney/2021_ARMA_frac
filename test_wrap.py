from IPython import get_ipython; get_ipython().magic('reset -sf')
import itasca as it
it.command("python-reset-state false")
import numpy as np
it.command('model restore "disc-mat.p3sav"')

inner_radius = it.fish.get("mv_W")/2.0
assert it.fish.get("mv_W") == it.fish.get("mv_D")
outer_radius = inner_radius*3
thickness = it.fish.get("mv_H")

it.command(f"""
model config dynamic
model domain extent {-1.1*outer_radius} {1.1*outer_radius} {-1.1*outer_radius} {1.1*outer_radius} {-1.1*thickness} {1.1*thickness} condition destroy
zone create cylindrical-shell ...
  point 0 0                 {0}              {-thickness/2.0} ...
  point 1 {outer_radius}    {0}              {-thickness/2.0} ...
  point 2 0                 {0}              {thickness/2.0} ...
  point 3 0                 {-outer_radius}  {-thickness/2.0} ...
  point 8 {inner_radius}    {0}              {-thickness/2.0} ...
  point 9 0                 {-inner_radius}  {-thickness/2.0} ...
  point 10 {inner_radius}    {0}              {thickness/2.0} ...
  point 11 0                 {-inner_radius}  {thickness/2.0} ...
  size 15 4 15 ratio 1.1 1.1 1


zone reflect origin 0 0 0 norm -1 0 0
zone reflect origin 0 0 0 norm 0 -1 0

zone cmodel assign elastic
zone property young [pbm_emod+lnm_emod] poisson 0.25
zone property density [cm_densityVal]
wall-zone create name 'dem_boundary' range cylinder end-1 0 0 {-thickness/2.0} end-2 0 0 {thickness/2.0} rad {inner_radius}

zone gridpoint fix velocity-z range position-z {thickness/2.0}
zone gridpoint fix velocity-z range position-z {-thickness/2.0}
zone face apply quiet-normal range cylinder end-1 0 0 {-thickness/2.0} end-2 0 0 {thickness/2.0} rad {.99*outer_radius} not
zone face apply velocity-strike 0 range cylinder end-1 0 0 {-thickness/2.0} end-2 0 0 {thickness/2.0} rad {.99*outer_radius} not
zone face apply velocity-dip 0 range cylinder end-1 0 0 {-thickness/2.0} end-2 0 0 {thickness/2.0} rad {.99*outer_radius} not

contact cmat default model linearpbond property pb_ten 1e100 pb_coh 1e100 method deformability emod {it.fish.get('mv_emod')} kratio 1.0

model clean all
contact method bond gap 0 {0.1*it.ball.find(1).radius()} range contact type 'ball-facet'
contact property lin_mode 1 pb_ten 1e100 pb_coh 1e100 range contact type 'ball-facet'

""")


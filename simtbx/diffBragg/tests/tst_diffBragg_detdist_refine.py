from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("--plot", action='store_true')
parser.add_argument("--residuals", action='store_true')
parser.add_argument("--oversample", type=int, default=0)
parser.add_argument("--curvatures", action="store_true")
parser.add_argument("--nopolar", action="store_true")
args = parser.parse_args()

from dxtbx.model.crystal import Crystal
from cctbx import uctbx
from scitbx.matrix import sqr, rec
from dxtbx.model import Panel
from copy import deepcopy
from scipy.spatial.transform import Rotation

from simtbx.diffBragg.nanoBragg_crystal import nanoBragg_crystal
from simtbx.diffBragg.sim_data import SimData
from simtbx.diffBragg import utils

ucell = (85.2, 96, 124, 90, 105, 90)
symbol = "P121"

# generate a random raotation
rotation = Rotation.random(num=1, random_state=1107)[0]
Q = rec(rotation.as_quat(), n=(4, 1))
rot_ang, rot_axis = Q.unit_quaternion_as_axis_and_angle()

# make the ground truth crystal:
a_real, b_real, c_real = sqr(uctbx.unit_cell(ucell).orthogonalization_matrix()).transpose().as_list_of_lists()
C = Crystal(a_real, b_real, c_real, symbol)
C.rotate_around_origin(rot_axis, rot_ang)

# Setup the simulation and create a realistic image
# with background and noise
# <><><><><><><><><><><><><><><><><><><><><><><><><>
nbcryst = nanoBragg_crystal()
nbcryst.dxtbx_crystal = C   # simulate ground truth
nbcryst.thick_mm = 0.1
nbcryst.Ncells_abc = 12, 12, 12

SIM = SimData()
SIM.detector = SimData.simple_detector(160, 0.1, (1024, 1024))

# grab the detector node (ground truth)
node = SIM.detector[0]
node_d = node.to_dict()
Origin = node_d["origin"][0], node_d["origin"][1], node_d["origin"][2]
distance = Origin[2]
gt_distance = distance
print("Ground truth originZ=%f" % (SIM.detector[0].get_origin()[2]))


# copy the detector and update the origin
det2 = deepcopy(SIM.detector)
# alter the detector distance by 2 mm
node_d["origin"] = Origin[0], Origin[1], Origin[2]+3
det2[0] = Panel.from_dict(node_d)
print("Modified originZ=%f" % (det2[0].get_origin()[2]))

SIM.crystal = nbcryst
SIM.instantiate_diffBragg(oversample=0)
SIM.D.progress_meter = False
SIM.D.verbose = 0 #1
SIM.D.nopolar = args.nopolar
SIM.water_path_mm = 0.005
SIM.air_path_mm = 0.1
SIM.add_air = True
SIM.add_Water = True
SIM.include_noise = True
#SIM.D.spot_scale = 1e8


SIM.D.add_diffBragg_spots()
spots = SIM.D.raw_pixels.as_numpy_array()
SIM._add_background()
SIM._add_noise()
# This is the ground truth image:
img = SIM.D.raw_pixels.as_numpy_array()
SIM.D.raw_pixels *= 0

# Simulate the perturbed image for comparison
SIM.D.update_dxtbx_geoms(det2, SIM.beam.nanoBragg_constructor_beam, 0)
SIM.D.add_diffBragg_spots()
SIM._add_background()
SIM._add_noise()
# Perturbed image:
img_pet = SIM.D.raw_pixels.as_numpy_array()
SIM.D.raw_pixels *= 0

from dxtbx.model import Experiment
from simtbx.nanoBragg import make_imageset
from cctbx_project.simtbx.diffBragg.phil import phil_scope
from simtbx.diffBragg import refine_launcher
E = Experiment()
E.detector = det2  # set the perturbed detector
E.beam = SIM.beam.nanoBragg_constructor_beam
E.crystal = C
E.imageset = make_imageset([img], E.beam, E.detector)

refls = utils.refls_from_sims([spots], E.detector, E.beam, thresh=20)

P = phil_scope.extract()
P.roi.shoebox_size = 20
P.roi.reject_edge_reflections = False
P.refiner.refine_detdist = [1]
P.refiner.ranges.originZ = -20/1000, 20/1000.
P.refiner.max_calls = [200]
P.refiner.tradeps = 1
P.refiner.curvatures = False
P.refiner.use_curvatures_threshold = 0
P.refiner.poissononly = False
P.refiner.verbose = True
P.refiner.big_dump = False
P.refiner.sigma_r = SIM.D.readout_noise_adu
P.refiner.adu_per_photon = SIM.D.quantum_gain
P.simulator.crystal.has_isotropic_ncells = True
P.simulator.init_scale = SIM.D.spot_scale
P.refiner.ncells_mask = "111"
P.simulator.beam.size_mm = SIM.beam.size_mm

RUC = refine_launcher.local_refiner_from_parameters(refls, E, P, miller_data=SIM.crystal.miller_array)
refined_distance_offset = E.detector[0].get_origin()[2] + RUC._get_detector_distance_val(0)*1000 - gt_distance
assert abs(refined_distance_offset) < 1e-2
print("OK")



#!/usr/bin/env python
# -*- coding: utf-8 -*-


from simtbx.nanoBragg    import nanoBragg, shapetype
from dxtbx.model.crystal import CrystalFactory
from scitbx.matrix       import sqr

import os
import dxtbx
import numpy as np
from matplotlib.pyplot   import imshow, colorbar, savefig, close
from matplotlib.colors   import LogNorm



def simulate_shot(distance, shape=shapetype.Tophat, cuda=True, seed=None,
                  add_noise=True):

    SIM = nanoBragg(detpixels_slowfast=(4096, 4096), pixel_size_mm=0.025,
                    verbose=10, oversample=0)

    cr = {'__id__': 'crystal',
          'real_space_a': (200, 0, 0),
          'real_space_b': (0, 180, 0),
          'real_space_c': (0, 0, 150),
          'space_group_hall_symbol': '-P 4 2'}

    cryst           = CrystalFactory.from_dict(cr)
    SIM.Amatrix     = sqr(cryst.get_A()).transpose().elems
    SIM.distance_mm = distance

    SIM.verbose        = 10
    SIM.progress_meter = True

    SIM.wavelength_A = 1.2
    SIM.flux         = 1e13
    SIM.beamsize_mm  = 0.005
    SIM.polarization = 1

    SIM.mosaic_spread_deg = 0.02
    SIM.mosaic_domains    = 10

    # FIXME this has to be equivalent to default_F, or else set in Fhkl,
    # otherwise the test fails
    SIM.F000       = 3e3
    SIM.default_F  = 3e3
    SIM.exposure_s = 1
    SIM.Ncells_abc = (15,15,15)

    # variable shape
    SIM.xtal_shape = shape

    # boost up the signal (number of mosaic blocks in crystal)
    SIM.spot_scale = 1e3

    SIM.show_params()

    if seed is not None:
        SIM.seed = seed
        SIM.randomize_orientation()
    if cuda:
        # NOTE: uncomment the following 4 lines and comment the
        # add_nanoBragg_spots_cuda() call in order to use current dev-mode
        # code!
        #SIM.allocate_cuda()
        #SIM.add_nanoBragg_spots_cuda_update()
        #SIM.get_raw_pixels_cuda()
        #SIM.deallocate_cuda()
        SIM.add_nanoBragg_spots_cuda_nvtx()
    else:
        SIM.add_nanoBragg_spots_nvtx()

    if add_noise:
        SIM.add_noise_nvtx()

    return SIM



def save_smv(SIM, frame_idx, frame_prefix="frame"):
    SIM.to_smv_format(fileout=f"{frame_prefix}_{frame_idx:03}.img")



def load_smv(frame_idx, frame_prefix="frame"):
    loader   = dxtbx.load(f"{frame_prefix}_{frame_idx:03}.img")
    raw_flex = loader.get_raw_data()
    data     = raw_flex.as_numpy_array()
    return data



def render_shot(img, frame_idx, img_min, img_max, log_scale=True,
                frame_prefix="frame"):
    if log_scale:
        imshow(img, norm=LogNorm(vmin=img_min, vmax=img_max))
    else:
        imshow(img, vmin=img_min, vmax=img_max)
    colorbar()
    savefig(f"{frame_prefix}_{frame_idx:03}.png")
    close("all")



if __name__ == "__main__":

    path_prefix = os.path.join("img", "highres")

    sim        = simulate_shot(1700)
    raw_pixels = sim.raw_pixels.as_numpy_array()

    render_shot(raw_pixels, 1, np.min(raw_pixels), np.max(raw_pixels),
                frame_prefix=path_prefix + "_log", log_scale=True)

    sim        = simulate_shot(100)
    raw_pixels = sim.raw_pixels.as_numpy_array()

    render_shot(raw_pixels, 2, np.min(raw_pixels), np.max(raw_pixels),
                frame_prefix=path_prefix + "_log", log_scale=True)
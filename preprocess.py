import json
import numpy as np
from glob import glob


def reader(filename):
    with open(filename) as f:
        info = json.load(f)
    rms_bbs = np.asarray(info['boxes'])
    fp_eds = info['edges']
    rms_type = info['room_type']
    eds_to_rms = info['ed_rm']
    s_r = 0
    for rmk in range(len(rms_type)):
        if rms_type[rmk] != 17:
            s_r = s_r + 1
    rms_bbs = np.array(rms_bbs) / 256.0
    fp_eds = np.array(fp_eds) / 256.0
    fp_eds = fp_eds[:, :4]
    tl = np.min(rms_bbs[:, :2], 0)
    br = np.max(rms_bbs[:, 2:], 0)
    shift = (tl + br) / 2.0 - 0.5
    rms_bbs[:, :2] -= shift
    rms_bbs[:, 2:] -= shift
    fp_eds[:, :2] -= shift
    fp_eds[:, 2:] -= shift
    tl -= shift
    br -= shift

    return rms_type, fp_eds, rms_bbs, eds_to_rms

base_dir = 'datasets/rplan'
with open(f'{base_dir}/list.txt') as f:
     lines = f.readlines()

out_size = 64
length_edges = []
subgraphs = []
for line in lines:
    a = []
    file_name = f'{base_dir}/{line[:-1]}'
    with open(file_name) as f2:
        rms_type, fp_eds, rms_bbs, eds_to_rms = reader(file_name)

    eds_to_rms_tmp = []
    for l in range(len(eds_to_rms)):
        eds_to_rms_tmp.append([eds_to_rms[l][0]])

    rms_masks = []
    im_size = 256
    fp_mk = np.zeros((out_size, out_size))
    nodes = rms_type
    for k in range(len(nodes)):
        eds = []
        for l, e_map in enumerate(eds_to_rms_tmp):
            if (k in e_map):
                eds.append(l)
        b = []
        for eds_poly in [eds]:
            length_edges.append({'file_name': file_name, 'edges_array': np.array([fp_eds[l][:4] for l in eds_poly])})

chk = [x['edges_array'].shape for x in length_edges]
idx = [i for i, x in enumerate(chk) if len(x) != 2]
final = [x['file_name'] for i, x in enumerate(length_edges) if i in idx]
final = [x.replace('\n', '') for x in final]

import os

for fin in final:
    try:
        os.remove(fin)
    except:
        pass

from metric.metirc_path_collector import train_test_info_creator
from metric.metric_reference import point_creator
from metric.metirc_result import evaluate
import os
from os.path import join, abspath
import sys

def from_label_to_metric(img_dir, mask_dir:str, tiles_dir:str, dst:str):
    pickle_dir = join(dst, 'temp_pkl')
    train_test_info_creator(mask_dir, tiles_dir, pickle_dir)
    test_pkl_p = abspath(join(pickle_dir, 'test.pkl'))
    other_pkl_p = abspath(join(pickle_dir, 'others.pkl'))
    print('Path collection, done!')
    # point_creator will be changed in the future, now we use the mask directory. This directory will be replaced by point_label_dir.
    point_creator(mask_dir, 'refer', pickle_dir, limit_pkl=test_pkl_p)
    refer_pkl_p = join(pickle_dir, 'refer.pkl')
    print('Refer points, done!')

    trainor_p = abspath('./metric/metirc_trainor.py')
    models_p = abspath(join(dst, 'progress_models'))
    os.system(f'for /L %i in (0, 10, 70) do python {trainor_p} {other_pkl_p} {test_pkl_p} {models_p} %i')
    print('Models training, done')
    eval_dst = join(dst, 'results')
    evaluate(models_p, img_dir, refer_pkl_p, eval_dst)

if __name__ == "__main__":
    img_dir = sys.argv[1]
    mask_dir = sys.argv[2]
    tiles_dir = sys.argv[3]
    dst = sys.argv[4]
    from_label_to_metric(img_dir, mask_dir, tiles_dir, dst)
import os
import argparse
import cv2

from utils.video_utils import get_video_array, crop_video
from utils.extraction import process_video
from utils.pc_complete_utils import compute_percent_complete
from utils.pose_features import get_num_moves, compute_time_elapsed, compute_total_distance_traveled

def get_parser():
    parser = argparse.ArgumentParser(description='Run script to produce a report from a climb video')
    parser.add_argument('-d', '--dir', type=str, default='../test_data',
                        help='filepath of climb video and hold image for generating report.txt')
    return parser

def get_data(args):
    files = os.listdir(args.dir)
    assert 'climb.mp4' in files
    assert 'holds.jpg' in files
    vid_path = os.path.join(args.dir, 'climb.mp4')
    img_path = os.path.join(args.dir, 'holds.jpg')

    raw_vid = get_video_array(vid_path)
    hold_img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
    return raw_vid, hold_img

def main(args):
    raw_vid, hold_img = get_data(args)
    
    # process video, extract all necessary information
    raw_vid, climb_holds_used, holds, colors, results_arr, landmarks_arr, all_positions, sig_positions, significances = process_video(raw_vid, hold_img)
    print("Video frames: ", raw_vid.shape[0])
    print("Holds Used Frames: ", len(climb_holds_used))
    print("All Positions Frames: ", len(all_positions['left_hand']))
    print("Sig Position Frames: ", len(sig_positions['left_hand']))

    percent_complete = compute_percent_complete(holds, all_positions)
    num_moves, distinct_holds_used = get_num_moves(climb_holds_used, significances)
    # move valididty
    time_elapsed = compute_time_elapsed(raw_vid, holds, all_positions=all_positions, fps=30)
    if time_elapsed == -1:
        print("Time elapsed could not be computed.")
    total_distance = compute_total_distance_traveled(sig_positions)
    
    print("")
    print("% Complete: ", percent_complete)
    print("# of Moves Taken: ", num_moves)
    print("Move Validity: ")
    print("Climb Duration: {} sec".format(time_elapsed))
    print("Total Distance Climbed: {:.2f} px".format(total_distance))

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    main(args)
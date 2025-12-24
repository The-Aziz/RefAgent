"""Simple script to run the Detector for a given project folder (projects/before/<project>)."""
import argparse
from settings import Settings
from refAgent.detector import Detector

parser = argparse.ArgumentParser()
parser.add_argument("project", help="project name (folder inside projects/before)")
args = parser.parse_args()

config = Settings()
proj = args.project
proj_dir = f"projects/before/{proj}"

det = Detector(config)
print("Running detector on:", proj_dir)
print(det.detect_god_classes(proj_dir))

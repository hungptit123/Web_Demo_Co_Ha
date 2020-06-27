MODEL_DIR = "model"
SIZEMODEL = 160
VIDEOCAPTURE = 0
MODEL_DETECT = "model_detect"

DATABASE_DIR = 'database'
DATABASE_NAME_LOAD = 'newest_database.pkl'
DATABASE_NAME_SAVE = 'newest_database.pkl'

IMAGES_DIR = 'images'
POS_COLOR = (0, 255, 0)
NEG_COLOR = (0, 0, 255)
THUMB_BOUNDER_COLOR = (255, 255, 255)
LINE_THICKNESS = 1
FONT_SIZE = 0.5
DIS_THUMB_X = 10
DIS_THUMB_Y = 30
DIS_BETWEEN_THUMBS = 5
FPS_POS = (10, 20)
DETECT_SCALE = 2
FLIP = True
SCREEN_SIZE = {
    'width' : 640,
    'height' : 480
}
TRAINING_AREA = (384, 0, 640, 480)
DETECT_DEVICE = 'auto'
EMBEDDING_DEVICE = 'auto'

def set_screen_size(w, h):
    global SCREEN_SIZE, TRAINING_AREA
    w = int(w)
    h = int(h)
    SCREEN_SIZE['width'] = w
    SCREEN_SIZE['height'] = h
    TRAINING_AREA = (int(3*w/5), 0, w, h)
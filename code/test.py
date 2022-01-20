import sys
from PySide2.QtWidgets import QApplication
from sksurgeryutils.common_overlay_apps import OverlayBaseApp
from sksurgeryarucotracker.arucotracker import ArUcoTracker;
from sksurgerycore.transforms.transform_manager import TransformManager
import numpy
          
#create an OverlayApp class, that inherits from OverlayBaseApp
class OverlayApp(OverlayBaseApp):

	def __init__(self, image_source):
		  print("__init__ Function Called")
		  """override the default constructor to set up sksurgeryarucotracker"""

		  #we'll use SciKit-SurgeryArUcoTracker to estimate the pose of the
		  #visible ArUco tag relative to the camera. We use a dictionary to
		  #configure SciKit-SurgeryArUcoTracker

		  ar_config = {
		      "tracker type": "aruco",
		      #Set to none, to share video source with OverlayBaseApp
		      "video source": 'none',
		      "debug": False,
		      #the aruco tag dictionary to use. DICT_4X4_50 will work with
		      #../tags/aruco_4by4_0.pdf
		      "dictionary" : 'DICT_4X4_50',
		      "marker size": 50, # in mm
		      #We need a calibrated camera. For now let's just use a
		      #a hard coded estimate. Maybe you could improve on this.
		      "camera projection": numpy.array([[560.0, 0.0, 320.0],
		                                        [0.0, 560.0, 240.0],
		                                        [0.0, 0.0, 1.0]],
		                                       dtype=numpy.float32),
		      "camera distortion": numpy.zeros((1, 4), numpy.float32)
		      }
		  self.tracker = ArUcoTracker(ar_config)
		  self.tracker.start_tracking()

		  #and call the constructor for the base class
		  if sys.version_info > (3, 0):
		      super().__init__(image_source)
		  else:
		      #super doesn't work the same in py2.7
		      OverlayBaseApp.__init__(self, image_source)
          
	def update(self):
		print("update Function Called")
		_, image = self.video_source.read()
		#add a method to move the rendered models
		self._aruco_detect_and_follow(image)
		
		self.vtk_overlay_window.set_camera_state({"ClippingRange": [1, 1000000]})
		
		self.vtk_overlay_window.set_video_image(image)
		self.vtk_overlay_window.Render()
	
	def _aruco_detect_and_follow(self, image):
		  print("_aruco_detect_and_follow Function Called")
		  """Detect any aruco tags present using sksurgeryarucotracker
		  """

		  #tracker.get_frame(image) returns 5 lists of tracking data.
		  #we'll only use the tracking matrices (tag2camera)
		  _port_handles, _timestamps, _frame_numbers, tag2camera, \
		                  _tracking_quality = self.tracker.get_frame(image)
		  
		  print(tag2camera is not None)
		  if tag2camera:
		      #pass tmera. If you have more than one tag
		      #visible, you may need to do something cleverer here.
		      print(tag2camera)
		      self._move_camera(tag2camera[0])
	
	def _move_camera(self, tag2camera):
		print("_move_camera Function Called")
		"""Internal method to move the rendered models in
		some interesting way"""

		#SciKit-SurgeryCore has a useful TransformManager that makes
		#chaining together and inverting transforms more intuitive.
		#We'll just use it to invert a matrix here.
		transform_manager = TransformManager()
		transform_manager.add("tag2camera", tag2camera)
		camera2tag = transform_manager.get("camera2tag")

		#Let's move the camera, rather than the model this time.
		self.vtk_overlay_window.set_camera_pose(camera2tag)
	
#first we create an application
app = QApplication([])

#then an instance of OverlayApp. The video source
#is set when we create the instance. This is an index
#starting at 0. If you have more than one webcam, you can
#try using different numbered sources
video_source = 0
viewer = OverlayApp(video_source)

#Set a model directory containing the models you wish
#to render and optionally a colours.txt defining the
#colours to render in.
model_dir = '../stone_kidney_model'
viewer.add_vtk_models_from_dir(model_dir)

#start the viewer
viewer.start()

#start the application
sys.exit(app.exec_())

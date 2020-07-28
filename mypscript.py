#!/usr/bin/python

from niryo_one_python_api.niryo_one_api import *
import sys
import argparse
import rospy
import time
import math



def createParser ():
	parser = argparse.ArgumentParser()
	parser.add_argument('mode', nargs='?')
	return parser




class NiryoMover:

	def __init__(self):
		rospy.init_node('niryo_one_example_python_api')
		self.niryo_obj = NiryoOne()
		self.manMode = createParser().parse_args().mode
		self.start()

	def start(self):
		print "--- Start"

		try:
			if self.manMode != 'nothing': 
				print('Start calibration\n')
				self.niryo_obj.calibrate_auto()
				print "Calibration finished !\n"

				degmob1 = math.radians(90)
				degmob2 = math.radians(0)
				degmob3 = math.radians(0)
				degmob4 = math.radians(-45)
				degmob5 = math.radians(-90)
				degmob6 = math.radians(-90)

				joint_target = [degmob1, degmob2, degmob3, degmob4, degmob5, degmob6]
				self.niryo_obj.move_joints(joint_target)

				self.manipulateByJoints()
				self.manipulateByPose()
				self.manipulateByMultiplePoints()

				if self.manMode != 'nothing':
					self.niryo_obj.activate_learning_mode(1)

		except NiryoOneException as e:

			print e
			self.niryo_obj.activate_learning_mode(1)

		print "--- End"	





	def getJointsList(self):
		joints_list = [math.radians(float(input())) for i in range(6)]
		return joints_list

	def getPositionList(self):
		position_list = [float(input(coordinate))/1000.0 for coordinate in ["pos:x = ", "pos:y = ", "pos:z = ", 
																   			"rot:x = ", "rot:y = ", "rot:z = "]]
		position_list[3] = math.radians(position_list[3] * 1000)
		position_list[4] = math.radians(position_list[4] * 1000)
		position_list[5] = math.radians(position_list[5] * 1000)
		print('\n')
		return position_list





	def moveAtJoints(self):
		joints_list = self.getJointsList()
		print('\n')
		print(joints_list)
		self.niryo_obj.move_joints(joints_list)

	def moveAtPoints(self, pl=0):
		if pl == 0:
			pl=self.getPositionList()
		print('\n')
		print(pl)
		self.niryo_obj.move_pose(pl[0], pl[1], pl[2], pl[3], pl[4], pl[5])






	def manipulateByJoints(self):
		if (self.manMode == 'joint_manipulate' or self.manMode == 'full'):
			print("Manipulate by joints\n")
			while int(input("\"1\" if have made, \"0\" if have not\n")) == 1:
				try:
					print("Enter angles in degress:")
					self.moveAtJoints()
				except NiryoOneException as e:
					print e


	def manipulateByPose(self):
		if (self.manMode == 'pose_manipulate' or self.manMode == 'full'):
			print("\nManipulate by pose\n")
			while int(input("\"1\" if have made, \"0\" if have not\n")) == 1:
				try:
					print("Enter every coordinate in mm:")
				 	self.moveAtPoints()
				except NiryoOneException as e:
					print e

	def manipulateByMultiplePoints(self):
		if (self.manMode == 'pose_by_points'):
			print('\nManipulate at points\n')
			while int(input("\"1\" if have made, \"0\" if have not\n")) == 1:
				try:
					points_count = int(input("Enter count of points: "))
					positions_list = [self.getPositionList() for i in range(points_count)]
					print(positions_list)
					for position in positions_list:
						print(position)
						self.moveAtPoints(position)
				except NiryoOneException as e:
					print e





if __name__ == '__main__':

	NiryoMover()


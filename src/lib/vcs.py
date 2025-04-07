#!/usr/bin/python3
# -- coding: utf-8 --

import requests
import json


class VCS_Tool:
	def __init__(self,address,port,username,password):
		self.address = address
		self.port = port
		self.username = username
		self.password = password
		self.session = requests.Session()
		self.session.headers.update({
			'accept': 'application/json'
		})
		self.login_url = 'http://'+address+':'+port+'/login'
		self.login_data = {'username': username, 'password': password}
		self.config_url = 'http://'+address+':'+port+'/vcs/vcsApi/v1/getConfig'
		self.config_data = {"tenantId": "public","groupId": "SLAM","dataId": "ep_qrcode_loc","md5":""}
		self.publis_url = 'http://'+address+':'+port+'/vcs/vcsApi/v1/publishConfig'
		self.publis_data = {"tenantId": " public","groupId": "SLAM","dataId": "ep_qrcode_loc","content":"","maxBackupCount":10,"type":"txt","forceUpdate":"1","appName":"path_follower","configDesc":"ep_can_driver_all配置"}

	def update_config(self,config_content):
		self.publis_data["content"] = config_content
		response = self.session.post(self.publis_url, data= self.publis_data)
		if response.status_code == 200:
			print("update config success")
			return True
		else:
			print("update config failed")
			return False
	
	def login(self):
		response = self.session.post(self.login_url, data=self.login_data)
		if response.status_code == 200:
			print("login success")
			return True
		else:
			print("login failed")
			return False

	def get_config(self):
		response = self.session.get(self.config_url, params=self.config_data)
		if response.status_code == 200:
			print("get config success")
			print(response.text)
			return response.text
		else:
			print("get config failed")
			return None

if __name__ == '__main__':
	vcs_tool = VCS_Tool('127.0.0.1','8888','ep','')
	vcs_tool.login()
	vcs_tool.get_config()
	# print(vcs_tool.address)
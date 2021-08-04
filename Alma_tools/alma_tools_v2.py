import requests
from time import sleep
from bs4 import BeautifulSoup as bs
import re
import os
import sys


pr_key = "YOUR KEY"
sb_key = "YOUR SB KEY"

##################################################################################################
class AlmaTools():
	
	""" 
	This class contains methods for getting, updating, creating and deleting Alma data via Alma's APIs.

	Attributes
	----------
	mms_id : str
		Alma MMS IDF
	holding_id: str
		Alma holding ID
	item_pid : str
		Alma item ID
	xml_record_data : str
		XML data to submit to Alma
	options : dict
		dictionary which contains any API request parameters additional to the necessary API key. Example: "{"limit":"100"}"
	status_code : int
		status code for the Alma request
	xml_response_data:
		response in xml format

	Methods
	-------
		__init__(self, key)
		get_bib(self, mms_id, options)
		update_bib(self, mms_id, xml_record_data, options)
		get_holdings(self, mms_id, options)
		get_holding(self, mms_id, holding_id, options)
		delete_holding(self, mms_id, holding_id)
		get_items(self, mms_id, holding_id, options)
		get_item(self, mms_id, holding_id, item_pid, options)
		update_item(self, mms_id, holding_id, item_pid, xml_record_data, options)
		delete_item(self, mms_id, holding_id, item_pid)
		get_representations(self, mms_id, options)
		get_representation(self, mms_id, rep_id, options)
		update_representation(self, mms_id, rep_id, xml_record_data, options)
		create_item_by_po_line(self, po_line, xml_record_data, options)
		get_portfolio(self, mms_id, portfolio_id, options)
		delete_portfolio(self, mms_id, portfolio_id, options)
		get_ecollection(self, mms_id, ecollection_id, oprions)

	"""

	def __init__(self, alma_key):
		
		"""	Initialises all the neccessary attributes for an Alma_tools object.
			
			Parameters:
			alma_key (str) - Code for appropriate Alma API key - "sb" for sandbox or "prod" for production
		"""
		if alma_key == "sb":
			self.alma_key = str(sb_key)
		elif alma_key == "prod":
			self.alma_key = str(pr_key)
		self.base_api_url = "https://api-ap.hosted.exlibrisgroup.com/almaws/v1/bibs/"
		self.acq_base_api_url = "https://api-ap.hosted.exlibrisgroup.com/almaws/v1/acq/po-lines/"
		self.config_base_url = "https://api-ap.hosted.exlibrisgroup.com/almaws/v1/conf/"
		self.mms_id = None
		self.holding_id = None
		self.item_pid = None
		self.xml_response_data = None
		self.status_code = None
		self.headers = {'content-type': 'application/xml'}
		
	def get_bib(self, mms_id, options={}):

		""" Retrieves the bibliographic record in XML for a given Alma MMS ID
		Parameters:
			mms_id(str) - Alma MMS ID
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
			self.status_code
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}", params=parameters)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def get_set(self, set_id, options={}):

		"""Retrieves sets by set_id
		Parameters:
			set_id(str) - Alma set id
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
			self.status_code"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r= requests.get(f"{self.config_base_url}sets/{set_id}",params = parameters)
		print(f'{self.config_base_url}sets/{set_id}')
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def get_set_members(self, set_id, options={}):

		parameters = {**{"apikey": self.alma_key}, **options}
		r= requests.get(f"{self.config_base_url}sets/{set_id}/members",params = parameters)
		print(f'{self.config_base_url}sets/{set_id}')
		self.xml_response_data = r.text
		self.status_code = r.status_code


	def get_ecollection(self, mms_id, ecollection_id, options = {}):

		"""
		Retrieves an electronic collection record in xml 
		Argumets:
			collection_id(str) - id of the collection
		"""

		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}/e-collections/{ecollection_id}", params=parameters)
		print(r.text)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def get_portfolio(self, mms_id, portfolio_id, options = {}):

		"""
		Retrieves a portfolio record in xml 
		Argumets:
			mms_id(str) - id of the bibliographic record
			portfolio_id(str) - id of the portfolio
		"""

		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}/portfolios/{portfolio_id}", params=parameters)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def delete_portfolio(self, mms_id, portfolio_id, options = {}):

		"""
		Deletes portfolio
		Argumets:
			mms_id(str) - id of the bibliographic record
			portfolio_id(str) - id of the portfolio
		Returns:
			None
		"""
		
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.delete (f"{self.base_api_url}{mms_id}/portfolios/{portfolio_id}", params=parameters)
		self.xml_response_data = r.text
		self.status_code = r.status_code



	def create_bib(self, xml_record_data, options = {}):

		"""
		Creates bibliographic record
		Paramrters:			
			xml_record_data(str) - xml of updated bib record data
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.post(f"{self.base_api_url}", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"))
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def delete_bib(self, mms_id,options = {}):

		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.delete(f"{self.base_api_url}{mms_id}", params=parameters)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def update_bib(self, mms_id, xml_record_data, options={}):

		"""
		Updates bibliographic record.
		Parameters:
			mms_id(str) - Alma MMS ID
			xml_record_data(str) - xml of updated bib record data
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
			self.status_code
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.put(f"{self.base_api_url}{mms_id}", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"))
		self.xml_response_data=  r.text
		self.status_code = r.status_code

	def get_holdings(self, mms_id, options={}):

		"""
		Retrieves all holdings attached to a given MMS ID
		Parameters:
			mms_id(str) - Alma MMS ID
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
			self.status_code
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}/holdings", params=parameters)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def get_holding(self, mms_id, holding_id, options={}):

		"""
		Retrieves an individual holding by holding ID
		Parameters:
			mms_id(str) - Alma MMS ID
			holding_id(str) - Alma holding ID
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
			self.status_code
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}/holdings{holding_id}", params=parameters)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def create_holding(self, mms_id, xml_record_data, options={}):

		"""
		Creates item
		Parameters:
			mms_id(str) - Alma MMS ID
			holding_id(str) Alma holding ID
			xml_record_data - item xml
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
			self.status_code
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.post(f"{self.base_api_url}{mms_id}/holdings", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"))
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def delete_holding(self, mms_id, holding_id):

		"""
		Deletes a holding by holding ID
		Parameters:
			mms_id(str) - Alma MMS ID
			holding_id(str) - Alma holding ID
		Returns:
			self.xml_response_data
			self.status_code
		"""
		r = requests.delete(f"{self.base_api_url}{mms_id}/holdings/{holding_id}?apikey={self.alma_key}")
		self.xml_response_data = r.text
		self.status_code = r.status_code
	
	def get_items(self, mms_id,  holding_id, options={}):

		"""
		Retrieves all items for MMS ID and holding ID
		Parameters:
			mms_id(str) - Alma MMS ID
			holding_id(str) - Alma holding ID
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
			self.status_code
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}/holdings/{holding_id}/items", params=parameters)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def get_item(self, mms_id, holding_id, item_pid, options={}):

		"""
		Retrieves an individual item by item PID
		Parameters:
			mms_id(str) - Alma MMS ID
			holding_id(str) Alma holding ID
			item_pid(str) - Alma item PID
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
			self.status_code
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}/holdings/{holding_id}/items/{item_pid}", params=parameters)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def create_item(self, mms_id, holding_id, xml_record_data, options={}):

		"""
		Creates item
		Parameters:
			mms_id(str) - Alma MMS ID
			holding_id(str) Alma holding ID
			xml_record_data - item xml
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
			self.status_code
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.post(f"{self.base_api_url}{mms_id}/holdings/{holding_id}/items", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"))
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def update_item(self, mms_id, holding_id, item_pid, xml_record_data, options={}):
		
		"""
		Updates item with new item XML data

		Parameters:
			mms_id(str) - Alma MMS ID
			xml_record_data(str) - XML of updated item record data
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
			self.status_code
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.put(f"{self.base_api_url}{mms_id}/holdings/{holding_id}/items/{item_pid}", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"))
		self.xml_response_data=  r.text
		self.status_code = r.status_code

	def delete_item( self, mms_id, holding_id, item_pid):

		"""
		Deletes item by item PID
		Parameters:
			mms_id(str) - Alma MMS ID
			holding_id(str) Alma holding ID
			item_pid(str) - Alma item PID
		Returns:
			self.xml_response_data
			self.status_code
		"""
		r = requests.delete(f"{self.base_api_url}{mms_id}/holdings/{holding_id}/items/{item_pid}?apikey={self.alma_key}")
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def get_representations(self, mms_id, options={}):

		"""
		Retrieves digital representations attached to a given MMS ID 
		Parameters:
			mms_id(str) - Alma MMS ID
			options(dict) - optional parameters for request
		Returns:
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}/representations", params=parameters)
		self.xml_response_data=  r.text
		self.status_code = r.status_code
	def get_representation(self, mms_id, rep_id, options={}):

		"""
		Retrieves digital representations attached to a given MMS ID 
		Parameters:
			mms_id(str) - Alma MMS ID
			options(dict) - optional parameters for request
			rep_id(str) - Alma representation id
		Returns:
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}/representations/{rep_id}", params=parameters)
		self.xml_response_data=  r.text
		self.status_code = r.status_code

	def update_representation(self, mms_id, rep_id, xml_record_data, options={}):

		"""
		Updates represeintation with new digital represeintation XML data

		Parameters:
			mms_id(str) - Alma MMS ID
			rep_id(str) - Alma representation id
			xml_record_data(str) - XML of updated item record data
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
			self.status_code
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.put(f"{self.base_api_url}{mms_id}/representations/{rep_id}", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"))
		self.xml_response_data=  r.text
		self.status_code = r.status_code



	def get_po_line(self, po_line, options={}):

		""" 
		Retrieves the purchase order line  in XML for a given Alma POL
		Parameters:
			po_line(str) - Alma POL
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
			self.status_code
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.acq_base_api_url}{po_line}", params=parameters)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def update_po_line(self, po_line, xml_record_data, options={}):

		"""
		Updates POL.
		Parameters:
			po_line(str) - Alma POL
			xml_record_data(str) - xml of updated POL 
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
			self.status_code
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.put(f"{self.acq_base_api_url}{po_line}", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"))
		self.xml_response_data=  r.text
		self.status_code = r.status_code


	def create_item_by_po_line(self, po_line, xml_record_data, options={}):

		"""
		Creates item.
		Parameters:
			po_line(str) - Alma POL
			xml_record_data(str) - new item in xml format
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
			self.status_code
		Notes:
			holding_id required in the  xml data
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.post(f"{self.acq_base_api_url}{po_line}/items", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"))
		self.xml_response_data = r.text
		self.status_code = r.status_code



def main():

	"""Example of usage"""

	#mms_id = ""

	my_api = AlmaTools("prod")
	# mis_mms_list = ['9919046572802836','9919046573002836']
	# for mms in mis_mms_list:
	# 		my_api.delete_bib(mms)
	# 		print(my_api.xml_response_data.encode("utf-8"))
	#######################################
	# my_api.get_bib("9919089664602836", {"limit":"100"})
	# print(my_api.xml_response_data.encode("utf-8"))
	# #######################################
	# my_api.get_holdings(mms_id, {"limit":"100"})
	# print(my_api.xml_response_data.encode("utf-8"))
	#######################################
	# my_api.update_bib(mms_id, my_api.xml_record_data)
	# print(my_api.status_code)
	#######################################
	# my_api.get_representations(mms_id)
	# print(my_api.xml_response_data.encode("utf-8"))
	###############################################
	# my_api.get_porfolio("9919012972402836","53354322810002836")
	# print(my_api.xml_response_data)
	# print(my_api.status_code)
	#########################################
	# my_api.get_ecollection("9918748064302836","61325625670002836")
	# print(my_api.xml_response_data)
	# print(my_api.status_code)
	# ####################################################################
	# my_api.get_po_line("POL-32856")
	# print(my_api.xml_response_data)
	# print(my_api.status_code)
	####################################################################
	# my_api.get_item("9918166772702836","22294172070002836","23361571080002836")
	# print(my_api.xml_response_data)
	# print(my_api.status_code)
	# ####################################################################
	# my_api.get_po_line("POL-32856")
	# print(my_api.xml_response_data)
	# print(my_api.status_code)
	####################################################################
	# my_list = [["9918166769702836","22294170890002836","23361559820002836"],["9918166769702836","22294170890002836","23361570070002836"],["9918166772702836","22294172070002836","23361571080002836"],["9918166769902836","22294170920002836","23361571070002836"],["9918166769502836","22294170850002836","23361559680002836"],["9918963672702836","22346162470002836","23361559670002836"],["9918166769602836","22294170870002836","23361571060002836"],["9916482513502836","22218301930002836","23361559620002836"],["9918166770602836","22294170970002836","23361557880002836"],["9918166772902836","22294172110002836","23361559600002836"],["9913788543502836","22194217920002836","23361571050002836"]]
	# for lst in my_list:
	# 	mms_id= lst[0]
	# 	holding_id = lst[1]
	# 	item_pid = lst[2]
	# 	my_api.delete_item(mms_id, holding_id, item_pid)
	# 	print(my_api.xml_response_data)
	##################################################################################
	# file_path = r"mms_to_delete.txt"
	# with open(file_path,"r") as f:
	# 	data = f.read()
	# for el in data.split("\n"):
	# 	my_api.delete_bib(el)
	#################################################################################
	# mms_list = ["9919077172602836" ,"9919078573602836","9919078670802836"]
	# for mms in mms_list:
	# 	my_api.delete_bib(mms)
	# 	print(my_api.xml_response_data)

	###############################FROM ALMA SET FULL VIEW SPREADSHEET#########################################################
	# workook_path = r"Y:\ndha\pre-deposit_prod\LD_working\podcasts\assets\results_Kelli.xlsx"
	# if os.path.exists(workook_path):


	# 	wb = load_workbook(workook_path)
	# 	#Enter name of the working sheet below
	# 	ws= wb.get_sheet_by_name("results")
	# 	#if now headers min_row =1
	# 	for row in ws.iter_rows(min_row=2):
	# 	#21for full results
	# 	#depending on where mms id is row[3] should be changed to number of column started from 0.
	# 		mms = row[26].value
	# 		my_api.delete_bib(row[26].value)
	# 		print(my_api.xml_response_data)
	
	#########################################GET REPRESENTATION####################################
	# my_api.get_representation ("9918991865302836", "32363085860002836")
	# print(my_api.xml_response_data)
	#########################################GET SET MEMBERS###############################################
	# my_api.get_set_members("10310621450002836",{"limit":"100"})
	# print(my_api.xml_response_data)
	# bibs = re.findall(r"<id>(.*?)</id>", my_api.xml_response_data)	
	# titles = re.findall(r'<description>(.*?)</description>', my_api.xml_response_data)
	# print(len(bibs))
	# for ind in range(len(bibs)):
	# 	print(bibs[ind])
	# 	print(titles[ind])





if __name__ == '__main__':
	main()

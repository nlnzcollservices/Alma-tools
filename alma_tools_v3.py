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
		delete_item(self, mms_id, holding_id, item_pid, options)
		get_representations(self, mms_id, options)
		get_representation(self, mms_id, rep_id, options)
		update_representation(self, mms_id, rep_id, xml_record_data, options)
		create_item_by_po_line(self, po_line, xml_record_data, options)
		get_portfolios(self, mms_id, portfolio_id, oprions)
		get_portfolio(self, mms_id, portfolio_id, options)
		create_portfolio(self, mms_id, options)
		update_portfolio(self, mms_id, portfolio_id, options)
		delete_portfolio(self, mms_id, portfolio_id, options)
		get_ecollection(self, mms_id, ecollection_id, options)
		get_invoice(self, invoice_id, options)
		get_invoice_linesself, (invoice_id, options)
		get_invoice_line(self, invoice_id, line_id, options)
		update_invoice_line(self, invoice_id, line_id, options)
		create_invoice(self, xml_record_data)
		get_po_lines(self)
		get_po_line(self, po_line)
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
		self.acq_base_vendor_url = "https://api-ap.hosted.exlibrisgroup.com/almaws/v1/acq/vendors/"
		self.config_base_url = "https://api-ap.hosted.exlibrisgroup.com/almaws/v1/conf/"
		self.acq_base_invoice_url ="https://api-ap.hosted.exlibrisgroup.com/almaws/v1/acq/invoices/"
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
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}", params=parameters,verify= False)
		print(r.url)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def get_set(self, set_id, options={}):

		"""
		Retrieves sets by set_id.
		Parameters:
			set_id(str) - id of the set

		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r= requests.get(f"{self.config_base_url}sets/{set_id}",params = parameters, verify = False)
		# print(f'{self.config_base_url}sets/{set_id}')
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def get_set_members(self, set_id, options={}):

		""" 
		Retrieves set members.
		Parameters:
			set_id(str) - id of the set
		"""

		parameters = {**{"apikey": self.alma_key}, **options}
		r= requests.get(f"{self.config_base_url}sets/{set_id}/members",params = parameters, verify = False)
		# print(f'{self.config_base_url}sets/{set_id}')
		self.xml_response_data = r.text
		self.status_code = r.status_code


	def get_ecollection(self, mms_id, ecollection_id, options = {}):

		"""
		Retrieves an electronic collection record in xml 
		Argumets:
			collection_id(str) - id of the collection
		"""

		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}/e-collections/{ecollection_id}", params=parameters,verify= False)
		# print(r.text)
		self.xml_response_data = r.text
		self.status_code = r.status_code
	def get_portfolios(self, mms_id, options = {}):

		"""
		Retrieves all portfolios for a bib record in xml 
		Argumets:
			mms_id(str) - id of the bibliographic record
		Returns:
			None
		"""

		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}/portfolios", params=parameters, verify = False)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def get_portfolio(self, mms_id, portfolio_id, options = {}):

		"""
		Retrieves a portfolio record in xml 
		Argumets:
			mms_id(str) - id of the bibliographic record
			portfolio_id(str) - id of the portfolio
		Returns:
			None
		"""

		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}/portfolios/{portfolio_id}", params=parameters, verify = False)
		self.xml_response_data = r.text
		self.status_code = r.status_code


	def create_portfolio(self, mms_id, xml_record_data, options = {}):

		"""
		Creates a portfolio for a bib
		Argumets:
			mms_id(str) - id of the bibliographic record
		Returns:
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		xml_record_data = xml_record_data.replace("\\", "")
		r = requests.post(f"{self.base_api_url}{mms_id}/portfolios/", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"), verify= False)
		#print(r.url)
		self.xml_response_data = r.text
		self.status_code = r.status_code
		
	def update_portfolio(self, mms_id, portfolio_id, xml_record_data, options = {}):

		"""
		Creates a portfolio for a bib
		Argumets:
			mms_id(str) - id of the bibliographic record
		Returns:
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		xml_record_data = xml_record_data.replace("\\", "")
		r = requests.put(f"{self.base_api_url}{mms_id}/portfolios/{portfolio_id}", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"), verify= False)
		#print(r.url)
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
		r = requests.delete (f"{self.base_api_url}{mms_id}/portfolios/{portfolio_id}", params=parameters, verify= False)
		self.xml_response_data = r.text
		self.status_code = r.status_code


	def get_invoice(self, invoice_id, options={}):

		"""
		Extracts invoice in xml format
		Argumets:
			invoice_id(str) - id of the invoice
		Returns:
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.acq_base_invoice_url}{invoice_id}",params=parameters, verify= False)
		# print(r.url)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def get_invoices(self, options={}):
		
		"""
		Extracts all invoices in xml format
		Returns:
			None
		"""

		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.acq_base_invoice_url}".rstrip("/"),params=parameters,verify= False)
		# print(r.url)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def get_invoice_lines(self, invoice_id, options={}):
		
		"""
		Extracts invoice lines in xml format
		Argumets:
			invoice_id(str) - id of the invoice
		Returns:
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.acq_base_invoice_url}{invoice_id}/lines",params=parameters,verify= False)
		# print(r.url)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def get_invoice_line(self, invoice_id, line_id, options={}):
		
		"""
		Extracts invoice linein xml format
		Argumets:
			invoice_id(str) - id of the invoice
			line_id(str) - id of the invoice line
		Returns:
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		print(f"{self.acq_base_invoice_url}{invoice_id}/lines/{line_id}")
		r = requests.get(f"{self.acq_base_invoice_url}{invoice_id}/lines/{line_id}",params=parameters,verify= False)
		print(r.url)
		self.xml_response_data = r.text
		self.status_code = r.status_code


	def create_bib(self, xml_record_data, options = {}):

		"""
		Creates bibliographic record
		Paramrters:			
			xml_record_data(str) - xml of updated bib record data
			options(dict) - optional parameters for request
		Returns:
			None
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.post(f"{self.base_api_url}", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"),verify= False)
		self.xml_response_data = r.text
		self.status_code = r.status_code
	

	def add_bib_to_collection(self, collection_id, xml_record_data, options = {}):

		"""
		Adds bibliographical record to collection
		Paramrters:			
			collection_id - id of collection in Alma
			xml_record_data(str) - xml contained single mms id only <bib><mms_id>999999</mms_id><bib>
			options(dict) - optional parameters for request
		Returns:
			None
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.post(f"{self.base_api_url}collections/{collection_id}/bibs", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"),verify= False)
		self.xml_response_data = r.text
		self.status_code = r.status_code



	def delete_bib(self, mms_id,options = {}):

		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.delete(f"{self.base_api_url}{mms_id}", params=parameters,verify= False)
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
			None
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.put(f"{self.base_api_url}{mms_id}", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"),verify= False)
		self.xml_response_data=  r.text
		self.status_code = r.status_code
		

	def update_invoice(self, invoice_id, xml_record_data, options={}):

		"""
		Updates invoice.
		Parameters:
			invoice_id(str) - Alma Invoice ID
			xml_record_data(str) - xml of updated bib record data
			options(dict) - optional parameters for request
		Returns:
			None
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.put(f"{self.acq_base_invoice_url}{invoice_id}", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"),verify= False)
		self.xml_response_data=  r.text
		self.status_code = r.status_code

	def update_invoice_line(self, invoice_id, line_id, xml_record_data, options={}):

		"""
		Updates invoice line.
		Parameters:
			invoice_id(str) - Alma Invoice ID
			line_id(str) - Alma invoice line id.
			xml_record_data(str) - xml of updated bib record data
			options(dict) - optional parameters for request
		Returns:
			None
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.put(f"{self.acq_base_invoice_url}{invoice_id}/lines/{line_id}", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"), verify= False)
		self.xml_response_data=  r.text
		self.status_code = r.status_code

	def process_invoice(self, invoice_id, options={"op":"process_invoice"}):

		"""
		Updates invoice after making new invoice and new lines to activate it.
		Parameters:
			invoice_id(str) - Alma Invoice ID
			options(dict) - optional parameters for request
		Returns:
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		xml_record_data = "<invoice></invoice>"
		r = requests.post(f"{self.acq_base_invoice_url}{invoice_id}", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"), verify= False)
		self.xml_response_data=  r.text
		self.status_code = r.status_code

	def create_invoice(self, xml_record_data, options={}):

		"""
		Creates invoice.
		Parameters:
			invoice_id(str) - Alma Invoice ID
			options(dict) - optional parameters for request
		Returns:
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.post(f"{self.acq_base_invoice_url}", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"), verify= False)
		self.xml_response_data=  r.text
		self.status_code = r.status_code



	def create_invoice_line(self, invoice_id, xml_record_data, options={}):

		"""
		Creates invoice line.
		Parameters:
			invoice_id(str) - Alma Invoice ID
			xml_record_data(str) - xml of updated bib record data
			options(dict) - optional parameters for request
		Returns:
			None
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.post(f"{self.acq_base_invoice_url}{invoice_id}/lines/", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"),verify= False)
		self.xml_response_data=  r.text
		self.status_code = r.status_code

	def get_holdings(self, mms_id, options={}):

		"""
		Retrieves all holdings attached to a given MMS ID
		Parameters:
			mms_id(str) - Alma MMS ID
			options(dict) - optional parameters for request
		Returns:
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}/holdings", params=parameters,verify= False)
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
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}/holdings/{holding_id}", params=parameters,verify= False)
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
			None
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.post(f"{self.base_api_url}{mms_id}/holdings", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"),verify= False)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def delete_holding(self, mms_id, holding_id):

		"""
		Deletes a holding by holding ID
		Parameters:
			mms_id(str) - Alma MMS ID
			holding_id(str) - Alma holding ID
		Returns:
			None
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
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}/holdings/{holding_id}/items", params=parameters,verify= False)
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
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.base_api_url}{mms_id}/holdings/{holding_id}/items/{item_pid}", params=parameters,verify= False)
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
			None
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		
		r = requests.post(f"{self.base_api_url}{mms_id}/holdings/{holding_id}/items", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"),verify= False)
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
			None
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.put(f"{self.base_api_url}{mms_id}/holdings/{holding_id}/items/{item_pid}", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"),verify= False)
		self.xml_response_data=  r.text
		self.status_code = r.status_code

	def delete_item( self, mms_id, holding_id, item_pid,options={}):

		"""
		Deletes item by item PID
		Parameters:
			mms_id(str) - Alma MMS ID
			holding_id(str) Alma holding ID
			item_pid(str) - Alma item PID
		Returns:
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.delete(f"{self.base_api_url}{mms_id}/holdings/{holding_id}/items/{item_pid}",params=parameters,verify= False)
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
		r = requests.get(f"{self.base_api_url}{mms_id}/representations", params=parameters, verify= False)
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
		r = requests.get(f"{self.base_api_url}{mms_id}/representations/{rep_id}", params=parameters,verify= False)
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
			None
		"""
		xml_record_data = xml_record_data#.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.put(f"{self.base_api_url}{mms_id}/representations/{rep_id}", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"),verify= False)
		# print(r.url)
		self.xml_response_data=  r.text
		self.status_code = r.status_code



	def get_po_line(self, po_line, options={}):

		""" 
		Retrieves the purchase order line  in XML for a given Alma POL
		Parameters:
			po_line(str) - Alma POL
			options(dict) - optional parameters for request
		Returns:
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.acq_base_api_url}{po_line}", params=parameters,verify= False)
		self.xml_response_data = r.text
		self.status_code = r.status_code


	

	def get_vendor(self, vendor_code, options={}):

		""" 
		Retrieves the purchase order line  in XML for a given Alma POL
		Parameters:
			vendor_code(str) - Alma vendor code
			options(dict) - optional parameters for request
		Returns:
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.acq_base_vendor_url}{vendor_code}", params=parameters,verify= False)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def get_po_lines(self, options={}):

		""" 
		Retrieves the purchase order lines  in XML for a given Alma POL
		Parameters:
			options(dict) - optional parameters for request
		Returns:
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.acq_base_api_url}", params=parameters,verify= False)
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
			None
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.put(f"{self.acq_base_api_url}{po_line}", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"),verify= False)
		self.xml_response_data=  r.text
		self.status_code = r.status_code
	def get_items_by_po_line(self, po_line, options={}):
		
		""" 
		Gets items by po_line
		Parameters:
			po_line(str) - Alma POL
		Returns:
			None
		"""

		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.get(f"{self.acq_base_api_url}{po_line}/items", params=parameters,verify= False)
		# print(r.url)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	
	def create_item_by_po_line(self, po_line, xml_record_data, options={}):

		"""
		Creates item.
		Parameters:
			po_line(str) - Alma POL
			xml_record_data(str) - new item in xml format
			options(dict) - optional parameters for request
		Returns:
			None
		Notes:
			holding_id required in the  xml data
		"""
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.post(f"{self.acq_base_api_url}{po_line}/items", headers=self.headers, params=parameters, data=xml_record_data.encode("utf-8"),verify= False)
		# print(r.url)
		self.xml_response_data = r.text
		self.status_code = r.status_code

	def receive_item(self, po_line, item_pid, xml_record_data, options={}):

		"""
		Creates item.
		Parameters:
			po_line(str) - Alma POL
			xml_record_data(str) - new item in xml format
			options(dict) - optional parameters for request
		Returns:
			None
		"""
		parameters = {**{"apikey": self.alma_key}, **options}
		r = requests.post(f"{self.acq_base_api_url}{po_line}/items/{item_pid}", xml_record_data, headers=self.headers, params=parameters,verify= False)
		self.xml_response_data = r.text
		self.status_code = r.status_code

def main():

	"""Example of usage"""

	mms_id = ""
	my_api = AlmaTools("prod")
	my_api.get_bib(mms_id)



if __name__ == '__main__':
	main()

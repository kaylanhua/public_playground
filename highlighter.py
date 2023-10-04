# pip3 install PyMuPDF
# pip3 install fitz
import re
import fitz 
import sys

class Redactor:
    
	# static methods work independent of class object
	@staticmethod
	def get_sensitive_data(lines):
		
		# EMAIL_REG = r"([\w\.\d]+\@[\w\d]+\.[\w\d]+(\.[\w\d]+)?)"
		EMAIL_REG = r"([\w\.\d]+\@[^\s]+)"
		PHONE_REG = r"(?<![-\w\.\,\?\!\'\"\(\)\:\;\\\/])(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[-.()\s]?\d{3}[-.()\s]?\d{4}(?!\w)"
		TWITTER_REG = r"@([A-Za-z0-9_]{1,15})"
		list = ["Plaza", "Lane", "Road", "Boulevard", "Drive", "Street", "Place", "Park", "Court", "Ave", "Dr", "Rd", "Blvd", "Ln", "St", "Pl", "Ct"]
		running_string = "Avenue"
		for name in list:
			running_string += "|" + name + "|" + name.upper()

		DETAILED_ADDR_REG = r"(?<![-\w\.\,\?\!\'\"\(\)\:\;])(\d{1,6})[ ]{1,3}(?:[\'\’A-Za-z0-9.-]{1,25}[ ]{1,3}){1}(?:" + running_string + r")\.?([ ](?:[A-Za-z0-9.-]{1,14})?)?"
		for line in lines:
			email_match = re.search(EMAIL_REG, line, re.IGNORECASE)
			phone_match = re.search(PHONE_REG, line)
			twitter_match = re.search(TWITTER_REG, line, re.IGNORECASE)
			addr_match = re.search(DETAILED_ADDR_REG, line)

			potential_matches = [email_match, phone_match, twitter_match, addr_match]
			for match in potential_matches:
				if match:
					yield match.group()

	# constructor
	def __init__(self, path):
		self.path = path

	def redaction(self):
	
		""" main redactor code """
		
		# opening the pdf
		doc = fitz.open(self.path)
		
		sigs = []
		# iterating through pages
		for page in doc:
		
			# _wrapContents is needed for fixing
			# alignment issues with rect boxes in some
			# cases where there is alignment issue
			# page._wrapContents()
			
			# getting the rect boxes which consists the matching email regex
			sensitive = self.get_sensitive_data(page.get_text("text")
												.split('\n'))
			for data in sensitive:
				areas = page.search_for(data)
				
				# drawing outline over sensitive datas
				# [page.add_redact_annot(area, fill = (0, 0, 0)) for area in areas]
				# add highlighting instead of blacking out
				[page.add_highlight_annot(area).set_colors(stroke=[1, 0, 1]) for area in areas]
				
			# applying the redaction
			page.apply_redactions()
			
		# saving it to a new pdf
		doc.save('redacted.pdf')
		print("Successfully redacted")

# driver code for testing
if __name__ == "__main__":
	
	# Check if an argument is provided
	if len(sys.argv) > 1:
		pdf_name = sys.argv[1]
	else:
		pdf_name = 'doc.pdf'

	redactor = Redactor(pdf_name)
	redactor.redaction()



   
 
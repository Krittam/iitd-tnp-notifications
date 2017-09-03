from HTMLParser import HTMLParser

class CompanyParser(HTMLParser):
    
    def __init__(self):
        # super().__init__() Python3
        self.reset()
        self._companies = []
        self.company_table = False
        self.company_row = False
        # self.company_cell = False
        self.company_count = 0
        self.company = None

    def handle_starttag(self, tag, attrs):
        if (tag == 'table' and self.validate_company_table(attrs)):
            # print("Encountered table  :")
            self.company_table = True
            # print(attrs)
        if (self.company_table and self.company_row and tag == 'tr'):            
            # print ('company',self.company)
            self._companies.append(self.company)            
            self.company = None 
            self.company_row = False
            return      
        if (self.company_table and tag == 'tr'):            
            self.company_count += 1
            self.company_row = True
    def handle_endtag(self, tag):
        if (self.company_table and tag == 'table'):
            self.company_table = False
            # print('table ended')
        if (tag == 'tr'):
            # print ('company table is',self.company_table)        
            pass
    def handle_data(self, data):
        if self.company_table and self.company_row:
            # print ('adding data', data)
            # print (self.company_count,len(self._companies))
            if not self.company:
                self.company = []
            self.company.append(data)
            # print(self.company)

    def validate_company_table(self,attrs):
        for key ,value in attrs:
            if key == 'class' and value =='sortable':
                return True
        return False

    def get_companies(self):
        if self.company:            
            self._companies.append(self.company)
        return self._companies

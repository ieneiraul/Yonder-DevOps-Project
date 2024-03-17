import requests
import pandas as pd
from datetime import datetime

class APIClient:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self, count):
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                data = response.json()[:count]
                return data
            else:
                print(f"Failed to fetch data from API. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

class ConsoleApp:
    def __init__(self, api_client):
        self.api_client = api_client
        self.data = None

    def export_to_excel(self, data, file_name):
        if data:
            df = pd.DataFrame(data)
            df.to_excel(file_name, index=False)
            print(f"Data exported to {file_name}")
        else:
            print("No data to export.")

    def find_suspended_licenses(self):
        if self.data:
            suspended_licenses = [item for item in self.data if item['suspendat']==True]
            self.export_to_excel(suspended_licenses, "suspended_licenses.xlsx") 
        else:
            print("No data available.")

    def find_valid_licenses_until_today(self):
        if self.data:
            today = datetime.today().date()
            items_until_today = [item for item in self.data if self.convert_to_date(item['dataDeExpirare']) >= today]
            self.export_to_excel(items_until_today, "valid_licenses_until_today.xlsx")
        else:
            print("No data available.")

    def convert_to_date(self, date_str):
        return datetime.strptime(date_str, '%d/%m/%Y').date() if isinstance(date_str, str) else date_str
    
    def find_licenses_by_category(self, category):
        if self.data:
            items_by_category = [item for item in self.data if item['categorie'] == category]
            self.export_to_excel(items_by_category, "licenses_by_category.xlsx")
        else:
            print("No data available.")

    def fetch_license_data(self):
        count = 150
        self.data = self.api_client.fetch_data(count)
        
    def console(self):
        print("Welcome! Please select an option from the menu:")
        num = 1
        while(num):
            print("1. List suspended licenses by the authority.")
            print("2. Extract valid licenses issued until today's date.")
            print("3. Find licenses based on category and their count.")
            print("0. Exit app.")
            try:
                num = int(input("Enter a number: "))
                if num == 1:
                    self.find_suspended_licenses()
                elif num == 2:
                    self.find_valid_licenses_until_today()
                elif num == 3:
                    category = input("Enter a category: ")
                    self.find_licenses_by_category(category)
                elif num == 0:
                    break   
                else:
                    print("You entered a number other than 1, 2, 3, or 0")
            except ValueError:
                print("Invalid input! Please enter a valid number.")

    def run(self):
        self.fetch_license_data()
        self.console()
        


def main():
    api_url = "http://localhost:30000/drivers-licenses/list?length=150"
    api_client = APIClient(api_url)
    app = ConsoleApp(api_client)
    app.run()

main()
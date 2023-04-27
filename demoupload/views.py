from django.shortcuts import render
from django.http import HttpResponse
import openpyxl
import json
from pprint import pprint
from demoupload.commons.utils import stringChecks

def UploadExcel(request):
    
    if "GET" == request.method:
        return render(request, 'index.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        # you may put validations here to check extension or file size
        try:
            wb = openpyxl.load_workbook(excel_file)
        except Exception as e:
            print("Invalid File", e)
            return render(request, 'index.html', {"message":"Invalid File"})

        # getting a particular sheet by name out of many sheets
        worksheet = wb.worksheets[0]
        # Loading Json
        try:
        
            with open("demoupload/jsons/welcome.json", "r") as f:
                json_data = json.load(f)
                
        except IOError as e:
            return render(request, 'index.html', { "message":"Failed to get json"})
        
        field_data = json_data['data_collection_form']['fields']
        
        excel_data = []
        # iterating over the rows
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)

        headers = excel_data[0]

        #check if headers are valid
        valid, invalidHeaders = stringChecks.checkValidHeader(headers)
        if not valid:
            message = "Error ! Following headers are in invalid format : \n " + (" , ".join(c for c in invalidHeaders))
            return render(request, 'index.html', { "message":message})


        for index,header in enumerate(headers):
            
            h = header.lower().strip().replace(" ","_")

            searched_field = list(filter(lambda k: k['name'] == h, field_data))
            options = [row[index] for row in excel_data if row[index] != "None"][1:]

            #check if options are in valid format
            valid, invalidHeaders = stringChecks.checkValidOptions(options)
            if not valid:
                message = f"Error !! One or more options in { header } are in invalid format"
                return render(request, 'index.html', { "message":message})


            if len(options) == 0:
                continue

            # Update if the field already exist
            if len(searched_field) > 0:
                field = searched_field[0]
                field['options'] = options
            # Adding new field
            else:
                field = {
                    "type":"select",
                    "label":h.title() + ":",
                    "name":h,
                    "options": options
                }
                field_data.append(field)


        # writing json
        json_object = json.dumps(json_data)

        try:
            # Writing to sample.json
            with open("demoupload/jsons/welcome.json", "w") as f:
                f.write(json_object)
        except IOError as e:
            print("Failed to write json", e)
            return render(request, 'index.html', {"message":"Failed to Update"})

        return render(request, 'index.html', {"excel_data":excel_data})

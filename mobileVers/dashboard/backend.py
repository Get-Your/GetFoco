"""
Get FoCo is a platform for application and administration of income-
qualified programs offered by the City of Fort Collins.
Copyright (C) 2019

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from django.shortcuts import render, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist

# Grace User Authentication
from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.hashers import check_password

from django.conf import settings

#below imports needed for blob storage
from azure.storage.blob import BlockBlobService

from .models import User
from application.models import MoreInfo, Addresses


def blobStorageUpload(filename, file):
    blob_service_client = BlockBlobService(
        account_name=settings.BLOB_STORE_NAME,
        account_key=settings.BLOB_STORE_KEY,
        endpoint_suffix=settings.BLOB_STORE_SUFFIX,
        )
    
    blob_service_client.create_blob_from_bytes(
        container_name = settings.USER_FILES_CONTAINER,
        blob_name = filename,
        blob = file.read(),
    )

def authenticate(username=None, password=None):
    User = get_user_model()
    try: #to allow authentication through phone number or any other field, modify the below statement
        user = User.objects.get(email=username)
        print(user)
        print(password)
        print(user.password)
        print(user.check_password(password))
        if user.check_password(password):
            return user 
        return None
    except User.DoesNotExist:
        return None

def get_user(self, user_id):
    try:
        return UserModel.objects.get(id=user_id)
    except UserModel.DoesNotExist:
        return None

def files_to_string(file_list):
    list_string = ""
    counter = 0

    print(counter)
    # Get File_List into easy to read list to print out in template
    for key, value in file_list.items():
        # only add things to the list_string if its true
        if value == True:
            # Also add commas based on counter
            if counter == 5:
                list_string += "\n"
                counter = 4
            elif counter == 4:
                list_string += "\n"
                counter = 3
            elif counter == 3:
                list_string += "\n"
                counter = 2
            elif counter == 2:
                list_string += "\n"
                counter = 1
            elif counter == 1:
                list_string += "\n"
                counter = 0
            else:
                counter = 5
            list_string += key
    return list_string

# redirect user to whatever page they need to go to every time by checking which steps they've
# completed in the application process
def what_page(user,request):
    if user.is_authenticated:
        
        searchForUser = request.user.id
        
        #for some reason, none of these login correctly... reviewing this now
        try: #check if the addresses.is_verified==True
            if Addresses.objects.all().filter(user_id_id=searchForUser).exists() and Addresses.objects.get(user_id_id=searchForUser).is_verified:
                print("Address has been verified")
            else:
                print("Still need to verify address")
                raise AttributeError()
            
        except AttributeError:
            return "application:address"

        try: #check if finances is filled
            value = request.user.eligibility
        except AttributeError:
            return "application:finances"

        try: #check if dependents / birthdays are filled
            if(MoreInfo.objects.all().filter(user_id_id=searchForUser).exists()):
                print("MoreInfo exists")
            else:
                print("MoreInfo doesn't exist")
                return "application:moreInfoNeeded"
        except AttributeError or ObjectDoesNotExist:
            return "application:moreInfoNeeded"
        
        try: #check if programs is filled out
            value = request.user.programs
        except AttributeError or ObjectDoesNotExist:
            return "application:programs"

        try: #check if files are all uploaded
            file_list = {
                "SNAP Card": request.user.programs.snap,
                # Have Reduced Lunch be last item in the list if we add more programs
                "PSD Reduced Lunch Approval Letter": request.user.programs.freeReducedLunch,
                "Affordable Connectivity Program": request.user.programs.ebb_acf,
                "Identification": request.user.programs.Identification,
                "Medicaid Card": request.user.programs.medicaid,
                "LEAP Letter": request.user.programs.leap,
            }

            Forms = request.user.files
            checkAllForms = [not(request.user.programs.snap),not(request.user.programs.freeReducedLunch),not(request.user.programs.ebb_acf),not(request.user.programs.Identification),not(request.user.programs.leap),not(request.user.programs.medicaid),]
            for group in Forms.all():
                if group.document_title == "SNAP":
                    checkAllForms[0] = True
                    file_list["SNAP Card"] = False
                if group.document_title == "Free and Reduced Lunch":
                    checkAllForms[1] = True
                    file_list["PSD Reduced Lunch Approval Letter"] = False
                if group.document_title == "ACP Letter":
                    checkAllForms[2] = True
                    file_list["Affordable Connectivity Program"] = False
                if group.document_title == "Identification":
                    checkAllForms[3] = True
                    file_list["Identification"] = False
                if group.document_title == "LEAP Letter":
                    checkAllForms[4] = True
                    file_list["LEAP Letter"] = False
                if group.document_title == "Medicaid":
                    checkAllForms[5] = True
                    file_list["Medicaid Card"] = False
            if False in checkAllForms:
                return "dashboard:files"
            else:
                print("files found")
        except AttributeError:
            return "dashboard:files"

        try: #check if ACP last four SSN is needed or not...
            if ((request.user.programs.ebb_acf) == True) and ((request.user.taxinformation.last4SSN) == "NULL"):
                return "application:filesInfoNeeded"
            else:
                print("last 4 ssn found")
        except:
            return "application:filesInfoNeeded"



        return "dashboard:dashboard"
    else:
        return "application:account"
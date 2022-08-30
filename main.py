import datetime
import logging
import os
import sdm_service
import sys
import base64

GRANT_TIMEOUT=60 #minutes
SECRET=base64.b64encode("1234:1234")

print("RUN_ID:", os.getenv("RUN_ID"))
print("SECRET:", SECRET)

def get_params():
    if not sys.argv or len(sys.argv) != 3:
        raise Exception("Invalid number of arguments")
    return sys.argv[1], sys.argv[2]

class GrantTemporaryAccess:
    service = sdm_service.create_sdm_service(
        os.getenv("RUN_ID"),
        SECRET,
        logging,
        host="ec2-35-87-197-41.us-west-2.compute.amazonaws.com:5000",
        insecure=True
    )

    def __init__(self, resource_name, user_email):
        self.resource_name = resource_name
        self.user_email = user_email
        
    def __get_resource_id(self):
        try: 
            resource = self.service.get_resource_by_name(self.resource_name)
            return resource.id
        except Exception as e:
            raise Exception(f"Invalid resource name {self.resource_name}") from e

    def __get_account_id(self):
        try: 
            account = self.service.get_account_by_email(self.user_email)
            return account.id
        except Exception as e:
            raise Exception(f"Invalid user email {self.user_email}") from e

    def execute(self):
        grant_start_from = datetime.datetime.now(datetime.timezone.utc)
        grant_valid_until = grant_start_from + datetime.timedelta(minutes=GRANT_TIMEOUT)
        self.service.grant_temporary_access(
            self.__get_resource_id(), 
            self.__get_account_id(), 
            grant_start_from, 
            grant_valid_until
        )

resource_name, user_email = get_params()
GrantTemporaryAccess(resource_name, user_email).execute()
print(f"Temporary grant successfullly created for {user_email} on {resource_name}")

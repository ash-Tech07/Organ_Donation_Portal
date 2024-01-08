
from thirdweb import ThirdwebSDK
from thirdweb.types import SDKOptions
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv('THIRD_WEB_SECRET_KEY')
private_key = os.getenv('THIRD_WEB_PRIVATE_KEY')


sdk = ThirdwebSDK("mumbai", options=SDKOptions(secret_key=secret_key))
contract = sdk.get_contract("0x8ca329BdFb1fa623B5111585b7D55F1168893eEB")


def getRecipientsData(key):
    return contract.call("recipients", key)

def addRecipient(patient_data):
    return contract.call("addRecipient", patient_data['_recipientID'], patient_data['_age'], patient_data['_bloodType'], patient_data['_cpra'], patient_data['_Disease'], patient_data['_timeOnDialysis'], patient_data['_numberOfPriorTransplants'], patient_data['_cPRA_cat'], patient_data['_HLA_A1'], patient_data['_HLA_A2'], patient_data['_HLA_B1'])

# print(addRecipient({'_recipientID': 16, '_age': 18, '_bloodType': 'O', '_cpra': 5, '_Disease': 'others', '_timeOnDialysis': 1, '_numberOfPriorTransplants': 0, '_cPRA_cat': 'under60', '_HLA_A1': '1', '_HLA_A2': '1', '_HLA_B1': '1'}))
print(getRecipientsData(16))

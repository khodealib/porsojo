from abc import ABC

from kavenegar import APIException, HTTPException, KavenegarAPI

from accounts.models.otp_token import OtpToken
from utils.exceptions import KavenegarAPIException, KavenegarUnexpectedHTTPException


class BaseOtpService(ABC):
    otp_code_model_class = OtpToken

    def send_otp(self, phone_number: str) -> None:
        pass

    def verify_otp(self, phone_number: str, otp: str) -> bool:
        otp_token = self.otp_code_model_class.objects.filter(phone_number=phone_number, code=otp).first()
        if otp_token and otp_token.code == int(otp) and not otp_token.is_expire:
            return True
        return False


class FakeOtpService(BaseOtpService):
    def send_otp(self, phone_number: str) -> None:
        otp_token = self.otp_code_model_class.objects.create(phone_number=phone_number, code=OtpToken.generate_code())
        print("--------------------------------")
        print(f"Send OTP to {phone_number}: {otp_token.code}")
        print("--------------------------------")


class KavenegarOtpService(BaseOtpService):
    def __init__(self, api_key: str):
        self.api = KavenegarAPI(api_key)

    def send_otp(self, phone_number: str) -> None:
        otp_token = self.otp_code_model_class.objects.create(phone_number=phone_number, code=OtpToken.generate_code())
        try:
            params = {
                "receptor": phone_number,
                "message": f"Your Token #{otp_token.code}",
            }
            response = self.api.sms_send(params)
            print("--------------------------------")
            print("Kavenegar console log")
            print(response)
            print("--------------------------------")
        except APIException as e:
            raise KavenegarAPIException
        except HTTPException as e:
            raise KavenegarUnexpectedHTTPException

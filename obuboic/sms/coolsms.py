from sdk.api.message import Message
from sdk.exceptions import CoolsmsException


def send_sms_code(api_key, api_secret, phone, code):
    # 4개의 필수 파라미터(to, from, type, text)
    params = dict()
    params['type'] = 'sms'  # Message Type : sms, lms, mms, ata
    params['to'] = phone
    params['from'] = '01027910138'
    params['text'] = '[어부바] 인증번호 ['+code+'] \n타인에게 절대 알려주지 마세요.'  # Message

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

        return 200

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

        return 400


def send_sms_link(api_key, api_secret, phone, content):
    # 4개의 필수 파라미터(to, from, type, text)
    params = dict()
    params['type'] = 'sms'  # Message Type : sms, lms, mms, ata
    params['to'] = phone
    params['from'] = '01027910138'
    params['text'] = content  # Message

    cool = Message(api_key, api_secret)
    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])

        return 200

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)

        return 400

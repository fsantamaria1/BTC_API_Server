from flask import make_response, jsonify

#This class generates API Responses
class ApiMessage(dict):
    def __init__(self, status_code, message):
        self.http_code = status_code
        self.message = message

    def __call__(self):
        json_response = jsonify({'message':self.message})
        return json_response, self.http_code
 

CouldNotVerify = ApiMessage(401, 'Could not verify')
CannotPerformThatAction = ApiMessage(403, 'Cannot perform that action!')
LoginRequired = ApiMessage(401, 'Login required')
InvalidCredentials = ApiMessage(401, 'Invalid username or password')
NoDataFound = ApiMessage(400, 'No data found!')

#Password related
NoPasswordFound = ApiMessage(400, 'No password found!')
PasswordTooShort = ApiMessage(400, 'Password too short')

#User related
UserCeated = ApiMessage(200, 'The user has been created!')
UserDeleted = ApiMessage(200, 'The user has been deleted')
UserPromoted = ApiMessage(200, 'The user has been promoted!')
UserDoesNotExist = ApiMessage(401, 'User does not exist')
UserAlreadyExists = ApiMessage(401, 'User already exists')
UsernameTooShort = ApiMessage(400, 'Username too short')
NoUsernameFound = ApiMessage(400, 'No username found!')
#Promotion
NoPromotionFound = ApiMessage(400, 'No promotion found')
NoValidPromotionFound = ApiMessage(400, 'No valid promotion found')

#Token related
TokenIsMissing = ApiMessage(401, 'Token is missing')
InvalidToken = ApiMessage(401, 'Token is invalid')

#Timesheet related
TimesheetAlreadyExists = ApiMessage(400, 'Timesheet already exists')
TimesheetCeated = ApiMessage(200, 'The timesheet has been created!')
TimesheetDoesNotExists = ApiMessage(400, 'Timesheet does not exists')
NoDivisionFound = ApiMessage(400, 'No division found')
NoJobNumberFound = ApiMessage(400, 'No job number found')
NoTextFound = ApiMessage(400, 'No text found')

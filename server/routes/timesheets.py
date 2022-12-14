from flask import current_app as app
from flask import request, jsonify
from server.resources import messages, db
from server.resources.models import Timesheet
from server.resources.decorators import token_required
import uuid
from server.resources.date_parser import date_parser

table_user_fields = [
    "division",
    "job_number",
    "work_order",
    "address",
    "job_date",
    "arrive_time",
    "left_time",
    "notes",
    "signature",
    "complete"
    ]

@app.route('/timesheet', methods=['POST'])
@token_required
def create_timesheet(current_user):
    #Make sure the user is active
    if not current_user.active:
        return messages.CannotPerformThatAction()
    
    try:
        #Grab all data from request
        data = request.get_json()

        # Loop through json to find missing data
        for field in table_user_fields:
            if not data.get(field):
                message = messages.ApiMessage(401, "fail", {'title': f"Missing data: {field}"})
                return message()

    except:
        return messages.NoDataFound()

    # Query dabatase to see if the timesheet already exists
    existing_timesheet = Timesheet.query.filter_by(job_number=data["job_number"]).first()

    if not existing_timesheet:

        #Convert string to datetime object
        job_date_obj = date_parser().string_to_date(data["job_date"])
        arrive_time_obj = date_parser().combine_date_and_time_strings(data["job_date"], data["arrive_time"])
        left_time_obj = date_parser().combine_date_and_time_strings(data["job_date"], data["left_time"])

        #Create new user
        new_timesheet = Timesheet(public_id=str(uuid.uuid4()), 
        division=data["division"], 
        job_number=data["job_number"] , 
        work_order=data["work_order"], 
        address=data["address"],
        job_date=job_date_obj,
        arrive_time=arrive_time_obj,
        left_time=left_time_obj,
        notes=data["notes"],
        signature=data["signature"],
        complete=data["complete"], 
        user_id=current_user.username)

        db.session.add(new_timesheet)
        db.session.commit()

        return messages.TimesheetCeated()
    else:
        return messages.TimesheetAlreadyExists()

@app.route('/timesheets', methods=['GET'])
@token_required
def get_all_timesheets(current_user):

    # Query database based on user role
    if current_user.active:
        if (current_user.admin) or (current_user.manager):
            timesheets = Timesheet.query.all()
        else:
            timesheets = Timesheet.query.filter_by(user_id=current_user.username)
    else:
        return messages.CannotPerformThatAction()

    output = []

    for timesheet in timesheets:
        timesheet_data = {}
        timesheet_data['public_id'] = timesheet.public_id
        timesheet_data['division'] = timesheet.division
        timesheet_data['job_number'] = timesheet.job_number
        timesheet_data['work_order'] = timesheet.work_order
        timesheet_data['address'] = timesheet.address
        timesheet_data['job_date'] = timesheet.job_date
        timesheet_data['arrive_time'] = timesheet.arrive_time
        timesheet_data['left_time'] = timesheet.left_time
        timesheet_data['notes'] = timesheet.notes
        timesheet_data['signature'] = timesheet.signature
        timesheet_data['complete'] = timesheet.complete
        timesheet_data['user_id'] = timesheet.user_id
        output.append(timesheet_data)

    # return jsonify({"timesheets": output})
    timesheet_data_message = messages.ApiMessage(200, "success", {"timesheets": output})
    return timesheet_data_message()

@app.route('/timesheets/<bi_number>', methods=['GET'])
@token_required
def get_one_timesheet(current_user, bi_number):

    if (current_user.active):
        timesheet = Timesheet.query.filter_by(job_number=bi_number).first()
        if not timesheet:
            return messages.TimesheetDoesNotExists()
    else:
        return messages.CannotPerformThatAction()

    output = []

    timesheet_data = {}
    timesheet_data['public_id'] = timesheet.public_id
    timesheet_data['division'] = timesheet.division
    timesheet_data['job_number'] = timesheet.job_number
    timesheet_data['work_order'] = timesheet.work_order
    timesheet_data['address'] = timesheet.address
    timesheet_data['job_date'] = timesheet.job_date
    timesheet_data['arrive_time'] = timesheet.arrive_time
    timesheet_data['left_time'] = timesheet.left_time
    timesheet_data['notes'] = timesheet.notes
    timesheet_data['signature'] = timesheet.signature
    timesheet_data['complete'] = timesheet.complete
    timesheet_data['user_id'] = timesheet.user_id
    output.append(timesheet_data)

    # return jsonify({"timesheet": output})
    timesheets_data_message = messages.ApiMessage(200, "success", {"timesheet": output})
    return timesheets_data_message()

@app.route('/timesheet/<bi_number>', methods=['DELETE'])
@token_required
def delete_timesheet(current_user, bi_number):
    if (current_user.active) and (current_user.admin):
        timesheet = Timesheet.query.filter_by(job_number=bi_number).first()
        if not timesheet:
            return messages.TimesheetDoesNotExists()
        db.session.delete(timesheet)
        db.session.commit()
        timesheet_deleted_message = messages.ApiMessage(200, "success", None)
        return timesheet_deleted_message()
    else:
        return messages.CannotPerformThatAction()

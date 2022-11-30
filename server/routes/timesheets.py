from flask import current_app as app
from flask import request, jsonify
from server.resources import messages, db
from server.resources.models import Timesheet
from server.resources.decorators import token_required
import uuid
from datetime import datetime

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
                message = messages.ApiMessage(401, f"Missing data: {field}")
                return message()

    except:
        return messages.NoDataFound()

    # Query dabatase to see if the timesheet already exists
    existing_timesheet = Timesheet.query.filter_by(job_number=data["job_number"]).first()

    if not existing_timesheet:

        #Create new user
        new_timesheet = Timesheet(public_id=str(uuid.uuid4()), 
        division=data["division"], 
        job_number=data["job_number"] , 
        work_order=data["work_order"], 
        address=data["address"],
        job_date=datetime.strptime(data["job_date"], '%Y-%m-%d').date(),
        arrive_time=datetime.strptime(data["arrive_time"], '%H:%M'),
        left_time=datetime.strptime(data["left_time"], '%H:%M'),
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

    return jsonify({"timesheets": output})

@app.route('/timesheets/<bi_number>', methods=['GET'])
@token_required
def get_one_timesheets(current_user, bi_number):

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

    return jsonify({"timesheet": output})
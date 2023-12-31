import json
import requests
from datetime import date, datetime, timedelta
from time import time
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import pytz
from util import local_settings

SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('calendar', 'v3', credentials=creds)

GPT_MODEL = "gpt-3.5-turbo-0613"
openai_api_key = local_settings.OPENAI_API_KEY

def chat_completion_request(messages, functions=None, function_call=None, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai_api_key,
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

limit1 = datetime.strptime("9:00:00", "%H:%M:%S").time()
limit2 = datetime.strptime("21:00:00", "%H:%M:%S").time()
limit3 = datetime.strptime("12:00:00", "%H:%M:%S").time()

def appointment_booking(arguments):
    try:
        provided_date =  str(datetime.strptime(json.loads(arguments)['date'], "%Y-%m-%d").date())
        provided_time = str(datetime.strptime(json.loads(arguments)['time'].replace("PM","").replace("AM","").strip(), "%H:%M:%S").time())
        start_date_time = provided_date + " " + provided_time
        timezone = pytz.timezone('Europe/Lisbon')
        start_date_time = timezone.localize(datetime.strptime(start_date_time, "%Y-%m-%d %H:%M:%S"))
        email_address = json.loads(arguments)['email_address']
        end_date_time = start_date_time + timedelta(hours=0.5)
        
        if provided_date and provided_time and email_address:
            slot_checking = appointment_checking(arguments)
            if slot_checking == "Slot is available for appointment. Would you like to proceed?":           
                if start_date_time < datetime.now(timezone):
                    return "Please enter valid date and time."
                else:
                    if day_list[start_date_time.date().weekday()] == "Saturday":
                        if start_date_time.time() >= limit1 and start_date_time.time() <= limit3:
                            event = {
                                'summary': "Appointment booking Chatbot using OpenAI's function calling feature",
                                'location': "Lisbon",
                                'description': "Appointment by chatbot",
                                'start': {
                                    'dateTime': start_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
                                    'timeZone': 'Europe/Lisbon',
                                },
                                'end': {
                                    'dateTime': end_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
                                    'timeZone': 'Europe/Lisbon',
                                },
                                'attendees': [
                                {'email': email_address},
                                
                                ],
                                'reminders': {
                                    'useDefault': False,
                                    'overrides': [
                                        {'method': 'email', 'minutes': 24 * 60},
                                        {'method': 'popup', 'minutes': 10},
                                    ],
                                },
                            }
                            service.events().insert(calendarId='primary', body=event).execute()
                            return "Appointment added successfully."
                        else:
                            return "Please try to book an appointment into working hours, which is 10 AM to 2 PM at saturday."
                    else:
                        if start_date_time.time() >= limit1 and start_date_time.time() <= limit2:
                            event = {
                                'summary': "Appointment booking Chatbot using OpenAI's function calling feature",
                                'location': "Lisbon",
                                'description': "This appointment has been scheduled with chatbot ",
                                
                                'start': {
                                    'dateTime': start_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
                                    'timeZone': 'Europe/Lisbon',
                                },
                                'end': {
                                    'dateTime': end_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
                                    'timeZone': 'Europe/Lisbon',
                                },
                                'attendees': [
                                {'email': email_address},
                                
                                ],
                                'reminders': {
                                    'useDefault': False,
                                    'overrides': [
                                        {'method': 'email', 'minutes': 24 * 60},
                                        {'method': 'popup', 'minutes': 10},
                                    ],
                                },
                            }
                            service.events().insert(calendarId='primary', body=event).execute()
                            return "Appointment added successfully."
                        else:
                            return "Please try to book an appointment into working hours, which is 10 AM to 7 PM."
            else:
                return slot_checking
        else:
            return "Please provide all necessary details: Start date, End date and Email address."
    except:
        return "We are facing an error while processing your request. Please try again."

def appointment_reschedule(arguments):
    try:
        provided_date =  str(datetime.strptime(json.loads(arguments)['date'], "%Y-%m-%d").date())
        provided_time = str(datetime.strptime(json.loads(arguments)['time'].replace("PM","").replace("AM","").strip(), "%H:%M:%S").time())
        start_date_time = provided_date + " " + provided_time
        timezone = pytz.timezone('Europe/Lisbon')
        start_date_time = timezone.localize(datetime.strptime(start_date_time, "%Y-%m-%d %H:%M:%S"))
        email_address = json.loads(arguments)['email_address']
        
        if provided_date and provided_time and email_address:
            if start_date_time < datetime.now(timezone):
                return "Please enter valid date and time."
            else:
                if day_list[start_date_time.date().weekday()] == "Saturday":
                    if start_date_time.time() >= limit1 and start_date_time.time() <= limit3:
                        end_date_time = start_date_time + timedelta(hours=2)
                        events = service.events().list(calendarId="primary").execute()
                        id = ""
                        final_event = None
                        for event in events['items']:
                            if event['attendees'][0]['email'] == email_address:
                                id = event['id']
                                final_event = event
                        if final_event:
                            if appointment_checking(arguments) == "Slot is available for appointment. Would you like to proceed?":
                                final_event['start']['dateTime'] = start_date_time.strftime("%Y-%m-%dT%H:%M:%S")
                                final_event['end']['dateTime'] = end_date_time.strftime("%Y-%m-%dT%H:%M:%S")
                                service.events().update(calendarId='primary', eventId=id, body=final_event).execute()
                                return "Appointment rescheduled."
                            else:
                                return "Sorry, slot is not available at this time, please try a different time."
                        else:
                            return "No registered event found on your id."
                    else:
                        return "Please try to book an appointment into working hours, which is 10 AM to 2 PM at saturday."
                else:
                    if start_date_time.time() >= limit1 and start_date_time.time() <= limit2:
                        end_date_time = start_date_time + timedelta(hours=2)
                        events = service.events().list(calendarId="primary").execute()
                        id = ""
                        final_event = None
                        for event in events['items']:
                            if event['attendees'][0]['email'] == email_address:
                                id = event['id']
                                final_event = event
                        if final_event:
                            if appointment_checking(arguments) == "Slot is available for appointment. Would you like to proceed?":
                                final_event['start']['dateTime'] = start_date_time.strftime("%Y-%m-%dT%H:%M:%S")
                                final_event['end']['dateTime'] = end_date_time.strftime("%Y-%m-%dT%H:%M:%S")
                                service.events().update(calendarId='primary', eventId=id, body=final_event).execute()
                                return "Appointment rescheduled."
                            else:
                                return "Sorry, slot is not available at this time, please try a different time."
                        else:
                            return "No registered event found on your id."
                    else:
                        return "Please try to book an appointment into working hours, which is 10 AM to 7 PM."
        else: 
            return "Please provide all necessary details: Start date, End date and Email address."
    except:
        return "We are unable to process, please try again."


def appointment_delete(arguments):
    try:
        provided_date =  str(datetime.strptime(json.loads(arguments)['date'], "%Y-%m-%d").date())
        provided_time = str(datetime.strptime(json.loads(arguments)['time'].replace("PM","").replace("AM","").strip(), "%H:%M:%S").time())
        email_address = json.loads(arguments)['email_address']

        if provided_date and provided_time and email_address:
            start_date_time = provided_date + " " + provided_time
            timezone = pytz.timezone('Europe/Lisbon')
            start_date_time = timezone.localize(datetime.strptime(start_date_time, "%Y-%m-%d %H:%M:%S"))
            if start_date_time < datetime.now(timezone):
                return "Please enter valid date and time."
            else:
                
                events = service.events().list(calendarId="primary").execute()
                id = ""
                for event in events['items']:
                    if event['attendees'][0]['email'] == email_address:
                        if datetime.fromisoformat(str(event['start']['dateTime'])) == datetime.fromisoformat(str(start_date_time)):
                            id = event['id']
                if id:
                    service.events().delete(calendarId='primary', eventId=id).execute()
                    return "Appointment deleted successfully."
                else:
                    return "No registered event found on your id."
        else:
            return "Please provide all necessary details: Start date, End date and Email address."
    except:
        return "We are unable to process, please try again."


def appointment_checking(arguments):
    try:
        provided_date =  str(datetime.strptime(json.loads(arguments)['date'], "%Y-%m-%d").date())
        provided_time = str(datetime.strptime(json.loads(arguments)['time'].replace("PM","").replace("AM","").strip(), "%H:%M:%S").time())
        start_date_time = provided_date + " " + provided_time
        timezone = pytz.timezone('Europe/Lisbon')
        start_date_time = timezone.localize(datetime.strptime(start_date_time, "%Y-%m-%d %H:%M:%S"))
        if start_date_time < datetime.now(timezone): 
            return "Please enter valid date and time." 
        else:
            if day_list[start_date_time.date().weekday()] == "Saturday":
                if start_date_time.time() >= limit1 and start_date_time.time() <= limit3:
                    end_date_time = start_date_time + timedelta(hours=2)
                    events_result = service.events().list(calendarId='primary', timeMin=start_date_time.isoformat(), timeMax=end_date_time.isoformat()).execute()
                    if events_result['items']:
                        return "Sorry slot is not available."
                    else:
                        return "Slot is available for appointment. Would you like to proceed?"
                else:
                    return "Please try to check an appointment within working hours, which is 10 AM to 2 PM at saturday."
            else:
                if start_date_time.time() >= limit1 and start_date_time.time() <= limit2:
                    end_date_time = start_date_time + timedelta(hours=2)
                    events_result = service.events().list(calendarId='primary', timeMin=start_date_time.isoformat(), timeMax=end_date_time.isoformat()).execute()
                    if events_result['items']:
                        return "Sorry slot is not available."
                    else:
                        return "Slot is available for appointment. Would you like to proceed?"
                else:
                    return "Please try to check an appointment within working hours, which is 10 AM to 7 PM."
    except:
        return "We are unable to process, please try again."

functions = [
    {
        "name": "appointment_booking",
        "description": "When user want to book appointment, then this function should be called.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "format": "date",
                    "example":"2023-07-23",
                    "description": "Date, when the user wants to book an appointment. The date must be in the format of YYYY-MM-DD.",
                },
                "time": {
                    "type": "string",
                    "example": "20:12:45", 
                    "description": "time, on which user wants to book an appointment on a specified date. Time must be in %H:%M:%S format.",
                },
                "email_address": {
                    "type": "string",
                    "description": "email_address of the user gives for identification.",
                }
            },
            "required": ["date","time","email_address"],
        },
    },
    {
        "name": "appointment_reschedule",
        "description": "When user want to reschedule appointment, then this function should be called.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "format": "date",
                    "example":"2023-07-23",
                    "description": "It is the date on which the user wants to reschedule the appointment. The date must be in the format of YYYY-MM-DD.",
                },
                "time": {
                    "type": "string",
                    "description": "It is the time on which user wants to reschedule the appointment. Time must be in %H:%M:%S format.",
                },
                "email_address": {
                    "type": "string",
                    "description": "email_address of the user gives for identification.",
                }
            },
            "required": ["date","time","email_address"],
        },
    },
    {
        "name": "appointment_delete",
        "description": "When user want to delete appointment, then this function should be called.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "format": "date",
                    "example":"2023-07-23",
                    "description": "Date, on which user has appointment and wants to delete it. The date must be in the format of YYYY-MM-DD.",
                },
                "time": {
                    "type": "string",
                    "description": "time, on which user has an appointment and wants to delete it. Time must be in %H:%M:%S format.",
                },
                "email_address": {
                    "type": "string",
                    "description": "email_address of the user gives for identification.",
                }
            },
            "required": ["date","time","email_address"],
        },
    },
    {
        "name": "appointment_checking",
        "description": "When user wants to check if appointment is available or not, then this function should be called.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "format": "date",
                    "example":"2023-07-23",
                    "description": "Date, when the user wants to book an appointment. The date must be in the format of YYYY-MM-DD.",
                },
                "time": {
                    "type": "string",
                    "example": "20:12:45", 
                    "description": "time, on which user wants to book an appointment on a specified date. Time must be in %H:%M:%S format.",
                }
            },
            "required": ["date","time"],
        },
    }]


day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

messages = [{"role": "system", "content": f"""You are an expert in booking appointments. You need to ask the user for the appointment date, appointment time, and email ID. The user can book the appointment from 9 AM to 9 PM from Monday to Friday, and from 10 AM to 2 PM on Saturdays. You need to remember that today's date is {date.today()} and day is {day_list[date.today().weekday()]}. Check if the time provided by the user is within the working hours then only you will proceed.

Instructions: 
- Don't make assumptions about what values to plug into functions, if the user does not provide any of the required parameters then you must need to ask for clarification.
- Make sure the email Id is valid and not empty.
- If a user request is ambiguous, then also you need to ask for clarification.
- When a user asks for a rescheduling date or time of the current appointment, then you must ask for the new appointment details only.
- If a user didn't specify "ante meridiem (AM)" or "post meridiem (PM)" while providing the time, then you must have to ask for clarification. If the user didn't provide day, month, and year while giving the time then you must have to ask for clarification.

Make sure to follow the instructions carefully while processing the request. 
"""}]

user_input = input("Please enter your question here: (if you want to exit then write 'exit' or 'bye'.) ")

while user_input.strip().lower() != "exit" and user_input.strip().lower() != "bye":
    
    messages.append({"role": "user", "content": user_input})

    # calling chat_completion_request to call ChatGPT completion endpoint
    chat_response = chat_completion_request(
        messages, functions=functions
    )

    # fetch response of ChatGPT and call the function
    assistant_message = chat_response.json()["choices"][0]["message"]

    if assistant_message['content']:
        print("Response is: ", assistant_message['content'])
        messages.append({"role": "assistant", "content": assistant_message['content']})
    else:
        fn_name = assistant_message["function_call"]["name"]
        arguments = assistant_message["function_call"]["arguments"]
        function = locals()[fn_name]
        result = function(arguments)
        print("Response is: ", result)
       
    user_input = input("Please enter your question here: ")
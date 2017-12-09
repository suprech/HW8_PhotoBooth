#import json
import boto3

# hard coded credentials for SQS
#access_key = "AKIAJZOZA5WTPBDERNZQ"
#access_secret = "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"
region = "us-east-1"
queue_url = "https://sqs.us-east-1.amazonaws.com/762995444827/testQueue"


def lambda_handler(event, context):
    # skill-specific. stick it to HW08 Photobooth Alexa skill.
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.659f664a-ff49-40bb-b100-c9c4a62858ba"):
        raise ValueError("Invalid Application ID")

    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])


def on_session_started(session_started_request, session):
    print("Starting new session.")


# function for launchintent.
def on_launch(launch_request, session):
    return get_welcome_response()


def on_intent(intent_request, session):
    # 'intent' variable is not used.
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    # code for intent cases.

    # called when taking a photo.
    if intent_name == "shutterIntent":
        return get_shutter_response()

    # called when launching the skill.
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()

    # called when terminating the session.
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()

    # called when applying sepia filter.
    elif intent_name == "sepiaIntent":
        return get_sepia_response()

    # called when applying grayscale filter.
    elif intent_name == "grayIntent":
        return get_gray_response()

    # called when reverting the filter effects.
    elif intent_name == "undoIntent":
        return get_undo_response()

    # called when printing the result.
    elif intent_name == "printIntent":
        return get_print_response()

    # called when uploading to the web server.
    elif intent_name == "uploadIntent":
        return get_upload_response()

    # called for the joke
    elif intent_name == "flatterIntent":
        return get_flatter_response()

    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print("Ending session.")
    # Cleanup goes here...


def handle_session_end_request():
    card_title = "HW08 Photobooth - Termination"
    speech_output = "Thank you for using the Photobooth."
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))


# function for posting a string message to the SQS target queue.
def post_message(client, message_body, url):
    response = client.send_message(QueueUrl=url, MessageBody=message_body)


# function for the welcome response.
def get_welcome_response():
    session_attributes = {}
    card_title = "HW08 Photobooth - Welcome"
    speech_output = "Welcome to the Alexa Photobooth skill, built by Hardware number eight of Korea University. " \
                    "I can take a picture, or " \
                    "praise someone."
    reprompt_text = "Please ask me do something, " \
                    "for example, take a picture."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# function for taking a photo.
def get_shutter_response():
    session_attributes = {}
    card_title = "HW08 Photobooth - Take a picture"
    reprompt_text = "" # 'None' does not silence the reprompt. maybe another kind of build_speechlet_response is needed.
    should_end_session = False

    # Alexa will speak this string when taking a photo.
    speech_output = "OK, I will count five."

    # post a message to the queue.
    client = boto3.client('sqs')
    post_message(client, "shutter", queue_url)

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

# function for applying sepia filter.
def get_sepia_response():
    session_attributes = {}
    card_title = "HW08 Photobooth - Apply sepia filter"
    reprompt_text = "" # 'None' does not silence the reprompt. maybe another kind of build_speechlet_response is needed.
    should_end_session = False

    # Alexa will speak this string when taking a photo.
    speech_output = "I just applied sepia filter to the picture."

    # post a message to the queue.
    client = boto3.client('sqs')
    post_message(client, "sepia", queue_url)

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


# function for applying grayscale filter.
def get_gray_response():
    session_attributes = {}
    card_title = "HW08 Photobooth - Apply grayscale filter"
    reprompt_text = ""  # 'None' does not silence the reprompt. maybe another kind of build_speechlet_response is needed.
    should_end_session = False

    # Alexa will speak this string when taking a photo.
    speech_output = "I just applied grayscale filter to the picture."

    # post a message to the queue.
    client = boto3.client('sqs')
    post_message(client, "gray", queue_url)

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


# function for undoing the filter application
def get_undo_response():
    session_attributes = {}
    card_title = "HW08 Photobooth - Undo"
    reprompt_text = ""  # 'None' does not silence the reprompt. maybe another kind of build_speechlet_response is needed.
    should_end_session = False

    # Alexa will speak this string when taking a photo.
    speech_output = "I just reverted the changes."

    # post a message to the queue.
    client = boto3.client('sqs')
    post_message(client, "undo", queue_url)

    return build_response(session_attributes,
                          build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))



# function for printing the result.
def get_print_response():
    session_attributes = {}
    card_title = "HW08 Photobooth - Print the result"
    reprompt_text = ""  # 'None' does not silence the reprompt. maybe another kind of build_speechlet_response is needed.
    should_end_session = False

    # Alexa will speak this string when taking a photo.
    speech_output = "I will send the result photo to the photo printer."

    # post a message to the queue.
    client = boto3.client('sqs')
    post_message(client, "print", queue_url)

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


# function for uploading the result to the web server.
def get_upload_response():
    session_attributes = {}
    card_title = "HW08 Photobooth - Upload"
    reprompt_text = ""  # 'None' does not silence the reprompt. maybe another kind of build_speechlet_response is needed.
    should_end_session = False

    # Alexa will speak this string when taking a photo.
    speech_output = "I will upload the result photo to the web server."

    # post a message to the queue.
    client = boto3.client('sqs')
    post_message(client, "upload", queue_url)

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

# function for a joke response.
def get_flatter_response():
    session_attributes = {}
    card_title = "HW08 Photobooth - Flatter"
    reprompt_text = ""
    should_end_session = False

    speech_output = "Professor Uhm and TA Wang are the best duo in the world."

    # post a message is not needed. just for conversations.

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }

